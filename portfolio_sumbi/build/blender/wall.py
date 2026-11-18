import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender')
from common import *
sc=reset(); sc.view_settings.view_transform='Standard'; sc.view_settings.exposure=-0.9
soil=mat('soil',(0.30,0.20,0.12),0.95,noise_bump=0.6,noise_scale=12,tex_mix=(0.26,0.18,0.11))
pave=mat('pave',(0.80,0.75,0.66),0.7,tex_mix=(0.7,0.65,0.57),noise_scale=8,noise_bump=0.1)
gravel=mat('gravel',(0.55,0.54,0.52),0.8)
pipe=mat('pipe',(0.92,0.92,0.92),0.4)
drain=mat('drain',(0.08,0.08,0.09),0.55,noise_bump=1.0,noise_scale=60)
prot=mat('prot',(0.72,0.72,0.70),0.8)
memb=mat('memb',(0.06,0.25,0.75),0.35)
conc=mat('conc',(0.58,0.58,0.56),0.85,noise_bump=0.15,noise_scale=50,tex_mix=(0.6,0.59,0.57))
rebar=mat('rebar',(0.22,0.2,0.18),0.5,metal=0.8)
ins=mat('ins',(0.95,0.85,0.35),0.7,noise_bump=0.05)
fin=mat('fin',(0.95,0.95,0.94),0.6)
mud=mat('mud',(0.6,0.59,0.57),0.9,noise_bump=0.1)
D=2.4  # depth along Y
g=0.14 # explode gap
# base: mud slab (버림)
box('mud',-2.0,3.2,0,D,-0.62,-0.52,mud)
# membrane horizontal on mud slab under mat
box('memb_h',0.0,3.2,0,D,-0.52,-0.50,memb)
# mat slab + wall
box('mat',0.0,3.2,0,D,-0.50,0.0,conc)
box('wall',0.0,0.40,0,D,0.0,2.2,conc)
# rebar ends on front cut face (double reinforcement) + vertical bars poking above top
for xr in (0.07,0.33):
    for z in [i*0.2+0.1 for i in range(11)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=0.013,depth=0.03,location=(xr,-0.012,z),rotation=(math.pi/2,0,0)); o=bpy.context.active_object; o.data.materials.append(rebar)
    for y in [i*0.25+0.12 for i in range(10)]:
        cyl('rv',xr,y,2.2,2.32,0.013,rebar,10)
    for y in [i*0.25+0.12 for i in range(10)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=0.013,depth=0.03,location=(xr,y,-0.012),rotation=(0,0,0))
        bpy.data.objects.remove(bpy.context.active_object)
# vertical membrane + boards exploded outward (-X)
box('memb_v',-0.03-g,-0.005-g,0,D,-0.5,2.15,memb)
box('memb_l',-0.03-g,0.0,0,D,-0.52,-0.50,memb)
box('prot',-0.06-2*g,-0.035-2*g,0,D,-0.5,2.1,prot)
dr=box('drain',-0.10-3*g,-0.07-3*g,0,D,-0.5,2.05,drain)
# soil block + paving on top
box('soil',-1.6-3*g,-0.12-3*g,0,D,-0.15,2.05,soil); box('soil_lo',-1.6-3*g,-1.0-3*g,0,D,-0.52,-0.15,soil)
for i,y0 in enumerate([0,0.82,1.64]):
    box(f'pave{i}',-1.6-3*g,-0.12-3*g,y0+0.01,y0+0.8,2.05,2.12,pave)
# gravel + perforated pipe at footing, carve region: place in front niche
random.seed(4)
for i in range(260):
    x=random.uniform(-0.95,-0.15)-3*g; y=random.uniform(0,D); z=random.uniform(-0.5,-0.18)
    if x>-0.12-3*g: continue
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=random.uniform(0.025,0.045),location=(x,y,z)); o=bpy.context.active_object; o.data.materials.append(gravel)
box('soil_cut',-1.0-3*g,-0.12-3*g,-0.001,D+0.001,-0.52,-0.15,mat('void',(0,0,0),1.0))
bpy.data.objects.remove(bpy.data.objects['soil_cut'])
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=0.08,depth=D,location=(-0.55-3*g,D/2,-0.4),rotation=(math.pi/2,0,0)); o=bpy.context.active_object; o.data.materials.append(pipe)
# interior: insulation (2 boards), air gap, finish, floor topping
box('ins1',0.40+g,0.50+g,0,D,0.0,1.08,ins); box('ins2',0.40+g,0.50+g,0,D,1.1,2.15,ins)
box('fin',0.56+2*g,0.585+2*g,0,D,0.06,2.1,fin)
box('topping',0.40,3.2,0.004,D,0.0,0.07,mat('top',(0.82,0.81,0.79),0.4))
world_color((0.93,0.91,0.88),0.7)
area('key',(3.5,-3.5,4.5),5,380,(1,0.97,0.92),rot=(math.radians(50),0,math.radians(40)))
area('fill',(-4,-2,3),4,120,(0.95,0.97,1.0),rot=(math.radians(60),0,math.radians(-60)))
sun(160,50,1.5)
camera((3.4,-4.6,3.6),target=(-0.2,1.0,0.5),lens=40)
render(OUTDIR+'/wall_layers.png',2200,1600,64)
