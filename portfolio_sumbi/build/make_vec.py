import math, io, os, numpy as np
from fontTools.ttLib import TTFont as FTFont
from fontTools.pens.basePen import BasePen
from PIL import Image, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
S='/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad'
IMG=S.replace('/scratchpad','/images'); FD=S+'/fonts/package/dist/public/static/alternative/'
OUT='/home/user/Mark_class_02/portfolio_sumbi'
PLANS=S+'/plans'
WATERC=(170,205,222)
for w in ['Light','Regular','Medium','SemiBold','Bold']: pdfmetrics.registerFont(TTFont('Pretendard-'+w,FD+f'Pretendard-{w}.ttf'))
W,H=420.,297.                       # layout space (mm), scaled to A4
PW,PH=landscape(A4); K=PW/(W*72/25.4)
FS=1.2*25.4/72                       # pt -> mm with A4 readability boost
def hexc(c): return tuple(v/255 for v in c)
BG=(242,238,232); INK=(38,38,38); SUB=(110,106,100); LINE=(190,184,176)
BASALT=(43,43,43); SONGI=(122,74,58); SEA=(94,116,128); SAND=(232,225,214); GOLD=(200,140,40); RED=(170,60,50); BLUE=(60,110,170)
OUTLINE=os.environ.get('OUTLINE')=='1'
c=canvas.Canvas(os.environ['OUTPDF'],pagesize=(PW,PH)); c.setTitle('SUMBI Portfolio'); c.setAuthor('')
def Y(y): return H-y
_FT={}
class RLPen(BasePen):
    def __init__(s,gs,path,ox,oy,k): super().__init__(gs); s.p=path; s.ox,s.oy,s.k=ox,oy,k
    def T(s,pt): return s.ox+pt[0]*s.k, s.oy+pt[1]*s.k
    def _moveTo(s,pt): s.p.moveTo(*s.T(pt))
    def _lineTo(s,pt): s.p.lineTo(*s.T(pt))
    def _curveToOne(s,a,b,c_): s.p.curveTo(*s.T(a),*s.T(b),*s.T(c_))
    def _closePath(s): s.p.close()
def outline_text(fname,sz,x,y,st):
    if fname not in _FT:
        f=FTFont(FD+fname+'.ttf'); _FT[fname]=(f,f.getGlyphSet(),f.getBestCmap(),f['hmtx'],f['head'].unitsPerEm)
    f,gs,cm,hm,upm=_FT[fname]; k=sz/upm; path=c.beginPath()
    for ch in st:
        g=cm.get(ord(ch)) or cm.get(32)
        gs[g].draw(RLPen(gs,path,x,y,k)); x+=hm[g][0]*k
    c.drawPath(path,stroke=0,fill=1,fillMode=1)
PG=[0]
def begin():
    PG[0]+=1; c.saveState(); c.scale(K*72/25.4,K*72/25.4)
    c.setFillColorRGB(*hexc(BG)); c.rect(0,0,W,H,stroke=0,fill=1)
def end(): c.restoreState(); c.showPage()
def fnt(w,s): return ('Pretendard-'+w, s*FS)
def text(x,y,s,w='Regular',size=10,fill=INK,anchor='la'):
    f,sz=fnt(w,size); c.setFont(f,sz); c.setFillColorRGB(*hexc(fill))
    h,v=anchor[0],anchor[1]
    by={'a':y+sz*0.82,'m':y+sz*0.36,'s':y}[v]
    tw=pdfmetrics.stringWidth(s,f,sz); bx={'l':x,'m':x-tw/2,'r':x-tw}[h]
    if OUTLINE: outline_text(f,sz,bx,Y(by),s)
    else: c.drawString(bx,Y(by),s)
def wrap(x,y,t,w='Regular',size=10,width=100,fill=INK,lh=1.65,right=False):
    f,sz=fnt(w,size)
    for para in t.split('\n'):
        line='';lines=[]
        for wd in para.split(' '):
            tt=(line+' '+wd).strip()
            if pdfmetrics.stringWidth(tt,f,sz)>width and line: lines.append(line); line=wd
            else: line=tt
        lines.append(line)
        for l in lines: text(x,y,l,w,size,fill,'ra' if right else 'la'); y+=sz*lh
    return y
def rect(x0,y0,x1,y1,fill=None,stroke=None,lw=0.5,r=0):
    if fill: c.setFillColorRGB(*hexc(fill))
    if stroke: c.setStrokeColorRGB(*hexc(stroke)); c.setLineWidth(lw)
    if r: c.roundRect(x0,Y(y1),x1-x0,y1-y0,r,stroke=1 if stroke else 0,fill=1 if fill else 0)
    else: c.rect(x0,Y(y1),x1-x0,y1-y0,stroke=1 if stroke else 0,fill=1 if fill else 0)
def line(pts,col=INK,lw=0.5,dash=None):
    c.setStrokeColorRGB(*hexc(col)); c.setLineWidth(lw); c.setDash(*(dash or ([],0)))
    p=c.beginPath(); p.moveTo(pts[0][0],Y(pts[0][1]))
    for x,y in pts[1:]: p.lineTo(x,Y(y))
    c.drawPath(p,stroke=1,fill=0); c.setDash([],0)
def poly(pts,fill):
    c.setFillColorRGB(*hexc(fill)); p=c.beginPath(); p.moveTo(pts[0][0],Y(pts[0][1]))
    for x,y in pts[1:]: p.lineTo(x,Y(y))
    p.close(); c.drawPath(p,stroke=0,fill=1)
def circ(x,y,r,fill,stroke=None,lw=0.4):
    c.setFillColorRGB(*hexc(fill))
    if stroke: c.setStrokeColorRGB(*hexc(stroke)); c.setLineWidth(lw)
    c.circle(x,Y(y),r,stroke=1 if stroke else 0,fill=1)
def arrow(p1,p2,col,lw=0.8,head=3.5):
    line([p1,p2],col,lw); a=math.atan2(p2[1]-p1[1],p2[0]-p1[0])
    poly([p2,(p2[0]-head*math.cos(a-0.4),p2[1]-head*math.sin(a-0.4)),(p2[0]-head*math.cos(a+0.4),p2[1]-head*math.sin(a+0.4))],col)
def img(pil,x,y,w,h):
    buf=io.BytesIO(); 
    if pil.mode=='RGBA': pil.save(buf,'PNG'); 
    else: pil.save(buf,'JPEG',quality=92)
    buf.seek(0); c.drawImage(ImageReader(buf),x,Y(y+h),w,h,mask='auto' if pil.mode=='RGBA' else None)
def header(no,title):
    text(15,12,'02','Light',30); text(31,13,'Residence','Light',9,SUB); text(31,18,'숨비 SUMBI','SemiBold',10)
    text(W-15,14,title,'Medium',10,INK,'ra'); line([(15,28),(W-15,28)],LINE,0.4)
    text(W-15,H-10,str(PG[0]),'Regular',8,SUB,'rs')
def tag(x,y,t='가정값 · 도면 수령 후 교체'):
    f,sz=fnt('Medium',7.5); tw=pdfmetrics.stringWidth(t,f,sz)
    rect(x,y,x+tw+6,y+6.5,fill=SONGI,r=3); text(x+3,y+3.25,t,'Medium',7.5,(255,255,255),'lm')
def north(x,y,label=True):
    poly([(x,y-8),(x-3.5,y+4),(x,y+1),(x+3.5,y+4)],INK); text(x,y-10,'N','SemiBold',9,INK,'ms')
    if label: text(x+8,y,'↓ 바다 (남측)','Medium',8.5,SEA,'lm')
SENT=(1,2,3)
SEEDS={1:[(750,1040),(1465,430)],4:[(480,620),(1480,640)]}
def _flood(n):
    from PIL import ImageDraw
    im=Image.open(f'{IMG}/{n}.jpg').convert('RGB'); w,h=im.size
    for pt in [(2,2),(w-3,2),(2,h-3),(w-3,h-3)]+SEEDS.get(n,[]):
        if im.getpixel(pt)!=SENT: ImageDraw.floodfill(im,pt,SENT,thresh=26)
    a=np.asarray(im).copy(); m=(a==SENT).all(2)
    # remove 1px halo next to background
    from PIL import ImageFilter as IF
    mm=np.asarray(Image.fromarray((m*255).astype('uint8')).filter(IF.MaxFilter(3)))>0
    return a,mm
def load(n,bgfix=True):
    if not bgfix: return Image.open(f'{IMG}/{n}.jpg').convert('RGB')
    a,m=_flood(n); a[m]=BG; return Image.fromarray(a)
def alpha_cut(n):
    a,m=_flood(n); r=Image.fromarray(np.dstack([a,np.where(m,0,255).astype('uint8')]),'RGBA'); return r.crop(r.getbbox())
def place(pil,x,y,bw,bh,align='l'):
    s=min(bw/pil.width,bh/pil.height); w,h=pil.width*s,pil.height*s
    if align=='r': x=x-w
    img(pil,x,y,w,h); return x,y,s
def marker(x,y,n,r=3.0):
    circ(x,y,r,BASALT,(255,255,255),0.5); text(x,y,str(n),'SemiBold',r*2.4,(255,255,255),'mm')

P1=[(720,360,'보조주방 · 팬트리'),(975,450,'주방 (아일랜드)'),(1195,450,'거실 · 다이닝'),(650,520,'계단실'),(825,440,'엘리베이터'),
    (770,650,'게스트룸'),(595,700,'화장실'),(1030,700,'테라스'),(1150,960,'마당'),(1395,1150,'가든 다이닝'),
    (1465,430,'외부 계단 (→ B1 출입구)'),(750,1040,'수영장 상부 오픈 (추정)'),(1355,540,'측면 출입문')]
P2=[(690,610,'계단실'),(860,540,'엘리베이터'),(1140,460,'거실'),(790,420,'침실'),(625,460,'화장실 1'),(1440,440,'드레스룸'),
    (1440,620,'화장실 2'),(630,780,'세탁실'),(810,1010,'안방'),(625,1020,'안방 화장실'),(1100,760,'곡선 테라스'),(1460,930,'오션 자쿠지')]
P3=[(560,340,'보일러 · 기계실'),(755,420,'엘리베이터'),(560,510,'계단실'),(515,660,'세탁실'),(515,830,'샤워실'),(700,700,'거실 (라운지)'),
    (945,400,'드레스룸'),(1185,400,'캠핑 창고'),(945,650,'현관'),(1330,700,'주차장 (4대)'),(1470,380,'외부 계단 · 출입구'),
    (680,1060,'수영장'),(970,1050,'화장실'),(1330,1050,'바이크 창고')]
CROP={1:(380,180,1700,1320),2:(380,180,1700,1320),3:(380,200,1660,1300)}

# 1 cover
begin()
place(load(4),5,(H-260)/2,260,260)
x=275; text(x,40,'Residence 02','Light',11,SUB); text(x,58,'숨비','SemiBold',64); text(x,96,'SUMBI','Light',20,SUB)
line([(x,118),(W-18,118)],INK,0.6)
wrap(x,126,"‘땅속에서 들어와 바다 위에서 숨을 내쉬는 집은 어떤 모습일까’\n에서 출발한 해안 단독주택 프로젝트입니다.",'Regular',11,128)
wrap(x,214,"Daepo-dong 2217, Seogwipo-si, Jeju, S.Korea\n지하 1층 · 지상 2층 단독주택\nB1 24,500 × 18,600 / 1F 21,200 × 18,600 / 2F 18,850 × 17,500\nModeling SketchUp · Drawing AutoCAD · Post-production Photoshop",'Regular',8.5,128,SUB)
end()

# 2 concept
begin(); header(2,'Concept')
text(15,40,'숨비소리','SemiBold',36)
wrap(15,64,"해녀가 깊은 물속에서 올라와 참았던 숨을 길게 내쉬는 소리.\n이 집은 그 한 번의 숨을 공간으로 옮겼습니다. 땅속(B1)에서 들어와 위로 오를수록 바다를 향해 열리고, 2층 자쿠지에서 비로소 숨이 트입니다.",'Regular',10.5,200)
cols=[('B1','깊음','Depth','잠수하듯 들어서는 층','주차장과 현관, 수영장, 바이크 · 캠핑 창고가 있는 땅속의 층. 집은 가장 깊은 곳에서 시작됩니다.',BASALT),
      ('1F','숨','Breath','수면 위, 함께 숨 쉬는 층','주방과 거실, 마당이 이어지는 가족 · 손님 · 반려동물의 층. 폴딩도어를 열면 실내와 마당, 바다가 하나로 이어집니다.',SAND),
      ('2F','쉼','Rest','바다 위에서 숨을 내쉬는 층','침실과 개인 거실, 곡선 테라스와 오션 자쿠지. 물에 몸을 담근 채 수평선을 마주하는 순간이 이 집의 숨비소리입니다.',SEA)]
cw=122
for i,(fl,k,e,t1,t2,col) in enumerate(cols):
    x=15+i*(cw+7); y=118
    rect(x,y,x+cw,y+8,fill=col); text(x,y+14,fl,'Light',12,SUB); text(x,y+22,k,'SemiBold',40); text(x+44 if len(k)==1 else x+62,y+38,e,'Light',12,SUB)
    text(x,y+60,t1,'SemiBold',10.5); wrap(x,y+70,t2,'Regular',9,cw-4,SUB)
line([(15,232),(W-15,232)],LINE,0.4)
text(15,240,'Client Persona','SemiBold',10)
wrap(70,240,"차와 바이크, 캠핑을 즐기고, 반려견 · 반려묘와 함께 살며, 손님 초대가 잦은 가족.  “집에 머무는 동안만은 효율이 아닌 취향과 쉼으로 채우고 싶다.”",'Regular',9.5,330,SUB)
end()

# 3 site
begin(); header(3,'Site Analysis'); tag(15,31,'배치 = 현장 모델 기준 · 해수면 높이 가정')
im_=Image.open('/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender/site_axo.png').convert('RGB'); img(im_,15,36,205,205)
def lab(x,y,t,col=INK,size=7.5,w='Medium'):
    f_,sz_=fnt(w,size); tw_=pdfmetrics.stringWidth(t,f_,sz_)
    rect(x-1.5,y-3,x+tw_+1.5,y+3,fill=(255,255,255) if col!=(255,255,255) else SEA,r=1.5); text(x,y,t,w,size,col,'lm')
for (x,y,t) in [(28,84,'주택단지'),(58,112,'해안도로'),(22,176,'야자수 광장 · 산책로'),(92,129,'숨비'),(128,119,'오션 자쿠지'),(165,95,'이웃 곡면 건물'),(64,190,'바위 호안')]: lab(x,y,t)
lab(140,214,'바다 · 남측',(255,255,255),8)
cx_,cy_=205,58; dx_,dy_=-0.82,-0.57
arrow((cx_,cy_),(cx_+dx_*12,cy_+dy_*12),INK,0.8,3); text(cx_+dx_*15,cy_+dy_*15,'N','SemiBold',9,INK,'mm')
text(15,246,'※ 현장 배치 기준 3D 모델 렌더 (Blender) · 주변 건물은 단순화','Regular',7,SUB)
x=240; y=45; text(x,y,'대지 조건','SemiBold',13); y+=11
for k,v in [('위치','제주 서귀포시 대포동 2217 (중문 · 주상절리대 인근 해안)'),('배치','바다 → 바위 호안 → 대지 → 야자수 광장 → 해안도로 → 주택단지'),
      ('향','남향 · 바다 조망 (현장 모델 그림자 방향 기준)'),('지형','도로 · 광장 레벨 평탄, 바다 쪽 바위 호안에서 해수면으로 높이차'),
      ('진입','보행 = 광장 진입로 → 외부 계단 → B1 출입구 · 현관 / 차량 = B1 주차장'),('기후','여름 남풍 · 태풍, 겨울 북서 계절풍, 높은 습도와 염분')]:
    text(x,y,k,'SemiBold',9); y=wrap(x+20,y,v,'Regular',9,145,SUB)+1.5
y+=5; text(x,y,'설계 대응','SemiBold',13); y+=11
for t in ['도로 · 광장 쪽은 닫고 바다 쪽으로만 연다 → 지나가는 시선 차단','B1은 땅에 묻어 주차 · 수영장 · 창고 등 몰입 공간으로','1F 마당, 2F 테라스 · 자쿠지 → 층마다 바다를 향한 외부공간','태풍 · 월파 대비: 호안 쪽 개구부 레벨 상향, B1 차수 · 집수정','염해 대응 창호 (알루미늄 불소도장) · 외부 금속 최소화']:
    y=wrap(x,y,'—  '+t,'Regular',9,165)+1
y+=5; text(x,y,'법규 확인 항목','SemiBold',13); y+=11
for t in ['토지이음 용도지역 · 국가유산(천연기념물) 보호구역 · 절대보전지역','지하층 인정 여부 (B1 지표면 노출 높이)','거실 채광 1/10 · 환기 1/20 (건축법 시행령)']:
    y=wrap(x,y,'□  '+t,'Regular',9,165,SUB)+1
end()

# 4 section
begin(); header(4,'Site Section  N — S'); tag(15,31,'평면 치수 = 도면 · 층고 · 해수면 = 가정값')
im_=Image.open('/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender/section.png').convert('RGB'); img(im_,15,40,390,175.5)
def P(Y,z): return (210+(3-Y)*8.478, 127.75-(z-0.5)*8.478)
def lab(x,y,t,col=INK,size=7.5,w='Medium',bg=(255,255,255)):
    f_,sz_=fnt(w,size); tw_=pdfmetrics.stringWidth(t,f_,sz_)
    if bg: rect(x-1.5,y-3,x+tw_+1.5,y+3,fill=bg,r=1.5)
    text(x,y,t,w,size,col,'lm')
for Y_,z_,t in [(18.3,6.6,'2F  쉼'),(18.3,3.0,'1F  숨'),(18.3,-0.7,'B1  깊음')]:
    x_,y_=P(Y_,z_); lab(x_,y_,t,INK,10,'SemiBold',None)
for Y_,z_,t in [(16.5,4.1,'거실 · 드레스룸'),(17.2,0.5,'주방 · 거실'),(9.8,0.5,'테라스'),(4.5,0.5,'마당'),(17.5,-3.7,'캠핑 창고'),(9.6,-3.7,'주차장'),(4.2,-3.7,'바이크 창고'),(9.4,4.3,'곡선 테라스'),(8.6,2.0,'오션 자쿠지')]:
    x_,y_=P(Y_,z_); lab(x_,y_,t,INK,7)
for z_,t in [(7.2,'FL +7.2'),(3.6,'FL +3.6'),(0,'FL ±0'),(-4.2,'FL −4.2')]:
    x_,y_=P(19.0,z_); text(x_-1,y_,t,'Regular',7,SUB,'rm')
x_,y_=P(27,0.9); lab(x_,y_,'해안도로 · 광장')
x_,y_=P(-2.0,1.2); lab(x_,y_,'바위 호안')
x_,y_=P(-13,-5.5); text(x_,y_,'바다 (해수면, 가정)','Medium',9,(255,255,255),'mm')
for z_ in (5.4,1.9):
    a_=P(0.0,z_); b_=P(-17,z_); arrow(a_,b_,SONGI,0.7,3)
x_,y_=P(-17,5.4); text(x_,y_-3,'수평선 조망','SemiBold',8,SONGI,'ra')
x_,y_=P(15,-5.3); text(x_,y_+2,'B1 바닥 < 해수면 (가정) → 외방수 · 차수 · 집수정 필수 (Detail 01)','Medium',7.5,RED)
text(15,222,'단면 위치: 동측 X = 17m 지점 (B1 캠핑 창고 · 주차장 · 바이크 창고 / 1F 주방 · 테라스 · 마당 / 2F 거실 · 테라스 · 자쿠지 통과) · 3D 모델 렌더 (Blender)','Regular',7,SUB)
wrap(W-15,36,"땅속(B1)에서 들어와 1층 마당과 2층 테라스로 오르며,\n층마다 남쪽 바다를 향해 한 번씩 숨을 내쉽니다.",'Regular',9.5,220,right=True)
text(15,H-14,'※ 깊이는 도면 치수 (B1 18,600 / 1F 실내 10,500 / 2F 실내 7,600 · 테라스 포함 16,000). 층고 B1 4.2m · 1F 3.6m · 2F 3.6m와 해수면 높이는 가정값입니다.','Regular',7,SUB)
end()

# 5 stack
begin(); header(5,'Vertical Layers')
def iso_from_top(n):
    a,m=_flood(n); r=Image.fromarray(np.dstack([a,np.where(m,0,255).astype('uint8')]),'RGBA')
    A=np.array([[930/1106,690/-1017],[565/1106,-615/-1017]]); inv=np.linalg.inv(A)
    W2,H2=2600,2000; off=np.array([700,-300])
    co=(inv[0,0],inv[0,1],-(inv[0,0]*off[0]+inv[0,1]*off[1]),inv[1,0],inv[1,1],-(inv[1,0]*off[0]+inv[1,1]*off[1]))
    t=r.transform((W2,H2),Image.AFFINE,co,resample=Image.BICUBIC); return t.crop(t.getbbox())
def shadowed(r):
    pad=50; out=Image.new('RGBA',(r.width+pad*2,r.height+pad*2),(0,0,0,0))
    al=Image.new('L',out.size,0); al.paste(r.getchannel('A').point(lambda v:int(v*0.25)),(pad+10,pad+16))
    sh=Image.new('RGBA',out.size,(90,80,70,0)); sh.putalpha(al.filter(ImageFilter.GaussianBlur(18)))
    out=Image.alpha_composite(out,sh); out.alpha_composite(r,(pad,pad)); return out
k=0.085
layers=[(iso_from_top(3),'B1  깊음','현관 · 주차장 · 수영장 · 바이크 · 캠핑 창고',232),(alpha_cut(4),'1F  숨','주방 · 거실 · 게스트룸 · 테라스 · 마당',158),(alpha_cut(5),'2F  쉼','침실 · 안방 · 거실 · 곡선 테라스 · 오션 자쿠지',88)]
for r,t1,t2,cy in layers:
    a=shadowed(r); w,h=a.width*k,a.height*k; img(a,125-w/2,cy-h/2,w,h)
    line([(125+w/2-25,cy),(255,cy)],LINE,0.4); text(260,cy-7,t1,'SemiBold',15); text(260,cy+4,t2,'Regular',9,SUB)
wrap(260,36,"B1에서 들어와 → 1F에서 모이고 → 2F에서 바다를 향해 숨을 내쉰다.\n아래는 깊고 고요하게, 위로 오를수록 바다를 향해 열립니다.",'Regular',10,145)
text(15,H-14,'※ B1은 아이소메트릭 렌더 수령 전까지 평면 렌더를 같은 각도로 변환한 임시 이미지입니다.','Regular',7.5,SUB)
end()

# 6-8 zoning
PLAN={'B1':'B1_','1F':'1_','2F':'2_'}
def zoning(fl,title,n,pts,t,dims,iso=None):
    begin(); header(0,title)
    cx0,cy0,cx1,cy1=CROP[n]; ox,oy,s=place(load(n).crop(CROP[n]),12,33,235,245)
    for i,(x,y,_) in enumerate(pts,1): marker(ox+(x-cx0)*s,oy+(y-cy0)*s,i,3.4)
    x=260; y=40
    if iso: _,_,si=place(load(iso).crop((150,0,1900,1450)),W-15,y,145,90,'r'); y+=1450*si+6
    text(x,y,'Zoning Plan','SemiBold',14); text(W-15,y+1,dims,'Regular',8.5,SUB,'ra'); y+=11
    y=wrap(x,y,t,'Regular',8.8,145,SUB)+5
    for i,(_,_,nm) in enumerate(pts):
        lx=x+3+(i//7)*72; ly=y+(i%7)*8; circ(lx,ly,2.6,BASALT); text(lx,ly,str(i+1),'SemiBold',6.5,(255,255,255),'mm'); text(lx+5,ly,nm,'Regular',9,INK,'lm')
    north(30,H-30); end()
    begin(); header(0,fl+'  Floor Plan')
    pl=Image.open(f'{PLANS}/{PLAN[fl]}.png').convert('RGB')
    a=np.asarray(pl).astype(int); a[(a>235).all(2)]=BG; pl=Image.fromarray(a.astype('uint8'))
    place(pl,(W-300)/2,34,300,240)
    text(15,H-14,'S = N.S. · 단위 mm · AutoCAD 도면','Regular',7.5,SUB); north(W-30,H-30,False); end()
zoning('B1','B1  깊음 · Depth',3,P3,"집은 가장 깊은 곳에서 시작됩니다. 외부 계단으로 내려와 현관에 들어서면 주차장과 거실(라운지), 수영장이 이어지고, 바이크 · 캠핑 창고가 취미의 층을 완성합니다. 주차장은 방화구획과 기계 배기로 생활공간과 분리합니다.",'24,500 × 18,600')
zoning('1F','1F  숨 · Breath',1,P1,"계단을 올라 1층에 서면 주방과 거실을 지나 폴딩도어 너머 테라스와 마당, 그리고 바다가 한 번에 열립니다. 가족 · 손님 · 반려동물이 모이는 환대의 층입니다.",'21,200 × 18,600',4)
zoning('2F','2F  쉼 · Rest',2,P2,"침실과 안방, 개인 거실을 모은 사적인 층. 바다 쪽으로 열린 곡선 테라스 끝의 오션 자쿠지는 몸을 물에 담근 채 수평선을 마주하는, 이 집의 숨비소리 같은 순간입니다.",'18,850 × 17,500',5)
begin(); header(0,'RF  Roof Plan')
pl=Image.open(f'{PLANS}/d___real.png').convert('RGB'); a_=np.asarray(pl).astype(int); a_[(a_>235).all(2)]=BG; pl=Image.fromarray(a_.astype('uint8'))
place(pl,(W-280)/2,36,280,225)
text(15,H-14,'옥상 · 계단실 · EV 코어 / 18,850 × 16,000 · 단위 mm · AutoCAD 도면','Regular',7.5,SUB); north(W-30,H-30,False); end()

# 9 material
begin(); header(9,'Material Board')
rng=np.random.default_rng(7)
def noise(h,w,s): return np.asarray(Image.fromarray((rng.random((h//s+2,w//s+2))*255).astype('uint8')).resize((w,h),Image.BICUBIC))/255.
def tex(kind,w,h):
    if kind=='basalt':
        b=0.17+0.08*noise(h,w,6)+0.05*rng.random((h,w)); a=np.stack([b,b,b*1.02],2)
        for _ in range(int(w*h/900)):
            x,y=rng.integers(0,w),rng.integers(0,h); r=rng.integers(2,7); a[max(0,y-r):y+r,max(0,x-r):x+r]*=0.45
    elif kind=='songi': g=noise(h,w,3)*0.6+0.4*rng.random((h,w)); a=np.stack([0.38+0.25*g,0.20+0.14*g,0.15+0.1*g],2)
    elif kind=='lime': g=0.9+0.05*noise(h,w,40)+0.02*noise(h,w,6); a=np.stack([g,g*0.975,g*0.94],2)
    elif kind=='oak':
        yy=np.arange(h)[:,None]; g=0.5+0.5*np.sin(yy/7+noise(h,w,25)*8); g=0.75+0.08*g+0.04*rng.random((h,w)); a=np.stack([g,g*0.86,g*0.68],2)
        for k in range(0,h,h//6): a[k:k+2,:]*=0.85
    elif kind=='concrete': g=0.6+0.07*noise(h,w,30)+0.05*rng.random((h,w)); a=np.stack([g,g,g*0.98],2)
    else:
        g=0.88+0.03*rng.random((h,w)); a=np.stack([g,g*0.97,g*0.93],2)
        for _ in range(int(w*h/500)):
            x,y=rng.integers(0,w),rng.integers(0,h); r=rng.integers(2,9); a[max(0,y-r):y+r,max(0,x-r):x+r]=[(0.48,0.29,0.23),(0.2,0.2,0.2),(0.6,0.58,0.55)][rng.integers(0,3)]
    return Image.fromarray((np.clip(a,0,1)*255).astype('uint8'))
mats=[('basalt','현무암 판석 (버너 마감)','테라스 · 외부 바닥 · 욕실 벽','회색 대리석 타일'),('songi','화산송이','조경 · 포인트 벽 · 화분','단색 잔디 경계'),
      ('lime','라임 플라스터','내벽 · 외벽','베이지 타일 외벽'),('oak','화이트오크 원목마루','1F · 2F 바닥','회색 우드 (전 층 동일)'),
      ('concrete','폴리싱 콘크리트','B1 주차장 · 거실 바닥','패턴 석재 차고'),('terrazzo','테라조 (송이 골재)','욕실 · 파우더룸','회색 욕실 타일 (전 층)')]
tw,th=118,78
for i,(k,n1,n2,n3) in enumerate(mats):
    x=15+(i%3)*(tw+12); y=38+(i//3)*(th+42)
    img(tex(k,990,654),x,y,tw,th); text(x,y+th+4,n1,'SemiBold',10); text(x,y+th+12,n2,'Regular',8.5,SUB); text(x,y+th+20,n3+' → 교체','Regular',7.5,SONGI)
for i,(col,nm) in enumerate([(BASALT,'#2B2B2B 현무암'),(SONGI,'#7A4A3A 송이'),(SEA,'#5E7480 바다'),(SAND,'#E8E1D6 모래')]):
    x=15+i*62; rect(x,272,x+12,282,fill=col); text(x+15,277,nm,'Regular',8.5,INK,'lm')
text(W-15,277,'※ 텍스처는 생성한 예시입니다 (실제 자재 사진 아님) · 실제 자재 사진/품번으로 교체','Regular',7,SUB,'rm')
end()

# ---------- detail helpers
CONC=(205,202,197); EARTH=(196,178,150); WP=(40,100,190); INS=(240,226,160); WATER=(170,205,222); DECK=(176,128,82); TILE=(70,70,70)
def hatch(x0,y0,x1,y1,kind,fill,col=(120,110,100)):
    rect(x0,y0,x1,y1,fill=fill); c.saveState(); p=c.beginPath(); p.rect(x0,Y(y1),x1-x0,y1-y0); c.clipPath(p,stroke=0,fill=0)
    if kind=='earth':
        for k in range(-int(y1-y0),int(x1-x0),4): line([(x0+k,y1),(x0+k+(y1-y0),y0)],col,0.25)
    elif kind=='conc':
        rr=np.random.default_rng(int(x0*7+y0))
        for _ in range(int((x1-x0)*(y1-y0)/9)): circ(x0+rr.random()*(x1-x0),y0+rr.random()*(y1-y0),0.25,(140,136,130))
    elif kind=='ins':
        for k in range(0,int(y1-y0)+4,3): line([(x0,y0+k),(x1,y0+k+1.5)],(200,170,90),0.25)
    elif kind=='drain':
        for k in range(0,int(y1-y0),2): line([(x0,y0+k),(x1,y0+k+1)],(90,90,90),0.3)
    elif kind=='gravel':
        rr=np.random.default_rng(3)
        for _ in range(int((x1-x0)*(y1-y0)/6)): circ(x0+rr.random()*(x1-x0),y0+rr.random()*(y1-y0),0.6,(150,140,125))
    c.restoreState()
def notes(x,y,items,width=140):
    for i,(t,d_) in enumerate(items,1):
        marker(x+3,y+2.5,i,2.8); text(x+9,y,t,'SemiBold',9)
        y=wrap(x+9,y+5.5,d_,'Regular',8,width,SUB,1.5)+2.5
    return y
def site_check(x,y,title,items,width=140):
    rect(x,y,x+width+12,y+6+len(items)*10.5,fill=(232,226,218)); text(x+4,y+3,title,'SemiBold',9,SONGI)
    for i,t in enumerate(items): wrap(x+4,y+10+i*10.5,'□  '+t,'Regular',8,width,INK,1.4)

# ---------- Detail 01 basement wall
begin(); header(10,'Detail 01 · 지하 외벽 방수 (B1)')
text(15,34,'해안 지하 = 지하수 · 염분 · 결로. 하자 1순위인 지하 누수를 외방수 + 배수 + 내부 결로 방지의 3단 구조로 막습니다.','Regular',9,SUB)
im_=Image.open('/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender/wall_layers.png').convert('RGB'); img(im_,15,42,235,171)
for i,(dx_,dy_) in enumerate([(740,560),(790,640),(838,720),(930,800),(1075,520),(1300,560),(1300,1250),(1480,990),(650,1000),(560,1110)],1): marker(15+dx_*0.1175,42+dy_*0.1175,i,2.8)
text(15,218,'좌 = 흙 쪽(외부) → 우 = B1 실내 · 3D 모델 렌더 (Blender) · 철근은 콘크리트 내부 복배근(절단면에 표시)','Regular',7,SUB)
notes(262,42,[('배수판 (드레인보드)','흙 속 물을 아래로 흘려 방수층에 수압이 걸리지 않게 함'),
    ('보호판','되메우기 시 돌·장비로부터 방수층 보호'),
    ('외방수 복합시트 2겹','구조체 바깥에서 1차 차단. 바닥 → 벽까지 끊김 없이 감쌈'),
    ('수밀 콘크리트 400','방수제 혼입 · 시공이음에 지수판'),
    ('단열재 (XPS 50)','외기 · 지중 냉기 차단 → 실내 결로 방지'),
    ('띄움벽 + 마감','벽과 마감 사이 공기층 → 곰팡이 방지'),
    ('기초 매트 슬래브','하부 방수층 위 타설, 버림콘크리트 위'),
    ('바닥 누름 콘크리트 + 폴리싱 마감','바닥 방수층 보호, B1 주차장 · 거실'),
    ('ø100 유공관 + 자갈','벽 하단 물을 모아 집수정 → 배수펌프'),
    ('버림 콘크리트','지반 정리 · 하부 방수 바탕면')],140)
site_check(262,236,'현장 체크 (하자 포인트)',['방수층 겹침 100mm 이상 · 모서리 보강','시공이음 지수판 누락 확인','집수정 펌프 2대 (예비) · 정전 대비'],140)
text(15,H-14,'N.S. (Not to Scale) · 개념 디테일','Regular',7.5,SUB)
end()

# ---------- Detail 02 jacuzzi
begin(); header(11,'Detail 02 · 2F 오션 자쿠지 단면')
text(15,34,'수면이 바다 쪽 수평선과 이어지는 인피니티 엣지. 바로 아래가 1층 테라스 · 마당이라서 방수 · 하중 · 점검을 가장 먼저 해결합니다.','Regular',9,SUB)
im_=Image.open('/tmp/claude-0/-home-user-Mark-class-02/a822d4e8-ff77-57b7-bc84-1bfa881b1c64/scratchpad/blender/jacuzzi.png').convert('RGB'); img(im_,15,42,235,156.7)
text(15,204,'2F 테라스에서 본 오션 자쿠지 · 해 질 녘 · 3D 모델 렌더 (Blender)','Regular',7,SUB)
notes(262,42,[('우드 데크 (페데스탈 지지)','데크 아래로 배수 → 테라스 방수층 보호'),
    ('RC 수조 구조체','바닥을 낮춘 단차 슬래브. 만수 하중 약 0.9t/㎡ + 마감 → 구조 검토'),
    ('1차 방수 (구조체)','우레탄 도막 또는 시트. 수조 바닥 → 벽 → 테라스까지 연속'),
    ('수면 · 인피니티 엣지','해측 벽 상단을 수면 높이로 → 물이 넘쳐 수평선과 이어짐'),
    ('진입 계단 3단','미끄럼 방지 현무암 · 단높이 200 이하 · 손잡이'),
    ('2차 방수 + 현무암 타일','수조 안 마감 아래 한 번 더 방수 (이중 방수)'),
    ('오버플로우 거터','넘친 물을 받아 여과 · 재순환'),
    ('유리 난간 h1,200','추락 방지 · 바다 조망 유지'),
    ('바닥 배수구','청소 · 동절기 완전 배수'),
    ('설비 점검실','순환펌프 · 히터 · 여과기 (소음 · 진동 방진)'),
    ('하부 천장 점검구','배관 누수 확인 · 교체 동선'),
    ('누수 감지 센서','하부 천장 내 · 스마트폰 알림')],140)
site_check(262,255,'현장 체크 (하자 포인트)',['방수 후 48시간 담수 테스트 (2회)','바닥 배수 기울기 1/100 이상'],140)
text(15,H-14,'N.S. (Not to Scale) · 개념 디테일','Regular',7.5,SUB)
end()

# 10 scene plan
begin(); header(12,'Scene Plan · 추가 렌더 6컷')
shots=[(1,(1000,420),(1000,780),'1F 주방 → 폴딩도어 너머 마당 · 바다','환대'),(1,(1150,880),(1150,1240),'1F 마당 끝, 석양의 수평선','숨'),
       (2,(1150,430),(1110,800),'2F 거실 → 곡선 테라스','쉼'),(2,(1380,760),(1580,980),'2F 오션 자쿠지 → 수평선 (클라이맥스)','숨비소리'),
       (3,(680,980),(680,1230),'B1 수영장 → 상부에서 내려오는 빛','깊음'),(3,(700,700),(1060,700),'B1 거실 → 유리벽 너머 주차장 (야간)','갤러리')]
pw=124
for j,n in enumerate((1,2,3)):
    cx0,cy0,_,_=CROP[n]; x0=15+j*(pw+9); ox,oy,s=place(load(n).crop(CROP[n]),x0,36,pw,120)
    text(x0,36+(CROP[n][3]-cy0)*s+3,['1F','2F','B1'][j],'SemiBold',10)
    for i,(nn,cp,tp,_,_) in enumerate(shots,1):
        if nn!=n: continue
        X=ox+(cp[0]-cx0)*s; Yy=oy+(cp[1]-cy0)*s; a=math.atan2(tp[1]-cp[1],tp[0]-cp[0]); L_=17
        for sgn in (-0.45,0.45): line([(X,Yy),(X+L_*math.cos(a+sgn),Yy+L_*math.sin(a+sgn))],SONGI,0.7)
        circ(X,Yy,2.6,SONGI,(255,255,255),0.4); text(X,Yy,str(i),'Bold',6.5,(255,255,255),'mm')
for i,(_,_,_,t,k) in enumerate(shots,1):
    x=15+((i-1)%2)*195; yy=180+((i-1)//2)*16
    circ(x+3.5,yy+3.5,3.5,SONGI); text(x+3.5,yy+3.5,str(i),'Bold',8,(255,255,255),'mm')
    text(x+10,yy+3.5,t,'Regular',10,INK,'lm'); text(x+185,yy+3.5,k,'Medium',9,SONGI,'rm')
text(15,H-18,'카메라 높이 1,500mm · 화각 24~28mm · 주간 4컷 / 석양 1컷 / 야간 1컷 · A4 300dpi(3508×2480) 출력','Regular',8,SUB)
end()
c.save(); print('ok')
