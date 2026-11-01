#!/usr/bin/env python3
"""Pull-only deploy with explicit public files and per-file atomic replacement."""
from pathlib import Path
import os, sys, subprocess, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1]
FILES=['index.html','style.css','words.js','core.js','i18n.js','app.js','manifest.webmanifest','icon.svg','icon-192.png','icon-512.png','flag-pt.svg','flag-en.svg','release.json','sw.js']
def fail(msg): raise SystemExit('ERROR: '+msg)
def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
def main():
 if len(sys.argv)!=2: fail('Usage: bash scripts/deploy.sh /absolute/existing/webroot')
 supplied=Path(sys.argv[1])
 if not supplied.is_absolute() or not supplied.is_dir(): fail('Destination must be an existing absolute directory')
 dest=supplied.resolve()
 if dest==Path('/') or dest==ROOT or dest in ROOT.parents or ROOT in dest.parents: fail('Source and destination must not overlap')
 if not os.access(dest,os.W_OK): fail('Destination is not writable')
 if not git('rev-parse','--show-toplevel')==str(ROOT): fail('Expected a dedicated repository checkout')
 if not git('symbolic-ref','--short','HEAD'): fail('Detached branch')
 if git('status','--porcelain','--untracked-files=all'): fail('Checkout must be clean, including untracked files')
 git('rev-parse','--abbrev-ref','@{upstream}')
 subprocess.run(['git','-C',str(ROOT),'fetch','--prune'],check=True)
 if int(git('rev-list','--count','@{upstream}..HEAD')): fail('Host has commits absent from upstream; refusing to deploy')
 subprocess.run(['git','-C',str(ROOT),'pull','--ff-only'],check=True)
 if git('status','--porcelain','--untracked-files=all'): fail('Checkout changed during pull')
 sources=[(ROOT/'public'/name,dest/name) for name in FILES]
 if (ROOT/'public').is_symlink(): fail('Symlinked public source')
 for source,target in sources:
  if source.is_symlink() or not source.is_file(): fail('Missing, nonregular or symlinked source: '+str(source))
  if target.is_symlink() or (target.exists() and not target.is_file()): fail('Nonregular or symlinked target: '+str(target))
 # Stage every asset before replacing any public file. sw.js is intentionally last.
 stage=Path(tempfile.mkdtemp(prefix='.verbal-stage-',dir=dest))
 try:
  os.chmod(stage,0o700)
  for source,target in sources:
   temp=stage/target.name
   shutil.copyfile(source,temp);os.chmod(temp,0o644)
  for source,target in sources:
   if target.is_symlink() or (target.exists() and not target.is_file()): fail('Destination changed while staging')
  for source,target in sources: os.replace(stage/target.name,target)
 finally: shutil.rmtree(stage)
 print('Verbal deployed from '+git('rev-parse','--short','HEAD')+' to '+str(dest))
 print('Only allowlisted assets replaced. Unrelated files, including .htaccess, preserved.')
if __name__=='__main__':
 try: main()
 except subprocess.CalledProcessError as e: fail('Git failed; publication stopped: '+str(e))
