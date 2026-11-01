#!/usr/bin/env python3
"""Exercise the actual common engine/profile using only disposable local Git repos."""
import subprocess,tempfile,shutil,hashlib,os
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]
def run(*args,cwd=None,ok=True,env=None):
 p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
 assert (p.returncode==0)==ok,(args,p.stdout,p.stderr)
 return p
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);remote=t/'remote.git';repo=t/'repo';author=t/'author';web=t/'web';web.mkdir()
 run('git','init','--bare',str(remote));run('git','clone',str(remote),str(author))
 for name in ['public','scripts']:shutil.copytree(SOURCE/name,author/name)
 for checkout in [author]:
  run('git','config','user.email','test@example.invalid',cwd=checkout);run('git','config','user.name','Test',cwd=checkout)
 def publish(message):
  run('git','add','.',cwd=author);run('git','commit','-m',message,cwd=author);run('git','push','-u','origin','HEAD',cwd=author)
 publish('initial');run('git','clone',str(remote),str(repo))
 run('git','config','user.email','test@example.invalid',cwd=repo);run('git','config','user.name','Test',cwd=repo)
 def deploy(*flags,dest=web,ok=True,env=None):return run('bash',str(repo/'scripts/deploy.sh'),*flags,str(dest),ok=ok,env=env)
 (web/'.htaccess').write_text('preserve');(web/'other.txt').write_text('preserve')
 before=sorted(p.name for p in web.iterdir());assert 'DRY RUN' in deploy('--dry-run').stdout;assert sorted(p.name for p in web.iterdir())==before
 deploy();assert (web/'index.html').read_bytes()==(repo/'public/index.html').read_bytes();assert (web/'.htaccess').read_text()=='preserve';assert (web/'other.txt').read_text()=='preserve';assert not (web/'scripts').exists();assert not list(web.glob('.basecentral-*'));assert (web/'index.html').stat().st_mode&0o777==0o644
 # Readonly dry-run does not fetch a newer remote; normal deployment pulls it.
 (author/'public/icon.svg').write_text((author/'public/icon.svg').read_text()+'\n');run('python3','scripts/prepare-release.py',cwd=author);publish('new valid release')
 head=run('git','rev-parse','HEAD',cwd=repo).stdout;deploy('--dry-run');assert run('git','rev-parse','HEAD',cwd=repo).stdout==head;deploy();assert run('git','rev-parse','HEAD',cwd=repo).stdout!=head
 (repo/'dirty').write_text('x');deploy(ok=False);(repo/'dirty').unlink();deploy(dest=repo/'public',ok=False)
 (web/'words.js').unlink();(web/'words.js').symlink_to(web/'other.txt');deploy(ok=False);assert (web/'other.txt').read_text()=='preserve';(web/'words.js').unlink()
 linked=t/'linked';linked.symlink_to(web,target_is_directory=True);deploy(dest=linked,ok=False)
 (repo/'public/icon.svg').write_text('ahead');run('git','add','.',cwd=repo);run('git','commit','-m','ahead',cwd=repo);deploy(ok=False);run('git','push',cwd=repo)
 # Even a clean pushed checkout cannot publish a mixed/stale release.
 old=(web/'icon.svg').read_bytes();result=deploy(ok=False);assert 'digest mismatch' in result.stderr;assert (web/'icon.svg').read_bytes()==old
 run('python3','scripts/prepare-release.py',cwd=repo);run('git','add','.',cwd=repo);run('git','commit','-m','refresh integrity',cwd=repo);run('git','push',cwd=repo)
 # --verify invokes HTTP checking; a fake curl avoids all external requests.
 bin=t/'bin';bin.mkdir();log=t/'curl.log';curl=bin/'curl';curl.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$VERIFY_LOG"\n');curl.chmod(0o755)
 env=dict(os.environ,PATH=str(bin)+os.pathsep+os.environ['PATH'],VERIFY_LOG=str(log));deploy('--verify',env=env);assert 'https://verbal.basecentral.link/' in log.read_text()
 run('git','checkout','--detach',cwd=repo);deploy(ok=False)
 print('PASS: shared deploy pull, readonly dry-run, verify, integrity, allowlist, permissions, preserved host files, locks/staging cleanup, dirty/ahead/detached, overlap and symlink safety.')
