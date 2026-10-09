"""Render the shipped world-effect BAMs as illustrative README GIFs.
Requires Pillow. The GIFs are not in-game captures. Game files are never edited.
"""
from pathlib import Path
import hashlib,json,struct,zlib
from PIL import Image,ImageChops,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'sr_original_spell_animations';OUT=ROOT/'docs/previews';OUT.mkdir(parents=True,exist_ok=True)
DEMO=[('spmagglo','native/spmagglo','SPMAGGLO · shared protection aura',10,[0],True),('entangle','native/spentaai','Entangle · SPENTA AI',10,[0],True),('ghost-armor','custom/sraghst','Ghost Armor · GHARMOR',15,[0],True),('chromatic-orb','native/spchrorb','Chromatic Orb · SPCHRORB',15,[0],True),('mantle','custom/sramant','Mantle · DVMANTLE',10,[0],True),('blade-barrier','iwd/srioblt','Blade Barrier · BBARRH1',15,[0,1,1,2],False)]
DEMO += [('sanctuary','iwd/sriosanc','Sanctuary · SANCTRY',15,[0],True),('protection-from-arrows','iwd/srioarrw','Protection from Arrows · PFNMISC',15,[0],True),('minor-globe','iwd/sriomglb','Minor Globe · MGOINVC',15,[0],True),('globe-of-invulnerability','iwd/sriogglb','Globe of Invulnerability · GOINVUC',15,[0],True)]
DEMO += [('glitterdust','iwd/sriodust','Glitterdust · GLDUSTA',15,[1],True),('resilient-sphere','iwd/srioosph','Resilient Sphere · ORSPHEC',15,[0],True),('resurrection','iwd/srioress','Resurrection · RESURRH',15,[0],True)]

def decode(path):
 b=path.read_bytes()
 if b[:4]==b'BAMC':
  expected=struct.unpack_from('<I',b,8)[0];b=zlib.decompress(b[12:]);assert len(b)==expected
 assert b[:8]==b'BAM V1  ';nf,nc,rle=struct.unpack_from('<HBB',b,8);fo,pal,look=struct.unpack_from('<III',b,12)
 rgb=[tuple(b[pal+i*4+j] for j in (2,1,0)) for i in range(256)];green=rle
 images=[]
 for i in range(nf):
  w,h,cx,cy,off=struct.unpack_from('<HHhhI',b,fo+i*12);pos=off&0x7fffffff;vals=[]
  if off&0x80000000:vals=list(b[pos:pos+w*h])
  else:
   while len(vals)<w*h:
    p=b[pos];pos+=1
    if p==rle:n=b[pos]+1;pos+=1;vals.extend([p]*min(n,w*h-len(vals)))
    else:vals.append(p)
  assert len(vals)==w*h
  im=Image.new('RGBA',(w,h));im.putdata([(*rgb[v],0 if v==green else 255) for v in vals]);images.append((im,cx,cy))
 cycles=[]
 for i in range(nc):
  count,first=struct.unpack_from('<HH',b,fo+12*nf+4*i);cycles.append(list(struct.unpack_from('<'+'H'*count,b,look+2*first)))
 return images,cycles

def main():
 manifest=[];thumbs=[]
 for slug,rel,label,fps,which,blend in DEMO:
  p=MOD/'assets'/(rel+'.bam');ims,cycles=decode(p);seq=sum((cycles[i] for i in which),[]);assert seq
  # Keep the BAM frame anchors fixed; avoid per-frame centering jitter.
  minx=min(-ims[i][1] for i in seq);miny=min(-ims[i][2] for i in seq)
  maxx=max(ims[i][0].width-ims[i][1] for i in seq);maxy=max(ims[i][0].height-ims[i][2] for i in seq)
  w,h=maxx-minx,maxy-miny;scale=min(2,300/max(w,1),198/max(h,1));frames=[]
  for i in seq:
   frame,cx,cy=ims[i];sprite=Image.new('RGBA',(w,h));sprite.alpha_composite(frame,(-cx-minx,-cy-miny));sprite=sprite.resize((max(1,round(w*scale)),max(1,round(h*scale))),Image.Resampling.NEAREST)
   canvas=Image.new('RGB',(336,252),'#151d28');x=(336-sprite.width)//2;y=12+(198-sprite.height)//2
   if blend:
    backing=canvas.crop((x,y,x+sprite.width,y+sprite.height));light=ImageChops.screen(backing,sprite.convert('RGB'));canvas.paste(light,(x,y),sprite.getchannel('A'))
   else:canvas.paste(sprite,(x,y),sprite)
   draw=ImageDraw.Draw(canvas);draw.text((14,221),label,fill='#e6edf3');draw.text((14,237),'BAM preview — not an in-game capture',fill='#8595a7');frames.append(canvas)
  gif=OUT/(slug+'.gif');delay=max(10,round(1000/fps/10)*10)
  frames[0].save(gif,save_all=True,append_images=frames[1:],duration=delay,loop=0,optimize=True)
  assert gif.stat().st_size<5_000_000
  with Image.open(gif) as check:assert check.size==(336,252) and check.n_frames>0
  manifest.append(dict(file='docs/previews/'+gif.name,asset=str(p.relative_to(ROOT)),asset_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),gif_sha256=hashlib.sha256(gif.read_bytes()).hexdigest(),bam_cycles=which,frame_rate=fps,preview_frame_delay_ms=delay,screen_blending_approximation=blend,game_capture=False))
  thumb=max(frames,key=lambda im:sum(i*n for i,n in enumerate(im.convert('L').histogram())));thumbs.append(thumb)
 sheet=Image.new('RGB',(1008,252*((len(thumbs)+2)//3)))
 for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*336,(i//3)*252))
 sheet.save(OUT/'contact-sheet.png');(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Rendered',len(DEMO),'verified previews of shipped animation BAMs; no icons.')
if __name__=='__main__':main()
