"""Audit every supplied BAM and all resource references; never alter source files.
Usage: python3 tools/audit_source_coverage.py IW_METADATA IW_BAMS EET_EXPORT SR_FOLDER OUTPUT
Requires NumPy. Original-root mappings are retained in docs/original_spell_roots.json.
Graph edges are evidence of references, not proof that every declared PRO field plays.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,re,struct,sys
from bam_compare import bam

ROOT=Path(__file__).resolve().parents[1];DOC=ROOT/'sr_original_spell_animations/docs'
IW,IWB,EET,SR,OUT=[Path(x).resolve() for x in sys.argv[1:6]];OUT.mkdir(parents=True,exist_ok=True)
def files(d):return {p.name.upper():p for p in d.iterdir() if p.is_file()}
def rr(b,o):return b[o:o+8].split(b'\0')[0].decode('ascii','replace').upper().strip()
def u16(b,o):return struct.unpack_from('<H',b,o)[0]
def u32(b,o):return struct.unpack_from('<I',b,o)[0]
def csvwrite(name,rows,fields=None):
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def ids(p):
 result=defaultdict(set)
 for line in p.read_text(errors='replace').splitlines():
  m=re.match(r'\s*(0x[\da-fA-F]+|\d+)\s+([\w#]+)',line)
  if m:result[int(m[1],16 if m[1].lower().startswith('0x') else 10)].add(m[2].upper())
 return result

class Graph:
 def __init__(self,f):
  self.f=f;self.edges=defaultdict(set);self.issues=[];self.proj=ids(f['PROJECTL.IDS']) if 'PROJECTL.IDS' in f else {}
  for n,p in sorted(f.items()):
   if p.suffix.upper() not in ('.SPL','.EFF','.VVC','.VEF','.PRO','.ITM'):continue
   try:self.parse(n,p.read_bytes())
   except (ValueError,struct.error,IndexError,AssertionError) as e:self.issues.append({'resource':n,'issue':'parse/bounds','detail':str(e)})
 def edge(self,n,res,ext,why):
  if res:self.edges[n].add((res+'.'+ext,why))
 def visual(self,n,res,why,vef=True):
  if not res:return
  ext=next((e for e in (('VEF','VVC') if vef else ('VVC',)) if res+'.'+e in self.f),'BAM')
  self.edge(n,res,ext,why)
 def projectile(self,n,num,why):
  if num<=1:return
  for res in self.proj.get(num-1,[]):self.edge(n,res,'PRO',why+' [MISSILE-1]')
  if num-1 not in self.proj:self.issues.append({'resource':n,'issue':'hardcoded/unmapped projectile','detail':str(num)})
 def effect(self,n,b,o,why,external=False):
  op=u32(b,16) if external else u16(b,o)
  p1=u32(b,28 if external else o+4);p2=u32(b,32 if external else o+8);res=rr(b,48 if external else o+20)
  why+=f' opcode {op}'
  if op in (146,148,232,259,326,333):self.edge(n,res,'SPL',why)
  elif op in (177,183,248,249,272,283):self.edge(n,res,'EFF',why)
  elif op in (111,112,122):self.edge(n,res,'ITM',why+' [weapon/item binding; not artwork import]')
  elif op==215:self.visual(n,res,why,vef=p2!=1)
  elif 153<=op<=158:self.visual(n,res if p2==1 else {153:'SANCTRY',154:'SPENTACI',155:'MINORGLB',156:'SPSHIELD',157:'WEBENTD',158:'GREASED'}[op],why,False)
  elif op==141:
   if p2<32 and p2%4 in (0,1,2):res=('SHAIR','SHEARTH','SHWATER')[p2%4]
   else:res={32:'SPBOOM',33:'SPBOOM',34:'SPBOOM',35:'FLMSTRK',36:'HLYMITE',37:'SHAIR',38:'SPDIMNDR',39:'SPFDEATH'}.get(p2,'')
   self.visual(n,res,why,False)
  elif op==140:
   if p2==0:self.projectile(n,p1,why)
   elif 9<=p2<=16:
    for res in self.proj.get(110+p2-9,[]):self.edge(n,res,'PRO',why)
  elif op==68:self.visual(n,res or 'SPGFLSH1',why,False)
  elif op in (67,331) and external:
   self.visual(n,rr(b,112),why+' arrival',False);self.visual(n,rr(b,120),why+' target',False)
  elif op==336:
   for i in range(min(p1,26)):
    for phase in '12':self.visual(n,res+phase+chr(65+i),why+' eye',False)
 def parse(self,n,b):
  ext=n.rsplit('.',1)[-1]
  if ext in ('SPL','ITM'):
   if ext=='SPL':assert b[:8] in (b'SPL V1  ',b'SPL\x03V1  ');header=40
   else:assert b[:8]==b'ITM V1  ';header=56
   assert len(b)>=114
   a,c,e=u32(b,100),u16(b,104),u32(b,106);assert a>=114 and a+c*header<=len(b) and e<=len(b)
   idx,cnt=u16(b,110),u16(b,112)
   for j in range(cnt):
    assert e+(idx+j+1)*48<=len(b)
    self.effect(n+'@CAST',b,e+(idx+j)*48,'casting/on-equip')
    self.effect(n+'@SUB',b,e+(idx+j)*48,'child casting/on-equip')
   for i in range(c):
    h=a+i*header;idx,cnt=u16(b,h+32),u16(b,h+30)
    self.projectile(n,u16(b,h+(38 if ext=='SPL' else 42)),f'ability {i+1} projectile')
    for j in range(cnt):
     assert e+(idx+j+1)*48<=len(b)
     self.effect(n,b,e+(idx+j)*48,f'ability {i+1}')
   self.edges[n+'@SUB'].update(self.edges[n])
  elif ext=='EFF':assert b[:8]==b'EFF V2.0' and len(b)>=128;self.effect(n,b,0,'external effect',True)
  elif ext=='VVC':
   assert b[:8]==b'VVC V1.0' and len(b)>=156
   self.edge(n,rr(b,8),'BAM','VVC main');self.edge(n,rr(b,136),'BAM','VVC alpha')
   if u32(b,32)&16:self.edge(n,rr(b,68),'BMP','VVC palette')
  elif ext=='VEF':
   assert b[:4]==b'VEF ' and len(b)>=24
   for a,c in ((u32(b,8),u32(b,12)),(u32(b,16),u32(b,20))):
    assert a+c*224<=len(b)
    for j in range(c):
     o=a+j*224;t=u32(b,o+12)
     if t in (1,2):self.visual(n,rr(b,o+16),f'VEF type {t}',t==2)
  elif ext=='PRO':
   assert b[:8]==b'PRO V1.0' and len(b)>=256
   for o in (68,76):self.edge(n,rr(b,o),'SPL',f'PRO spell 0x{o:x}')
   self.visual(n,rr(b,32),'PRO source [declared]')
   typ=u16(b,8)
   if typ<2:return
   assert len(b)>=512
   self.edge(n,rr(b,260),'BAM','PRO travel [flag-dependent]')
   if u32(b,256)&32:self.edge(n,rr(b,268),'BAM','PRO shadow')
   if u32(b,256)&1:self.edge(n,rr(b,284),'BMP','PRO palette')
   for o in (310,318,326):self.edge(n,rr(b,o),'BAM','PRO trail [declared]')
   if typ==3:
    assert len(b)>=768
    for o,label in ((540,'center'),(552,'spread'),(560,'ring')):self.visual(n,rr(b,o),'PRO '+label+' [activation not assumed]')
    # Old graph retained both conventions. Keep this uncertainty explicit.
    for o in (532,538):
     if o==532 and (not (u16(b,512)&16) or u16(b,514)):continue
     number=u16(b,o)
     if not number:continue
     for key in (number,number-1):
      for res in self.proj.get(key,[]):self.edge(n,res,'PRO',f'PRO nested 0x{o:x} [index/activation unconfirmed]')
 def walk(self,root):
  seen={};queue=[(root,root)]
  while queue:
   n,path=queue.pop()
   if n in seen:continue
   seen[n]=path
   for dst,why in sorted(self.edges.get(n,[])):
    child=dst+'@SUB' if dst.endswith(('.SPL','.ITM')) else dst
    queue.append((child,path+' -> '+dst+' ('+why+')'))
  return seen

iwfiles=files(IW);eetfiles=files(EET);srfiles={}
for p in sorted(SR.rglob('*')):
 if p.is_file():srfiles.setdefault(p.name.upper(),p)
gi,ge,gs=Graph(iwfiles),Graph(eetfiles),Graph(srfiles)
roots=json.loads((DOC/'original_spell_roots.json').read_text())
paths=[];iw_roots=defaultdict(set);cast_roots=defaultdict(set)
for r in roots:
 if not r['iwdee_spell']:continue
 for phase,suffix in [('postcast',''),('casting','@CAST')]:
  for n,path in gi.walk(r['iwdee_spell']+'.SPL'+suffix).items():
   if not n.endswith(('.BAM','.BMP','.ITM@SUB')):continue
   paths.append(dict(bg_spell=r['bg_spell'],iwdee_spell=r['iwdee_spell'],phase=phase,asset=n,path=path))
   (iw_roots if phase=='postcast' else cast_roots)[n].add(r['bg_spell'])
csvwrite('source_dependency_paths.csv',paths)
decoded={};inventory=[]
for label,d in [('IWDEE',IWB),('EET',EET),('SR',SR)]:
 decoded[label]=[]
 for p in sorted(d.rglob('*')):
  if not p.is_file() or p.suffix.upper()!='.BAM':continue
  x=bam(p);x['path']=str(p.relative_to(d));decoded[label].append(x)
  inventory.append(dict(source=label,path=x['path'],sha256=x['sha256'],frames=x['frames'],cycles=x['cycles']))
csvwrite('source_BAM_inventory.csv',inventory)
iwmanifest=json.loads((DOC/'iwd_asset_manifest.json').read_text());srmanifest=json.loads((DOC/'asset_manifest.json').read_text())
included_iw={a['source'].upper() for a in iwmanifest if a['destination'].endswith('.bam')}
included_sr={a['source'].upper() for a in srmanifest if a['destination'].endswith('.bam')}
sr_root_set={r[0] for r in json.loads((DOC/'test_config.json').read_text())['spells']}|{'SPPR105','SPWI118'}
decisions=[]
for a in decoded['IWDEE']:
 full=[];art=[];shape=[];partial=[]
 for s in decoded['EET']:
  if a['raw_sha256']==s['raw_sha256'] or (a['visible'] and a['render_sha256']==s['render_sha256']):full.append(s['name']);continue
  sc={x['art_hash'] for x in s['cycle_data'] if x['visible']}
  ac=[x['art_hash'] for x in a['cycle_data'] if x['visible']]
  if ac and all(x in sc for x in ac):art.append(s['name'])
  elif any(x in sc for x in ac):partial.append(s['name'])
  if any(x['visible'] and y['visible'] and x['shape_hash']==y['shape_hash'] for x in a['cycle_data'] for y in s['cycle_data']):shape.append(s['name'])
 bg=iw_roots[a['name']]
 status='included' if a['name'] in included_iw else 'EET_exact_graphic_match' if full else 'EET_all_visible_cycle_art_match' if art else 'no_original_BG_spell_mapping' if not bg else 'SR_spell_overlap' if bg<=sr_root_set else 'distinct_candidate_not_integrated'
 sr_full=[];sr_art=[];sr_selected=[]
 for s in decoded['SR']:
  complete=a['raw_sha256']==s['raw_sha256'] or (a['visible'] and a['render_sha256']==s['render_sha256'])
  ac=[x['art_hash'] for x in a['cycle_data'] if x['visible']];sc={x['art_hash'] for x in s['cycle_data'] if x['visible']}
  same_art=bool(ac) and all(x in sc for x in ac)
  if complete:sr_full.append(s['path'])
  if same_art:sr_art.append(s['path'])
  if (complete or same_art) and s['path'].upper() in included_sr:sr_selected.append(s['path'])
 decisions.append(dict(iwdee_bam=a['name'],source_sha256=a['sha256'],status=status,BG_roots=' | '.join(sorted(bg)),casting_roots=' | '.join(sorted(cast_roots[a['name']])),EET_complete=' | '.join(full),EET_all_cycle_art=' | '.join(art),EET_partial_art=' | '.join(partial),EET_shape_only_diagnostic=' | '.join(shape),SR_complete_all_archive=' | '.join(sr_full),SR_all_cycle_art_all_archive=' | '.join(sr_art),SR_matches_selected_original_spell_art=' | '.join(sr_selected)))
csvwrite('iwd_selection_recheck.csv',decisions)
# Classify pending phases from their actual paths, never assume every candidate
# is a projectile. This prevents a direct cue such as MMAGICH being overlooked.
pending=[]
for a in decisions:
 if a['status']!='distinct_candidate_not_integrated':continue
 evidence=[p for p in paths if p['asset']==a['iwdee_bam'] and p['phase']=='postcast']
 direct=[p for p in evidence if '.PRO (' not in p['path']]
 if a['iwdee_bam'] in ('GREASEB.BAM','GREASEC.BAM'):
  reason='Conditional IWDEE child visual has no matching EET child; existing EET uses opcode 158; condition-aware binding not implemented'
 elif a['iwdee_bam'] in ('MAGICSTN.BAM','SLIVINH.BAM','SSORBH.BAM','SSORBT.BAM'):
  reason='Installed EET weapon/item or travel binding differs; inspect the temporary weapon and actual hit route before importing art'
 elif direct:
  reason='Direct postcast cue requires review of the matching installed EET cue; not a projectile-only candidate'
 else:
  reason='Declared PRO travel/area/nested phase; installed binding and flag/controller/palette/timing compatibility not yet verified'
 pending.append(dict(bam=a['iwdee_bam'],BG_roots=a['BG_roots'],reason=reason,representative_IWDEE_path=' | '.join(p['path'] for p in (direct or evidence)[:2]),SR_overlap=False))
csvwrite('iwd_pending_candidates.csv',pending,['bam','BG_roots','reason','representative_IWDEE_path','SR_overlap'])
# A selected BAM can still have unbound uses in other original spells.
parents=json.loads((DOC/'iwd_child_mapping.json').read_text());bindings=defaultdict(set)
for r in json.loads((DOC/'iwd_spell_mapping.json').read_text()):bindings[r[1]+'.BAM'].add(parents.get(r[0],r[0]))
for r in json.loads((DOC/'iwd_overlay_mapping.json').read_text()):bindings[r['art']+'.BAM'].add(r['spell'])
unbound=[]
for a in decisions:
 if a['status']!='included':continue
 for root in sorted(iw_roots[a['iwdee_bam']]-bindings[a['iwdee_bam']]):
  for p in paths:
   if p['phase']=='postcast' and p['bg_spell']==root and p['asset']==a['iwdee_bam']:
    unbound.append(dict(bam=a['iwdee_bam'],bg_spell=root,path=p['path'],reason='BAM included for other bindings; this source phase is not installed'))
csvwrite('iwd_unbound_included_art.csv',unbound,['bam','bg_spell','path','reason'])
active_text='\n'.join(p.read_text(errors='replace') for p in SR.rglob('*') if p.suffix.lower() in ('.tpa','.tp2','.tph'))
active_text=re.sub(r'/\*.*?\*/','',active_text,flags=re.S);active_text=re.sub(r'//[^\n]*','',active_text)
sr_rows=[]
extra_reasons={'A#SHOPE':'copied for Symbol of Stunning, but no active SPL/EFF/PRO reference to its VVC','A#SPAIN':'Symbol of Weakness replaces original Symbol of Fear; no live VVC binding','DVHOLYA1':'Protection from Evil aura installation commented out','DVHOLYA2':'Protection from Evil aura installation commented out','SPDIMNDR':'archive BAM is not copied by active installer','SPCCOLDL':'COPY_EXISTING edits game BAM; archive variant is not copied','SPSTORMS':'new Storm Shield spell','DVVTRSPH':'new Vitriolic Sphere spell','DVVTRTRA':'new Vitriolic Sphere projectile','ICELANCE':'new Icelance spell','DVSBURST':'Sound Burst replaces original Deafness','MESTSH':'Mestil Acid Sheath replaces original blue Fire Shield','MSTONE':'weapon/inventory artwork; no live world BAM field'}
for a in decoded['SR']:
 name=a['name'];stem=name[:-4];p=SR/a['path'];binaryrefs=[];visualrefs=[]
 for n,edges in gs.edges.items():
  if any(dst==name for dst,why in edges):visualrefs.append(n)
 icons=[]
 for n,f in srfiles.items():
  if n.endswith(('.SPL','.ITM')):
   b=f.read_bytes()
   if len(b)>=114 and b[:4] in (b'SPL ',b'ITM '):
    if rr(b,58)==stem:icons.append(n+': memorized icon')
    if n.endswith('.ITM'):
     for o in (68,88):
      if rr(b,o)==stem:icons.append(n+': item icon')
    ao,c=u32(b,100),u16(b,104)
    for i in range(c):
     size=40 if n.endswith('.SPL') else 56
     if ao+(i+1)*size<=len(b) and rr(b,ao+i*size+4)==stem:icons.append(n+': ability icon');break
 copied=bool(re.search(r'COPY\s+~[^~]*[\\/]'+re.escape(p.name)+r'~',active_text,re.I))
 if a['path'].upper() in included_sr:status='included';reason='bundled original-spell animation'
 elif '/WINGS/' in '/'+a['path'].upper():status='avatar_or_equipment';reason='celestial wings/equipment artwork'
 elif stem in extra_reasons:
  reason=extra_reasons[stem];status='unreferenced_or_inactive' if stem in ('A#SHOPE','A#SPAIN','DVHOLYA1','DVHOLYA2','SPDIMNDR','SPCCOLDL') else 'new_spell_or_item'
 elif icons or re.search(r'(?:SPWI|SPPR|DVWI|DVPR)\d{3}[ABC]$',stem):status='icon';reason='spell/item icon field/naming; no world-effect binding found' if not visualrefs else 'icon with additional references requiring review'
 elif not visualrefs:status='item_or_unused';reason='no world-effect BAM field in supplied SPL/EFF/VVC/PRO graph'
 else:status='needs_review';reason='unclassified world-effect reference'
 sr_rows.append(dict(source_path=a['path'],source_sha256=a['sha256'],status=status,reason=reason,active_direct_COPY=copied,visual_references=' | '.join(visualrefs),icon_references=' | '.join(sorted(set(icons)))))
csvwrite('sr_source_selection.csv',sr_rows)
issues=[]
for source,g in [('IWDEE',gi),('EET',ge),('SR',gs)]:
 issues.extend(dict(source=source,**r) for r in g.issues)
csvwrite('source_parse_issues.csv',issues,['source','resource','issue','detail'])
missing=[]
for r in paths:
 base=r['asset'].removesuffix('@SUB');present=base in iwfiles or base in files(IWB)
 if not present:missing.append(r)
csvwrite('missing_IWDEE_dependencies.csv',missing,['bg_spell','iwdee_spell','phase','asset','path'])
eet_missing=[]
for root in sorted({r['bg_spell'] for r in roots}):
 for n,path in ge.walk(root+'.SPL').items():
  if n.removesuffix('@SUB') not in eetfiles:eet_missing.append(dict(bg_spell=root,asset=n,path=path))
csvwrite('missing_EET_dependencies.csv',eet_missing,['bg_spell','asset','path'])
summary=dict(version='v0.2.0-beta.5',inputs={k:len(v) for k,v in decoded.items()},physical_frames={k:sum(x['frames'] for x in v) for k,v in decoded.items()},IWDEE_statuses=dict(Counter(r['status'] for r in decisions)),SR_statuses=dict(Counter(r['status'] for r in sr_rows)),SR_unclassified=[r for r in sr_rows if r['status']=='needs_review'],missing_IWDEE_asset_names=sorted({r['asset'] for r in missing}),included_IWD_SR_matches=[r for r in decisions if r['status']=='included' and r['SR_matches_selected_original_spell_art']],shape_is_not_duplicate_evidence=True,partial_cycle_is_not_full_duplicate_evidence=True,graph_PRO_activation_is_not_assumed=True,complete_IWDEE_import=False,game_rendering_tested=False)
(OUT/'source_coverage_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
