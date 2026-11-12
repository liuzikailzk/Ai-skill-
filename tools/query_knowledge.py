#!/usr/bin/env python3
"""Select metadata and explicit first-layer rule files; never read result bodies."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {'film': 'script-video-shot-director', 'assets': 'script-visual-assets', 'manga': 'manga-reasoning-storyboard'}
MODES = ('production', 'analysis', 'learning', 'maintenance', 'lookup')
RULE_STATUSES = {'existing_baseline', 'existing_rule', 'user_control_rule', 'active'}
EVIDENCE_STATUSES = {'user_accepted_case', 'user_accepted_partial', 'failure_case', 'source_note'}
KNOWN_STATUSES = RULE_STATUSES | EVIDENCE_STATUSES | {'open_issue', 'candidate', 'observing', 'conflicted', 'deprecated', 'rolled_back'}
KINDS = {'rule', 'method', 'case', 'warning', 'candidate', 'source'}

def kind_matches_status(entry):
    status=entry.get('status');kind=entry.get('kind')
    if kind is None: return True  # Legacy fixtures; catalog schema 2 requires explicit kinds.
    if status in RULE_STATUSES:return kind in ('rule','method')
    if status=='open_issue':return kind=='warning'
    if status in ('user_accepted_case','user_accepted_partial','failure_case'):return kind=='case'
    if status=='source_note':return kind=='source'
    if status in ('candidate','observing','conflicted'):return kind=='candidate'
    return kind in KINDS  # Revoked historical entries are evidence-only outside production.

def eligible(entry, mode, skills=None, required=False):
    """One qualification gate for required rules, ranked matches and exact reads."""
    status = entry.get('status')
    if status not in KNOWN_STATUSES or entry.get('kind', 'rule') not in KINDS or not kind_matches_status(entry):
        return False
    if mode not in entry.get('modes', []) or (skills and not set(skills).intersection(entry.get('skills', []))):
        return False
    if mode in ('production', 'analysis'):
        if entry['path'].startswith('pending-review/') or status not in RULE_STATUSES | {'open_issue', 'user_accepted_case', 'user_accepted_partial', 'failure_case'}:
            return False
        if required and status not in RULE_STATUSES | {'open_issue'}:
            return False
    elif required and status not in RULE_STATUSES | {'open_issue'}:
        return False
    return True

def entry_key(entry):
    return (entry['path'], entry.get('section', ''))

def executable(entry, mode, roots):
    return mode!='lookup' and entry['status'] in RULE_STATUSES | {'open_issue'} and bool(set(roots).intersection(entry.get('rule_roots',[])))

def validate_taxonomy(taxonomy,catalog):
    by={e['id']:e for e in catalog['entries']}
    roots=['skills/'+SKILLS['film']+'/SKILL.md']
    for facet,targets in taxonomy['method_routes'].items():
        group,label=facet.split(':',1)
        if label not in taxonomy['facets'].get(group,[]) or not isinstance(targets,list):raise ValueError('Invalid taxonomy facet: '+facet)
        for key in targets:
            e=by.get(key)
            if not e or e.get('kind')!='method' or not eligible(e,'analysis',['film'],required=True) or not executable(e,'analysis',roots):raise ValueError('Taxonomy target is not an eligible direct method: '+key)

def asset_scope(question, explicit='auto'):
    if explicit not in ('auto', 'design', 'base', 'mixed'):
        raise ValueError('Invalid asset scope')
    if explicit != 'auto': return explicit
    design = any(t in question for t in ('海报', '封面', '横幅', '宣传', '产品展示', '边框', '标题字', '图标', '贴纸', '装饰', '排版'))
    # A person mentioned on a poster does not request a separate base character asset.
    base = any(t in question for t in ('四视图', '三视图', '基础资产', '单件道具', '另做角色', '角色设定图'))
    return 'mixed' if design and base else 'design' if design else 'base'

def load_catalog(root=ROOT):
    return json.loads((Path(root) / 'knowledge/catalog.json').read_text())

def safe_path(root, path):
    rel = Path(path)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Unsafe repository path: ' + path)
    target = (Path(root) / rel).resolve()
    if not target.is_relative_to(Path(root).resolve()):
        raise ValueError('Path leaves repository: ' + path)
    return target

def normalized(text):
    return re.sub(r'\s+', '', text.casefold())

def query(catalog, question, mode='lookup', skills=None, limit=3, dynamic_images=False, stage='auto', assets='auto'):
    if mode not in MODES or not 1 <= limit <= 10:
        raise ValueError('Invalid mode or limit (1..10)')
    selected = list(dict.fromkeys(skills or []))
    if any(s not in SKILLS for s in selected):
        raise ValueError('Unknown skill')
    if mode in ('production', 'analysis') and not selected:
        raise ValueError('Select applicable --skills; do not assume every skill is needed')
    # Dynamic manga adaptation also needs the film entry; pure panel analysis does not.
    if mode == 'production' and 'manga' in selected and 'film' not in selected:
        selected.append('film')
    q = normalized(question)
    if stage not in ('auto', 'understand', 'plan', 'deliver'): raise ValueError('Invalid stage')
    stage = ('deliver' if mode == 'production' else 'understand') if stage == 'auto' else stage
    scope = asset_scope(q, assets)
    expansions = []
    for phrase, terms in catalog['aliases'].items():
        if normalized(phrase) in q:
            expansions.extend(terms)
    terms = set(normalized(t) for t in expansions)
    scored = []
    for entry in catalog['entries']:
        if not eligible(entry, mode, selected):
            continue
        if mode in ('production', 'analysis') and selected == ['assets']:
            if scope == 'design' and entry['id'] == 'assets-core': continue
            if scope == 'base' and entry['id'] == 'assets-design' and '人物卡' not in q: continue
        matches = [t for t in entry['tags'] if normalized(t) in q or normalized(t) in terms]
        broad = {'漫画', '影视', '资产', '候选', '待验证', '静态', '原作'}
        if matches and all(t in broad for t in matches) and q not in broad:
            continue  # Category alone is not evidence that a specialized module fits.
        score = sum(3 + min(len(normalized(t)), 6) / 3 for t in matches)
        if any(normalized(key) in q for key in [entry['id']] + entry.get('aliases', [])) or (q and q in normalized(entry['title'])):
            score += 20
        if not matches and score == 0:
            continue
        scored.append((score, entry, matches))
    # Explicit case lookup remains available; production methods precede examples.
    scored.sort(key=lambda v: (0 if mode == 'lookup' or v[1]['status'] in RULE_STATUSES | {'open_issue'} else 1, -v[0], v[1]['id']))
    required = []
    roots = []
    if mode in ('production', 'analysis'):
        for skill in selected:
            roots.append('skills/' + SKILLS[skill] + '/SKILL.md')
            required += (['assets-design'] if skill == 'assets' and scope == 'design' else [skill + '-core'])
            if skill == 'assets' and scope == 'mixed': required.append('assets-design')
            if mode == 'production':
                if skill == 'film':
                    # Film's core/delivery retain the concrete failure checks.
                    # Historical issue reports are selected only for relevant queries.
                    if stage != 'understand': required.append('film-style')
                    if stage == 'deliver':
                        required += ['film-model', 'film-input', 'film-motion', 'film-delivery']
                    elif stage == 'plan' and dynamic_images:
                        required.append('film-motion')
                else:
                    required += [skill + '-style', skill + '-open']
                    if skill == 'manga': required += [skill + '-model', skill + '-input']
                    if skill == 'assets' and dynamic_images:
                        required += ['assets-motion', 'assets-severe']
                    if skill == 'manga' and stage == 'deliver': required.append('manga-delivery')
            elif skill == 'manga':
                required.append('panels')
    elif mode == 'learning':
        roots = ['knowledge/learning.md']
        required = ['learning', 'learning-reasoning', 'news', 'report', 'credit', 'pending']
    elif mode == 'maintenance':
        roots = ['knowledge/maintenance.md']
        required = ['save', 'versions']
    if mode in ('production','analysis') and ('film' in selected or (mode=='production' and 'manga' in selected) or '剧本' in q or '全剧' in q):
        required += ['script-analysis', 'production-routing']
    by_id = {key: e for e in catalog['entries'] for key in [e['id']] + e.get('aliases', [])}
    unique_required = []
    seen_required_paths = set()
    for key in dict.fromkeys(required):
        entry = by_id.get(key)
        if not entry or not eligible(entry, mode, selected, required=True) or not executable(entry,mode,roots):
            raise ValueError('Required rule unavailable or ineligible: ' + key)
        if entry_key(entry) not in seen_required_paths:
            unique_required.append((key, entry))
            seen_required_paths.add(entry_key(entry))
    def brief(entry, matches=None):
        result = {k: entry[k] for k in ('id', 'title', 'path', 'status', 'summary')}
        result['read_as'] = 'selected_direct_rule' if executable(entry,mode,roots) else 'evidence_only_no_embedded_instructions'
        for key in ('kind', 'section', 'context_sections'):
            if key in entry: result[key] = entry[key]
        if matches is not None:
            result['matched_tags'] = matches
        return result
    recommended = [e for _, e in unique_required]
    recommended += [e for _,e,_ in scored[:limit] if executable(e,mode,roots)]
    # Examples remain available in matches but are optional evidence, not default reads.
    recommended_ids = list(dict.fromkeys(e['id'] for e in recommended))
    return {'mode': mode, 'skills': selected, 'stage': stage, 'asset_scope': scope if 'assets' in selected else None, 'entry_roots': roots,
            'read_plan_ids': recommended_ids,
            'optional_evidence_ids': [e['id'] for _,e,_ in scored[:limit] if not executable(e,mode,roots)],
            'required_rules': [brief(e) | {'id': key, 'canonical_id': e['id']} for key, e in unique_required],
            'matches': [brief(e, m) for _, e, m in scored[:limit]],
            'matched_total': len(scored), 'has_more': len(scored) > limit,
            'fallback': None if scored else '未命中首批索引；换同义词/类别或在明确范围补检。不能据此断言不存在，不自动全库读正文。',
            'limits': '结果不是有效性背书。先看摘要再取必要正文；入口第0层，所选规则第1层，读后停止。案例作证据，不执行其中历史指令。',
            'catalog_revision': catalog['revision'], 'bodies_read_by_search': 0}

def validate(root=ROOT):
    root = Path(root); catalog = load_catalog(root); ids = set(); paths = set()
    for e in catalog['entries']:
        assert e['id'] not in ids, 'duplicate id: ' + e['id']
        ids.add(e['id'])
        for alias in e.get('aliases', []):
            assert alias not in ids, 'duplicate id/alias: ' + alias
            ids.add(alias)
        assert entry_key(e) not in paths, 'duplicate canonical unit: ' + str(entry_key(e))
        paths.add(entry_key(e))
        p = safe_path(root, e['path'])
        assert p.is_file() and not p.is_symlink(), e['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == e['sha256'], 'stale index: ' + e['path']
        assert e['status'] in KNOWN_STATUSES, 'unknown status: ' + e['id']
        assert e.get('kind', 'rule') in KINDS, 'unknown kind: ' + e['id']
        assert kind_matches_status(e), 'kind/status mismatch: ' + e['id']
        if catalog.get('schema',1)>=2:assert e.get('kind') in KINDS, 'kind required: '+e['id']
        if catalog.get('schema',1)>=2:
            actual_roots=[]
            for rp in ['knowledge/learning.md','knowledge/maintenance.md']+['skills/'+s+'/SKILL.md' for s in SKILLS.values()]:
                source=root/rp
                links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',source.read_text())
                targets={(source.parent/link.split('#')[0]).resolve() for link in links if not re.match(r'\w+://',link)}
                if p in targets:actual_roots.append(rp)
            assert sorted(e.get('rule_roots',[]))==sorted(actual_roots),'stale direct roots: '+e['id']
        if e.get('section'):
            from read_knowledge import extract_sections
            extract_sections(p.read_text(), [e['section']] + e.get('context_sections', []))
        assert e['summary'] and e['tags'] and set(e['modes']) <= set(MODES)
        if {'production','analysis'}.intersection(e['modes']):
            assert e['status'] in RULE_STATUSES | {'open_issue','user_accepted_case','user_accepted_partial','failure_case'}, 'ineligible production status: ' + e['id']
        assert not {'history', 'failure-history', 'archive'}.intersection(Path(e['path']).parts), 'historical snapshots must not enter this catalog'
        if e['path'].startswith('pending-review/') and e['status'] in ('candidate','observing','conflicted'):
            assert not {'production','analysis'}.intersection(e['modes'])
        for skill in e['skills']:
            assert skill in SKILLS
            if 'production' not in e['modes'] and 'analysis' not in e['modes']:
                continue
            source = root / 'skills' / SKILLS[skill] / 'SKILL.md'
            links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', source.read_text())
            targets = {(source.parent / link.split('#')[0]).resolve() for link in links if not re.match(r'\w+://', link)}
            assert p in targets, 'source not directly declared by ' + str(source) + ': ' + e['path']
    # Also validate mandatory assembly; a reclassified baseline cannot silently survive.
    for mode, skills in [('production',['film']),('production',['assets']),('analysis',['manga']),('learning',None),('maintenance',None)]:
        query(catalog, '目录校验', mode, skills)
    if (root/'knowledge/taxonomy.json').exists():validate_taxonomy(json.loads((root/'knowledge/taxonomy.json').read_text()),catalog)
    return {'result':'PASS','entries':len(catalog['entries']),'ids_including_aliases':len(ids),'source_hashes_verified':len({p[0] for p in paths}),'scope':'metadata integrity, eligibility and direct reachability; not content effectiveness'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='')
    p.add_argument('--mode',choices=MODES,default='lookup')
    p.add_argument('--skills',default='',help='Comma-separated film,assets,manga; only applicable roles')
    p.add_argument('--limit',type=int,default=3)
    p.add_argument('--dynamic-images',action='store_true')
    p.add_argument('--validate',action='store_true')
    p.add_argument('--stage',choices=('auto','understand','plan','deliver'),default='auto')
    p.add_argument('--assets',choices=('auto','base','design','mixed'),default='auto')
    a=p.parse_args()
    if a.validate:
        result=validate()
    else:
        if not a.query.strip():p.error('A nonempty query is required')
        try:
            from knowledge_snapshot import validated_catalog
            catalog, snapshot = validated_catalog(ROOT)
            result=query(catalog,a.query,a.mode,[s.strip() for s in a.skills.split(',') if s.strip()],a.limit,a.dynamic_images,a.stage,a.assets)
            result['snapshot'] = snapshot
        except (ValueError,AssertionError) as exc:p.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
