#!/usr/bin/env python3
"""Refresh derived file hashes after an explicitly authorized source/version edit."""
import hashlib
import json
import re
from pathlib import Path
from query_knowledge import ROOT
from build_knowledge_views import generate

def record(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}

def refresh(root=ROOT):
    root=Path(root)
    catalog=json.loads((root/'knowledge/catalog.json').read_text())
    roots=['knowledge/learning.md','knowledge/maintenance.md']+[p.relative_to(root).as_posix() for p in (root/'skills').glob('*/SKILL.md')]
    direct={rp:{((root/rp).parent/link.split('#')[0]).resolve() for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(root/rp).read_text()) if not re.match(r'\w+://',link)} for rp in roots}
    for e in catalog['entries']:
        e['sha256']=record(root/e['path'])['sha256']
        e['rule_roots']=sorted(rp for rp,targets in direct.items() if (root/e['path']).resolve() in targets)
    (root/'knowledge/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    for path,text in generate(root).items():
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    latest=json.loads((root/'registry/latest.json').read_text())
    if latest.get('schema')!=2:raise ValueError('Expected full schema-2 release manifest; do not flatten legacy delta manifests silently')
    for name,s in latest['skills'].items():
        folder=root/s['path'];s['version']=json.loads((folder/'version.json').read_text())['version']
        s['files']={p.relative_to(folder).as_posix():record(p) for p in sorted(folder.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
        s['file_count']=len(s['files']);s['content_sha256']=hashlib.sha256(json.dumps(s['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    latest['shared_files']={p.relative_to(root).as_posix():record(p) for p in sorted((root/'knowledge/shared').rglob('*')) if p.is_file()}
    paths={'AGENTS.md','README.md','requirements-dev.txt','knowledge/catalog.json','knowledge/taxonomy.json','knowledge/library-map.md','knowledge/learning.md','knowledge/maintenance.md','knowledge/skill-refresh.md','registry/library-inventory.json'}
    paths.update(p.relative_to(root).as_posix() for folder in ('tools','knowledge/views','.github/workflows') for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    latest['runtime_files']={p:record(root/p) for p in sorted(paths)}
    (root/'registry/latest.json').write_text(json.dumps(latest,ensure_ascii=False,indent=2)+'\n')
    return {'skills':len(latest['skills']),'shared_files':len(latest['shared_files']),'runtime_files':len(paths)}

if __name__=='__main__':print(json.dumps(refresh()))
