#!/usr/bin/env python3
"""One reproducible, read-only entry point for release checks."""
import os
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT/'skills/script-video-shot-director/scripts'))
commands=[
    ['-m','unittest','discover','-s','tools/tests','-v'],
    ['-m','unittest','discover','-s','skills/script-video-shot-director/tests','-v'],
    ['tools/verify_backup.py'],['tools/verify_versions.py','--policy-cases'],
    ['tools/query_knowledge.py','--validate'],['tools/check_references.py','--follow-outside'],
    ['tools/build_knowledge_views.py','--check'],['tools/plan_learning.py','--check-index'],
]
paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
for path in set(paths):
    if path.endswith('.json') and (ROOT/path).is_file():json.loads((ROOT/path).read_text())
catalog=json.loads((ROOT/'knowledge/catalog.json').read_text());ids={e['id'] for e in catalog['entries']}
taxonomy=json.loads((ROOT/'knowledge/taxonomy.json').read_text())
for facet,targets in taxonomy['method_routes'].items():
    group,label=facet.split(':',1)
    assert label in taxonomy['facets'][group] and set(targets)<=ids, 'Invalid taxonomy route: '+facet
for args in commands:subprocess.run([sys.executable]+args,cwd=ROOT,env=env,check=True)
print('PASS: repository checks; generated media and user preference are not evaluated')
