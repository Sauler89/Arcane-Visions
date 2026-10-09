"""Verify real WeiDU install/reinstall/uninstall on owner-supplied EET exports.
Usage: python3 tests/verify_iwd_on_export.py EET_EXPORT_DIR WEIDU [RESULT_DIR]
No installed game is changed or launched.
"""
from pathlib import Path
import ast,hashlib,json,shutil,struct,subprocess,sys,tempfile,zlib
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'sr_original_spell_animations'
SOURCE=Path(sys.argv[1]).resolve();WEIDU=Path(sys.argv[2]).resolve()
OUT=Path(sys.argv[3]).resolve() if len(sys.argv)>3 else Path(tempfile.mkdtemp(prefix='sra-iwd-results-'));OUT.mkdir(parents=True,exist_ok=True)
ROWS=json.loads((MOD/'docs/iwd_spell_mapping.json').read_text());CORE=json.loads((MOD/'docs/test_config.json').read_text())
OVERLAYS=json.loads((MOD/'docs/iwd_overlay_mapping.json').read_text())
OVERLAY_BY={r['spell']:r for r in OVERLAYS}
helper=ast.parse((ROOT/'tests/verify_installer.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name in ('parse','opcode','assert_preserved')],type_ignores=[]),'<checks>','exec'))
asset_helper=ast.parse((ROOT/'tests/verify_assets.py').read_text())
exec(compile(ast.Module(body=[n for n in asset_helper.body if isinstance(n,ast.FunctionDef) and n.name=='bam'],type_ignores=[]),'<BAM checks>','exec'))
manifest=json.loads((MOD/'docs/iwd_asset_manifest.json').read_text());assets={Path(a['destination']).name:a for a in manifest};frames=0
for a in manifest:
 p=ROOT/a['destination'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==a['installed_sha256'];assert len(p.stem)<=8
 if p.suffix=='.bam':frames+=bam(b)[0];assert a['source_sha256']==a['installed_sha256']
 else:
  assert len(b)==492 and b[:8]==b'VVC V1.0';dep=b[8:16].split(b'\0')[0].decode()+'.bam';assert dep in assets
  cycles=bam((ROOT/assets[dep]['destination']).read_bytes())[1]
  assert all(struct.unpack_from('<I',b,o)[0] in (0,0xffffffff) or 1<=struct.unpack_from('<I',b,o)[0]<=len(cycles) for o in (104,108,144))
  assert all(b[o:o+8]==bytes(8) for o in (16,68,120,128,136,148))
game=Path(tempfile.mkdtemp(prefix='sra-iwd-eet-'))
try:
 shutil.copytree(ROOT,game,dirs_exist_ok=True);ov=game/'override';ov.mkdir()
 for p in SOURCE.iterdir():
  if p.is_file() and p.suffix.upper() in ('.SPL','.EFF','.PRO','.VVC','.VEF','.BAM','.BMP','.IDS'):shutil.copy2(p,ov/p.name)
 (ov/'eet.flag').write_bytes(b'Fixture');(game/'chitin.key').write_bytes(b'KEY V1  '+struct.pack('<IIII',0,0,24,24));(game/'dialog.tlk').write_bytes(b'TLK V1  '+struct.pack('<HII',0,1,44)+bytes(26))
 def resource(name):return next(p for p in ov.iterdir() if p.name.lower()==name.lower())
 def snap():
  files=[p for p in ov.iterdir() if p.name.lower()!='add_spell.ids'];result={p.name.lower():hashlib.sha256(p.read_bytes()).hexdigest() for p in files};assert len(result)==len(files),'case-colliding game filenames';return result
 def run(args,label):
  p=subprocess.run([str(WEIDU),'sr_original_spell_animations/setup-sr_original_spell_animations.tp2','--noautoupdate','--language','0','--no-exit-pause',*args],cwd=game,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(OUT/(label+'.log')).write_text(p.stdout);assert p.returncode==0,p.stdout[-10000:]
 originals={s:resource(s+'.spl').read_bytes() for s in dict.fromkeys([r[0] for r in ROWS]+list(OVERLAY_BY))};before=snap();tlk=(game/'dialog.tlk').read_bytes()
 def check_iwd():
  report=[]
  for spell in originals:
   old=originals[spell];new=resource(spell+'.spl').read_bytes();assert len(old)==len(new);assert new!=old,spell
   ao,n,eo=struct.unpack_from('<IHI',old,100);assert old[:eo]==new[:eo],spell+' header/icon/projectile change'
   gidx,gcount=struct.unpack_from('<HH',old,110);assert old[eo+gidx*48:eo+(gidx+gcount)*48]==new[eo+gidx*48:eo+(gidx+gcount)*48]
   og,oh=parse(old);ng,nh=parse(new);assert og==ng
   spell_rows=[r for r in ROWS if r[0]==spell];overlay=OVERLAY_BY.get(spell);names={overlay['private']} if overlay else {'srio'+r[2] for r in spell_rows}
   count=0
   for (_,fx),(_,fy) in zip(oh,nh):
    assert len(fx)==len(fy)
    for e,f in zip(fx,fy):
     if e==f:continue
     if overlay:
      assert opcode(e)==opcode(f)==overlay['opcode']
     else:assert opcode(e) in (141,215) and opcode(f)==215
     assert f[20:28].split(b'\0')[0].decode() in names
     allowed=set(range(20,28))
     if overlay:allowed|=set(range(8,12));assert struct.unpack_from('<I',f,8)[0]==1
     elif opcode(e)==141:allowed|={0,1}|set(range(8,12))
     if not overlay and not spell_rows[0][6]:allowed|=set(range(12,13))|set(range(14,18))
     assert all(a==b for i,(a,b) in enumerate(zip(e,f)) if i not in allowed),spell+' changed conditions or gameplay'
     count+=1
   assert count==n*(1 if overlay else len(spell_rows)),(spell,count,n)
   report.append(dict(spell=spell,abilities=n,visual_effects_replaced=count,all_mechanics_and_conditions_preserved=True))
  return report
 run(['--force-install-list','10'],'IWD_install');report=check_iwd();installed=snap()
 assert {x for x in before if before[x]!=installed[x]}=={x.lower()+'.spl' for x in originals}
 run(['--force-install-list','10'],'IWD_reinstall');assert snap()==installed
 run(['--force-uninstall-list','10'],'IWD_uninstall');assert snap()==before
 run(['--force-install-list','0','10'],'SR_IWD_install');check_iwd()
 for spell,*_ in CORE['spells']:assert_preserved((SOURCE/(spell+'.SPL')).read_bytes(),resource(spell+'.spl').read_bytes(),spell)
 both=snap();allowed={x.lower()+'.spl' for x in originals}|{r[0].lower()+'.spl' for r in CORE['spells']}|{'spentaai.bam','spentaci.bam','spchrorb.bam','spmagglo.bam','spmagglo.vvc'}
 assert {x for x in before if before[x]!=both[x]}<=allowed
 run(['--force-install-list','0','10'],'SR_IWD_reinstall');assert snap()==both
 run(['--force-uninstall-list','10','0'],'SR_IWD_uninstall');assert snap()==before
 # A later mod's additional visual must cause a safe skip, not layering or deletion.
 p=resource('sppr308.spl');b=bytearray(p.read_bytes());ao,n,eo=struct.unpack_from('<IHI',b,100);cnt,idx=struct.unpack_from('<HH',b,ao+30)
 # Replace one nonvisual effect with an unknown visual, retaining valid layout.
 off=next(eo+(idx+j)*48 for j in range(cnt) if struct.unpack_from('<H',b,eo+(idx+j)*48)[0] not in (141,215))
 struct.pack_into('<H',b,off,215);b[off+20:off+28]=b'UNKNOWN\0';p.write_bytes(b);unknown=bytes(b)
 run(['--force-install-list','10'],'IWD_unknown_visual_guard');assert p.read_bytes()==unknown
 run(['--force-uninstall-list','10'],'IWD_guard_uninstall');p.write_bytes(originals['SPPR308']);assert snap()==before
 assert (game/'dialog.tlk').read_bytes()==tlk
 result=dict(status='PASS',component=10,spells=len(originals),persistent_overlay_spells=len(OVERLAYS),bam_assets=len(manifest)//2,vvc_assets=len(manifest)//2,frames_validated=frames,spell_checks=report,standalone_install=True,combined_with_SR=True,reinstall_stable=True,uninstall_byte_exact=True,unknown_visual_skipped=True,icons_projectiles_globals_nonvisual_effects_and_conditions_preserved=True,game_rendering_tested=False,baseline='owner-supplied modded EET exports; isolated fixture with synthetic KEY/TLK',excluded_framework_cache='ADD_SPELL.IDS')
 (OUT/'IWD_validation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS:',len(originals),'real EET spells;',len(manifest)//2,'BAM/VVC pairs; standalone/combined install, stable reinstall, full uninstall, unknown-visual guard. No game rendering test.')
finally:shutil.rmtree(game)
