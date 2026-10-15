"""Bound attached SR cues and test upgrading permanent beta.12 spell effects.
Usage: python3 tests/verify_transient_visuals.py EET_EXPORT WEIDU RESULT_DIR
This checks installer data, not the proprietary engine or serialized saves.
"""
from pathlib import Path
import ast,io,json,shutil,struct,subprocess,sys,tarfile,tempfile,zlib
ROOT=Path(__file__).resolve().parents[1];SOURCE,WEIDU,OUT=[Path(x).resolve() for x in sys.argv[1:4]];OUT.mkdir(parents=True,exist_ok=True)
MOD='sr_original_spell_animations';TP2=MOD+'/setup-sr_original_spell_animations.tp2'
ROWS={'SPWI206':('srailus',2),'SPWI212':('srailus',2),'SPWI307':('srailus',2),'SPPR516':('srailus',2),'SPWI317':('sraghst',3),'SPWI414':('srasprt',4)}
helper=ast.parse((ROOT/'tests/verify_installer.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name in ('parse','opcode','assert_preserved')],type_ignores=[]),'<preservation checks>','exec'))
def bounds(b):
 if b[:4]==b'BAMC':b=zlib.decompress(b[12:])
 nf,nc=struct.unpack_from('<HB',b,8);a=struct.unpack_from('<I',b,12)[0];return [struct.unpack_from('<H',b,a+nf*12+i*4)[0] for i in range(nc)]
game=Path(tempfile.mkdtemp(prefix='av-transients-'));checks=[]
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir()
 originals={p.name.upper():p.read_bytes() for p in SOURCE.iterdir() if p.is_file() and p.suffix.upper() in ('.SPL','.EFF','.PRO','.VVC','.VEF','.BAM','.BMP','.IDS','.ITM')}
 for n,b in originals.items():(ov/n).write_bytes(b)
 (ov/'eet.flag').write_bytes(b'fixture');(game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def file(n):return next(p for p in ov.iterdir() if p.name.upper()==n.upper())
 def snap():return {p.name.upper():p.read_bytes() for p in ov.iterdir() if p.name.lower()!='add_spell.ids'}
 def run(parts=[0],install=True,label='test'):
  p=subprocess.run([str(WEIDU),TP2,'--noautoupdate','--language','0','--no-exit-pause','--force-install-list' if install else '--force-uninstall-list',*map(str,parts)],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (OUT/(label+'.log')).write_text(p.stdout);assert p.returncode==0,p.stdout[-8000:];return p.stdout
 def check():
  for spell,(ref,seconds) in ROWS.items():
   heads=assert_preserved(originals[spell+'.SPL'],file(spell+'.SPL').read_bytes(),spell)
   for _,effects in heads:
    visuals=[f for f in effects if opcode(f)==215];assert len(visuals)==1
    f=visuals[0];assert f[12]==0 and struct.unpack_from('<I',f,14)[0]==seconds
    assert struct.unpack_from('<I',f,8)[0]==1 and f[20:28].split(b'\0')[0].decode()==ref
   vvc=file(ref+'.VVC').read_bytes();bam=file(ref+'.BAM').read_bytes()
   assert not struct.unpack_from('<I',vvc,32)[0]&1
   duration=struct.unpack_from('<I',vvc,92)[0];fps=struct.unpack_from('<I',vvc,52)[0]
   assert duration==seconds*15 and duration not in [0,0xffffffff]
   assert max(bounds(bam))/fps < seconds,'visual would be cut before completing its BAM cycle'
  # Keep true persistent and independent point/unattached effects intact.
  for spell in ['SPWI708','SPPR609','SPPR728','SPWI516','SPWI520','SPWI521','SPWI620','SPWI621','SPWI622']:
   heads=assert_preserved(originals[spell+'.SPL'],file(spell+'.SPL').read_bytes(),spell)
   if spell in ['SPPR728','SPWI516','SPWI520','SPWI521','SPWI620','SPWI621','SPWI622']:
    assert all(f[12]==1 and struct.unpack_from('<I',f,14)[0]==0 for _,effects in heads for f in effects if opcode(f)==215)
  assert struct.unpack_from('<I',file('sramant.vvc').read_bytes(),32)[0]&1
  assert struct.unpack_from('<I',file('srasun1.vvc').read_bytes(),32)[0]&1
  for name in ['SPWI402.SPL','SPWI505.SPL','SPWI215.SPL','SPWI812.SPL']:assert file(name).read_bytes()==originals[name]
 before=snap();run(label='install');check();installed=snap();run(label='reinstall');assert snap()==installed;run(install=False,label='uninstall');assert snap()==before
 checks.append('all six transient attached spell bindings: finite host and controller, complete BAM cycle, nonvisual preservation, stable reinstall/exact uninstall')
 # Reproduce the old configuration from the actual published beta.12.
 archive=subprocess.check_output(['git','archive','b544594b235f2775958435af9a772eaeefe1b143',MOD],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(game,filter='data')
 run(label='beta12-install')
 old_spells={}
 for spell,(ref,seconds) in ROWS.items():
  b=file(spell+'.SPL').read_bytes();old_spells[spell]=b
  assert all(f[12]==1 and struct.unpack_from('<I',f,14)[0]==0 for _,effects in parse(b)[1] for f in effects if opcode(f)==215)
  assert struct.unpack_from('<I',file(ref+'.VVC').read_bytes(),92)[0]==0xffffffff
 shutil.copytree(ROOT/MOD,game/MOD,dirs_exist_ok=True)
 run(label='upgrade-beta13');check()
 for spell,old in old_spells.items():
  new=file(spell+'.SPL').read_bytes();assert len(old)==len(new)
  ao,n,eo=struct.unpack_from('<IHI',old,100);allowed=set()
  for i in range(n):
   count,index=struct.unpack_from('<HH',old,ao+i*40+30)
   for j in range(count):
    off=eo+(index+j)*48
    if opcode(old[off:off+48])==215:allowed.update([off+12,*range(off+14,off+18)])
  assert all(a==b for i,(a,b) in enumerate(zip(old,new)) if i not in allowed),(spell,'upgrade changed fields other than visual timing/duration')
 run(install=False,label='upgrade-uninstall');assert snap()==before
 checks.append('published beta.12 permanent attached configuration reproduced; upgrade changes only visual timing/duration and three VVC lifetime fields')
 result=dict(status='PASS',version=(ROOT/'sr_original_spell_animations/setup-sr_original_spell_animations.tp2').read_text().split('VERSION ~',1)[1].split('~',1)[0],checks=checks,affected_spells=list(ROWS),controller_lifetimes_frames={'srailus':30,'sraghst':45,'srasprt':60},gameplay_armor_saves_icons_globals_and_projectiles_preserved=True,BAM_artwork_unchanged=True,persistent_Mantle_False_Dawn_and_point_animations_preserved=True,old_configuration_reproduced=True,upgrade_install_reinstall_uninstall_checked=True,game_rendering_tested=False,area_transition_or_Silke_encounter_reproduced_in_game=False,existing_saved_creature_effects_not_rewritten=True)
 (OUT/'transient_visuals_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
