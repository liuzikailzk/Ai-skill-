#!/usr/bin/env python3
"""Verify all public Skill files using an immutable base and control-rule delta."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
top=json.loads((root/'registry/latest.json').read_text())
if top.get('schema')==3:
    rel=Path(top['base_manifest'])
    assert not rel.is_absolute() and '..' not in rel.parts
    manifest=json.loads((root/'registry'/rel).read_text())
    for name,change in top['overrides'].items():
        s=manifest['skills'][name]
        assert change['path']==s['path'] and change['version']==s['version']
        s['files'].update(change['files'])
        s['file_count']=len(s['files'])
        s['content_sha256']=hashlib.sha256(json.dumps(s['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    manifest['release_id']=top['release_id']
else:
    manifest=top
expected=set();count=0
for name,skill in manifest['skills'].items():
    assert name in ['script-visual-assets','script-video-shot-director','manga-reasoning-storyboard']
    base=root/skill['path'];assert base==root/'skills'/name
    fs=skill['files']
    assert len(fs)==skill['file_count']
    assert hashlib.sha256(json.dumps(fs,sort_keys=True,separators=(',',':')).encode()).hexdigest()==skill['content_sha256']
    for rel,record in fs.items():
        p=base/rel;assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
        assert p.is_file() and not p.is_symlink(),str(p)
        data=p.read_bytes()
        assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],str(p)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==record['git_blob_sha'],str(p)
        expected.add(p.relative_to(root).as_posix());count+=1
actual={p.relative_to(root).as_posix() for p in (root/'skills').rglob('*') if p.is_file()}
assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
# Shared rule bodies are outside packages but are part of this published release.
shared = manifest.get('shared_files', {})
actual_shared = {p.relative_to(root).as_posix() for p in (root/'knowledge/shared').rglob('*') if p.is_file()}
assert set(shared) == actual_shared, 'Shared rule inventory mismatch'
for path, record in shared.items():
    p = root/path
    assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink()
    data = p.read_bytes()
    assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], path
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == record['git_blob_sha'], path
print(json.dumps({'result':'PASS','skills':len(manifest['skills']),'files':count,'shared_files':len(shared),'release_id':manifest['release_id'],'scope':'Public repository file integrity'},ensure_ascii=False))
if (root/'registry/version-policy.json').is_file():
    import subprocess,sys
    subprocess.run([sys.executable,str(root/'tools/verify_versions.py')],check=True)
