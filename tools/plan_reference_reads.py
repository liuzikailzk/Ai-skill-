#!/usr/bin/env python3
"""Plan explicit rule roots and one direct layer; never parse a dependency."""
import argparse
import json
from pathlib import Path
from check_references import extract, resolve

def plan(root, seeds, state=None):
    root=Path(root).resolve();canonical=[];state=state or {}
    for source in seeds:
        p=(root/source).resolve()
        if not p.is_relative_to(root) or not p.is_file():raise ValueError('Invalid explicit root: '+source)
        canonical.append(p.relative_to(root).as_posix())
    seeds=sorted(set(canonical))
    if state.get('seed_roots') is not None and state['seed_roots']!=seeds:
        raise ValueError('Task roots are fixed; do not promote a dependency to a new root to reset depth')
    for source in seeds:
        p=(root/source).resolve()
        if not p.is_relative_to(root) or not p.is_file():raise ValueError('Invalid explicit root: '+source)
    visited=set(state.get('read_paths',[]));planned={};skipped=[]
    for source in seeds:
        planned[source]={'path':source,'depth':0,'via':None}
    for source in seeds:
        text=(root/source).read_text()  # Only seed contents are parsed, not B/C contents.
        for number,raw,kind,line,code in extract(text):
            ref=resolve(root,Path(source),raw,kind,line,code)
            target=ref.get('target')
            if ref['status']!='exists' or not target:continue
            if target==source:
                skipped.append({'path':target,'reason':'self_reference_ignored'});continue
            if Path(target).suffix not in ('.md','.json','.txt','.yaml','.yml'):continue
            if target not in planned:planned[target]={'path':target,'depth':1,'via':source,'line':number}
    return {'max_reference_depth':1,'seed_roots':seeds,'planned_reads':[v for k,v in planned.items() if k not in visited],
            'already_read_skipped':sorted(set(planned)&visited),'skipped':skipped,
            'rule':'Stop after a depth-1 file; do not follow its outgoing links or reset roots. Static file inventories are not runtime rule loading.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('seeds',nargs='+');p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--state',type=Path);a=p.parse_args()
    state=json.loads(a.state.read_text()) if a.state and a.state.exists() else None
    result=plan(a.root,a.seeds,state)
    if a.state and not a.state.exists():
        a.state.parent.mkdir(parents=True,exist_ok=True);a.state.write_text(json.dumps({'seed_roots':result['seed_roots'],'read_paths':[]},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
