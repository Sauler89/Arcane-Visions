"""Build optional IWDEE graphics; requires the owner's exported IWDEE resources.
Usage: python3 tools/build_iwd_component.py PATH_TO_METADATA PATH_TO_BAMS
This does not regenerate or change the SR component.
"""
from pathlib import Path
import csv,hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'sr_original_spell_animations'
# BG root, IWD art, replacement identifier, expected old visual, expected target, old parameter2, preserve installed timed cue
ROWS=[
('SPPR308','RPARALH','para','SPRMCURS',2,1,False),
('SPPR411','POISONH','pois','POISON',2,1,False),
('SPPR417','LRESTORH','lres','SPSTRENH',2,1,False),
('SPPR502','CCWOUNH','crit','SPHEALIN',2,1,False),
('SPPR603','BBARRH1','blt','SPBLDTOP',1,1,True),
('SPPR603','BBARRH2','blb','SPBLDBTM',1,1,True),
('SPPR708','FODEATH','deth',141,2,39,False),
('SPPR711','REGENERH','regn','ICWRATI',2,1,False),
('SPPR713','GRESTORH','gres','SPSTRENH',2,0,False),
('SPPR722','FODEATH','deth','SPFINGER',2,0,False),
('SPWI605','DSPELLH','dead',141,2,39,False),
('SPWI612','PWSILEH','pwsi','SPPOWWRD',2,1,False),
('SPWI711','CONFUSH','conf',141,2,6,False),
('SPWI713','FODEATH','deth',141,2,39,False),
('SPWI715','PWSTUNH','pwst','SPPOWWRD',2,1,False),
('SPWI812','ADHWILH','wilt',141,2,2,False),
('SPWI922','SPDRGNBR','drag','SPDRGNBR',1,2,False),
('SPWI224','GLDUSTA','dust','GLDUSTH',2,1,False),
('SPWI413A','ORSPHEC','osph','MINORGLB',2,1,True),
('SPPR712A','RESURRH','ress','ICRAISEI',2,0,False),
('SPPR607','HEALH','heal','SPHEALIN',2,1,False),
('SPPR212','SPOISOH','spoi',141,2,2,False),
('SPPR310','MMAGICH','misc',141,2,9,False),
('SPPR709','CONFUSH','conf','SPCONFUS',2,1,True),
('SPWI401','CONFUSH','conf','SPCONFUS',2,1,True),
('SPWI508','CONFUSH','conf','SPCONFUS',2,1,True),
('SPWI508','CONFUSH','conf','SPCONFUS',2,1,True),
]
CONTROLLERS={'GLDUSTA':'GLDUSTH','ORSPHEC':'#OTILUKE'}
# Only patch children when the original root still calls that child after casting.
PARENTS={'SPWI413A':'SPWI413','SPPR712A':'SPPR712'}
# Persistent engine overlays were absent from the original 141/215-only selection.
# BG root, IWD BAM, private code, BG overlay opcode, target, source controller.
OVERLAYS=[
('SPPR109','SANCTRY','sanc',153,1,'#PRONM'),
('SPWI311','PFNMISC','arrw',156,2,'#PRONM'),
('SPWI406','MGOINVC','mglb',155,1,'#PRONM'),
('SPWI602','GOINVUC','gglb',155,1,'#GLOBINV'),
('SPWI215','WEBC','webc',157,2,'WEBC'),
]

def main():
 src=Path(sys.argv[1]);bams=Path(sys.argv[2]);assets=MOD/'assets/iwd';assets.mkdir(exist_ok=True)
 source_files={p.name.upper():p for p in src.iterdir() if p.is_file()}
 bam_files={p.name.upper():p for p in bams.iterdir() if p.is_file()}
 for p in assets.iterdir():
  if p.suffix in ('.bam','.vvc'):p.unlink()
 manifest=[]
 for art,code in sorted({(r[1],r[2]) for r in ROWS}):
  name='srio'+code;original=bam_files[art+'.BAM'].read_bytes();(assets/(name+'.bam')).write_bytes(original)
  controller_name=CONTROLLERS.get(art,art)
  vpath=source_files.get(controller_name+'.VVC');synth=vpath is None
  controller=source_files['SPOISOH.VVC'].read_bytes() if synth else vpath.read_bytes()
  v=bytearray(controller);assert len(v)==492 and v[:8]==b'VVC V1.0'
  assert v[16:24]==bytes(8) and v[68:76]==bytes(8) and v[136:144]==bytes(8)
  v[8:16]=name.encode().ljust(8,b'\0');v[96:104]=name.encode().ljust(8,b'\0')
  for o in (120,128,148):v[o:o+8]=bytes(8)
  # The SPL effect controls the duration of looping Blade Barrier visuals.
  struct.pack_into('<I',v,92,0xffffffff)
  (assets/(name+'.vvc')).write_bytes(v)
  for ext,data in [('bam',original),('vvc',v)]:
   manifest.append(dict(source=art+'.BAM' if ext=='bam' else controller_name+'.VVC' if not synth else 'SPOISOH.VVC (template for '+art+'.BAM)',destination='sr_original_spell_animations/assets/iwd/'+name+'.'+ext,installed_sha256=hashlib.sha256(data).hexdigest(),source_sha256=hashlib.sha256(original if ext=='bam' else controller).hexdigest(),synthesized_controller=synth if ext=='vvc' else False))
 (MOD/'docs/iwd_asset_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (MOD/'docs/iwd_spell_mapping.json').write_text(json.dumps(ROWS,indent=2)+'\n')
 overlay_manifest=[]
 for spell,art,code,op,target,controller_name in OVERLAYS:
  name='srio'+code;original=bam_files[art+'.BAM'].read_bytes()
  (assets/(name+'.bam')).write_bytes(original)
  controller=source_files[controller_name+'.VVC'].read_bytes();v=bytearray(controller)
  assert len(v)==492 and v[:8]==b'VVC V1.0'
  assert all(v[o:o+8]==bytes(8) for o in (16,68,136))
  assert struct.unpack_from('<I',v,32)[0]&1 # persistent loop
  v[8:16]=name.encode().ljust(8,b'\0');v[96:104]=name.encode().ljust(8,b'\0')
  for o in (120,128,148):v[o:o+8]=bytes(8)
  struct.pack_into('<I',v,92,0xffffffff)
  (assets/(name+'.vvc')).write_bytes(v)
  for ext,data,source_data in [('bam',original,original),('vvc',v,controller)]:
   synthesized=ext=='vvc' and art not in ('PFNMISC','GOINVUC','WEBC')
   manifest.append(dict(source=art+'.BAM' if ext=='bam' else controller_name+'.VVC'+(' (loop template for '+art+'.BAM)' if synthesized else ''),destination='sr_original_spell_animations/assets/iwd/'+name+'.'+ext,installed_sha256=hashlib.sha256(data).hexdigest(),source_sha256=hashlib.sha256(source_data).hexdigest(),synthesized_controller=synthesized))
  overlay_manifest.append(dict(spell=spell,art=art,private=name,opcode=op,target=target,default_resource={153:'SANCTRY',155:'MINORGLB',156:'SPSHIELD',157:'WEBENTD'}[op],iwd_reference={153:'SANCTRY',156:'#PRONM',157:'WEBC',155:'MGOINVC' if spell=='SPWI406' else '#GLOBINV'}[op]))
 (MOD/'docs/iwd_asset_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (MOD/'docs/iwd_overlay_mapping.json').write_text(json.dumps(overlay_manifest,indent=2)+'\n')
 tpa=(ROOT/'tools/iwd_patch_template.tpa').read_text()+'\n'+(ROOT/'tools/iwd_dependency_template.tpa').read_text()
 for spell in dict.fromkeys(r[0] for r in ROWS):
  rows=[r for r in ROWS if r[0]==spell];r=rows[0];op=141 if r[3]==141 else 215;old='' if op==141 else r[3]
  extra=''
  if len(rows)==2:extra=' srio_old2 = ~'+rows[1][3]+'~ srio_new2 = ~srio'+rows[1][2]+'~'
  parent=PARENTS.get(spell)
  if parent:tpa+=f'\nLAF srio_check_child STR_VAR srio_root = ~{parent}~ srio_child = ~{spell}~ RET srio_linked END\nACTION_IF srio_linked BEGIN\n'
  tpa+=f'\nACTION_IF FILE_EXISTS_IN_GAME ~{spell}.spl~ BEGIN\n  COPY_EXISTING ~{spell}.spl~ ~override~\n    LPF srio_replace INT_VAR srio_op = {op} srio_p2 = {r[5]} srio_target = {r[4]} srio_loop = {int(r[6])} srio_expected = {len(rows)}\n      STR_VAR srio_old = ~{old}~ srio_new = ~srio{r[2]}~{extra} END\n  BUT_ONLY_IF_IT_CHANGES\nEND ELSE BEGIN PRINT ~IWD Spell Animations: {spell}.spl missing, skipped.~ END\n'
  if parent:tpa+=f'END ELSE BEGIN PRINT ~IWD Spell Animations: {parent}.spl no longer calls {spell}.spl after casting; skipped.~ END\n'
 (MOD/'docs/iwd_child_mapping.json').write_text(json.dumps(PARENTS,indent=2)+'\n')
 (MOD/'lib/iwd_animations.tpa').write_text(tpa)
 overlay=(ROOT/'tools/iwd_overlay_template.tpa').read_text()
 for r in overlay_manifest:
  overlay+=f'\nACTION_IF FILE_EXISTS_IN_GAME ~{r["spell"]}.spl~ BEGIN\n  COPY_EXISTING ~{r["spell"]}.spl~ ~override~\n    LPF srio_overlay INT_VAR srio_op = {r["opcode"]} srio_target = {r["target"]} srio_allow_vvc = {int(r["spell"]=="SPWI602")}\n      STR_VAR srio_default = ~{r["default_resource"]}~ srio_iwd = ~{r["iwd_reference"]}~ srio_art = ~{r["art"]}~ srio_new = ~{r["private"]}~ END\n  BUT_ONLY_IF_IT_CHANGES\nEND ELSE BEGIN PRINT ~IWD Spell Animations: {r["spell"]}.spl missing, skipped.~ END\n'
 (MOD/'lib/iwd_overlays.tpa').write_text(overlay)
 # Keep the collision guard in sync with every generated private pair.
 tp2=MOD/'setup-sr_original_spell_animations.tp2';text=tp2.read_text()
 import re
 pairs=' '.join('~'+Path(a['destination']).name+'~' for a in manifest)
 start=text.index('BEGIN @10');text=text[:start]+re.sub(r'(ACTION_FOR_EACH av_private IN ).*?( BEGIN)',lambda m:m[1]+pairs+m[2],text[start:],count=1)
 tp2.write_text(text)
 print(len(set(r[0] for r in ROWS))+len(OVERLAYS),'spells;',len(manifest)//2,'BAMs + same number VVCs')
if __name__=='__main__':main()
