"""WeiDU Spell Trap isolation/lifetime contracts on real exports and guard fixtures.
Usage: python3 tests/verify_spelltrap.py EET_EXPORT WEIDU RESULT_DIR
Does not launch a game or simulate engine rendering/absorption.
"""
from pathlib import Path
import ast,hashlib,json,shutil,struct,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'sr_original_spell_animations'
SOURCE=Path(sys.argv[1]).resolve();WEIDU=Path(sys.argv[2]).resolve();OUT=Path(sys.argv[3]).resolve();OUT.mkdir(parents=True,exist_ok=True)
a=ast.parse((ROOT/'tests/verify_installer.py').read_text())
exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ('parse','opcode')],type_ignores=[]),'<helpers>','exec'))
files={p.name.lower():p.read_bytes() for p in SOURCE.iterdir() if p.is_file() and p.suffix.lower() in ('.spl','.eff','.vvc','.pro','.vef','.bam','.bmp','.itm','.ids')}
original=files['spwi902.spl'];callback=files['spwi902b.spl'];reports=[]
def patch_effect(b,number,offset,fmt,value):
 b=bytearray(b);eo=struct.unpack_from('<I',b,106)[0];struct.pack_into(fmt,b,eo+number*48+offset,value);return bytes(b)
def check(b,old=original):
 g,hs=parse(old);ng,nhs=parse(b);assert g==ng and len(hs)==len(nhs)
 assert old[:106]==b[:106] and old[110:114]==b[110:114]
 for (h,fx),(nh,nfx) in zip(hs,nhs):
  assert h[:30]==nh[:30] and h[34:]==nh[34:] and nfx[:-2]==fx
  assert [opcode(e) for e in nfx[-2:]]==[291,215]
  trap=next(e for e in fx if opcode(e)==259)
  for e in nfx[-2:]:
   assert e[2:4]==trap[2:4] and e[12:20]==trap[12:20] and e[36:]==trap[36:]
   assert struct.unpack_from('<I',e,8)[0]==1
  assert nfx[-1][20:28]==b'sratrap\0' and nfx[-2][20:28]==bytes(8)
def case(name,changes=None,profile='eet.flag',accept=True,order=(20,),collision=None,rejected=False):
 game=Path(tempfile.mkdtemp(prefix='av-trap-'))
 try:
  shutil.copytree(MOD,game/MOD.name);ov=game/'override';ov.mkdir()
  for n,b in files.items():(ov/n).write_bytes(b)
  for n,b in (changes or {}).items():
   if b is None:(ov/n).unlink(missing_ok=True)
   else:(ov/n).write_bytes(b)
  if collision:(ov/collision).write_bytes(b'collision sentinel')
  (ov/profile).write_bytes(b'fixture');(game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
  def snap():return {p.name.lower():p.read_bytes() for p in ov.iterdir() if p.name.lower()!='add_spell.ids'}
  def run(args,label,success=True):
   p=subprocess.run([str(WEIDU),str(MOD.name+'/setup-sr_original_spell_animations.tp2'),'--noautoupdate','--language','0','--no-exit-pause',*args],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   (OUT/(name+'-'+label+'.log')).write_text(p.stdout);assert (p.returncode==0)==success,p.stdout[-8000:]
  before=snap();run(['--force-install-list',*map(str,order)],'install',not collision)
  if collision or rejected:assert snap()==before
  elif accept:
   after=snap();check(after['spwi902.spl'],before['spwi902.spl']);assert after['spwi902b.spl']==before['spwi902b.spl']
   assert after['sratrap.bam']==(MOD/'assets/spelltrap/sratrap.bam').read_bytes()
   if order==(20,):
    assert set(after)-set(before)=={'sratrap.bam','sratrap.vvc'}
    assert {n for n in before if before[n]!=after[n]}=={'spwi902.spl'}
   run(['--force-install-list',*map(str,order)],'reinstall');assert snap()==after
   if len(order)>1:
    run(['--force-uninstall-list','20'],'partial-uninstall')
    partial=snap();assert partial['spwi902.spl']==before['spwi902.spl']
    assert 'sratrap.bam' not in partial and 'sratrap.vvc' not in partial
    assert all(v==partial[k] for k,v in after.items() if k not in ('spwi902.spl','sratrap.bam','sratrap.vvc'))
    run(['--force-install-list','20'],'restore-trap');assert snap()==after
   run(['--force-uninstall-list',*map(str,reversed(order))],'uninstall');assert snap()==before
  else:
   assert snap()==before
   run(['--force-uninstall-list','20'],'uninstall');assert snap()==before
  reports.append(dict(case=name,status='PASS',patched=accept and not collision and not rejected))
 finally:shutil.rmtree(game)
for p in ['eet.flag','oh6000.are','oh1000.are']:case(p,profile=p)
case('unsupported-IWDEE',profile='howparty.2da',accept=False,rejected=True)
case('truncated-cleanup',{'spwi902b.spl':b'SPL V1  '},accept=False)
case('combined',order=(0,10,20));case('reverse',order=(20,10,0))
case('missing-spell',{'spwi902.spl':None},accept=False)
case('missing-cleanup',{'spwi902b.spl':None},accept=False)
case('bad-cleanup',{'spwi902b.spl':patch_effect(callback,0,0,'<H',142)},accept=False)
case('conditional-cleanup',{'spwi902b.spl':patch_effect(callback,0,18,'<B',50)},accept=False)
case('truncated',{'spwi902.spl':b'SPL V1  '},accept=False)
case('wrong-level',{'spwi902.spl':original[:52]+struct.pack('<I',8)+original[56:]},accept=False)
case('bad-table',{'spwi902.spl':original[:106]+struct.pack('<I',0xffffffff)+original[110:]},accept=False)
# Effect table: global 0, root first trap 6. Last trap is 14.
case('missing-trap-level',{'spwi902.spl':patch_effect(original,14,8,'<I',2)},accept=False)
case('unknown-visual',{'spwi902.spl':patch_effect(original,3,0,'<H',215)},accept=False)
case('unequal-duration',{'spwi902.spl':patch_effect(original,14,14,'<I',600)},accept=False)
case('delayed-trap',{'spwi902.spl':patch_effect(original,6,12,'<B',3)},accept=False)
case('wrong-target',{'spwi902.spl':patch_effect(original,6,2,'<B',2)},accept=False)
b=bytearray(original)
for n in range(6,15):
 eo=struct.unpack_from('<I',b,106)[0];o=eo+n*48
 b[o+3]=8;b[o+13]=3;b[o+18:o+20]=bytes([85,5]);struct.pack_into('<Ii',b,o+36,1,-3);struct.pack_into('<I',b,o+14,240)
case('conditional-traps',{'spwi902.spl':bytes(b)},accept=False)
b=bytearray(original)
for n in range(6,15):
 eo=struct.unpack_from('<I',b,106)[0];o=eo+n*48;b[o+3]=8;b[o+13]=3;struct.pack_into('<I',b,o+14,240)
case('uniform-custom-duration',{'spwi902.spl':bytes(b)})
ao,n,eo,gi,gn=struct.unpack_from('<IHIHH',original,100);head=original[ao:ao+40];g=original[eo:eo+gn*48];fx=original[eo+gn*48:]
b=bytearray(original[:ao]+head*3+g+fx*3);struct.pack_into('<HI',b,104,3,ao+120)
for i in range(3):struct.pack_into('<H',b,ao+i*40+32,gn+i*14)
case('three-ability-headers',{'spwi902.spl':bytes(b)})
b=bytearray(b);struct.pack_into('<H',b,ao+40+32,gn)
case('shared-effect-block',{'spwi902.spl':bytes(b)},accept=False)
for n in ['sratrap.bam','SRATRAP.VVC']:case('collision-'+n,collision=n)
result=dict(status='PASS',cases=reports,source_spell_sha256=hashlib.sha256(original).hexdigest(),original_effects_byte_identical=True,only_SPWI902_patched_by_component20=True,native_resources_unchanged_by_component20=True,exhaustion_callback_unchanged=True,reinstall_stable=True,uninstall_exact=True,game_rendering_tested=False)
(OUT/'spelltrap_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',cases=len(reports)),indent=2))
