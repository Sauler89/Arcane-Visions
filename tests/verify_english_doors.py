"""Verify English-only packaging, native door preservation and beta.11 upgrade.
Usage: python3 tests/verify_english_doors.py EET_EXPORT WEIDU RESULT_DIR
The git checkout must contain the pinned beta.11 commit for the upgrade case.
"""
from pathlib import Path
import io,json,re,shutil,struct,subprocess,sys,tarfile,tempfile
ROOT=Path(__file__).resolve().parents[1];SOURCE,WEIDU,OUT=[Path(x).resolve() for x in sys.argv[1:4]];OUT.mkdir(parents=True,exist_ok=True)
MOD='sr_original_spell_animations';TP2=MOD+'/setup-sr_original_spell_animations.tp2'
tp=(ROOT/TP2).read_text();assert re.findall(r'^LANGUAGE ~([^~]+)~',tp,re.M)==['English']
assert not (ROOT/MOD/'languages/italian').exists()
assert not any(p.name=='README.it.md' for p in ROOT.rglob('*'))
assert not any(p.stem.lower()=='srasdor' for p in (ROOT/MOD/'assets').rglob('*'))
assert not any(word in (ROOT/MOD/'lib/animations.tpa').read_text().lower() for word in ['srasdor','spwi505','spwi402'])
original={p.name.upper():p.read_bytes() for p in SOURCE.iterdir() if p.is_file() and p.suffix.upper() in ('.SPL','.EFF','.PRO','.VVC','.VEF','.BAM','.BMP','.IDS','.ITM')}
preserved=[n for n in ['SPWI402.SPL','SPWI505.SPL','SPWI109.SPL','SPDIMNDR.BAM','DDOORH.BAM','DDOORH.VVC','SPWI215.SPL','SPWI812.SPL'] if n in original]
assert {'SPWI402.SPL','SPWI505.SPL','SPDIMNDR.BAM','DDOORH.BAM'}<=set(preserved)
game=Path(tempfile.mkdtemp(prefix='av-english-doors-'));checks=[]
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir()
 for n,b in original.items():(ov/n).write_bytes(b)
 (ov/'eet.flag').write_bytes(b'fixture');(game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def snap():return {p.name.upper():p.read_bytes() for p in ov.iterdir() if p.name.lower()!='add_spell.ids'}
 def file(n):return next(p for p in ov.iterdir() if p.name.upper()==n.upper())
 def run(parts,install=True,language=0,label='test'):
  p=subprocess.run([str(WEIDU),TP2,'--noautoupdate','--language',str(language),'--no-exit-pause','--force-install-list' if install else '--force-uninstall-list',*map(str,parts)],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (OUT/(label+'.log')).write_text(p.stdout);assert p.returncode==0,p.stdout[-8000:];return p.stdout
 before=snap()
 for parts in [[0],[10],[0,10]]:
  label='-'.join(map(str,parts));run(parts,label=label);after=snap()
  for n in preserved:assert after[n]==before[n],n+' changed'
  assert not {'SRASDOR.BAM','SRASDOR.VVC'}&after.keys()
  assert file('SPWI317.SPL').read_bytes()!=original['SPWI317.SPL'] if 0 in parts else True
  run(parts,label=label+'-reinstall');assert snap()==after
  run(parts[::-1],False,label=label+'-uninstall');assert snap()==before
  checks.append(label+': native door spells/art preserved; reinstall/exact uninstall')
 # Reinstalling the updated mod restores Shadow Door from WeiDU's old backup.
 archive=subprocess.check_output(['git','archive','dd1afb19158f0b9dd288f9ee1b0ed6aae1ab588c',MOD],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(game,filter='data')
 old_tp=(game/TP2).read_text();assert 'LANGUAGE ~Italiano~' in old_tp and 'beta.11' in old_tp
 run([0,10],language=1,label='old-beta11-Italian-install')
 assert file('SPWI505.SPL').read_bytes()!=original['SPWI505.SPL']
 assert file('srasdor.bam').exists()
 # Replace the distribution without deleting WeiDU's backup directory.
 old_italian=game/MOD/'languages/italian';shutil.rmtree(old_italian)
 for name in ['srasdor.bam','srasdor.vvc']:(game/MOD/'assets/custom'/name).unlink()
 shutil.copytree(ROOT/MOD,game/MOD,dirs_exist_ok=True)
 run([0,10],language=0,label='upgrade-to-current-English')
 after=snap()
 for n in preserved:assert after[n]==before[n],n+' not restored after upgrade'
 assert not {'SRASDOR.BAM','SRASDOR.VVC'}&after.keys()
 assert all(re.search(r'\s#0\s+#'+str(c)+r'\s', (game/'WeiDU.log').read_text()) for c in [0,10])
 run([0,10],label='upgrade-reinstall');assert snap()==after
 run([10,0],False,label='upgrade-uninstall');assert snap()==before
 checks.append('beta.11 Italian -> current English: Shadow Door restored, obsolete assets removed, stable reinstall/exact uninstall')
 result=dict(status='PASS',version=(ROOT/'sr_original_spell_animations/setup-sr_original_spell_animations.tp2').read_text().split('VERSION ~',1)[1].split('~',1)[0],installer_languages=['English'],checks=checks,preserved_resources=preserved,source='owner-supplied EET exports with synthetic KEY/TLK',old_Italian_install_upgrade_tested=True,obsolete_door_assets_removed=True,no_global_native_door_replacement=True,game_rendering_tested=False)
 (OUT/'english_doors_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:shutil.rmtree(game)
