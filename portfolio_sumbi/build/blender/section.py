import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender')
import common
from common import *
import house
sc=reset(); m=house.M()
common.CLIPX=17.0
house.build_house(m,interior=True,lights=True)
earth=m['earth']; ce=m['cap_earth']
box('earth_n',0,30,18.6,40,-12,0,earth,ce); box('earth_b',0,30,0,18.6,-12,-4.5,earth,ce)
box('earth_e',24.5,30,0,18.6,-12,0,earth,ce)
box('plaza',0,30,18.6,40,-0.05,0.02,m['stone'],m['cap_conc'])
box('road',0,30,24,31,0.02,0.04,mat('asph',(0.3,0.3,0.31),0.9),m['cap_conc'])
# riprap slope mass under rocks
from common import prism
# slope solid in YZ: build as boxes stepping
for i in range(14):
    y0=-0.6*(i+1); z1=-0.3*i
    box(f'rip{i}',0,30,y0,y0+0.6,-12,z1,mat('ripm',(0.2,0.2,0.2),0.9),mat('ripcap',(0.3,0.3,0.3),0.9))
bases=rock_bases(); place_rocks(bases,m['basalt'],(17,30),(-7.5,-0.2),lambda y: y*3.4/7.3,260,0.6,1.4)
sea=mat('sea',(0.2,0.3,0.36),0.08,noise_bump=0.1,noise_scale=4)
box('sea',0,60,-60,-8.4,-12,-3.0,sea,mat('seacap',(0.33,0.45,0.52),0.6))
world_color((0.95,0.93,0.9),1.0); bpy.context.scene.view_settings.view_transform='Standard'
sun(200,22,3.0,(1,0.85,0.68))
camera((-20,3,0.5),rot=(90,0,-90),ortho=46)
render(OUTDIR+'/section.png',3000,1350,48)
