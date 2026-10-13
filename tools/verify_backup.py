#!/usr/bin/env python3
"""Read-only verification of the complete backed-up skill payload."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'registry/latest.json').read_text())
expected=set();count=0
for name,skill in manifest['skills'].items():
    assert name in ['script-visual-assets','script-video-shot-director','manga-reasoning-storyboard'],name
    base=root/skill['path'];assert base==root/'skills'/name
    files=skill['files']
    assert len(files)==skill['file_count'],name
    assert hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()==skill['content_sha256'],name
    for rel,record in files.items():
        p=base/rel;assert not Path(rel).is_absolute() and '..' not in Path(rel).parts,rel
        assert p.is_file() and not p.is_symlink(),str(p)
        data=p.read_bytes();assert len(data)==record['bytes'],str(p)
        assert hashlib.sha256(data).hexdigest()==record['sha256'],str(p)
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==record['git_blob_sha'],str(p)
        expected.add(p.relative_to(root).as_posix());count+=1
actual={p.relative_to(root).as_posix() for p in (root/'skills').rglob('*') if p.is_file()}
assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
print(json.dumps({'result':'PASS','skills':len(manifest['skills']),'files':count,'release_id':manifest['release_id'],'scope':'Local file integrity only'},ensure_ascii=False))
