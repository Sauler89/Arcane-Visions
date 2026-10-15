"""Reproduce the old BGEE gate and verify both components in isolated fixtures.
Usage: python3 tests/verify_bgee.py WEIDU RESULT_DIR
Synthetic SPL/resources and KEY/TLK; no full BGEE installation or game renderer.
"""
from pathlib import Path
import ast,json,shutil,struct,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];WEIDU=Path(sys.argv[1]).resolve();OUT=Path(sys.argv[2]).resolve();OUT.mkdir(parents=True,exist_ok=True)
MOD='sr_original_spell_animations';TP2=MOD+'/setup-sr_original_spell_animations.tp2'
helper=ast.parse((ROOT/'tests/verify_installer.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name in ('effect','spl','parse','opcode','assert_preserved')],type_ignores=[]),'<fixture helpers>','exec'))
game=Path(tempfile.mkdtemp(prefix='av-bgee-'));checks=[]
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir()
 (game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 patched=(game/TP2).read_text();old=patched.replace('GAME_IS ~bgee bg2ee eet~','GAME_IS ~eet bg2ee~')
 assert old!=patched
 def file(n):return next(p for p in ov.iterdir() if p.name.lower()==n.lower())
 def snap():return {p.name.lower():p.read_bytes() for p in ov.iterdir() if p.name.lower()!='add_spell.ids'}
 def seed(profile):
  for p in list(ov.iterdir()):p.unlink()
  markers={'BGEE':['oh1000.are'],'BGEE+SoD':['oh1000.are'],'BG2EE':['oh6000.are'],'EET':['eet.flag'],'IWDEE':['ar2116.are','ar9109.are','howparty.2da'],'PSTEE':['ar0104a.are','pstchar.2da'],'classic-BG1':['ar0125.are'],'classic-BG2':['ar0083.are','ar6111.are']}
  for n in markers[profile]:(ov/n).write_bytes(b'fixture')
  if profile=='BGEE+SoD':(ov/'campaign.2da').write_text('2DA V1.0\n0\n NAME\n1 SOD\n')
  for name in ['spentaai.bam','spentaci.bam','spchrorb.bam','spmagglo.bam']:(ov/name).write_bytes(b'original native art')
  for name in ['SPWI206','SPWI212','SPWI307','SPWI317','SPWI414']:(ov/(name.lower()+'.spl')).write_bytes(spl())
  # A priest cue recognized by the existing IWD patcher.
  b=bytearray(spl());a,n,e=struct.unpack_from('<IHI',b,100)
  for i in range(n):
   cnt,idx=struct.unpack_from('<HH',b,a+i*40+30)
   for j in range(cnt):
    off=e+(idx+j)*48;op=struct.unpack_from('<H',b,off)[0]
    if op==141:struct.pack_into('<H',b,off,142)
    elif op==215:b[off+20:off+28]=b'SPRMCURS';struct.pack_into('<I',b,off+14,3)
  (ov/'sppr308.spl').write_bytes(b)
  # Sanctuary state and protections must survive redirecting its graphic.
  x=bytearray(b)
  for i in range(n):
   cnt,idx=struct.unpack_from('<HH',x,a+i*40+30)
   for j in range(cnt):
    off=e+(idx+j)*48
    if struct.unpack_from('<H',x,off)[0]==215:
     struct.pack_into('<H',x,off,153);x[off+2]=1;struct.pack_into('<I',x,off+8,0);struct.pack_into('<I',x,off+14,60);x[off+20:off+28]=bytes(8)
  (ov/'sppr109.spl').write_bytes(x)
  (ov/'spwi215.spl').write_bytes(spl());(ov/'spwi812.spl').write_bytes(spl())
  (ov/'origeff.eff').write_bytes(b'nonvisual effect sentinel');(ov/'unchanged.itm').write_bytes(b'item icon sentinel')
 def run(parts,language=0,install=True,label='test'):
  p=subprocess.run([str(WEIDU),TP2,'--noautoupdate','--language',str(language),'--no-exit-pause','--force-install-list' if install else '--force-uninstall-list',*map(str,parts)],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (OUT/(label+'.log')).write_text(p.stdout);assert p.returncode==0,p.stdout[-8000:];return p.stdout
 def verify(before,components):
  after=snap();assert {n for n in after if n.endswith('.spl')}=={n for n in before if n.endswith('.spl')},'missing spells were created'
  changed={n for n in before if before[n]!=after[n]}
  sr={'spwi206.spl':'srailus','spwi212.spl':'srailus','spwi307.spl':'srailus','spwi317.spl':'sraghst','spwi414.spl':'srasprt'}
  iwd={'sppr308.spl':'sriopara','sppr109.spl':'sriosanc'}
  expected=set()
  if 0 in components:expected.update(sr);expected.update(['spentaai.bam','spentaci.bam','spchrorb.bam','spmagglo.bam'])
  if 10 in components:expected.update(iwd)
  assert changed==expected,(components,changed,expected)
  if 0 in components:
   for name,ref in sr.items():
    heads=assert_preserved(before[name],after[name],name)
    assert all(any(opcode(f)==215 and f[20:28].split(b'\0')[0].decode()==ref for f in effects) for _,effects in heads)
  if 10 in components:
   for name,ref in iwd.items():
    b=before[name];c=after[name];a,n,e=struct.unpack_from('<IHI',b,100);allowed=set();hits=0
    for i in range(n):
     cnt,idx=struct.unpack_from('<HH',b,a+i*40+30)
     for j in range(cnt):
      off=e+(idx+j)*48
      if b[off:off+48]==c[off:off+48]:continue
      assert opcode(b[off:off+48])==opcode(c[off:off+48])==(153 if name=='sppr109.spl' else 215)
      assert c[off+20:off+28].split(b'\0')[0].decode()==ref
      allowed.update(off+k for k in range(20,28));hits+=1
      if name=='sppr109.spl':allowed.update(range(off+8,off+12));assert struct.unpack_from('<I',c,off+8)[0]==1
      else:allowed.update([off+12,*range(off+14,off+18)]);assert c[off+12]==1 and struct.unpack_from('<I',c,off+14)[0]==0
    assert hits==n and len(b)==len(c) and all(x==y for k,(x,y) in enumerate(zip(b,c)) if k not in allowed)
  assert not {'sriosorb.pro','skybolt.bam'}&after.keys(),'missing BG2-only routes should be skipped'
  assert (game/'dialog.tlk').read_bytes()==tlk
  return after
 tlk=(game/'dialog.tlk').read_bytes()
 for profile in ['BGEE','BGEE+SoD']:
  seed(profile);before=snap();(game/TP2).write_text(old)
  for comp in [0,10]:
   output=run([comp],label=profile+'-old-'+str(comp));assert 'SKIPPING:' in output and snap()==before
   checks.append(profile+': reproduced old component '+str(comp)+' rejection')
  (game/TP2).write_text(patched)
 for profile in ['BGEE','BGEE+SoD','BG2EE','EET']:
  for language in [0]:
   for parts in [[0],[10],[0,10]]:
    seed(profile);before=snap();label=profile+'-'+str(language)+'-'+'-'.join(map(str,parts))
    output=run(parts,language,label=label);assert 'SUCCESSFULLY INSTALLED' in output and 'SKIPPING:' not in output
    installed=verify(before,parts);run(parts,language,label=label+'-reinstall');assert snap()==installed
    run(parts[::-1],language,False,label+'-uninstall');assert snap()==before
    checks.append(label+': install/reinstall/exact uninstall, mechanics and missing-resource skips')
  seed(profile);before=snap();run([0]);sr_only=verify(before,[0]);run([10]);both=verify(before,[0,10]);run([10],install=False);assert snap()==sr_only;run([0],install=False);assert snap()==before
  run([10]);iwd_only=verify(before,[10]);run([0]);assert verify(before,[0,10])==both;run([0],install=False);assert snap()==iwd_only;run([10],install=False);assert snap()==before
  checks.append(profile+': both component orders and both partial uninstalls')
 for profile in ['IWDEE','PSTEE','classic-BG1','classic-BG2']:
  seed(profile);before=snap()
  for comp in [0,10]:
   output=run([comp],label=profile+'-rejected-'+str(comp));assert 'SKIPPING:' in output and snap()==before
   checks.append(profile+': unsupported component '+str(comp)+' skipped before writes')
 result=dict(status='PASS',version=(ROOT/'sr_original_spell_animations/setup-sr_original_spell_animations.tp2').read_text().split('VERSION ~',1)[1].split('~',1)[0],cases=len(checks),checks=checks,baseline='synthetic SPL/native resources and minimal KEY/TLK; WeiDU game markers, not actual BGEE exports',profiles=['BGEE','BGEE+SoD','BG2EE','EET'],components=[0,10],languages=['English'],old_BGEE_gate_reproduced=True,missing_spells_not_created=True,missing_projectile_and_weapon_routes_skipped=True,mechanics_icons_globals_and_unrelated_files_preserved=True,reinstall_stable=True,component_order_independent=True,partial_uninstall_preserves_retained_component=True,uninstall_byte_exact=True,game_rendering_tested=False,actual_BGEE_installation_tested=False)
 (OUT/'BGEE_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
