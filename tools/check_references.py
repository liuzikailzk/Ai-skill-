#!/usr/bin/env python3
"""Inventory local Markdown references and report strongly connected components.

Explicit Markdown destinations resolve strictly relative to their source file.
Bare paths use source-, package-, or repository-relative scope, then a unique
in-package basename for otherwise unqualified filenames. Every resolution mode
and exclusion is recorded. Cycles are reported; this tool never edits documents.
"""
import argparse
from collections import Counter, defaultdict, deque
import html
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

NAMES = ('script-video-shot-director','manga-reasoning-storyboard','script-visual-assets')
EXT = r'(?:md|json|txt|py|ya?ml|svg|png|jpe?g|webp|mp4|csv|html|zip)'
BARE = re.compile(r'(?<![A-Za-z0-9_./-])(?:\.{1,2}/|/)?(?:[A-Za-z0-9_*{}$-]+?|<[^>\n]+>)(?:/(?:[A-Za-z0-9_\u4e00-\u9fff*{}$.-]+?|<[^>\n]+>))*?\.'+EXT+r'(?:#[A-Za-z0-9_%-]+)?(?![A-Za-z0-9_.-])', re.I)
URL = re.compile(r'(?:https?://|mailto:|skill://|sandbox:)[^\s<>`）\]）]+')
LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
DEFINITION = re.compile(r'^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)')
REF_LINK = re.compile(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]')
TEMPLATE = re.compile(r'YYYY|MM-DD|案例名|<[^>]*>|[{}*]|(?:^|/)(?:xxx|example|record|report|audit-report|evidence-matrix|candidate-[^/]*|queries|cross-skill-transfer)\.(?:md|json)$|(?:^|/)human-brief\.txt$',re.I)

def package(source):
    parts=source.parts
    return Path(*parts[:2]) if len(parts)>1 and parts[0]=='skills' and parts[1] in NAMES else None

def extract(text):
    """Return one occurrence per actual destination, not both label and target."""
    lines=text.splitlines(); definitions={}; fence=None; code_lines=set()
    for number,line in enumerate(lines,1):
        fm=re.match(r'^\s*(`{3,}|~{3,})',line)
        if fm:
            fence=None if fence and fm[1][0]==fence else fm[1][0]
            code_lines.add(number); continue
        if fence: code_lines.add(number)
        dm=DEFINITION.match(line)
        if dm: definitions[dm[1].lower()] = dm[2].strip('<>')
    found=[]
    for number,line in enumerate(lines,1):
        occupied=[]
        for m in URL.finditer(line): occupied.append(m.span())
        dm=DEFINITION.match(line)
        if dm:
            found.append((number,dm[2].strip('<>'),'markdown_definition',line,number in code_lines))
            continue
        for m in LINK.finditer(line):
            found.append((number,m[1].strip('<>'),'markdown_link',line,number in code_lines)); occupied.append(m.span())
        for m in REF_LINK.finditer(line):
            key=(m[2] or m[1]).lower()
            if key in definitions:
                found.append((number,definitions[key],'markdown_reference',line,number in code_lines))
            else:
                found.append((number,'[undefined:'+key+']','undefined_reference',line,number in code_lines))
            occupied.append(m.span())
        for m in re.finditer(r'`([^`\n]+)`',line):
            if any(a<=m.start()<b for a,b in occupied):continue
            if re.fullmatch(r'[^\s]+\.'+EXT+r'(?:#[^\s]+)?',m[1],re.I):
                found.append((number,m[1],'bare_path',line,number in code_lines));occupied.append(m.span())
        for m in BARE.finditer(line):
            if any(a<=m.start()<b for a,b in occupied): continue
            raw=m[0]
            if m.start()>0 and line[m.start()-1]=='<':raw='<'+raw+'>'
            found.append((number,raw,'bare_path',line,number in code_lines))
    return found

def resolve(root,source,raw,kind,line,in_code):
    raw=html.unescape(raw); url=urlsplit(raw)
    if url.scheme or raw.startswith('//'): return {'status':'external','target':None}
    if not url.path: return {'status':'same_document_fragment','target':source.as_posix()}
    path=unquote(url.path)
    if kind=='undefined_reference': return {'status':'undefined_reference','target':None}
    if raw=='私有素材入口未公开':return {'status':'unpublished_private_artifact','target':None,'reason':'Source explicitly states that original private media were not published'}
    if TEMPLATE.search(path) and (kind=='bare_path' or re.search(r'YYYY|MM-DD|案例名|[<>{}*]',path)):
        return {'status':'template','target':None,'reason':'Parameterized/example/output placeholder, not an existing load target'}
    if kind=='bare_path' and Path(path).name=='manifest.json' and '<' in line and 'before.json' in line:
        return {'status':'template','target':None,'reason':'Manifest companion of the explicitly parameterized backup destination'}
    p=package(source); candidates=[]
    if kind=='bare_path' and path=='skills/三套version.json' and p:
        paths=[f'skills/{n}/version.json' for n in NAMES]
        if all((root/x).is_file() for x in paths):return {'status':'exists','target':(p/'version.json').as_posix(),'resolution':'three_skill_version_set','set_targets':paths}
    def add(value,mode):
        resolved=(root/value).resolve()
        if resolved.is_relative_to(root):
            item=(resolved.relative_to(root),mode)
            if item not in candidates:candidates.append(item)
    add(source.parent/path,'source_relative')
    if kind=='bare_path':
        # An explicitly named Skill in the immediate clause takes precedence.
        for n in NAMES:
            if n in line or (n=='script-video-shot-director' and re.search(r'影视(?:分镜)?(?:Skill|技能|包|版)',line)):
                add(Path('skills')/n/path,'named_skill_relative')
        if p: add(p/path,'package_relative')
        add(Path(path.lstrip('/')),'repository_relative')
        if path.split('/')[0] in NAMES:add(Path('skills')/path,'named_skill_path')
        if p and Path(path).name=='manifest.json' and '/' not in path:
            earlier=re.search(r'(history/[^\s，；。与及]+/before\.json)',line)
            if earlier:add(p/Path(earlier[1]).parent/path,'same_clause_backup_sibling')
        if Path(path).name=='global-state.json' and re.search(r'共用|影视',line):
            add(Path('skills/script-video-shot-director/references/audit/global-state.json'),'canonical_shared_ledger')
    existing=[(v,m) for v,m in candidates if (root/v).is_file()]
    if existing:
        # Prefer named scope when a bare cross-Skill reference explicitly supplies it.
        named=[(v,m) for v,m in existing if m=='named_skill_relative']
        target,mode=(named[0] if named else existing[0])
        return {'status':'exists','target':target.as_posix(),'resolution':mode}
    if kind=='bare_path' and p and '/' not in path:
        matches=sorted((root/p).rglob(path))
        matches=[x for x in matches if x.is_file()]
        if len(matches)==1:return {'status':'exists','target':matches[0].relative_to(root).as_posix(),'resolution':'unique_package_basename'}
        if len(matches)>1:
            historical=source.name=='learning-log.md' or '/cases/' in source.as_posix()
            return {'status':'historical_ambiguous' if historical else 'ambiguous','target':None,'candidates':[x.relative_to(root).as_posix() for x in matches],'reason':'Historical basename has multiple possible artifacts; no unverified target chosen' if historical else 'Multiple in-package matches'}
    if kind=='bare_path' and (source.name=='learning-log.md' or '/cases/' in source.as_posix() or source.name.startswith('test-') or (source.parts[0]=='pending-review' and '/cases/' in path)):
        return {'status':'historical_artifact_unavailable','target':None,'reason':'Historical provenance mention; resource not present at the repository snapshot. Not an executable load target and not a successful check.','candidates':[v.as_posix() for v,m in candidates]}
    if kind=='bare_path' and (in_code or re.search(r'保存|产出|报告位置|生成|快照|备份|before\.json|manifest\.json',line)):
        return {'status':'unresolved_output_or_example','target':None,'candidates':[v.as_posix() for v,m in candidates]}
    return {'status':'missing','target':None,'candidates':[v.as_posix() for v,m in candidates]}

def strongly_connected(graph):
    index=0; ids={}; low={}; stack=[]; active=set(); groups=[]
    def visit(v):
        nonlocal index
        ids[v]=low[v]=index;index+=1;stack.append(v);active.add(v)
        for w in sorted(graph.get(v,set())):
            if w not in ids:visit(w);low[v]=min(low[v],low[w])
            elif w in active:low[v]=min(low[v],ids[w])
        if low[v]==ids[v]:
            component=[]
            while True:
                w=stack.pop();active.remove(w);component.append(w)
                if w==v:break
            if len(component)>1 or v in graph.get(v,set()):groups.append(sorted(component))
    for v in sorted(graph):
        if v not in ids:visit(v)
    return sorted(groups,key=lambda g:g[0])

def witness(graph,nodes):
    allowed=set(nodes)
    for a in nodes:
        for b in sorted(graph.get(a,set())&allowed):
            if a==b:
                if len(nodes)==1:return [a,a]
                continue
            queue=deque([(b,[a,b])]);seen={b}
            while queue:
                c,path=queue.popleft()
                for d in sorted(graph.get(c,set())&allowed):
                    if d==a:return path+[a]
                    if d not in seen:seen.add(d);queue.append((d,path+[d]))
    return []

def scan(root,follow_outside=False):
    root=root.resolve(); sources=sorted(p.relative_to(root) for n in NAMES for p in (root/'skills'/n).rglob('*.md'))
    initial=set(sources); queue=deque(sources); visited=set(); records=[]; graph=defaultdict(set)
    while queue:
        source=queue.popleft()
        if source in visited:continue
        visited.add(source);text=(root/source).read_text();graph[source.as_posix()]
        for number,raw,kind,line,in_code in extract(text):
            r={'source':source.as_posix(),'line':number,'raw':raw,'kind':kind,'in_code_block':in_code,**resolve(root,source,raw,kind,line,in_code)}
            r['scope']='skill' if source in initial else 'transitive_external_md'
            records.append(r)
            if r['status']=='exists' and r['target'].endswith('.md'):
                target=Path(r['target']);graph[source.as_posix()].add(target.as_posix())
                if target in initial or follow_outside:
                    if target not in visited:queue.append(target)
    groups=[]
    for nodes in strongly_connected(graph):
        edges=[{'source':a,'target':b,'occurrences':[{'line':r['line'],'raw':r['raw'],'kind':r['kind']} for r in records if r['source']==a and r['target']==b and r['status']=='exists']} for a in nodes for b in sorted(graph.get(a,set())&set(nodes))]
        pairs=[[a,b] for a in nodes for b in sorted(graph.get(a,set())&set(nodes)) if a<b and a in graph.get(b,set())]
        groups.append({'id':f'CYCLE-{len(groups)+1:02d}','nodes':nodes,'node_count':len(nodes),'edge_count':len(edges),'edges':edges,'direct_pairs':pairs,'witness':witness(graph,nodes),'status':'reported_not_modified'})
    primary=[r for r in records if r['scope']=='skill']; statuses=Counter(r['status'] for r in primary)
    per={n:{'markdown_files':sum(1 for p in sources if p.parts[1]==n),'reference_occurrences':sum(1 for r in primary if Path(r['source']).parts[1]==n),'statuses':dict(Counter(r['status'] for r in primary if Path(r['source']).parts[1]==n))} for n in NAMES}
    return {'scope':{'skill_markdown_files':len(sources),'source_files':[p.as_posix() for p in sources],'transitive_markdown_files':len(visited-initial),'transitive_file_list':[p.as_posix() for p in sorted(visited-initial)],'all_skill_files':sum(p.is_file() for n in NAMES for p in (root/'skills'/n).rglob('*'))},'summary':{'reference_occurrences':len(primary),'statuses':dict(statuses),'existing_unique_targets':len({r['target'] for r in primary if r['status']=='exists'}),'markdown_graph_edges':sum(len(e) for e in graph.values()),'cycle_groups':len(groups),'cyclic_files':sum(g['node_count'] for g in groups),'self_references':sum(1 for a,e in graph.items() if a in e),'direct_cycle_pairs':sum(len(g['direct_pairs']) for g in groups)},'per_skill':per,'cycles':groups,'references':records,'limitations':['External URLs are inventoried but not network-tested.','File fragments are retained but heading anchors are not validated.','Bare paths use explicit resolution modes, not Markdown URL semantics.','Templates/output examples are reported separately; unresolved items require review, never silently pass.','SCC groups compactly cover all cyclic edges; witnesses and direct pairs are examples, not an exhaustive enumeration of every simple cycle.','A static reference cycle does not by itself prove a runtime infinite loop.']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json',type=Path)
    parser.add_argument('--follow-outside',action='store_true')
    args=parser.parse_args();report=scan(args.root,args.follow_outside)
    if args.json:args.json.parent.mkdir(parents=True,exist_ok=True);args.json.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'scope':report['scope']|{'source_files':None},'summary':report['summary'],'per_skill':report['per_skill']},ensure_ascii=False))
    if any(r['status'] in ('missing','ambiguous','undefined_reference','unresolved_output_or_example') for r in report['references']):return 1
    if report['cycles'] or any(r['status'].startswith('historical_') or r['status']=='unpublished_private_artifact' for r in report['references']):return 2
    return 0

if __name__=='__main__':
    raise SystemExit(main())
