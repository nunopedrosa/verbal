#!/usr/bin/env python3
"""Disposable local Git repositories; never contacts the production host."""
import subprocess,tempfile,shutil
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]
def run(*args,cwd=None,ok=True):
 p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 assert (p.returncode==0)==ok,(args,p.stdout,p.stderr)
 return p
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);remote=t/'remote.git';repo=t/'repo';web=t/'web';web.mkdir()
 run('git','init','--bare',str(remote));run('git','clone',str(remote),str(repo))
 for name in ['public','scripts']:shutil.copytree(SOURCE/name,repo/name)
 run('git','config','user.email','test@example.invalid',cwd=repo);run('git','config','user.name','Test',cwd=repo)
 run('git','add','.',cwd=repo);run('git','commit','-m','initial',cwd=repo);run('git','push','-u','origin','HEAD',cwd=repo)
 def deploy(dest=web,ok=True):return run('bash',str(repo/'scripts/deploy.sh'),str(dest),ok=ok)
 (web/'.htaccess').write_text('preserve');(web/'other.txt').write_text('preserve');deploy();assert (web/'index.html').read_bytes()==(repo/'public/index.html').read_bytes();assert (web/'.htaccess').read_text()=='preserve';assert not (web/'deploy.py').exists();assert not list(web.glob('.verbal-stage-*'))
 (repo/'dirty').write_text('x');deploy(ok=False);(repo/'dirty').unlink()
 deploy(repo/'public',ok=False)
 (web/'words.js').unlink();(web/'words.js').symlink_to(web/'other.txt');deploy(ok=False);assert (web/'other.txt').read_text()=='preserve';(web/'words.js').unlink()
 (repo/'public/icon.svg').write_text('ahead');run('git','add','.',cwd=repo);run('git','commit','-m','ahead',cwd=repo);deploy(ok=False)
 run('git','push',cwd=repo);deploy()
 run('git','checkout','--detach',cwd=repo);deploy(ok=False)
 print('PASS: clean pull deployment, allowlist, preserved files, stage cleanup, dirty/ahead/detached refusal, overlap and symlink safety.')
