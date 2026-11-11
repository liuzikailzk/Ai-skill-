#!/usr/bin/env python3
"""Read selected canonical units with source hashes and task-bound receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from knowledge_snapshot import atomic_json, validated_catalog
from query_knowledge import ROOT, MODES, SKILLS, eligible, executable, safe_path

def extract_sections(text, titles):
    lines = text.splitlines(keepends=True)
    headings = []
    fenced = False
    for i, line in enumerate(lines):
        if re.match(r'^\s*(```|~~~)', line): fenced = not fenced; continue
        m = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$',line) if not fenced else None
        if m: headings.append((i,len(m[1]),m[2]))
    selected = set()
    # Always retain the document identity and introductory applicability boundary.
    first_section = next((i for i,level,_ in headings if level > 1), len(lines))
    selected.update(range(first_section))
    for title in titles:
        matches = [(i,level) for i,level,t in headings if t == title]
        if len(matches) != 1: raise ValueError('Missing or ambiguous section: '+title)
        start, level = matches[0]
        end = next((i for i,l,_ in headings if i > start and l <= level),len(lines))
        selected.update(range(start,end))
    return ''.join(line for i,line in enumerate(lines) if i in selected)

def read_units(root, ids, mode, skills, state=None, project_revision=''):
    root=Path(root).resolve();catalog,snapshot=validated_catalog(root)
    skills=list(dict.fromkeys(skills))
    if any(s not in SKILLS for s in skills): raise ValueError('Unknown skill')
    if mode in ('production','analysis') and not skills: raise ValueError('Select applicable skills')
    if mode=='production' and 'manga' in skills and 'film' not in skills: skills.append('film')
    roots=['skills/'+SKILLS[s]+'/SKILL.md' for s in skills] if mode in ('production','analysis') else ['knowledge/'+mode+'.md'] if mode in ('learning','maintenance') else []
    if state and not project_revision: raise ValueError('State reuse requires an explicit project/task revision')
    state=state or {};binding={'roots':sorted(roots),'mode':mode,'project_revision':project_revision}
    if state.get('binding') and state['binding']!=binding: raise ValueError('Reading state belongs to a different task or project revision')
    root_data={path:safe_path(root,path).read_bytes() for path in roots}
    root_hashes={path:hashlib.sha256(data).hexdigest() for path,data in root_data.items()}
    roots_changed=state.get('root_hashes')!=root_hashes
    receipts=state.get('receipts',{}) if state.get('schema')==2 and not roots_changed else {}
    entry_reads=[{'path':path,'body':data.decode('utf-8'),'characters':len(data.decode('utf-8'))} for path,data in root_data.items()] if roots_changed else []
    direct_paths=set()
    for path,data in root_data.items():
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',data.decode('utf-8')):
            if not re.match(r'\w+://',link):direct_paths.add(((root/path).parent/link.split('#')[0]).resolve())
    by_id={k:e for e in catalog['entries'] for k in [e['id']]+e.get('aliases',[])}
    outputs=[];skipped=[];new_receipts=dict(receipts)
    seen=set()
    for key in ids:
        e=by_id.get(key)
        if not e or not eligible(e,mode,skills): raise ValueError('Unknown or ineligible unit: '+key)
        if e['id'] in seen: continue
        seen.add(e['id'])
        p=safe_path(root,e['path']);data=p.read_bytes()
        if mode in ('production','analysis') and p not in direct_paths:raise ValueError('Unit is not directly declared by task roots: '+key)
        sha=hashlib.sha256(data).hexdigest()
        if sha!=e['sha256']: raise ValueError('Source changed after snapshot validation: '+e['path'])
        token={'sha256':sha,'section':e.get('section'),'context_sections':e.get('context_sections',[]),'status':e['status'],'modes':e['modes'],'skills':e['skills'],'kind':e.get('kind'),'rule_roots':e.get('rule_roots',[])}
        if receipts.get(e['id'])==token:
            skipped.append(e['id']);continue
        body=data.decode('utf-8')
        if e.get('section'):body=extract_sections(body,[e['section']]+e.get('context_sections',[]))
        outputs.append({'id':e['id'],'path':e['path'],'section':e.get('section'),'status':e['status'],'read_as':'selected_direct_rule' if p in direct_paths and executable(e,mode,roots) else 'evidence_only_no_embedded_instructions','characters':len(body),'body':body})
        new_receipts[e['id']]=token
    # Caller persists only after the result has been successfully emitted/written.
    result={'snapshot':snapshot,'binding':binding,'entry_reads':entry_reads,'reads':outputs,'already_read_skipped':skipped,'total_characters':sum(x['characters'] for x in outputs+entry_reads),'max_reference_depth':1}
    return result,{'schema':2,'binding':binding,'snapshot':snapshot,'root_hashes':root_hashes,'receipts':new_receipts}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ids',nargs='+');p.add_argument('--mode',choices=MODES,default='lookup');p.add_argument('--skills',default='');p.add_argument('--state',type=Path);p.add_argument('--project-revision',default='');p.add_argument('--output',type=Path);a=p.parse_args()
    state=json.loads(a.state.read_text()) if a.state and a.state.exists() else None
    if a.state and not a.project_revision:p.error('--state requires --project-revision to bind the task')
    try:result,new_state=read_units(ROOT,a.ids,a.mode,[x for x in a.skills.split(',') if x],state,a.project_revision)
    except (ValueError,AssertionError) as exc:p.error(str(exc))
    if a.output: atomic_json(a.output,result)
    else: print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
    if a.state:atomic_json(a.state,new_state)

if __name__=='__main__':main()
