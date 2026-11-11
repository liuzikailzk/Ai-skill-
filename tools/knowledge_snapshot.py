#!/usr/bin/env python3
"""Validate once per unchanged working snapshot; never mix index and source revisions."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

def digest(data):
    return hashlib.sha256(data).hexdigest()

def atomic_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(value, f, ensure_ascii=False, indent=2); f.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)

def validated_catalog(root, cache_path=None):
    from query_knowledge import load_catalog, safe_path, validate
    root = Path(root).resolve()
    catalog_bytes = (root/'knowledge/catalog.json').read_bytes()
    catalog = json.loads(catalog_bytes)
    paths = {'knowledge/catalog.json', 'AGENTS.md'}
    paths.update(e['path'] for e in catalog['entries'])
    paths.update(p.relative_to(root).as_posix() for p in (root/'skills').glob('*/SKILL.md'))
    paths.update(p.relative_to(root).as_posix() for p in (root/'tools').glob('*.py'))
    for extra in ('knowledge/taxonomy.json','knowledge/learning.md','knowledge/maintenance.md'):
        if (root/extra).exists(): paths.add(extra)
    def signature():
        items = {}
        for path in sorted(paths):
            p = safe_path(root, path)
            if not p.is_file() or (root/path).is_symlink(): raise ValueError('Invalid snapshot file: '+path)
            s = p.stat()
            items[path] = [s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_ino]
        head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
        return {'head':head, 'files':items, 'catalog_sha256':digest((root/'knowledge/catalog.json').read_bytes())}
    sig = signature()
    if sig['catalog_sha256'] != digest(catalog_bytes): raise ValueError('Catalog changed during loading; retry')
    cache_path = Path(cache_path) if cache_path else Path(os.environ.get('XDG_CACHE_HOME', str(Path.home()/'.cache')))/'ai-skill'/digest(str(root).encode())/'snapshot.json'
    try: cached = json.loads(cache_path.read_text())
    except (OSError, ValueError): cached = {}
    cache_hit = cached.get('schema') == 1 and cached.get('signature') == sig
    if not cache_hit:
        validate(root)
        if signature() != sig: raise ValueError('Repository changed during validation; retry on a fixed revision')
        atomic_json(cache_path, {'schema':1,'signature':sig})
    snapshot_id = digest(json.dumps(sig,sort_keys=True).encode())
    return catalog, {'id':snapshot_id,'commit':sig['head'],'catalog_sha256':sig['catalog_sha256'],'validation_reused':cache_hit}
