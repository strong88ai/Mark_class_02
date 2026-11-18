import bpy, bmesh, math, random
from mathutils import Vector
OUTDIR='/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender'
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'
    try:
        sc.cycles.use_denoising=True; sc.cycles.denoiser='OPENIMAGEDENOISE'
    except Exception as e: print('denoise',e)
    sc.view_settings.view_transform='AgX'
    return sc
_M={}
def mat(name,color,rough=0.6,metal=0.0,transmission=0.0,ior=1.45,emit=None,emit_str=0.0,noise_bump=0.0,noise_scale=20,wood=False,alpha=1.0,coat=0.0,tex_mix=None):
    key=name
    if key in _M: return _M[key]
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*color,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    b.inputs['IOR'].default_value=ior
    try: b.inputs['Transmission Weight'].default_value=transmission
    except: b.inputs['Transmission'].default_value=transmission
    if coat:
        try: b.inputs['Coat Weight'].default_value=coat
        except: pass
    if emit:
        b.inputs['Emission Color'].default_value=(*emit,1); b.inputs['Emission Strength'].default_value=emit_str
    if wood:
        w=nt.nodes.new('ShaderNodeTexWave'); w.wave_type='BANDS'; w.bands_direction='X'; w.inputs['Scale'].default_value=WOODSCALE; w.inputs['Distortion'].default_value=WOODDIST; w.inputs['Detail'].default_value=3
        tc=nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'],w.inputs['Vector'])
        cr=nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color=(*[c*0.75 for c in color],1); cr.color_ramp.elements[1].color=(*color,1)
        nt.links.new(w.outputs['Fac'],cr.inputs['Fac']); nt.links.new(cr.outputs['Color'],b.inputs['Base Color'])
    if tex_mix:
        n=nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value=noise_scale; n.inputs['Detail'].default_value=8
        tc=nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'],n.inputs['Vector'])
        cr=nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color=(*tex_mix,1); cr.color_ramp.elements[1].color=(*color,1)
        nt.links.new(n.outputs['Fac'],cr.inputs['Fac']); nt.links.new(cr.outputs['Color'],b.inputs['Base Color'])
    if noise_bump:
        n=nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value=noise_scale; n.inputs['Detail'].default_value=10
        tc=nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'],n.inputs['Vector'])
        bp=nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value=noise_bump
        nt.links.new(n.outputs['Fac'],bp.inputs['Height']); nt.links.new(bp.outputs['Normal'],b.inputs['Normal'])
    _M[key]=m; return m
def mesh_obj(name,verts,faces,material,coll=None):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); (coll or bpy.context.scene.collection).objects.link(ob)
    if material: ob.data.materials.append(material)
    return ob
CLIPX=None
WOODSCALE=6; WOODDIST=6
def box(name,x0,x1,y0,y1,z0,z1,material,cap=None):
    if CLIPX is not None:
        if x1<=CLIPX: return None
        if x0<CLIPX:
            x0=CLIPX
            if cap is not None: mesh_obj(name+'_cap',[(CLIPX-0.002,y0,z0),(CLIPX-0.002,y1,z0),(CLIPX-0.002,y1,z1),(CLIPX-0.002,y0,z1)],[(0,1,2,3)],cap)
    v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return mesh_obj(name,v,f,material)
def clip_poly(poly,xc):
    out=[]; n=len(poly)
    for i in range(n):
        a=poly[i]; b=poly[(i+1)%n]; ain=a[0]>=xc; bin_=b[0]>=xc
        if ain: out.append(a)
        if ain!=bin_:
            t=(xc-a[0])/(b[0]-a[0]); out.append((xc,a[1]+t*(b[1]-a[1])))
    return out
def prism(name,poly,z0,z1,material,cap=None):
    p=poly
    if CLIPX is not None:
        p=clip_poly(poly,CLIPX)
        if len(p)<3: return None
    # ensure CCW
    area=sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))
    if area<0: p=p[::-1]
    n=len(p); v=[(x,y,z0) for x,y in p]+[(x,y,z1) for x,y in p]
    f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
    ob=mesh_obj(name,v,f,material)
    me=ob.data; bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.triangulate(bm,faces=[fa for fa in bm.faces if len(fa.verts)>4]); bm.to_mesh(me); bm.free()
    if cap is not None and CLIPX is not None:
        for fa in me.polygons:
            if all(abs(me.vertices[i].co.x-CLIPX)<1e-6 for i in fa.vertices): pass
    return ob
def cyl(name,x,y,z0,z1,r,material,vert=16):
    if CLIPX is not None and x<CLIPX: return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=vert,radius=r,depth=z1-z0,location=(x,y,(z0+z1)/2)); ob=bpy.context.active_object; ob.name=name; ob.data.materials.append(material); return ob
def rock_bases(n=6,seed=3):
    random.seed(seed); bases=[]
    for i in range(n):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1); ob=bpy.context.active_object
        for v in ob.data.vertices: v.co*=0.75+random.random()*0.45
        ob.scale=(1.0+random.random()*0.5,0.8+random.random()*0.4,0.55+random.random()*0.3)
        bpy.ops.object.transform_apply(scale=True)
        bpy.ops.object.shade_flat(); bases.append(ob.data); bpy.data.objects.remove(ob)
    return bases
def place_rocks(bases,material,xr,yr,zf,count,smin=0.6,smax=1.6,seed=5):
    random.seed(seed); coll=bpy.context.scene.collection
    for i in range(count):
        x=random.uniform(*xr); y=random.uniform(*yr)
        if CLIPX is not None and x<CLIPX+0.8: continue
        me=random.choice(bases); ob=bpy.data.objects.new('rock',me); coll.objects.link(ob)
        s=random.uniform(smin,smax); ob.scale=(s,s,s); ob.location=(x,y,zf(y)+random.uniform(-0.3,0.2))
        ob.rotation_euler=(random.random()*0.6,random.random()*0.6,random.random()*6.28)
        if not me.materials: me.materials.append(material)
def sun(direction_deg_az,elev,strength=3.0,color=(1,0.95,0.88),angle=2.0):
    ld=bpy.data.lights.new('sun','SUN'); ld.energy=strength; ld.color=color; ld.angle=math.radians(angle)
    ob=bpy.data.objects.new('sun',ld); bpy.context.scene.collection.objects.link(ob)
    az=math.radians(direction_deg_az); el=math.radians(elev)
    d=Vector((math.sin(az)*math.cos(el),math.cos(az)*math.cos(el),math.sin(el)))  # direction TO sun (az from north, clockwise)
    ob.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler(); return ob
def area(name,loc,size,energy,color=(1,0.85,0.65),rot=(0,0,0)):
    ld=bpy.data.lights.new(name,'AREA'); ld.energy=energy; ld.size=size; ld.color=color
    ob=bpy.data.objects.new(name,ld); ob.location=loc; ob.rotation_euler=rot; bpy.context.scene.collection.objects.link(ob); return ob
def world_color(c,strength=1.0):
    w=bpy.data.worlds.new('w'); bpy.context.scene.world=w; w.use_nodes=True
    w.node_tree.nodes['Background'].inputs['Color'].default_value=(*c,1); w.node_tree.nodes['Background'].inputs['Strength'].default_value=strength
def camera(loc,target=None,rot=None,ortho=None,lens=35):
    cd=bpy.data.cameras.new('cam'); ob=bpy.data.objects.new('cam',cd); bpy.context.scene.collection.objects.link(ob); bpy.context.scene.camera=ob
    ob.location=loc
    if ortho: cd.type='ORTHO'; cd.ortho_scale=ortho
    else: cd.lens=lens
    if target is not None: ob.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler()
    if rot: ob.rotation_euler=[math.radians(a) for a in rot]
    cd.clip_end=2000; return ob
def render(path,w,h,samples=48):
    sc=bpy.context.scene; sc.render.resolution_x=w; sc.render.resolution_y=h; sc.cycles.samples=samples
    sc.cycles.max_bounces=12; sc.cycles.transmission_bounces=12; sc.cycles.glossy_bounces=8; sc.cycles.transparent_max_bounces=12
    sc.render.filepath=path; sc.render.image_settings.file_format='PNG'; bpy.ops.render.render(write_still=True)
