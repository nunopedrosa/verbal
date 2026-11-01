#!/usr/bin/env python3
"""Refresh worker integrity metadata and private deployment checksums."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
p=root/'public'
profile=(root/'scripts/deploy-profile.sh').read_text()
allowed=re.search(r"PUBLIC_FILES=\$\(cat <<'PUBLIC_FILES'\n([\s\S]*?)\nPUBLIC_FILES\n\)",profile).group(1).splitlines()
actual=sorted(f.name for f in p.iterdir())
assert len(allowed)==len(set(allowed)) and sorted(allowed)==actual,'Public files differ from reviewed deployment allowlist'
assert all((p/name).is_file() and not (p/name).is_symlink() for name in allowed),'Nonregular public asset'
sw=(p/'sw.js').read_text();version=re.search("VERSION='([^']+)'",sw).group(1)
assert "VERSION='"+version+"'" in (p/'app.js').read_text(),'Version mismatch'
def sha(file):return hashlib.sha256(file.read_bytes()).hexdigest()
files={name:sha(p/name) for name in sorted(allowed) if name not in ('sw.js','release.json')}
body=(json.dumps({'version':version,'files':files},sort_keys=True,separators=(',',':'))+'\n').encode()
(p/'release.json').write_bytes(body)
(p/'sw.js').write_text(re.sub("MANIFEST_HASH='[^']+'","MANIFEST_HASH='"+hashlib.sha256(body).hexdigest()+"'",sw))
(root/'scripts/deploy-hashes.txt').write_text(''.join(sha(p/name)+' '+name+'\n' for name in sorted(allowed)))
print('Integrity metadata ready for Verbal '+version)
