#!/usr/bin/env python3
"""Create self-contained solo deduction sheets. Dev-only: ReportLab, Node; no app changes."""
from pathlib import Path
import json, random, subprocess, sys
from collections import Counter
from functools import reduce
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'
TMP=ROOT/'tmp/pdfs'
FONT=ROOT.parent/'doctools/web/vendor/pdfjs/standard_fonts'
for name,file in [('Body','LiberationSans-Regular.ttf'),('Bold','LiberationSans-Bold.ttf')]:
 if (FONT/file).exists():pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
 else:
  from reportlab.pdfbase.pdfmetrics import Font
  pdfmetrics.registerFont(Font(name,'Helvetica-Bold' if name=='Bold' else 'Helvetica','WinAnsiEncoding'))
banks=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);vm.runInContext(fs.readFileSync('public/words.js','utf8')+';this.b=BANKS;',c);process.stdout.write(JSON.stringify(c.b));"],cwd=ROOT,text=True))
def score(guess,answer):
 out=['x']*len(answer);left=Counter(answer)
 for i,ch in enumerate(guess):
  if ch==answer[i]:out[i]='=';left[ch]-=1
 for i,ch in enumerate(guess):
  if out[i]!='=' and left[ch]>0:out[i]='~';left[ch]-=1
 return ''.join(out)
def make(answer,index,bank_size=None,count=None):
 n=len(answer);bank_size=bank_size or (8 if index<4 else 12 if index<8 else 16);count=count or (2 if index<4 else 3)
 rng=random.Random(20261102+index)
 pool=[w for w in banks[str(n)] if w!=answer]
 assert answer in banks[str(n)]
 ranked=sorted(pool,key=lambda w:(-sum((Counter(w)&Counter(answer)).values()),-sum(a==b for a,b in zip(w,answer)),w))[:100]
 for attempt in range(600):
  candidates=sorted([answer]+rng.sample(ranked,bank_size-1));masks={}
  for word in pool:
   feedback=score(word,answer);mask=sum(1<<i for i,w in enumerate(candidates) if score(word,w)==feedback)
   if mask not in masks:masks[mask]=(word,feedback)
  full=(1<<bank_size)-1;chosen=[];remaining=full
  for step in range(count):
   valid=[]
   for mask,(word,feedback) in masks.items():
    result=remaining&mask;size=result.bit_count()
    if step<count-1 and count-step<=size<remaining.bit_count() or step==count-1 and size==1:
     if mask.bit_count()>1 and word not in [r[0] for r in chosen]:valid.append((mask,word,feedback,result))
   rng.shuffle(valid)
   if step==count-1:
    valid=[v for v in valid if all((full & v[0] & reduce(lambda a,b:a&b,[r[2] for j,r in enumerate(chosen) if j!=remove],full)).bit_count()>1 for remove in range(len(chosen)))]
   if not valid:break
   mask,word,feedback,remaining=valid[0];chosen.append((word,feedback,mask))
  if len(chosen)==count and remaining.bit_count()==1:
   clues=[{'word':w,'score':s} for w,s,_ in chosen]
   survivors=[w for w in candidates if all(score(row['word'],w)==row['score'] for row in clues)]
   assert survivors==[answer]
   return {'number':index+1,'length':n,'answer':answer,'bank':candidates,'clues':clues}
 raise RuntimeError('Cannot construct irredundant puzzle: '+answer)
answers=['CASA','GATO','MESA','LAGO','LIVRO','PRAIA','CAVALO','JANELA','FORMIGA','LARANJA','CASTANHA','MONTANHA']
puzzles=[make(word,i) for i,word in enumerate(answers)]
# Independent check against the app's repeated-letter scorer for every candidate/clue.
cases=[[r['word'],w] for p in puzzles for r in p['clues'] for w in p['bank']]
actual=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),C=require('./public/core.js'),cases=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(cases.map(([g,a])=>C.score(g,a).map(v=>({correct:'=',present:'~',absent:'x'})[v]).join(''))));"],cwd=ROOT,input=json.dumps(cases),text=True))
assert actual==[score(g,a) for g,a in cases]
for p in puzzles:
 for omitted in range(len(p['clues'])):
  others=[r for i,r in enumerate(p['clues']) if i!=omitted]
  assert sum(all(score(r['word'],w)==r['score'] for r in others) for w in p['bank'])>1
TEXT={
'en':dict(sub='Solo deduction puzzles - paper and pencil only',levels=['Warm-up','Look closer','Fine detail'],rules=['One word from each bank is the hidden answer. The guesses below already have their feedback.','Cross out words that contradict a clue, then write the only possible answer. No new feedback is needed.','Accents and cedillas are normalized. Plurals are allowed. You need no dictionary or device.'],legend='=  correct place       ~  present elsewhere       x  no further copy of this letter',repeat='Repeated letters count: x can mean no extra copy, even when another copy is marked = or ~.',letters='letters',bank='Word bank - cross out impossible candidates',answer='Your answer',notes='Notes',footer='Print pages 1-3 for play. Keep page 4 aside until you want to check.',solutions='Solutions',solosub='Keep this page separate from the puzzles.',only='Each puzzle has exactly one answer within its printed word bank.',verified='Every clue is needed: removing any one leaves more than one candidate.',end='A complete paper game: no hidden-answer lookup is needed while solving.'),
'pt':dict(sub='Desafios de dedução a solo - só papel e lápis',levels=['Para começar','Olhar com atenção','Pormenores'],rules=['Uma palavra de cada lista é a resposta. As tentativas abaixo já têm as respetivas pistas.','Risca as palavras que contradizem alguma pista e escreve a única resposta possível. Não precisas de novas pistas.','Acentos e cedilhas são normalizados. São aceites plurais. Não precisas de dicionário nem de um dispositivo.'],legend='=  posição certa       ~  existe noutra posição       x  não existe outra ocorrência desta letra',repeat='As repetições contam: x pode significar que não há outra cópia, mesmo que uma esteja marcada com = ou ~.',letters='letras',bank='Palavras possíveis - risca as que não servem',answer='A tua resposta',notes='Notas',footer='Imprime as páginas 1-3 para jogar. Guarda a página 4 para conferir no fim.',solutions='Soluções',solosub='Mantém esta página separada dos desafios.',only='Cada desafio tem exatamente uma resposta entre as palavras da sua lista.',verified='Todas as pistas são necessárias: sem uma delas, sobra mais de uma candidata.',end='Um jogo completo em papel: não precisas de consultar a resposta enquanto resolves.')}
W,H=A4
M=32
CW=(W-2*M-24)/2
BODY_TOP=H-185
CARD_H=(BODY_TOP-43-20)/2

def text(c,x,y,value,size=10,font='Body'):
 c.setFont(font,size);c.setFillGray(0);c.drawString(x,y,value)
def fitted(c,x,y,value,width,size=10,font='Body'):
 assert pdfmetrics.stringWidth(value,font,size)<=width,(value,pdfmetrics.stringWidth(value,font,size),width)
 text(c,x,y,value,size,font)
def header(c,t,page):
 text(c,M,H-53,'v. verbal',31,'Bold');text(c,M,H-76,t['sub'],11)
 c.setLineWidth(.8);c.line(M,H-88,W-M,H-88)
 for i,line in enumerate(t['rules']):fitted(c,M,H-105-i*14,line,W-2*M,9.0)
 fitted(c,M,H-153,t['legend'],W-2*M,10,'Bold')
 fitted(c,M,H-168,t['repeat'],W-2*M,8.6)
 text(c,W-M-100,H-48,t['levels'][page],10,'Bold')
def footer(c,t,page):
 c.setLineWidth(.4);c.line(M,30,W-M,30);fitted(c,M,17,t['footer'],W-2*M-35,8);text(c,W-M-15,17,str(page)+'/4',8)
def cells(c,x,y,word,feedback=None,blank=False):
 size=25;gap=2;height=30
 for i,ch in enumerate(word):
  left=x+i*(size+gap);c.setLineWidth(.5);c.rect(left,y,size,height,stroke=1,fill=0)
  if not blank:
   c.setFont('Bold',16);c.drawCentredString(left+size/2,y+13,ch)
   c.setFont('Bold',9);c.drawCentredString(left+size/2,y+3,feedback[i])
def card(c,t,p,x,top):
 text(c,x,top,f"{p['number']:02d}   /   {p['length']} {t['letters']}",12,'Bold')
 c.setLineWidth(.4);c.line(x,top-8,x+CW,top-8)
 cursor=top-43
 for row in p['clues']:cells(c,x,cursor,row['word'],row['score']);cursor-=32
 cursor-=1;text(c,x,cursor,t['bank'],8.5,'Bold');cursor-=15
 cols=4 if p['length']<=5 else 3
 col_width=CW/cols
 for i,word in enumerate(p['bank']):
  xx=x+(i%cols)*col_width;yy=cursor-(i//cols)*13
  c.setLineWidth(.4);c.rect(xx,yy,5,5,stroke=1,fill=0)
  fitted(c,xx+9,yy-1,word,col_width-10,9,'Bold')
 cursor-=((len(p['bank'])+cols-1)//cols)*13+11
 text(c,x,cursor,t['answer'],9,'Bold');cursor-=35;cells(c,x,cursor,' '*p['length'],blank=True)
 cursor-=14;text(c,x,cursor,t['notes'],8);c.setLineWidth(.3);c.line(x+29,cursor-1,x+CW,cursor-1)
 assert cursor>top-CARD_H+2,('Card overflow',p['number'],cursor,top-CARD_H)
def build(lang):
 t=TEXT[lang];name='verbal-paper-solo-en.pdf' if lang=='en' else 'verbal-papel-solo-pt.pdf';path=OUT/name
 c=canvas.Canvas(str(path),pagesize=A4,pageCompression=1);c.setTitle('Verbal - '+t['sub']);c.setAuthor('BaseCentral / Verbal');c.setSubject('12 self-contained paper-and-pencil word deduction puzzles; separate solutions')
 for page in range(3):
  header(c,t,page)
  for i,p in enumerate(puzzles[page*4:page*4+4]):card(c,t,p,M+(i%2)*(CW+24),BODY_TOP-(i//2)*(CARD_H+20))
  footer(c,t,page+1);c.showPage()
 text(c,M,H-56,'v. verbal',31,'Bold');text(c,M,H-98,t['solutions'],25,'Bold');text(c,M,H-122,t['solosub'],11)
 c.setLineWidth(.8);c.line(M,H-140,W-M,H-140)
 for i,p in enumerate(puzzles):
  col=i%3;row=i//3;x=M+col*(W-2*M)/3;y=H-190-row*105
  text(c,x,y,f"{p['number']:02d} / {p['length']} {t['letters']}",10)
  text(c,x,y-25,p['answer'],17,'Bold')
  text(c,x,y-45,' / '.join(r['word'] for r in p['clues'][:2]),8)
  if len(p['clues'])>2:text(c,x,y-58,' / '.join(r['word'] for r in p['clues'][2:]),8)
 fitted(c,M,145,t['only'],W-2*M,11,'Bold');fitted(c,M,125,t['verified'],W-2*M,10)
 fitted(c,M,95,t['end'],W-2*M,10);footer(c,t,4);c.save();return path
def catalogue():
 # Freeze the original playable catalogue. Appending print-only ids must never
 # change a stored daily/free puzzle's identity or invalidate its backup.
 data=json.loads((ROOT/'scripts/fixtures/paper-print-1000.json').read_text())
 assert len(data)==1000
 assert data[:400]==json.loads((ROOT/'scripts/fixtures/paper-print-400.json').read_text())
 assert data[:60]==json.loads((ROOT/'scripts/fixtures/paper-v1.json').read_text())
 for n in range(4,9):
  chosen=[p for p in data if p['length']==n]
  added=[]
  for i,word in enumerate(banks[str(n)]):
   if len(data)+len(added)>=1700:break
   if any(p['answer']==word for p in chosen+added):continue
   try:p=make(word,40000+n*1000+i,8 if n==4 else 12 if n<7 else 16,2 if n==4 else 3)
   except RuntimeError:
    try:p=make(word,40000+n*1000+i,12,2)
    except RuntimeError:continue
   p=dict(p);p.pop('number');p['id']='paper-print-v4-'+str(n)+'-'+str(len(added)+1);added.append(p)
  data.extend(added)
  print('Verified length',n,':',len(chosen)+len(added),'puzzles; total',len(data),flush=True)
 assert len(data)==1700 and len({p['id'] for p in data})==1700 and len({p['answer'] for p in data})==1700
 for p in data:
  assert [w for w in p['bank'] if all(score(r['word'],w)==r['score'] for r in p['clues'])]==[p['answer']]
  for omitted in range(len(p['clues'])):
   rows=[r for j,r in enumerate(p['clues']) if j!=omitted]
   assert sum(all(score(r['word'],w)==r['score'] for r in rows) for w in p['bank'])>1
 target=ROOT/'public/paper-data.js'
 if target.exists():
  existing=json.loads(subprocess.check_output(['node','-e',"process.stdout.write(JSON.stringify(require('./public/paper-data.js')));"],cwd=ROOT,text=True))
  if data[:len(existing)]!=existing:raise RuntimeError('Released puzzle definitions/order changed; retain old ids and data')
 body="/* Immutable paper-v1 gameplay and append-only print-v2/v3/v4 catalogue. Preserve ids/content/order. */\n(function(root){'use strict';var data="+json.dumps(data,separators=(',',':'))+";if(typeof module==='object'&&module.exports)module.exports=data;else root.VerbalPaperData=data;})(this);\n"
 target.write_text(body)
 print('Verified catalogue:',len(data),'puzzles,',target.stat().st_size,'bytes',flush=True)

if __name__=='__main__' and '--catalogue' in sys.argv:
 catalogue()
elif __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
 (TMP/'paper-puzzles.json').write_text(json.dumps(puzzles,indent=2)+'\n')
 for lang in ['en','pt']:print(build(lang))
 print('PASS: 12 unique solutions; every clue essential; all scoring matches Verbal core.')
