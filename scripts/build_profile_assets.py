#!/usr/bin/env python3
"""Build the profile's exact, dependency-free scientific SVG illustrations.

Run: python3 scripts/build_profile_assets.py
Animations play once; their default and reduced-motion view is the final frame.
"""
from pathlib import Path
from html import escape
import json
import math
import random
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'profile'
PALETTES = {
    'light': dict(bg='#f8fafc', panel='#ffffff', ink='#182b40', muted='#536579',
                  line='#d9e2ec', teal='#087f86', violet='#7152ad', faint='#eaf2f5'),
    'dark': dict(bg='#101a2a', panel='#162337', ink='#edf3fa', muted='#a7b8cc',
                 line='#31425a', teal='#71d8d2', violet='#c3a9f0', faint='#203249'),
}

def text(x, y, value, size=16, fill='ink', weight=400, anchor='start', mono=False):
    family = 'Consolas,DejaVu Sans Mono,monospace' if mono else 'Arial,Helvetica,sans-serif'
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{P.get(fill,fill)}">'
            f'{escape(str(value))}</text>')

def line(x1,y1,x2,y2,color='line',width=1.5,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{P.get(color,color)}" stroke-width="{width}" {extra}/>'

def rect(x,y,w,h,fill='panel',stroke='none',r=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{P.get(fill,fill)}" stroke="{P.get(stroke,stroke)}" {extra}/>'

def circle(x,y,r,color,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P.get(color,color)}" {extra}/>'

def animation_css():
    # Four discrete states; no visual interpolation of quantum probabilities.
    rules = ['.frame{opacity:0}.f3{opacity:1}']
    for i in range(4):
        start, end = i*25, (i+1)*25
        points = ['0%{opacity:0}', '100%{opacity:0}']
        if i == 0:
            points = ['0%{opacity:1}', '25%,100%{opacity:0}']
        elif i == 3:
            points = ['0%{opacity:0}', '75%,100%{opacity:1}']
        else:
            points = [f'0%{{opacity:0}}',f'{start}%{{opacity:1}}',f'{end}%,100%{{opacity:0}}']
        rules.append(f'@keyframes f{i}{{'+''.join(points)+'}')
        rules.append(f'.f{i}{{animation:f{i} 10s steps(1,end) 1 both}}')
    rules.append('@media(prefers-reduced-motion:reduce){.frame{animation:none!important;opacity:0!important}.f3{opacity:1!important}}')
    return '<style>'+''.join(rules)+'</style>'

def svg(w,h,title,desc,body,animated=False):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            +(animation_css() if animated else '')
            +rect(1,1,w-2,h-2,'bg','line',16)+body+'</svg>\n')

def header(compact):
    w,h = (400,232) if compact else (840,204)
    b=text(30,35,'PHYSICS  /  COMPUTATION',13,'teal',700,mono=True)
    b+=text(28,98,'Ashish Patel',49,'ink',700)
    b+=text(31,133,'M.Sc. Physics · IIT Indore',21,'muted')
    if compact:
        b+=line(30,157,370,157)
        b+=text(30,186,'Quantum computing · Machine learning',17,'ink')
        b+=text(30,212,'Computer vision',17,'ink')
    else:
        b+=text(31,177,'Quantum computing  ·  Machine learning  ·  Computer vision',16,'ink')
        # Equal, quiet motifs for gates, a learned boundary, and pixels.
        for x in [592,665,738]: b+=rect(x,43,60,82,'panel','line',10)
        b+=line(599,84,645,84,'teal',2)+rect(610,70,25,28,'panel','teal',4)
        b+=text(622.5,90,'H',16,'teal',700,'middle')
        b+=line(674,109,716,61,'violet',1.8)
        for dx,dy,c in [(12,27,'teal'),(18,50,'teal'),(34,33,'violet'),(41,56,'violet')]:
            b+=circle(665+dx,43+dy,3,c)
        for y in range(3):
            for x in range(3): b+=rect(749+x*12,65+y*12,9,9,'teal' if x==1 else 'faint',r=1)
    return svg(w,h,'Ashish Patel — Physics and computation','M.Sc. Physics, IIT Indore. Interests in quantum computing, machine learning, and computer vision.',b)

H = ((1/math.sqrt(2),1/math.sqrt(2)),(1/math.sqrt(2),-1/math.sqrt(2)))
X = ((0.,1.),(1.,0.))

def matvec(m,v): return tuple(sum(a*b for a,b in zip(row,v)) for row in m)

STATES=[(1.,0.)]
for gate in [H,H,X]: STATES.append(matvec(gate,STATES[-1]))
LABELS=['|0⟩','|+⟩','|0⟩','|1⟩']
OPS=['Start in zero','H creates superposition','H again restores zero','X swaps zero to one']

def quantum_frame(i,compact):
    cy=124 if compact else 127
    gx=[118,216,314] if compact else [126,225,324]
    b=line(72,cy,366 if compact else 407,cy,'line',2)
    b+=text(34,cy+7,'|0⟩',23,'ink',mono=True)
    for n,(x,label) in enumerate(zip(gx,['H','H','X'])):
        applied=n<i
        col=('teal' if label=='H' else 'violet') if applied else 'muted'
        b+=rect(x-22,cy-23,44,46,'panel',col,7)
        b+=text(x,cy+8,label,24,col,700,'middle')
        b+=text(x,cy+49,str(n+1),13,'muted',anchor='middle',mono=True)
    b+=circle((gx[i-1] if i else 72),cy,4,'teal') if i==0 else ''
    if compact:
        b+=line(30,195,370,195)
        b+=text(34,225,'STATE',13,'muted',700,mono=True)
        b+=text(32,271,LABELS[i],35,'teal',mono=True)
        b+=text(34,308,f'Step {i} / 3',16,'muted')
        bx,by,bh,bw,gap=214,340,86,42,84
        b+=text(277,225,'MEASUREMENT',13,'muted',700,'middle',mono=True)
    else:
        b+=line(445,83,445,204)
        b+=text(473,106,'STATE',12,'muted',700,mono=True)
        b+=text(470,151,LABELS[i],32,'teal',mono=True)
        b+=text(473,184,f'Step {i} / 3',14,'muted')
        bx,by,bh,bw,gap=616,181,65,46,104
        b+=text(691,87,'MEASUREMENT',12,'muted',700,'middle',mono=True)
    for k,amp in enumerate(STATES[i]):
        prob=amp*amp
        x=bx+k*gap
        b+=rect(x,by-bh,bw,bh,'faint',r=3)
        if prob>1e-10: b+=rect(x,by-bh*prob,bw,bh*prob,'teal' if k==0 else 'violet',r=3)
        b+=text(x+bw/2,by-bh-8,f'{prob*100:.0f}%',15,'ink',600,'middle')
        b+=text(x+bw/2,by+23,f'P({k})',15,'muted',anchor='middle',mono=True)
    b+=text(34,376,OPS[i],17,'ink',600) if compact else text(34,202,OPS[i],16,'ink',600)
    return b

def quantum(compact,animated):
    w,h=(400,426) if compact else (840,264)
    b=text(30,34,'01 / QUANTUM FUNDAMENTALS',13,'teal',700,mono=True)
    b+=text(30,65,'Gates change a state.',25,'ink',700)
    for i in (range(4) if animated else [3]):
        body=quantum_frame(i,compact)
        b+=f'<g class="frame f{i}">{body}</g>' if animated else body
    b+=text(30,h-20,'Ideal circuit · no intermediate measurement',14,'muted')
    return svg(w,h,'Quantum gates: H, H, X','Educational illustration. Zero becomes plus, then zero, then one. Probability bars show computational-basis measurement at the indicated stage.',b,animated)

def make_data():
    rng=random.Random(218)
    points=[]
    for label in (0,1):
        center=-.72 if label==0 else .72
        for _ in range(16):
            points.append((max(-2.5,min(2.5,rng.gauss(center,.78))),
                           max(-2.5,min(2.5,rng.gauss(center,.78))),label))
    return points

DATA=make_data()

def sigmoid(x): return 1/(1+math.exp(-x))

def loss(w):
    return sum(max(z:=w[0]*x+w[1]*y+w[2],0)-label*z+math.log1p(math.exp(-abs(z)))
               for x,y,label in DATA)/len(DATA)

def gradient(w):
    d=[0.,0.,0.]
    for x,y,label in DATA:
        e=sigmoid(w[0]*x+w[1]*y+w[2])-label
        for j,v in enumerate((x,y,1.)): d[j]+=e*v/len(DATA)
    return d

STEPS=[0,20,100,400]
MODELS=[]
w=[0.,0.,0.]
for step in range(401):
    if step in STEPS: MODELS.append(w[:])
    d=gradient(w)
    w=[v-.15*g for v,g in zip(w,d)]

IMAGE=[[int(x>=3) for x in range(5)] for _ in range(5)]
KERNEL=[[-1,0,1],[-2,0,2],[-1,0,1]]

def convolve(image,kernel):
    """True 2D convolution, valid region, unit stride; kernel is flipped."""
    return [[sum(image[y+j][x+i]*kernel[2-j][2-i] for j in range(3) for i in range(3))
             for x in range(len(image[0])-2)] for y in range(len(image)-2)]

EDGE=convolve(IMAGE,KERNEL)

def boundary(w):
    a,b,c=w
    points=[]
    if abs(b)>1e-12:
        for x in [-2.6,2.6]:
            y=-(a*x+c)/b
            if -2.6<=y<=2.6: points.append((x,y))
    if abs(a)>1e-12:
        for y in [-2.6,2.6]:
            x=-(b*y+c)/a
            if -2.6<=x<=2.6: points.append((x,y))
    return points[:2]

def ml_plot(i,x,y,w,h,compact):
    b=rect(x,y,w,h,'panel','line',6)
    sx=lambda z:x+(z+2.6)/5.2*w
    sy=lambda z:y+h-(z+2.6)/5.2*h
    for tick in [-1.3,0,1.3]:
        b+=line(sx(tick),y,sx(tick),y+h,'line',.7)
        b+=line(x,sy(tick),x+w,sy(tick),'line',.7)
    pts=boundary(MODELS[i])
    if len(pts)==2: b+=line(sx(pts[0][0]),sy(pts[0][1]),sx(pts[1][0]),sy(pts[1][1]),'ink',2)
    for px,py,label in DATA:
        b+=circle(round(sx(px),3),round(sy(py),3),4 if compact else 3.2,'teal' if label==0 else 'violet')
    b+=text(x+w+9,y+h+1,'x₁',14,'muted')+text(x-2,y-8,'x₂',14,'muted')
    return b

def vision(i,x,y,compact):
    cell=17 if compact else 16
    kcell=18 if compact else 15
    outcell=21 if compact else 19
    kx=x+5*cell+30
    ox=kx+3*kcell+34
    b=text(x,y-13,'IMAGE',14 if compact else 12,'muted',700,mono=True)
    b+=text(kx,y-13,'FILTER',14 if compact else 12,'muted',700,mono=True)
    b+=text(ox,y-13,'EDGES',14 if compact else 12,'muted',700,mono=True)
    for yy,row in enumerate(IMAGE):
        for xx,value in enumerate(row):
            b+=rect(x+xx*cell,y+yy*cell,cell-2,cell-2,'teal' if value else 'faint',r=2)
    ky=y+(5*cell-3*kcell)/2
    for yy,row in enumerate(KERNEL):
        for xx,value in enumerate(row):
            b+=text(kx+xx*kcell+kcell/2,ky+yy*kcell+13,value,14 if compact else 12,'ink',anchor='middle',mono=True)
    oy=y+(5*cell-3*outcell)/2
    for yy,row in enumerate(EDGE):
        for xx,value in enumerate(row):
            b+=rect(ox+xx*outcell,oy+yy*outcell,outcell-2,outcell-2,'faint' if value==0 else 'violet',r=2)
            b+=text(ox+xx*outcell+(outcell-2)/2,oy+yy*outcell+14,abs(value),14 if compact else 11,'ink' if value==0 else ('#ffffff' if THEME=='light' else '#101a2a'),600,'middle',mono=True)
    py,px=[(0,0),(0,1),(1,2),(2,2)][i]
    b+=rect(x+px*cell-1,y+py*cell-1,3*cell-1,3*cell-1,'none','violet',3,extra='stroke-width="2"')
    b+=rect(ox+px*outcell-1,oy+py*outcell-1,outcell,outcell,'none','teal',3,extra='stroke-width="2"')
    return b

def ml_vision(compact,animated):
    w,h=(400,426) if compact else (840,264)
    b=text(30,34,'02 / MACHINE LEARNING + VISION',13,'violet',700,mono=True)
    b+=text(30,65,'Learn patterns. Find edges.',25,'ink',700)
    for i in (range(4) if animated else [3]):
        if compact:
            s=ml_plot(i,40,94,160,118,True)
            s+=text(232,117,'LOGISTIC',13,'muted',700,mono=True)
            s+=text(232,138,'REGRESSION',13,'muted',700,mono=True)
            s+=text(232,171,f'Step {STEPS[i]}',17,'ink',600)
            s+=text(232,199,'Synthetic data',15,'muted')
            s+=line(30,234,370,234)
            s+=vision(i,40,272,True)
            s+=text(40,393,'Fixed Sobel filter · edge magnitude',15,'muted')
        else:
            s=ml_plot(i,47,100,203,110,False)
            s+=text(276,121,'LOGISTIC',12,'muted',700,mono=True)
            s+=text(276,140,'REGRESSION',12,'muted',700,mono=True)
            s+=text(276,174,f'Step {STEPS[i]}',15,'ink',600)
            s+=text(276,201,'Synthetic data',13,'muted')
            s+=line(445,83,445,214)
            s+=vision(i,478,118,False)
            s+=text(478,226,'Fixed Sobel filter · edge magnitude',14,'muted')
            s+=text(47,244,'Educational examples · 32 synthetic samples',13,'muted')
        b+=f'<g class="frame f{i}">{s}</g>' if animated else s
    return svg(w,h,'Machine learning and computer vision','New educational illustrations. Logistic regression is fitted on 32 synthetic samples. A fixed Sobel filter computes edge magnitudes from a binary image; it is not a trained network.',b,animated)

def verify_math():
    for state in STATES: assert abs(sum(a*a for a in state)-1)<1e-12
    expected=[(1.,0.),(.5,.5),(1.,0.),(0.,1.)]
    for state,probs in zip(STATES,expected):
        assert all(abs(a*a-p)<1e-12 for a,p in zip(state,probs))
    assert all(abs(x-y)<1e-12 for x,y in zip(matvec(H,matvec(H,(.6,.8))),(.6,.8)))
    assert all(abs(x-y)<1e-12 for x,y in zip(matvec(X,matvec(X,(.6,.8))),(.6,.8)))
    # Gradient checked independently by finite differences.
    trial=[.3,-.2,.1]
    for j,g in enumerate(gradient(trial)):
        lo=trial[:]; hi=trial[:]; lo[j]-=1e-6; hi[j]+=1e-6
        assert abs(g-(loss(hi)-loss(lo))/2e-6)<1e-8
    losses=[loss(w) for w in MODELS]
    assert all(b<a for a,b in zip(losses,losses[1:]))
    for model in MODELS[1:]:
        for x,y in boundary(model): assert abs(model[0]*x+model[1]*y+model[2])<1e-12
    assert EDGE == [[0,-4,-4]]*3
    assert convolve([[1]*5 for _ in range(5)],KERNEL)==[[0]*3]*3
    assert convolve([row[::-1] for row in IMAGE],KERNEL)==[[4,4,0]]*3
    return losses

if __name__=='__main__':
    losses=verify_math()
    OUT.mkdir(parents=True,exist_ok=True)
    files=[]
    for THEME,P in PALETTES.items():
        for compact in (False,True):
            middle='-compact' if compact else ''
            path=OUT/f'header{middle}-{THEME}.svg'
            path.write_text(header(compact));files.append(path)
            for name,make in [('quantum',quantum),('ml-vision',ml_vision)]:
                for animated in (True,False):
                    still='' if animated else '-still'
                    path=OUT/f'{name}{middle}{still}-{THEME}.svg'
                    path.write_text(make(compact,animated));files.append(path)
    for path in files:
        ET.parse(path)
        assert '<script' not in path.read_text()
    print(json.dumps({'assets':len(files),'total_bytes':sum(f.stat().st_size for f in files),
                      'quantum_probabilities':[[round(a*a,8) for a in s] for s in STATES],
                      'logistic_training_loss':losses,'signed_convolution':EDGE},indent=2))
