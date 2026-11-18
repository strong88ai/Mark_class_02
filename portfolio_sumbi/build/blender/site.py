import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender')
from common import *
import house
sc=reset(); m=house.M()
white=mat('wm',(0.9,0.89,0.86),0.8); asph=mat('asph',(0.36,0.36,0.37),0.9); yel=mat('yel',(0.85,0.65,0.1),0.6)
walk=mat('walk',(0.28,0.22,0.19),0.9); sea=mat('sea',(0.24,0.33,0.38),0.12,noise_bump=0.15,noise_scale=3)
tree=mat('tree',(0.32,0.42,0.28),0.9); trunk=mat('trunk',(0.45,0.38,0.3),0.9)
house.build_house(m,interior=True,lights=False)
box('plaza',-75,0,0,22,-0.05,0,m['stone']); box('plaza2',0,24.5,18.6,22,-0.05,0,m['stone'])
box('walk',-75,0,9.5,11.5,0,0.01,walk); box('walk2',-41,-38.5,11.5,22,0,0.01,walk)
box('sidewalk',-75,70,22,24,-0.05,0.08,white)
box('road',-75,70,24,31,-0.1,-0.02,asph); box('yline',-75,70,27.4,27.6,-0.02,-0.01,yel)
box('sidewalk2',-75,70,31,33,-0.05,0.08,white)
random.seed(2)
for i,x in enumerate(range(-70,62,14)):
    h=random.choice([6,7,8.5]); box(f'hs{i}',x,x+10,36,45,0,h,white)
    box(f'hsr{i}',x+1,x+6,37,42,h,h+2.2,white)
for x in range(-70,-3,7):
    for y in (6.5,14.5):
        cyl('tr',x,y,0,3.6,0.14,trunk); bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(x,y,4.1)); o=bpy.context.active_object; o.scale=(1.8,1.8,0.8); o.data.materials.append(tree)
box('nb_lawn',24.5,48,0,22,-0.05,0.02,m['lawn'])
o=box('neighbor',28,44,4,18,0,7,white); mod=o.modifiers.new('bv','BEVEL'); mod.width=4.5; mod.segments=10
o.modifiers.new('sub','SUBSURF').levels=2
box('nb_glass',30,42,3.9,4.0,0,4,m['glass'])
box('ground_e',48,70,0,22,-0.05,0,m['stone'])
bases=rock_bases(); place_rocks(bases,m['basalt'],(-75,70),(-7.5,-0.2),lambda y: y*3/7.3,1600,0.7,1.7)
box('sea',-300,300,-300,-5,-3.4,-3.0,sea)
world_color((0.95,0.93,0.9),1.0); bpy.context.scene.view_settings.view_transform='Standard'
sun(215,35,3.4)
camera((-30,-46,44),target=(12,7,1),ortho=58)
render(OUTDIR+'/site_axo.png',2200,2200,40)
