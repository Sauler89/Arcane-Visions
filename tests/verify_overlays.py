"""Persistent-overlay regressions using real owner-supplied EET spell exports.
Usage: python3 tests/verify_overlays.py EET_EXPORT_DIR /path/to/weidu [RESULT_DIR]
No complete game is installed or launched.
"""
from pathlib import Path
import ast,json,shutil,struct,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];SOURCE=Path(sys.argv[1]).resolve();WEIDU=Path(sys.argv[2]).resolve()
OUT=Path(sys.argv[3]).resolve() if len(sys.argv)>3 else Path(tempfile.mkdtemp(prefix='av-overlay-results-'));OUT.mkdir(parents=True,exist_ok=True)
ROWS=json.loads((ROOT/'sr_original_spell_animations/docs/iwd_overlay_mapping.json').read_text())
helper=ast.parse((ROOT/'tests/verify_installer.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name in ('parse','opcode')],type_ignores=[]),'<SPL parser>','exec'))
game=Path(tempfile.mkdtemp(prefix='av-overlays-'));checks=[]
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir()
 (ov/'eet.flag').write_bytes(b'fixture');(game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def resource(name):return next(p for p in ov.iterdir() if p.name.lower()==name.lower())
 def snap():
  files=[p for p in ov.iterdir() if p.name.lower()!='add_spell.ids'];data={p.name.lower():p.read_bytes() for p in files};assert len(data)==len(files);return data
 def run(install=True,success=True):
  p=subprocess.run([str(WEIDU),'sr_original_spell_animations/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','1','--no-exit-pause','--force-install-list' if install else '--force-uninstall-list','10'],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert (p.returncode==0)==success,p.stdout[-8000:];return p.stdout
 def offsets(b,op):
  ao,n,eo=struct.unpack_from('<IHI',b,100);result=[]
  for i in range(n):
   cnt,idx=struct.unpack_from('<HH',b,ao+i*40+30)
   result.extend(eo+(idx+j)*48 for j in range(cnt) if struct.unpack_from('<H',b,eo+(idx+j)*48)[0]==op)
  return result
 def case(row,label,data,changes):
  p=ov/(row['spell'].lower()+'.spl');p.write_bytes(data);before=snap();log=run();new=resource(p.name).read_bytes()
  if changes:
   assert new!=data,label;assert len(new)==len(data)
   allowed={o+k for o in offsets(data,row['opcode']) for k in list(range(8,12))+list(range(20,28))}
   assert all(a==b for i,(a,b) in enumerate(zip(data,new)) if i not in allowed),label+' changed state, duration, conditions, headers or mechanics'
   oldfx,newfx=parse(data)[1],parse(new)[1]
   for (_,a),(_,b) in zip(oldfx,newfx):
    assert len(a)==len(b)
    for e,f in zip(a,b):
     if e!=f:assert opcode(e)==opcode(f) and e[12:20]==f[12:20] and e[28:]==f[28:]
  else:assert new==data and 'skipped' in log,label
  installed=snap();run();assert snap()==installed,label+' unstable reinstall';run(False);assert snap()==before,label+' uninstall'
  resource(p.name).unlink();checks.append(row['spell']+': '+label)
 for r in ROWS:
  b=(SOURCE/(r['spell']+'.SPL')).read_bytes();os=offsets(b,r['opcode']);assert os
  conditional=bytearray(b)
  for o in os:
   conditional[o+3]=7;conditional[o+13]=3;conditional[o+18:o+20]=bytes([73,22]);struct.pack_into('<Ii',conditional,o+36,12,-6);struct.pack_into('<I',conditional,o+14,137)
  case(r,'conditional state/duration retained',bytes(conditional),True)
  for ref in dict.fromkeys([r['default_resource'],r['iwd_reference']]):
   x=bytearray(b)
   for o in os:struct.pack_into('<I',x,o+8,1);x[o+20:o+28]=ref.encode().ljust(8,b'\0')
   case(r,'recognized custom '+ref,bytes(x),True)
  for label,field,fmt,value in [('wrong target',2,'B',2 if r['target']==1 else 1),('delayed overlay',12,'B',4),('zero duration',14,'I',0),('unsupported mode',8,'I',3)]:
   x=bytearray(b)
   for o in os:struct.pack_into('<'+fmt,x,o+field,value)
   case(r,label,bytes(x),False)
  x=bytearray(b)
  for o in os:struct.pack_into('<I',x,o+8,1);x[o+20:o+28]=b'UNKNOWN\0'
  case(r,'unknown custom resource',bytes(x),False)
  # A second active visual is not erased or covered by a new overlay.
  x=bytearray(b);ao,n,eo=struct.unpack_from('<IHI',x,100)
  for i in range(n):
   cnt,idx=struct.unpack_from('<HH',x,ao+i*40+30);o=next(eo+(idx+j)*48 for j in range(cnt) if struct.unpack_from('<H',x,eo+(idx+j)*48)[0]!=r['opcode'])
   struct.pack_into('<H',x,o,215);x[o+20:o+28]=b'UNKNOWN\0'
  case(r,'additional unknown visual',bytes(x),False)
  # The new names participate in the pre-copy collision guard.
  name=r['private']+'.vvc';(ov/name).write_bytes(b'other mod');before=snap();log=run(success=False);assert 'private resource' in log and snap()==before;resource(name).unlink();checks.append(r['spell']+': private-name collision')
 # Major globe can already use IWDEE's opcode 215; keep that opcode/state behavior.
 r=next(r for r in ROWS if r['spell']=='SPWI602');b=bytearray((SOURCE/'SPWI602.SPL').read_bytes())
 for o in offsets(b,155):struct.pack_into('<H',b,o,215);struct.pack_into('<I',b,o+8,1);b[o+20:o+28]=b'#GLOBINV'
 alt=dict(r,opcode=215);case(alt,'major globe opcode 215 retained',bytes(b),True)
 # Exercise malformed layouts against the new patcher, not just the old cue patcher.
 r=ROWS[0];b=(SOURCE/(r['spell']+'.SPL')).read_bytes();ao,n,eo=struct.unpack_from('<IHI',b,100)
 for label,off,fmt,value in [('ability outside file',100,'I',0xfffffff0),('effects overlap abilities',106,'I',100),('global outside file',112,'H',65535),('ability effects outside file',ao+30,'H',65535)]:
  x=bytearray(b);struct.pack_into('<'+fmt,x,off,value);case(r,label,bytes(x),False)
 result=dict(status='PASS',cases=len(checks),checks=checks,game_rendering_tested=False)
 (OUT/'overlay_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
