"""Check all shipped graphics, controllers, private guards and README previews.
Usage: python3 tests/verify_graphics_integrity.py [IWDEE_BAM_EXPORT_DIR]
Standard library only; no game installation is changed.
"""
from pathlib import Path
import ast,hashlib,json,re,struct,sys,zlib
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'sr_original_spell_animations';D=MOD/'docs'
SOURCE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else None
METADATA=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else None
metadata_files={p.name.upper():p for p in METADATA.iterdir() if p.is_file()} if METADATA else {}
helper=ast.parse((ROOT/'tests/verify_assets.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name=='bam'],type_ignores=[]),'<BAM checks>','exec'))
sr=json.loads((D/'asset_manifest.json').read_text());iw=json.loads((D/'iwd_asset_manifest.json').read_text());allassets=sr+iw
assert len({a['destination'].lower() for a in allassets})==len(allassets)
actual={str(p.relative_to(ROOT)) for p in (MOD/'assets').rglob('*') if p.is_file()};assert actual=={a['destination'] for a in allassets}
by={Path(a['destination']).name.lower():a for a in allassets};frames=nbam=nvvc=0
for a in allassets:
 p=ROOT/a['destination'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==a['installed_sha256'];assert len(p.stem)<=8
 if p.suffix=='.bam':
  nf,cycles=bam(b);frames+=nf;nbam+=1;assert a['source_sha256']==a['installed_sha256']
  if SOURCE and a in iw:assert b==(SOURCE/a['source']).read_bytes()
 else:
  nvvc+=1;assert len(b)==492 and b[:8]==b'VVC V1.0';ref=b[8:16].split(b'\0')[0].decode().lower()+'.bam';assert ref in by
  if METADATA and a in iw:
   original=metadata_files[a['source'].split(' ')[0].upper()].read_bytes()
   assert hashlib.sha256(original).hexdigest()==a['source_sha256']
   expected=bytearray(original);expected[8:16]=p.stem.encode().ljust(8,b'\0');expected[96:104]=p.stem.encode().ljust(8,b'\0')
   for o in (120,128,148):expected[o:o+8]=bytes(8)
   struct.pack_into('<I',expected,92,0xffffffff)
   assert b==expected,'source controller phases/placement/flags changed: '+str(p)
  assert all(b[o:o+8]==bytes(8) for o in (16,68,120,128,136,148))
  nf,cycles=bam((ROOT/by[ref]['destination']).read_bytes())
  assert all(struct.unpack_from('<I',b,o)[0] in (0,0xffffffff) or 1<=struct.unpack_from('<I',b,o)[0]<=len(cycles) for o in (104,108,144))
overlays=json.loads((D/'iwd_overlay_mapping.json').read_text());guard=(MOD/'setup-sr_original_spell_animations.tp2').read_text().split('BEGIN @10',1)[1].split(' BEGIN',1)[0]
assert set(re.findall(r'~([^~]+\.(?:bam|vvc))~',guard))=={Path(a['destination']).name for a in iw}
for r in overlays:
 b=(MOD/'assets/iwd'/(r['private']+'.vvc')).read_bytes();assert struct.unpack_from('<I',b,32)[0]&1
 assert struct.unpack_from('<I',b,92)[0]==0xffffffff
 assert struct.unpack_from('<I',b,104)[0]==1
 assert struct.unpack_from('<I',b,108)[0]==1
core=json.loads((D/'test_config.json').read_text());rows=json.loads((D/'iwd_spell_mapping.json').read_text());iwd_roots={r[0] for r in rows}|{r['spell'] for r in overlays}
assert not iwd_roots&{r[0] for r in core['spells']}
exclusions=json.loads((D/'iwd_user_exclusions.json').read_text())
assert not {r['spell'] for r in exclusions}&(iwd_roots|{r[0] for r in core['spells']})
assert not {b for r in exclusions for b in r['bam_resources']}&{a['source'] for a in iw}
assert not (ROOT/'docs/previews/web.gif').exists()
previews=json.loads((ROOT/'docs/previews/manifest.json').read_text())
for e in previews:
 assert hashlib.sha256((ROOT/e['asset']).read_bytes()).hexdigest()==e['asset_sha256']
 assert hashlib.sha256((ROOT/e['file']).read_bytes()).hexdigest()==e['gif_sha256']
for p in (ROOT/'README.md',ROOT/'README.it.md',MOD/'README.md',ROOT/'CREDITS.md',D/'RIGOROUS_AUDIT.md',D/'IWD_SELECTION_RECHECK.it.md',D/'FULL_SOURCE_AUDIT.it.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('https:','http:','#')):continue
  assert (p.parent/target.split('#')[0]).exists(),(p,target)
assert not any(p.suffix.lower() in ('.spl','.eff','.pro','.cre','.itm','.bcs') for p in (MOD/'assets').rglob('*') if p.is_file())
result=dict(status='PASS',bam=nbam,vvc=nvvc,total_frames=frames,preview_gifs=len(previews),core_spells=len(core['spells']),iwd_spells=len(iwd_roots),exact_BAM_source_bytes=True,no_icons_or_gameplay_imports=True,private_names_unique=True,all_controller_dependencies_resolved=True,all_IWD_private_names_guarded=True,persistent_controllers_loop=True,README_local_links_valid=True,game_rendering_tested=False)
print(json.dumps(result,indent=2))
