"""Audit regressions: IWD format guards, visual conditions and private-name collisions.
Usage: python3 tests/verify_regressions.py /path/to/weidu
"""
from pathlib import Path
import ast,json,shutil,struct,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];WEIDU=Path(sys.argv[1]).resolve()
helper=ast.parse((ROOT/'tests/verify_installer.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name in ('effect','spl','parse','opcode')],type_ignores=[]),'<fixture helpers>','exec'))
def base():
 b=bytearray(spl());ao,n,eo=struct.unpack_from('<IHI',b,100)
 for i in range(n):
  cnt,idx=struct.unpack_from('<HH',b,ao+i*40+30)
  for j in range(cnt):
   o=eo+(idx+j)*48;op=struct.unpack_from('<H',b,o)[0]
   if op==215:
    b[o+20:o+28]=b'SPRMCURS';struct.pack_into('<I',b,o+14,3)
   elif op==141:struct.pack_into('<H',b,o,142)
 return bytes(b)
def mutate(b,off,fmt,value):
 x=bytearray(b);struct.pack_into(fmt,x,off,value);return bytes(x)
game=Path(tempfile.mkdtemp(prefix='arcane-visions-regressions-'));results=[]
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir();(ov/'eet.flag').write_bytes(b'fixture')
 (game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def snap():
  files=[p for p in ov.iterdir() if p.name.lower()!='add_spell.ids'];result={p.name.lower():p.read_bytes() for p in files};assert len(result)==len(files),'case-colliding paths';return result
 def path(n):return next(p for p in ov.iterdir() if p.name.lower()==n)
 def run(component,install=True,success=True):
  p=subprocess.run([str(WEIDU),'sr_original_spell_animations/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','1','--no-exit-pause','--force-install-list' if install else '--force-uninstall-list',str(component)],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert (p.returncode==0)==success,p.stdout[-8000:];return p.stdout
 b=base();ao,n,eo=struct.unpack_from('<IHI',b,100)
 bad=[('truncated',b'SPL V1  '),('signature',b'BAD V1  '+b[8:]),('ability-offset',mutate(b,100,'<I',0xfffffff0)),('ability-count',mutate(b,104,'<H',65535)),('effect-before-abilities',mutate(b,106,'<I',100)),('effect-offset',mutate(b,106,'<I',0xfffffff0)),('global-index',mutate(b,110,'<H',65535)),('global-count',mutate(b,112,'<H',65535)),('ability-effect-count',mutate(b,ao+30,'<H',65535)),('ability-effect-index',mutate(b,ao+32,'<H',65535)),('global-overlap',mutate(b,ao+32,'<H',0)),('shared-ability-block',mutate(b,ao+40+32,'<H',2)),('no-abilities',mutate(b,104,'<H',0))]
 p=ov/'sppr308.spl'
 for label,data in bad:
  p.write_bytes(data);before=snap();out=run(10);assert path('sppr308.spl').read_bytes()==data,label;run(10,False);assert snap()==before;results.append(label)
 # An unused global index is legal when the global count is zero.
 empty=mutate(mutate(b,110,'<H',65535),112,'<H',0);p.write_bytes(empty);before=snap();run(10);assert path('sppr308.spl').read_bytes()!=empty;run(10,False);assert snap()==before;results.append('unused-global-index')
 # Conditional application remains byte-exact outside the visual reference/timing.
 conditional=bytearray(b)
 for i in range(n):
  cnt,idx=struct.unpack_from('<HH',b,ao+i*40+30)
  for j in range(cnt):
   o=eo+(idx+j)*48
   if opcode(b[o:o+48])==215:
    conditional[o+3]=9;conditional[o+13]=3;conditional[o+18:o+20]=bytes([68,30]);struct.pack_into('<Ii',conditional,o+36,12,-5)
 p=path('sppr308.spl');p.write_bytes(conditional);before=snap();run(10);new=path('sppr308.spl').read_bytes();assert new!=conditional
 for (_,fx),(_,fy) in zip(parse(conditional)[1],parse(new)[1]):
  for a,c in zip(fx,fy):
   if a!=c:assert a[2:12]==c[2:12] and a[13]==c[13] and a[18:20]==c[18:20] and a[28:48]==c[28:48], [(i,x,y) for i,(x,y) in enumerate(zip(a,c)) if x!=y]
 run(10,False);assert snap()==before;results.append('conditional-visual-preserved')
 # These unexpected configurations must not receive a replacement animation.
 for label,field,fmt,value in [('wrong-target',2,'B',1),('delayed-visual',12,'B',4),('persistent-unknown-visual',14,'I',600)]:
  v=bytearray(b)
  for i in range(n):
   cnt,idx=struct.unpack_from('<HH',b,ao+i*40+30)
   for j in range(cnt):
    o=eo+(idx+j)*48
    if opcode(b[o:o+48])==215:struct.pack_into('<'+fmt,v,o+field,value)
  p.write_bytes(v);before=snap();run(10);assert path('sppr308.spl').read_bytes()==v;run(10,False);assert snap()==before;results.append(label)
 # State-bearing overlays are also visuals; never layer over an unknown one.
 for overlay in range(153,159):
  v=bytearray(b)
  for i in range(n):
   cnt,idx=struct.unpack_from('<HH',b,ao+i*40+30)
   o=next(eo+(idx+j)*48 for j in range(cnt) if opcode(b[eo+(idx+j)*48:eo+(idx+j+1)*48])==142)
   struct.pack_into('<H',v,o,overlay)
  p=path('sppr308.spl');p.write_bytes(v);before=snap();run(10);assert path('sppr308.spl').read_bytes()==v;run(10,False);assert snap()==before;results.append('additional-overlay-'+str(overlay))
 # Collisions must fail before native resources or spells are modified.
 for comp,name in [(0,'sraghst.bam'),(10,'sriopara.vvc')]:
  (ov/name).write_bytes(b'another mod owns this name');(ov/'spmagglo.bam').write_bytes(b'native sentinel');before=snap();out=run(comp,success=False);assert 'private resource' in out;assert snap()==before;path(name).unlink();results.append('collision-component-'+str(comp))
 # Both components reject unsupported games before any resource write.
 path('eet.flag').unlink()
 for comp in (0,10):
  before=snap();out=run(comp);assert 'SKIPPING:' in out;assert snap()==before;results.append('unsupported-game-component-'+str(comp))
 print(json.dumps(dict(status='PASS',cases=len(results),checks=results,game_rendering_tested=False),indent=2))
finally:shutil.rmtree(game)
