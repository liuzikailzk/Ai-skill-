#!/usr/bin/env python3
"""Plan explicit rule roots and one direct layer; never parse a dependency."""
import argparse
import json
import hashlib
from pathlib import Path
from check_references import extract, resolve

def plan(root, seeds, state=None, selected_paths=None, project_revision=''):
    root=Path(root).resolve();canonical=[];state=state or {}
    for source in seeds:
        p=(root/source).resolve()
        if not p.is_relative_to(root) or not p.is_file():raise ValueError('Invalid explicit root: '+source)
        canonical.append(p.relative_to(root).as_posix())
    seeds=sorted(set(canonical))
    if state.get('seed_roots') is not None and state['seed_roots']!=seeds:
        raise ValueError('Task roots are fixed; do not promote a dependency to a new root to reset depth')
    if state.get('read_hashes') and (not project_revision or state.get('project_revision')!=project_revision):
        raise ValueError('Read-state reuse requires the same explicit project/task revision')
    for source in seeds:
        p=(root/source).resolve()
        if not p.is_relative_to(root) or not p.is_file():raise ValueError('Invalid explicit root: '+source)
    planned={};skipped=[]
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
    allowed=list(planned)
    if selected_paths is not None:
        selected=set()
        for path in selected_paths:
            p=(root/path).resolve()
            if not p.is_relative_to(root):raise ValueError('Selected path leaves repository')
            selected.add(p.relative_to(root).as_posix())
        if not selected <= set(planned):raise ValueError('Selected file is not directly reachable from task roots')
        planned={k:v for k,v in planned.items() if k in selected or k in seeds}
    root_hashes={source:hashlib.sha256((root/source).read_bytes()).hexdigest() for source in seeds}
    receipts=state.get('read_hashes',{}) if state.get('root_hashes')==root_hashes else {}
    visited={k for k in planned if receipts.get(k)==hashlib.sha256((root/k).read_bytes()).hexdigest()}
    return {'max_reference_depth':1,'seed_roots':seeds,'project_revision':project_revision,'root_hashes':root_hashes,'allowed_direct_paths':allowed,
            'selection_required':selected_paths is None,
            'planned_reads':[v for k,v in planned.items() if k not in visited],
            'already_read_skipped':sorted(set(planned)&visited),'skipped':skipped,
            'rule':'Without selected_paths this is only an allowed-file inventory, NOT a mandatory reading list. Legacy path-only receipts are invalidated. Stop after depth 1.'}

def record_successful_reads(root, seeds, successful_paths, state=None, project_revision=''):
    """Call only after successful reading; planning never marks anything as read."""
    if not project_revision:raise ValueError('Recording reads requires an explicit project/task revision')
    result=plan(root,seeds,state,successful_paths,project_revision)
    hashes=dict((state or {}).get('read_hashes',{})) if (state or {}).get('root_hashes')==result['root_hashes'] else {}
    for path in successful_paths:
        p=(Path(root)/path).resolve();key=p.relative_to(Path(root).resolve()).as_posix()
        hashes[key]=hashlib.sha256(p.read_bytes()).hexdigest()
    return {'schema':2,'seed_roots':result['seed_roots'],'project_revision':project_revision,'root_hashes':result['root_hashes'],'read_hashes':hashes}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('seeds',nargs='+');p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--state',type=Path);p.add_argument('--selected',nargs='*');p.add_argument('--project-revision',default='');a=p.parse_args()
    state=json.loads(a.state.read_text()) if a.state and a.state.exists() else None
    if a.state and not a.project_revision:p.error('--state requires --project-revision')
    result=plan(a.root,a.seeds,state,a.selected,a.project_revision)
    if a.state and not a.state.exists():
        a.state.parent.mkdir(parents=True,exist_ok=True);a.state.write_text(json.dumps({'schema':2,'seed_roots':result['seed_roots'],'project_revision':a.project_revision,'root_hashes':result['root_hashes'],'read_hashes':{}},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
