"""Independent same-layer copper screening; not an insulation certification.
Arc chord sag and circular buffer error are controlled by --step (radians).
Unsupported copper shapes fail closed. Requires shapely and sexpdata.
"""
import sys, math, json, hashlib
from pathlib import Path
import sexpdata
from shapely.geometry import Point, LineString, box
from shapely.affinity import rotate, translate

def children(n, key):
    return [x for x in n[1:] if isinstance(x,list) and x and str(x[0])==key]
def one(n,key,default=None):
    a=children(n,key)
    if a:return a[0][1:]
    if default is not None:return default
    raise ValueError('Missing '+key)
def audit(path, step):
    raw=Path(path).read_bytes(); root=sexpdata.loads(raw.decode())
    items=[]; pads=[]; nets={int(n[1]):str(n[2]) for n in children(root,'net')}
    q=math.ceil(math.pi/2/step)
    def add(g,net,layers,label):
        items.append((g,int(net),set(layers),label))
    for fp in children(root,'footprint'):
        ref=next(str(p[2]) for p in children(fp,'property') if p[1]=='Reference')
        pos=one(fp,'at'); ang=float(pos[2]) if len(pos)>2 else 0
        for p in children(fp,'pad'):
            xy=one(p,'at'); w,h=map(float,one(p,'size')); typ=str(p[3])
            if typ=='circle' and abs(w-h)<1e-9:g=Point(0,0).buffer(w/2,quad_segs=q)
            elif typ=='rect':g=box(-w/2,-h/2,w/2,h/2)
            elif typ=='oval':
                a=max(w,h); b=min(w,h)
                ends=[(-(a-b)/2,0),((a-b)/2,0)] if w>=h else [(0,-(a-b)/2),(0,(a-b)/2)]
                g=LineString(ends).buffer(b/2,quad_segs=q)
            else:raise ValueError('Unsupported pad '+typ)
            # KiCad pad angle is board absolute; position rotates with footprint.
            pa=float(xy[2]) if len(xy)>2 else ang
            g=rotate(g,-pa,origin=(0,0))
            t=math.radians(-ang); x=pos[0]+xy[0]*math.cos(t)-xy[1]*math.sin(t); y=pos[1]+xy[0]*math.sin(t)+xy[1]*math.cos(t)
            g=translate(g,x,y)
            ls=[str(l) for l in one(p,'layers')]; ls=['F.Cu','B.Cu'] if '*.Cu' in ls else [l for l in ls if l.endswith('.Cu')]
            net=one(p,'net',[0])[0]; add(g,net,ls,ref+'.'+str(p[1]));pads.append((ref,str(p[1]),net,x,y))
    for kind in ['segment','arc']:
        for n in children(root,kind):
            a=tuple(map(float,one(n,'start'))); b=tuple(map(float,one(n,'end')))
            if kind=='segment':pts=[a,b]
            else:
                m=tuple(map(float,one(n,'mid')))
                ax,ay=a;mx,my=m;bx,by=b
                d=2*(ax*(my-by)+mx*(by-ay)+bx*(ay-my))
                if abs(d)<1e-12:raise ValueError('Degenerate arc')
                aa=ax*ax+ay*ay;mm=mx*mx+my*my;bb=bx*bx+by*by
                cx=(aa*(my-by)+mm*(by-ay)+bb*(ay-my))/d
                cy=(aa*(bx-mx)+mm*(ax-bx)+bb*(mx-ax))/d
                sa=math.atan2(ay-cy,ax-cx); ma=math.atan2(my-cy,mx-cx); ea=math.atan2(by-cy,bx-cx)
                sweep=(ea-sa)%(2*math.pi)
                if (ma-sa)%(2*math.pi)>sweep:sweep-=2*math.pi
                count=max(2,math.ceil(abs(sweep)/step));r=math.hypot(ax-cx,ay-cy)
                pts=[(cx+r*math.cos(sa+sweep*i/count),cy+r*math.sin(sa+sweep*i/count)) for i in range(count+1)]
            net=int(one(n,'net')[0]); layer=str(one(n,'layer')[0]); uid=str(one(n,'uuid')[0])
            add(LineString(pts).buffer(float(one(n,'width')[0])/2,quad_segs=q),net,[layer],kind+':'+uid)
    for kind in ['zone','via']:
        if children(root,kind):raise ValueError('Unsupported '+kind)
    results=[]
    for i,(g,n,ls,label) in enumerate(items):
        for h,nn,ll,other in items[i+1:]:
            if n!=nn and ls&ll:results.append({'distance_mm':g.distance(h),'a':label,'a_net':nets[n],'b':other,'b_net':nets[nn],'layers':sorted(ls&ll)})
    results.sort(key=lambda r:r['distance_mm'])
    # Electrical pad-to-pad connectivity using copper intersections, both layers for PTH.
    disconnected=[]
    for net in sorted(set(p[2] for p in pads)):
        ix=[i for i,v in enumerate(items) if v[1]==net]; parent={i:i for i in ix}
        def find(i):
            while parent[i]!=i:i=parent[i]
            return i
        for j,i in enumerate(ix):
            for k in ix[j+1:]:
                if items[i][2]&items[k][2] and items[i][0].distance(items[k][0])<1e-7:parent[find(i)]=find(k)
        groups={find(i) for i in ix if i<len(pads)}
        if len(groups)>1:disconnected.append({'net':nets[net],'pad_components':len(groups)})
    return {'sha256':hashlib.sha256(raw).hexdigest(),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'step_radians':step,'pads':len(pads),'tracks_arcs':len(items)-len(pads),'pairs':len(results),'minimum_pairs':results[:10],'disconnected_pad_nets':disconnected,'pad_netlist':pads}
if __name__=='__main__':
    print(json.dumps(audit(sys.argv[1],float(sys.argv[2]) if len(sys.argv)>2 else 0.01),indent=2))
