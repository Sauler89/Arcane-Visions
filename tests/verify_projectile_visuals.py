"""Test installed-data projectile cloning and shared lightning guards on EET exports.
Usage: python3 tests/verify_projectile_visuals.py EET_EXPORT WEIDU RESULT_DIR
"""
from pathlib import Path
import json,shutil,struct,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];SOURCE,WEIDU,OUT=[Path(x).resolve() for x in sys.argv[1:4]]
OUT.mkdir(parents=True,exist_ok=True);MOD='sr_original_spell_animations'
names=['SORB.ITM','SPPR614.SPL','PFIRE3.PRO','SPPR302.SPL','SKYBOLT.PRO','SKYBOLT.BAM','PROJECTL.IDS','MISSILE.IDS']
original={n:(SOURCE/n).read_bytes() for n in names};game=Path(tempfile.mkdtemp(prefix='av-projectiles-'));checks=[]
def rr(b,o):return b[o:o+8].split(b'\0')[0].decode().lower()
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir()
 (game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26));(ov/'eet.flag').write_bytes(b'fixture')
 def file(n):return next(p for p in ov.iterdir() if p.name.upper()==n.upper())
 def snap():return {p.name.upper():p.read_bytes() for p in ov.iterdir() if p.name.lower()!='add_spell.ids'}
 def run(install=True):
  r=subprocess.run([str(WEIDU),MOD+'/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','0','--no-exit-pause','--force-install-list' if install else '--force-uninstall-list','10'],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert r.returncode==0,r.stdout[-7000:]
  return r.stdout
 cases=['recognized','different-speed-and-sound','orb-detached','orb-unknown-projectile','orb-unknown-travel','orb-area-projectile','orb-pillar','orb-extra-source','orb-extra-trail','orb-wrong-orientation','orb-truncated','orb-unknown-hit','lightning-other-chain','lightning-truncated-root','lightning-truncated-pro','lightning-delayed-impact','lightning-area-pro','lightning-other-travel','lightning-missing-bam','lightning-missing-root']
 for label in cases:
  data={n:bytearray(b) for n,b in original.items()};orb_ok=not label.startswith('orb-');call_ok=not label.startswith('lightning-')
  if label=='different-speed-and-sound':struct.pack_into('<H',data['PFIRE3.PRO'],10,93);data['PFIRE3.PRO'][16:24]=b'CUSTOM\0\0'
  elif label=='orb-detached':
   b=data['SPPR614.SPL'];a,n,e=struct.unpack_from('<IHI',b,100);c,i=struct.unpack_from('<HH',b,a+30)
   for j in range(c):
    o=e+(i+j)*48
    if struct.unpack_from('<H',b,o)[0]==111:b[o+20:o+28]=b'OTHER\0\0\0'
  elif label=='orb-unknown-projectile':struct.pack_into('<H',data['SORB.ITM'],struct.unpack_from('<I',data['SORB.ITM'],100)[0]+42,1)
  elif label=='orb-unknown-travel':data['PFIRE3.PRO'][260:268]=b'CUSTOM\0\0'
  elif label=='orb-area-projectile':struct.pack_into('<H',data['PFIRE3.PRO'],8,3)
  elif label=='orb-pillar':struct.pack_into('<I',data['PFIRE3.PRO'],44,128)
  elif label=='orb-extra-source':data['PFIRE3.PRO'][32:40]=b'OTHER\0\0\0'
  elif label=='orb-extra-trail':data['PFIRE3.PRO'][310:318]=b'OTHER\0\0\0'
  elif label=='orb-wrong-orientation':data['PFIRE3.PRO'][307]=9
  elif label=='orb-truncated':data['PFIRE3.PRO']=data['PFIRE3.PRO'][:300]
  elif label=='orb-unknown-hit':
   b=data['SORB.ITM'];a,n,e=struct.unpack_from('<IHI',b,100);b[e+20:e+28]=b'UNKNOWN\0'
  elif label=='lightning-other-chain':struct.pack_into('<H',data['SPPR302.SPL'],struct.unpack_from('<I',data['SPPR302.SPL'],100)[0]+38,40)
  elif label=='lightning-truncated-root':data['SPPR302.SPL']=data['SPPR302.SPL'][:114]
  elif label=='lightning-truncated-pro':data['SKYBOLT.PRO']=data['SKYBOLT.PRO'][:300]
  elif label=='lightning-delayed-impact':struct.pack_into('<I',data['SKYBOLT.PRO'],44,128)
  elif label=='lightning-area-pro':struct.pack_into('<H',data['SKYBOLT.PRO'],8,3)
  elif label=='lightning-other-travel':data['SKYBOLT.PRO'][260:268]=b'OTHER\0\0\0'
  elif label=='lightning-missing-bam':del data['SKYBOLT.BAM']
  elif label=='lightning-missing-root':del data['SPPR302.SPL']
  for p in list(ov.iterdir()):
   if p.name.lower()!='eet.flag':p.unlink()
  for n,b in data.items():(ov/n.lower()).write_bytes(b)
  before=snap();run();after=snap()
  for n in ['SPPR614.SPL','SPPR302.SPL','PFIRE3.PRO','SKYBOLT.PRO']:
   if n in data:assert after[n]==data[n],(label,n,'source gameplay changed')
  assert ('SRIOSORB.PRO' in after)==orb_ok,(label,'clone')
  old=bytes(data['SORB.ITM']);a,n,e=struct.unpack_from('<IHI',old,100);new=after['SORB.ITM']
  allowed={e+j for j in range(20,28)}
  if orb_ok:
   expected=bytearray(data['PFIRE3.PRO']);struct.pack_into('<I',expected,256,0x280);expected[260:268]=b'srioorbt';expected[307]=9
   assert after['SRIOSORB.PRO']==expected,(label,'clone gameplay bytes')
   allowed.update((a+42,a+43));assert struct.unpack_from('<H',new,a+42)[0]!=struct.unpack_from('<H',old,a+42)[0]
  else:assert new[a+42:a+44]==old[a+42:a+44]
  assert len(old)==len(new) and all(x==y for i,(x,y) in enumerate(zip(old,new)) if i not in allowed),(label,'weapon mechanics')
  if call_ok:assert after['SKYBOLT.BAM']==(ROOT/MOD/'assets/iwd_native/skybolt.bam').read_bytes()
  elif 'SKYBOLT.BAM' in data:assert after['SKYBOLT.BAM']==data['SKYBOLT.BAM']
  else:assert 'SKYBOLT.BAM' not in after
  run();assert snap()==after;run(False);assert snap()==before
  checks.append(label)
 # A generated-PRO collision must abort before any writes.
 for p in list(ov.iterdir()):
  if p.name.lower()!='eet.flag':p.unlink()
 for n,b in original.items():(ov/n.lower()).write_bytes(b)
 (ov/'sriosorb.pro').write_bytes(b'foreign resource');before=snap()
 r=subprocess.run([str(WEIDU),MOD+'/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','0','--no-exit-pause','--force-install-list','10'],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 assert r.returncode!=0 and snap()==before,'private PRO collision changed resources';checks.append('private-PRO-collision')
 result=dict(status='PASS',cases=len(checks),checks=checks,installed_PRO_gameplay_and_audio_preserved=True,original_PROs_and_root_SPLs_byte_identical=True,only_SORB_projectile_reference_and_hit_art_changed=True,SKYBOLT_shared_BAM_only=True,reinstall_stable=True,uninstall_byte_exact=True,game_rendering_tested=False)
 (OUT/'projectile_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
