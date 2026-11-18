from common import *
def M():
    return dict(
        conc=mat('conc',(0.72,0.71,0.69),0.8,noise_bump=0.05,noise_scale=40),
        white=mat('white',(0.88,0.87,0.84),0.7),
        plaster=mat('plaster',(0.92,0.9,0.86),0.85,noise_bump=0.03,noise_scale=30),
        glass=mat('glass',(0.85,0.92,0.95),0.02,transmission=1.0,ior=1.45),
        oak=mat('oak',(0.62,0.44,0.28),0.5,wood=True),
        stone=mat('stone',(0.78,0.74,0.66),0.75,tex_mix=(0.66,0.62,0.55),noise_scale=6),
        basalt=mat('basalt',(0.14,0.14,0.14),0.85,noise_bump=0.25,noise_scale=25,tex_mix=(0.08,0.08,0.08)),
        lawn=mat('lawn',(0.22,0.36,0.14),0.95,tex_mix=(0.17,0.29,0.1),noise_scale=30,noise_bump=0.2),
        water=mat('water',(0.25,0.75,0.78),0.03,transmission=0.9,ior=1.33,emit=(0.2,0.7,0.75),emit_str=0.6),
        car=mat('car',(0.06,0.06,0.07),0.25,metal=0.6,coat=1.0),
        car2=mat('car2',(0.3,0.33,0.38),0.25,metal=0.6,coat=1.0),
        dark=mat('dark',(0.12,0.12,0.12),0.6),
        red=mat('red',(0.55,0.08,0.06),0.35),
        cap_conc=mat('cap_conc',(0.16,0.16,0.16),0.9),
        cap_earth=mat('cap_earth',(0.72,0.69,0.64),0.95),
        earth=mat('earth',(0.55,0.47,0.37),0.95,noise_bump=0.1),
        warm=mat('warm',(1,0.8,0.55),0.5,emit=(1,0.78,0.5),emit_str=8.0),
        songi=mat('songi',(0.42,0.22,0.16),0.8),
    )
OX=3.3
def L(x,ytop): return (OX+x,18.6-ytop)
def build_house(m,interior=True,lights=True):
    # ---------------- B1 (z -4.2..0)
    box('b1_floor',0,24.5,0,18.6,-4.5,-4.2,m['conc'],m['cap_conc'])
    # roof slab with openings: pool skylight X3.3..10.5 Y0.4..4.5 ; stairwell X19.5..24.5 Y10.5..18.6
    box('b1_roof_a',0,24.5,4.5,10.5,-0.3,0,m['conc'],m['cap_conc'])
    box('b1_roof_b',0,19.5,10.5,18.6,-0.3,0,m['conc'],m['cap_conc'])
    box('b1_roof_c',0,3.3,0,4.5,-0.3,0,m['conc'],m['cap_conc'])
    box('b1_roof_d',10.5,24.5,0,4.5,-0.3,0,m['conc'],m['cap_conc'])
    box('skylight',3.3,10.5,0.4,4.5,-0.08,-0.04,m['glass'])
    for nm,a in [('w_w',(0,0.4,0,18.6)),('w_e',(24.1,24.5,0,18.6)),('w_s',(0,24.5,0,0.4)),('w_n',(0,24.5,18.2,18.6))]:
        box('b1_'+nm,a[0],a[1],a[2],a[3],-4.2,-0.3,m['conc'],m['cap_conc'])
    for nm,a in [('p1',(14.5,24.1,10.4,10.6)),('p2',(10.5,24.1,4.4,4.6)),('p3',(14.4,14.6,4.6,18.2)),('p4',(19.4,19.6,10.6,18.2)),('p5',(10.4,10.6,0.4,4.4)),('p6',(0.4,14.4,14.0,14.2))]:
        box('b1_'+nm,a[0],a[1],a[2],a[3],-4.2,-0.3,m['white'],m['cap_conc'])
    if interior:
        box('pool',2.0,9.1,1.2,2.6,-4.25,-4.18,m['water'])
        for i,(cx,cy,mm) in enumerate([(17.3,8.9,'car'),(21.8,8.9,'car2'),(17.3,6.1,'car2'),(21.8,6.1,'car')]):
            b=box(f'car{i}',cx-2.4,cx+2.4,cy-0.95,cy+0.95,-4.2,-3.6,m[mm]); 
            b2=box(f'carT{i}',cx-1.3,cx+1.0,cy-0.85,cy+0.85,-3.6,-2.9,m['dark'])
            for o in (b,b2):
                if o: mod=o.modifiers.new('bv','BEVEL'); mod.width=0.25; mod.segments=4
        for i,xc in enumerate([16,17.3,18.6,19.9,21.2,22.5]):
            box(f'bike{i}',xc-0.35,xc+0.35,1.4,3.5,-4.2,-3.1,m['red'] if i%2 else m['dark'])
        for i in range(3): box(f'shelf{i}',15.0+i*1.4,15.8+i*1.4,17.0,18.2,-4.2,-2.2,m['oak'])
        box('rack',23.4,24.1,0.6,4.2,-4.2,-2.4,m['dark'])
    if lights:
        for x,y in [(17,8),(21,8),(18,2.5),(22,2.5),(6,2),(7,9),(17,14)]: area('l',(x,y,-0.6),2.5,30)
    # ---------------- 1F (z 0..3.6) footprint A X3.3..19.3 Y10.8..18.6, B X3.3..9.6 Y6.6..10.8
    box('f1_n',3.3,19.3,18.4,18.6,0,3.3,m['plaster'],m['cap_conc'])
    box('f1_w',3.3,3.5,6.6,18.6,0,3.3,m['plaster'],m['cap_conc'])
    box('f1_eA',19.1,19.3,10.8,18.6,0,3.3,m['plaster'],m['cap_conc'])
    box('f1_glassA',9.6,19.1,10.75,10.85,0,3.3,m['glass'])
    box('f1_sB',3.3,9.6,6.6,6.8,0,3.3,m['plaster'],m['cap_conc'])
    box('f1_eB',9.4,9.6,6.6,10.8,0,3.3,m['plaster'],m['cap_conc'])
    box('f1_roofA',3.3,19.3,10.8,18.6,3.3,3.6,m['conc'],m['cap_conc'])
    box('f1_roofB',3.3,9.6,6.6,10.8,3.3,3.6,m['conc'],m['cap_conc'])
    box('f1_floor',3.5,19.1,10.8,18.4,0,0.05,m['oak'],m['cap_conc'])
    if interior:
        box('island',9.5,13.6,14.0,15.1,0.05,0.95,m['white'],m['cap_conc'])
        box('dining',14.7,17.9,13.9,15.1,0.7,0.78,m['oak'])
        for xx in (15.0,17.5): box('dleg'+str(xx),xx,xx+0.1,14.3,14.7,0.05,0.7,m['dark'])
        box('kcounter',9.6,19.0,17.8,18.4,0.05,0.95,m['oak'],m['cap_conc'])
        box('kupper',9.6,19.0,18.0,18.4,1.6,2.5,m['oak'],m['cap_conc'])
        box('sofa1f',12,15,11.6,12.5,0.05,0.75,m['white'])
    if lights:
        for x in (11,15,18): area('l1',(x,14.5,3.2),2.5,35)
    box('terrace',9.6,19.3,5.7,10.8,0,0.06,m['stone'],m['cap_conc'])
    box('outtable',12,14.5,7.8,8.8,0.72,0.8,m['oak'])
    box('lawn',11.1,24.3,0.4,5.7,0,0.05,m['lawn'],m['cap_earth'])
    box('lawn2',19.3,24.3,5.7,6.6,0,0.05,m['stone'])
    box('planter',18.3,19.6,7.1,10.6,0,1.0,m['conc'],m['cap_conc'])
    # perimeter parapet (wood frame)
    for nm,a in [('pw',(3.3,3.6,0.0,6.6)),('ps',(3.3,24.5,0.0,0.4)),('pe',(24.2,24.5,0.0,10.5))]:
        box('par_'+nm,a[0],a[1],a[2],a[3],0,1.1,m['oak'],m['cap_conc'])
    box('rail_sky',3.6,11.1,6.55,6.6,0,1.1,m['glass'])
    # exterior stair to B1 (X21.3..22.7) steps
    for i in range(14):
        z=-0.3*i; y0=15.9-i*0.26
        box(f'st{i}',21.3,22.7,y0-0.28,y0,z-0.3,z,m['conc'],m['cap_conc'])
    # ---------------- 2F (z 3.6..7.2)
    north=[(3.3,11.0),(22.15,11.0),(22.15,18.6),(3.3,18.6)]
    wing=[(3.3,1.1),(10.8,1.1),(10.8,11.0),(3.3,11.0)]
    terr=[L(x,y) for x,y in [(7.5,7.6),(18.85,7.6),(18.85,16.3),(12.4,11.9),(10.0,11.2),(8.4,11.9),(7.5,13.5)]]
    prism('f2_slabN',north,3.3,3.6,m['conc'],m['cap_conc']); prism('f2_slabW',wing,3.3,3.6,m['conc'],m['cap_conc']); prism('f2_terr',terr,3.3,3.6,m['oak'],m['cap_conc'])
    box('f2_n',3.3,22.15,18.4,18.6,3.6,6.9,m['plaster'],m['cap_conc'])
    box('f2_e',21.95,22.15,11.0,18.6,3.6,6.9,m['plaster'],m['cap_conc'])
    box('f2_w',3.3,3.5,1.1,18.6,3.6,6.9,m['plaster'],m['cap_conc'])
    box('f2_s',3.3,10.8,1.1,1.3,3.6,6.9,m['plaster'],m['cap_conc'])
    box('f2_glassN',10.8,21.95,10.95,11.05,3.6,6.9,m['glass'])
    box('f2_wallN_end',10.8,11.0,11.0,11.2,3.6,6.9,m['plaster'],m['cap_conc'])
    box('f2_eW',10.6,10.8,1.1,4.0,3.6,6.9,m['plaster'],m['cap_conc'])
    box('f2_glassW',10.65,10.75,4.0,11.0,3.6,6.9,m['glass'])
    prism('f2_roofN',north,6.9,7.2,m['white'],m['cap_conc']); prism('f2_roofW',[(3.3,2.6),(10.8,2.6),(10.8,11.0),(3.3,11.0)],6.9,7.2,m['white'],m['cap_conc'])
    box('f2_roofW2',3.3,10.8,1.1,2.6,6.9,7.2,m['white'],m['cap_conc'])
    box('core',3.3,9.7,11.2,15.2,7.2,9.8,m['white'],m['cap_conc'])
    for nm,a in [('rp1',(3.3,22.15,18.45,18.6)),('rp2',(22.0,22.15,11.0,18.6))]: box(nm,a[0],a[1],a[2],a[3],7.2,7.6,m['white'],m['cap_conc'])
    box('roofgreen',11,21.5,11.5,18.0,7.2,7.3,m['lawn'])
    if interior:
        box('sofa2f',14.0,18.0,15.6,16.6,3.6,4.3,m['white']); box('sofa2fb',17.2,18.0,13.0,15.6,3.6,4.3,m['white'])
        box('bed',4.2,6.4,2.4,4.6,3.6,4.1,m['white']); box('dress',18.5,21.9,17.6,18.4,3.6,5.8,m['oak'])
    if lights:
        for x,y in [(15,15),(19,15),(6,6),(6,15)]: area('l2',(x,y,6.8),2.5,30)
    # jacuzzi
    jac=[L(x,y) for x,y in [(12.4,10.2),(15.5,10.2),(18.8,12.1),(18.8,16.0),(12.4,11.7)]]
    prism('jac_basin',jac,2.4,3.6,m['basalt'],m['cap_conc'])
    cx=sum(p[0] for p in jac)/5; cy=sum(p[1] for p in jac)/5
    inner=[(cx+(x-cx)*0.9,cy+(y-cy)*0.9) for x,y in jac]
    prism('jac_water',inner,3.0,3.6,m['water'])
    # glass railing along diagonal + east edge
    pts=[L(18.85,7.6),L(18.85,16.3),L(12.4,11.9),L(10.0,11.2),L(8.4,11.9),L(7.5,13.5)]
    for i in range(len(pts)-1):
        (x0,y0),(x1,y1)=pts[i],pts[i+1]; dx,dy=x1-x0,y1-y0; ln=math.hypot(dx,dy); nx,ny=-dy/ln*0.02,dx/ln*0.02
        prism(f'rail{i}',[(x0-nx,y0-ny),(x1-nx,y1-ny),(x1+nx,y1+ny),(x0+nx,y0+ny)],3.6,4.7,m['glass'])
    for x,y in [(15.8,6.6),(21.7,2.9),(21.7,10.6),(12.6,7.3)]: cyl('col',x,y,0.0,3.3,0.15,m['white'])
