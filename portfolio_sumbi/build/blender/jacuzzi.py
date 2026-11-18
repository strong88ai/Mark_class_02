import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender')
from common import *
import house
import common
common.WOODSCALE=40; common.WOODDIST=0.6
sc=reset(); m=house.M()
m['glass'].node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value=1.15
house.build_house(m,interior=True,lights=True)
for n in ('jac_basin','jac_water'): bpy.data.objects.remove(bpy.data.objects[n])
jac=[house.L(x,y) for x,y in [(12.4,10.2),(15.5,10.2),(18.8,12.1),(18.8,16.0),(12.4,11.7)]]
cx=sum(p[0] for p in jac)/5; cy=sum(p[1] for p in jac)/5
inner=[(cx+(x-cx)*0.86,cy+(y-cy)*0.86) for x,y in jac]
tile=mat('tile',(0.2,0.21,0.22),0.35,noise_bump=0.08,noise_scale=30)
cut=prism('jcut',jac,2.0,4.0,tile)
t_=bpy.data.objects['f2_terr']; md=t_.modifiers.new('b','BOOLEAN'); md.operation='DIFFERENCE'; md.object=cut; md.solver='EXACT'
bpy.context.view_layer.objects.active=t_; bpy.ops.object.modifier_apply(modifier='b'); bpy.data.objects.remove(cut)
prism('jfloor',jac,2.4,2.6,tile)
for i in range(5):
    a,b=jac[i],jac[(i+1)%5]; c_,d=inner[(i+1)%5],inner[i]
    prism(f'jring{i}',[a,b,c_,d],2.6,3.62,tile)
wat=mat('wat2',(0.55,0.88,0.92),0.02,transmission=1.0,ior=1.33)
xs=[p[0] for p in jac]; ys=[p[1] for p in jac]
mesh_obj('jwater',[(min(xs),min(ys),3.56),(max(xs),min(ys),3.56),(max(xs),max(ys),3.56),(min(xs),max(ys),3.56)],[(0,1,2,3)],wat)
for k,(y0,y1,zt) in enumerate([(7.95,8.35,3.3),(7.55,7.95,3.0),(7.15,7.55,2.75)]): box(f'jstep{k}',16.3,18.3,y0,y1,2.6,zt,tile)
area('uw',(cx,cy,2.75),3.0,220,(0.6,0.95,1.0))
area('uw2',(cx+1.5,cy-1.5,2.75),2.0,150,(0.6,0.95,1.0))
bases=rock_bases(); place_rocks(bases,m['basalt'],(-20,50),(-7.5,-0.2),lambda y: y*3/7.3,700,0.7,1.6)
sea=mat('sea2',(0.05,0.12,0.16),0.06,noise_bump=0.25,noise_scale=1.5)
box('sea',-500,500,-800,-5,-3.4,-3.0,sea)
box('lawn_e',24.5,60,0,22,-0.05,0.02,m['lawn'])
# dusk sky
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; nt=w.node_tree
bg=nt.nodes['Background']
try:
    sky=nt.nodes.new('ShaderNodeTexSky')
    for t in ('NISHITA','MULTIPLE_SCATTERING','SINGLE_SCATTERING'):
        try: sky.sky_type=t; break
        except Exception: pass
    try: sky.sun_elevation=math.radians(2.0); sky.sun_rotation=math.radians(230)
    except Exception as e: print('sky param',e)
    nt.links.new(sky.outputs['Color'],bg.inputs['Color']); bg.inputs['Strength'].default_value=0.35
    print('sky type',sky.sky_type)
except Exception as e:
    print('sky fail',e); bg.inputs['Color'].default_value=(0.9,0.6,0.45,1)
sun(230,3,2.2,(1,0.55,0.3),angle=1.0)
sc.view_settings.view_transform='AgX'
try: sc.view_settings.look='AgX - Medium High Contrast'
except Exception: pass
camera((16.4,9.9,4.85),target=(20.6,4.4,3.2),lens=20)
render(OUTDIR+'/jacuzzi.png',2400,1600,96)
