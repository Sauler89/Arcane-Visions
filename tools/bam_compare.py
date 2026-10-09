"""Canonical BAM V1 comparison. Audit utility; requires NumPy. No game writes."""
import struct,zlib,hashlib
import numpy as np
def sha(b):return hashlib.sha256(b).hexdigest()

def bam(p):
    original=p.read_bytes();b=original
    if b[:4]==b'BAMC':
        b=zlib.decompress(b[12:]);assert len(b)==struct.unpack_from('<I',original,8)[0]
    assert b[:8]==b'BAM V1  ',(p,'unsupported signature')
    nf,nc,rle=struct.unpack_from('<HBB',b,8)
    fo,pal,lookup=struct.unpack_from('<III',b,12)
    assert fo+12*nf+4*nc<=len(b) and pal+1024<=len(b)
    palette=np.frombuffer(b[pal:pal+1024],dtype=np.uint8).reshape(256,4)
    rgb=palette[:,[2,1,0]].copy()
    greens=np.nonzero((rgb==np.array([0,255,0])).all(axis=1))[0]
    transparent=rle
    rgba=np.empty((256,4),dtype=np.uint8);rgba[:,:3]=rgb;rgba[:,3]=255;rgba[transparent]=0
    frames=[]; artframes=[];shapeframes=[];emissiveframes=[];visible=[];maxw=maxh=0
    for i in range(nf):
        w,h,cx,cy,data=struct.unpack_from('<HHhhI',b,fo+i*12)
        o=data&0x7fffffff;size=w*h;vals=bytearray()
        if data&0x80000000:
            assert o+size<=len(b);vals.extend(b[o:o+size])
        else:
            while len(vals)<size:
                v=b[o];o+=1
                if v==rle:
                    n=b[o]+1;o+=1;vals.extend(bytes([v])*min(n,size-len(vals)))
                # NI BamV1Decoder stops at the frame boundary; a final RLE run may extend beyond it.
                else:vals.append(v)
            assert len(vals)==size,(p,i,'RLE overflow')
        pixels=rgba[np.frombuffer(vals,dtype=np.uint8)]
        frames.append(sha(struct.pack('<HHhh',w,h,cx,cy)+pixels.tobytes()))
        visible.append(bool((pixels[:,3]!=0).any()))
        image=pixels.reshape(h,w,4)
        ys,xs=np.nonzero(image[:,:,3])
        if len(xs):
            cropped=image[ys.min():ys.max()+1,xs.min():xs.max()+1]
            dims=struct.pack('<HH',cropped.shape[1],cropped.shape[0])
            artframes.append(sha(dims+cropped.tobytes()))
            shapeframes.append(sha(dims+cropped[:,:,3].tobytes()))
        else: artframes.append(sha(b'empty'));shapeframes.append(sha(b'empty'))
        # Diagnostic for blended effects: black contributes no emitted RGB.
        emitted=image.copy();emitted[~emitted[:,:,:3].any(axis=2)]=0
        ys,xs=np.nonzero(emitted[:,:,3])
        if len(xs):
            c=emitted[ys.min():ys.max()+1,xs.min():xs.max()+1]
            emissiveframes.append(sha(struct.pack('<HH',c.shape[1],c.shape[0])+c.tobytes()))
        else:emissiveframes.append(sha(b'empty'))
        maxw=max(maxw,w);maxh=max(maxh,h)
    cycles=[]
    for i in range(nc):
        n,first=struct.unpack_from('<HH',b,fo+12*nf+4*i)
        assert lookup+2*(first+n)<=len(b)
        seq=struct.unpack_from('<'+'H'*n,b,lookup+2*first) if n else ()
        assert all(x<nf for x in seq),(p,'bad cycle lookup')
        digest=sha(b''.join(bytes.fromhex(frames[x]) for x in seq))
        def compact_hash(values):
            compact=[]
            for x in seq:
                if not compact or compact[-1]!=values[x]:compact.append(values[x])
            return sha(b''.join(bytes.fromhex(v) for v in compact))
        cycles.append(dict(index=i,frames=n,hash=digest,art_hash=compact_hash(artframes),shape_hash=compact_hash(shapeframes),emissive_hash=compact_hash(emissiveframes),visible=any(visible[x] for x in seq)))
    canonical=sha(b''.join(struct.pack('<I',c['frames'])+bytes.fromhex(c['hash']) for c in cycles))
    return dict(name=p.name.upper(),bytes=len(original),sha256=sha(original),raw_sha256=sha(b),frames=nf,cycles=nc,max_width=maxw,max_height=maxh,render_sha256=canonical,cycle_data=cycles,visible=any(visible))
