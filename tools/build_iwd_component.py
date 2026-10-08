"""Build optional IWDEE graphics; requires the owner's exported IWDEE resources.
Usage: python3 tools/build_iwd_component.py PATH_TO_METADATA PATH_TO_BAMS
This does not regenerate or change the SR component.
"""
from pathlib import Path
import csv,hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'sr_original_spell_animations'
# BG root, IWD art, replacement identifier, expected old visual, expected target, old parameter2, sustained
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
]

def main():
 src=Path(sys.argv[1]);bams=Path(sys.argv[2]);assets=MOD/'assets/iwd';assets.mkdir(exist_ok=True)
 for p in assets.iterdir():
  if p.suffix in ('.bam','.vvc'):p.unlink()
 manifest=[]
 for art,code in sorted({(r[1],r[2]) for r in ROWS}):
  name='srio'+code;original=(bams/(art+'.BAM')).read_bytes();(assets/(name+'.bam')).write_bytes(original)
  vpath=src/(art+'.VVC');synth=not vpath.exists()
  controller=(src/'SPOISOH.VVC').read_bytes() if synth else vpath.read_bytes()
  v=bytearray(controller);assert len(v)==492 and v[:8]==b'VVC V1.0'
  assert v[16:24]==bytes(8) and v[68:76]==bytes(8) and v[136:144]==bytes(8)
  v[8:16]=name.encode().ljust(8,b'\0');v[96:104]=name.encode().ljust(8,b'\0')
  for o in (120,128,148):v[o:o+8]=bytes(8)
  # The SPL effect controls the duration of looping Blade Barrier visuals.
  struct.pack_into('<I',v,92,0xffffffff)
  (assets/(name+'.vvc')).write_bytes(v)
  for ext,data in [('bam',original),('vvc',v)]:
   manifest.append(dict(source=art+'.'+ext.upper() if ext=='bam' or not synth else 'SPOISOH.VVC (template for '+art+'.BAM)',destination='sr_original_spell_animations/assets/iwd/'+name+'.'+ext,installed_sha256=hashlib.sha256(data).hexdigest(),source_sha256=hashlib.sha256(original if ext=='bam' else controller).hexdigest(),synthesized_controller=synth if ext=='vvc' else False))
 (MOD/'docs/iwd_asset_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (MOD/'docs/iwd_spell_mapping.json').write_text(json.dumps(ROWS,indent=2)+'\n')
 tpa=(ROOT/'tools/iwd_patch_template.tpa').read_text()
 for spell in dict.fromkeys(r[0] for r in ROWS):
  rows=[r for r in ROWS if r[0]==spell];r=rows[0];op=141 if r[3]==141 else 215;old='' if op==141 else r[3]
  extra=''
  if len(rows)==2:extra=' srio_old2 = ~'+rows[1][3]+'~ srio_new2 = ~srio'+rows[1][2]+'~'
  tpa+=f'\nACTION_IF FILE_EXISTS_IN_GAME ~{spell}.spl~ BEGIN\n  COPY_EXISTING ~{spell}.spl~ ~override~\n    LPF srio_replace INT_VAR srio_op = {op} srio_p2 = {r[5]} srio_target = {r[4]} srio_loop = {int(r[6])} srio_expected = {len(rows)}\n      STR_VAR srio_old = ~{old}~ srio_new = ~srio{r[2]}~{extra} END\n  BUT_ONLY_IF_IT_CHANGES\nEND ELSE BEGIN PRINT ~IWD Spell Animations: {spell}.spl missing, skipped.~ END\n'
 (MOD/'lib/iwd_animations.tpa').write_text(tpa)
 print(len(set(r[0] for r in ROWS)),'spells;',len(manifest)//2,'BAMs + same number VVCs')
if __name__=='__main__':main()
