"""Exercise temporary-weapon hit edits and safe skips using real EET exports.
Usage: python3 tests/verify_item_visuals.py EET_EXPORT WEIDU RESULT_DIR
"""
from pathlib import Path
import json, shutil, struct, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE,WEIDU,OUT=[Path(x).resolve() for x in sys.argv[1:4]]
OUT.mkdir(parents=True,exist_ok=True)
MOD='sr_original_spell_animations'
rows=json.loads((ROOT/MOD/'docs/iwd_item_mapping.json').read_text())
files={p.name.upper():p for p in SOURCE.iterdir() if p.is_file()}
game=Path(tempfile.mkdtemp(prefix='av-item-'))
checks=[]
def offsets(b,stride):
 a,n,e=struct.unpack_from('<IHI',b,100)
 for i in range(n):
  count,idx=struct.unpack_from('<HH',b,a+i*stride+30)
  for j in range(count):yield e+(idx+j)*48
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True)
 ov=game/'override';ov.mkdir();(ov/'eet.flag').write_bytes(b'fixture')
 (game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24))
 (game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def snap():return {p.name.lower():p.read_bytes() for p in ov.iterdir() if p.name.lower()!='add_spell.ids'}
 def run(install=True):
  p=subprocess.run([str(WEIDU),MOD+'/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','0','--no-exit-pause','--force-install-list' if install else '--force-uninstall-list','10'],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert p.returncode==0,p.stdout[-6000:]
 for root,item,art,code,old,p2 in rows:
  rb=files[root+'.SPL'].read_bytes();ib=files[item+'.ITM'].read_bytes()
  for label in ['recognized','conditions','detached','root-absent','false-link','root-wrong-target','root-wrong-mode','root-delayed','root-truncated','unknown','extra-visual','wrong-target','delayed','item-truncated','wrong-signature']:
   for p in list(ov.iterdir()):
    if p.suffix.lower() in ('.itm','.spl'):p.unlink()
   r=bytearray(rb);b=bytearray(ib)
   link=next(o for o in offsets(r,40) if struct.unpack_from('<H',r,o)[0]==111)
   cue=next(o for o in offsets(b,56) if struct.unpack_from('<H',b,o)[0] in (141,215))
   if label=='detached':r[link+20:link+28]=b'OTHER\0\0\0'
   elif label=='false-link':struct.pack_into('<H',r,link,206)
   elif label=='root-wrong-target':r[link+2]=2
   elif label=='root-wrong-mode':struct.pack_into('<I',r,link+8,1)
   elif label=='root-delayed':r[link+12]=4
   elif label=='root-truncated':r=r[:114]
   elif label=='unknown':struct.pack_into('<H',b,cue,215);b[cue+20:cue+28]=b'UNKNOWN\0'
   elif label=='extra-visual':
    off=next(o for o in offsets(b,56) if o!=cue);struct.pack_into('<H',b,off,215);b[off+20:off+28]=b'UNKNOWN\0'
   elif label=='wrong-target':b[cue+2]=1
   elif label=='delayed':b[cue+12]=4
   elif label=='item-truncated':b=b[:114]
   elif label=='wrong-signature':b[:8]=b'SPL V1  '
   elif label=='conditions':
    b[cue+18:cue+20]=bytes([83,17]);struct.pack_into('<Ii',b,cue+36,2,-4)
   if label!='root-absent':(ov/(root+'.spl')).write_bytes(r)
   p=ov/(item+'.itm');p.write_bytes(b);before=snap();run();after=snap();new=p.read_bytes()
   changed=label in ('recognized','conditions');assert (new!=b)==changed,(item,label)
   if label!='root-absent':assert (ov/(root+'.spl')).read_bytes()==r
   if changed:
    allowed={cue+k for k in range(20,28)}
    if old==141:allowed.update(cue+k for k in (0,1,8,9,10,11))
    assert len(new)==len(b) and all(x==y for i,(x,y) in enumerate(zip(b,new)) if i not in allowed)
    assert new[cue+20:cue+28]==('srio'+code).encode().ljust(8,b'\0')
   run();assert snap()==after;run(False);assert snap()==before
   checks.append(item+': '+label)
 result=dict(status='PASS',cases=len(checks),checks=checks,root_bytes_preserved=True,item_headers_icons_projectiles_mechanics_and_conditions_preserved=True,reinstall_stable=True,uninstall_byte_exact=True,game_rendering_tested=False)
 (OUT/'item_validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
