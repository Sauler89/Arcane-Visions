"""Check runtime root/child guards and exact visual edits on actual EET exports.
Usage: python3 tests/verify_child_visuals.py EET_EXPORT WEIDU [RESULT_DIR]
"""
from pathlib import Path
import json,shutil,struct,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];SOURCE=Path(sys.argv[1]).resolve();WEIDU=Path(sys.argv[2]).resolve()
OUT=Path(sys.argv[3]).resolve() if len(sys.argv)>3 else Path(tempfile.mkdtemp(prefix='av-child-results-'));OUT.mkdir(parents=True,exist_ok=True)
PARENTS=json.loads((ROOT/'sr_original_spell_animations/docs/iwd_child_mapping.json').read_text())
source={p.name.upper():p for p in SOURCE.iterdir() if p.is_file()};game=Path(tempfile.mkdtemp(prefix='av-children-'));checks=[]
def offsets(b):
 a,n,e=struct.unpack_from('<IHI',b,100)
 for i in range(n):
  count,idx=struct.unpack_from('<HH',b,a+i*40+30)
  for j in range(count):yield e+(idx+j)*48
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir();(ov/'eet.flag').write_bytes(b'fixture')
 (game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def resource(n):return next(p for p in ov.iterdir() if p.name.upper()==n.upper())
 def snap():
  fs=[p for p in ov.iterdir() if p.name.lower()!='add_spell.ids'];d={p.name.lower():p.read_bytes() for p in fs};assert len(d)==len(fs);return d
 def run(install=True):
  p=subprocess.run([str(WEIDU),'sr_original_spell_animations/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','0','--no-exit-pause','--force-install-list' if install else '--force-uninstall-list','10'],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert p.returncode==0,p.stdout[-6000:];return p.stdout
 for child,parent in PARENTS.items():
  rb=source[parent+'.SPL'].read_bytes();cb=source[child+'.SPL'].read_bytes()
  detached=bytearray(rb)
  for o in offsets(detached):
   if detached[o+20:o+28].split(b'\0')[0].decode().upper()==child:detached[o+20:o+28]=b'OTHER\0\0\0'
  immune=bytearray(rb)
  for o in offsets(immune):
   if immune[o+20:o+28].split(b'\0')[0].decode().upper()==child:struct.pack_into('<H',immune,o,206)
  extra=bytearray(cb)
  nonvisual=next(o for o in offsets(extra) if struct.unpack_from('<H',extra,o)[0] not in (141,215,153,154,155,156,157,158))
  struct.pack_into('<H',extra,nonvisual,215);extra[nonvisual+20:nonvisual+28]=b'UNKNOWN\0'
  for label,root_data,child_data,changed in [('recognized chain',rb,cb,True),('root absent',None,cb,False),('root detached',bytes(detached),cb,False),('same-name immunity is not a cast',bytes(immune),cb,False),('truncated root',rb[:114],cb,False),('additional child visual',rb,bytes(extra),False)]:
   for p in list(ov.iterdir()):
    if p.suffix.lower()=='.spl':p.unlink()
   if root_data is not None:(ov/(parent+'.spl')).write_bytes(root_data)
   (ov/(child+'.spl')).write_bytes(child_data);before=snap();log=run();after=snap();new=resource(child+'.spl').read_bytes()
   assert (new!=child_data)==changed,(child,label)
   if root_data is not None:assert resource(parent+'.spl').read_bytes()==root_data,'root was written'
   if changed:
    assert len(new)==len(child_data)
    allowed={o+k for o in offsets(child_data) if struct.unpack_from('<H',child_data,o)[0]==215 for k in list(range(20,28))+([12]+list(range(14,18)) if child=='SPPR712A' else [])}
    assert all(a==b for i,(a,b) in enumerate(zip(child_data,new)) if i not in allowed),'mechanics changed'
   else:assert 'skipped' in log
   run();assert snap()==after;run(False);assert snap()==before
   checks.append(child+': '+label)
 result=dict(status='PASS',cases=len(checks),checks=checks,root_bytes_preserved=True,child_mechanics_conditions_and_timing_preserved=True,reinstall_stable=True,uninstall_byte_exact=True,game_rendering_tested=False)
 (OUT/'child_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
