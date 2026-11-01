#!/usr/bin/env python3
"""Refresh integrity metadata after changing any public asset; no third-party deps."""
from pathlib import Path
import hashlib,json,re
p=Path(__file__).resolve().parents[1]/'public'
sw=(p/'sw.js').read_text();version=re.search("VERSION='([^']+)'",sw).group(1)
assert "VERSION='"+version+"'" in (p/'app.js').read_text(), 'Version mismatch'
files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.iterdir()) if f.is_file() and f.name not in ('sw.js','release.json')}
body=(json.dumps({'version':version,'files':files},sort_keys=True,separators=(',',':'))+'\n').encode()
(p/'release.json').write_bytes(body)
hash=hashlib.sha256(body).hexdigest();(p/'sw.js').write_text(re.sub("MANIFEST_HASH='[^']+'","MANIFEST_HASH='"+hash+"'",sw))
print('Integrity metadata ready for Verbal '+version)
