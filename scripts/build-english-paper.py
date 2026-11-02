#!/usr/bin/env python3
"""Reproduce immutable English deduction catalogue from reviewed English banks.
No network or external packages. Released records must remain byte-equivalent.
"""
import json, random, subprocess
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def score(g,a):
 out=['x']*len(a);left=Counter(a)
 for i,c in enumerate(g):
  if c==a[i]:out[i]='=';left[c]-=1
 for i,c in enumerate(g):
  if out[i]!='=' and left[c]>0:out[i]='~';left[c]-=1
 return ''.join(out)
def make(answer, pool, index):
 rng=random.Random(71000+index);n=len(answer)
 others=[w for w in pool if w!=answer]
 for attempt in range(1000):
  bank=sorted([answer]+rng.sample(others,7));full=255;target=1<<bank.index(answer);masks={}
  for word in others:
   feedback=score(word,answer)
   mask=sum(1<<i for i,w in enumerate(bank) if score(word,w)==feedback)
   if mask.bit_count()>1 and mask!=full:masks.setdefault(mask,(word,feedback))
  pairs=[(a,b) for a in masks for b in masks if a<b and a&b==target]
  if pairs:
   a,b=rng.choice(pairs)
   return dict(length=n,answer=answer,bank=bank,clues=[dict(word=masks[m][0],score=masks[m][1]) for m in (a,b)])
 raise RuntimeError('Cannot construct '+answer)
def main():
 content=json.loads((ROOT/'vendor/english/editorial.json').read_text())
 data=json.loads((ROOT/'scripts/fixtures/paper-en-200.json').read_text())
 assert len(data)==200
 seen={p['answer'] for p in data}
 for n in range(4,9):
  pool=content['banks'][str(n)];added=0
  for i,answer in enumerate(pool):
   if answer in seen:continue
   p=make(answer,pool,20000+n*1000+i);added+=1
   p['id']=f'paper-en-print-v2-{n}-{added}';data.append(p);seen.add(answer)
 assert len(data)==1671 and len(seen)==1671
 target=ROOT/'public/paper-en-data.js'
 if target.exists():
  old=json.loads(subprocess.check_output(['node','-e',"process.stdout.write(JSON.stringify(require('./public/paper-en-data.js')));"],cwd=ROOT,text=True))
  assert data[:len(old)]==old,'Released English definitions changed'
 target.write_text("/* Immutable English deduction v1 and append-only print v2. Preserve released records. */\n(function(root){'use strict';var data="+json.dumps(data,separators=(',',':'))+";if(typeof module==='object'&&module.exports)module.exports=data;else root.VerbalPaperEnglishData=data;})(this);\n")
 print('Verified English catalogue:',len(data))
if __name__=='__main__':main()
