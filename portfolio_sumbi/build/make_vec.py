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
def begin():
    c.saveState(); c.scale(K*72/25.4,K*72/25.4)
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
    text(W-15,H-10,str(no),'Regular',8,SUB,'rs')
def tag(x,y,t='가정값 · 도면 수령 후 교체'):
    f,sz=fnt('Medium',7.5); tw=pdfmetrics.stringWidth(t,f,sz)
    rect(x,y,x+tw+6,y+6.5,fill=SONGI,r=3); text(x+3,y+3.25,t,'Medium',7.5,(255,255,255),'lm')
def north(x,y,label=True):
    poly([(x,y-8),(x-3.5,y+4),(x,y+1),(x+3.5,y+4)],INK); text(x,y-10,'N','SemiBold',9,INK,'ms')
    if label: text(x+8,y,'↓ 바다 (남측)','Medium',8.5,SEA,'lm')
def load(n,bgfix=True):
    im=Image.open(f'{IMG}/{n}.jpg').convert('RGB')
    if bgfix:
        a=np.asarray(im).astype(int); m=np.abs(a-a[5,5]).sum(2)<22; a[m]=BG; im=Image.fromarray(a.astype('uint8'))
    return im
def alpha_cut(n):
    im=Image.open(f'{IMG}/{n}.jpg').convert('RGB'); a=np.asarray(im).astype(int)
    al=np.where(np.abs(a-a[5,5]).sum(2)<22,0,255).astype('uint8')
    r=Image.fromarray(np.dstack([a.astype('uint8'),al]),'RGBA'); return r.crop(r.getbbox())
def place(pil,x,y,bw,bh,align='l'):
    s=min(bw/pil.width,bh/pil.height); w,h=pil.width*s,pil.height*s
    if align=='r': x=x-w
    img(pil,x,y,w,h); return x,y,s
def marker(x,y,n,r=3.0):
    circ(x,y,r,BASALT,(255,255,255),0.5); text(x,y,str(n),'SemiBold',r*2.4,(255,255,255),'mm')

P1=[(720,360,'주방 · 팬트리'),(975,450,'아일랜드 키친'),(1195,450,'다이닝 (8인)'),(650,520,'계단'),(825,440,'엘리베이터'),
    (770,650,'게스트룸'),(595,700,'욕실'),(1030,700,'테라스 다이닝 (10인)'),(1150,960,'잔디마당 · 펫 가든'),(1395,1150,'가든 다이닝'),
    (1465,430,'채광 보이드'),(750,1040,'하부 오픈 (B1 상부)'),(1355,540,'현관 (동측 진입)')]
P2=[(690,610,'계단'),(860,540,'엘리베이터'),(1140,460,'거실'),(790,420,'침실 1 · 서재'),(625,460,'욕실 1'),(1440,440,'드레스룸'),
    (1440,620,'부부욕실'),(630,780,'세탁실'),(810,1010,'침실 2'),(625,1020,'욕실 2'),(1100,760,'곡선 테라스'),(1460,930,'오션 자쿠지')]
P3=[(560,340,'기계실'),(755,420,'엘리베이터'),(560,510,'계단'),(515,660,'바 · 키친'),(515,830,'샤워실'),(700,700,'패밀리 라운지'),
    (945,400,'다목적실'),(1185,400,'컬렉션룸'),(945,650,'파우더룸'),(1330,700,'차고 (4대)'),(1470,380,'차고 전용 계단'),
    (680,1060,'실내수영장'),(970,1050,'샤워 · 탈의'),(1330,1050,'바이크 갤러리')]
CROP={1:(380,180,1700,1320),2:(380,180,1700,1320),3:(380,200,1660,1300)}

# 1 cover
begin()
place(load(4),5,(H-260)/2,260,260)
x=275; text(x,40,'Residence 02','Light',11,SUB); text(x,58,'숨비','SemiBold',64); text(x,96,'SUMBI','Light',20,SUB)
line([(x,118),(W-18,118)],INK,0.6)
wrap(x,126,"‘바다 앞, 땅속에서 숨을 고르는 집은 어떤 모습일까’\n에서 출발한 해안 단독주택 프로젝트입니다.",'Regular',11,125)
wrap(x,222,"Daepo-dong 2217, Seogwipo-si, Jeju, S.Korea\n지상 1층 · 지하 2층 단독주택\nModeling SketchUp · Post-production Photoshop",'Regular',8.5,125,SUB)
end()

# 2 concept
begin(); header(2,'Concept')
text(15,40,'숨비소리','SemiBold',36)
wrap(15,64,"해녀가 깊은 물속에서 올라와 참았던 숨을 길게 내쉬는 소리.\n이 집은 그 한 번의 숨을 공간으로 옮겼습니다. 땅속으로 내려갈수록 고요해지고, 바다를 향해 열리는 순간 숨이 트입니다.",'Regular',10.5,200)
cols=[('1F','숨','Breath','수면 위, 함께 숨 쉬는 층','가족 · 손님 · 반려동물이 모이는 주방과 잔디마당. 폴딩도어를 열면 실내와 마당, 그리고 수평선이 하나로 이어집니다.',SAND),
      ('B1','쉼','Rest','숨을 고르는 층','침실과 거실을 모은 사적인 층. 남측으로 열린 곡선 테라스와 오션 자쿠지가 땅속에서도 바다를 끌어들입니다.',SEA),
      ('B2','깊음','Depth','깊이 잠기는 층','차와 바이크, 수영장이 있는 몰입의 층. 가장 깊은 곳에서 수면과 바다가 겹쳐 보이도록 남측 수평창을 계획합니다.',BASALT)]
cw=122
for i,(fl,k,e,t1,t2,col) in enumerate(cols):
    x=15+i*(cw+7); y=118
    rect(x,y,x+cw,y+8,fill=col); text(x,y+14,fl,'Light',12,SUB); text(x,y+22,k,'SemiBold',40); text(x+44,y+38,e,'Light',12,SUB)
    text(x,y+60,t1,'SemiBold',10.5); wrap(x,y+70,t2,'Regular',9,cw-4,SUB)
line([(15,232),(W-15,232)],LINE,0.4)
text(15,240,'Client Persona','SemiBold',10)
wrap(70,240,"차와 바이크를 모으고, 반려견·반려묘와 함께 살며, 손님 초대를 즐기는 4인 가족.  “집에 머무는 동안만은 효율이 아닌 취향과 쉼으로 채우고 싶다.”",'Regular',9.5,330,SUB)
end()

# 3 site
begin(); header(3,'Site Analysis'); tag(15,31)
rect(15,40,220,53,fill=(205,200,192)); text(117,46.5,'북측 진입도로 (가정)','Medium',9,INK,'mm')
rect(15,222,220,282,fill=SEA)
for k in range(6): line([(15,228+k*5),(220,228+k*5)],(120,140,152),0.3)
text(117,262,'바다 · 남측 (대포 해안)','Medium',11,(255,255,255),'mm')
px0,py0,px1,py1=55,70,180,200
rect(px0,py0,px1,py1,fill=(250,248,244),stroke=INK,lw=0.8)
rect(px0+8,py0+8,px1-35,py0+70,fill=(220,214,205)); text((px0+px1-27)/2,py0+39,'건물','Medium',10,INK,'mm')
rect(px0+50,py0+78,px1-8,py1-8,fill=(150,170,120)); text((px0+50+px1-8)/2,py1-30,'잔디마당','Medium',9,(255,255,255),'mm')
for yy in range(int(py0+15),int(py1),22): line([(px0-25,yy),(px0-8,yy)],SUB,0.3)
text(px0-16,py0+5,'등고선','Regular',6.5,SUB,'ms')
arrow((px1+3,py0+30),(px1+26,py0+30),SONGI); text(px1+5,py0+23,'차량 → B2','Medium',7.5,SONGI)
for ax in (px0+70,px0+100): arrow((ax,py1-2),(ax,py1+20),SEA,1.2,4)
text(px0+85,py1+14,'조망축','SemiBold',8,INK,'mm')
c.setStrokeColorRGB(*hexc(GOLD)); c.setLineWidth(0.9); c.arc(px0-5,Y(py1+14),px1+5,Y(py0+10),205,130)
text(px0+4,py1-30,'태양궤적 (남중)','Regular',7.5,GOLD)
arrow((px0-35,py0-10),(px0-10,py0+15),SUB); text(px0-37,py0-14,'겨울 북서풍','Regular',7.5,SUB)
arrow((px1-10,218),(px1-10,py1+4),RED); text(px1-6,212,'태풍 · 해풍','Medium',7.5,RED)
north(205,68,False)
x=240; y=45; text(x,y,'대지 조건','SemiBold',13); y+=11
for k,v in [('위치','제주 서귀포시 대포동 2217 (중문 · 주상절리대 인근 해안)'),('향','남향 · 바다 조망 (잔디마당 · 수영장 방향과 일치)'),
      ('지형','북측 도로에서 남측 바다로 약 7m 하강 (가정)'),('진입','보행 = 동측 현관 / 차량 = 동측 경사로로 B2 차고 (가정)'),
      ('기후','여름 남풍 · 태풍, 겨울 북서 계절풍, 높은 습도와 염분')]:
    text(x,y,k,'SemiBold',9); y=wrap(x+20,y,v,'Regular',9,145,SUB)+1.5
y+=6; text(x,y,'설계 대응','SemiBold',13); y+=11
for t in ['지상 1층만 드러내 해안 경관을 지키고 볼륨은 땅속으로','지형 하강을 이용해 B1 남측을 테라스로 개방, 지하에서도 채광 · 조망 확보','태풍 방향(남측) 개구부는 하단 레벨 상향 + 배수 집수정','염해 대응 창호 (알루미늄 불소도장) · 외부 금속 최소화']:
    y=wrap(x,y,'—  '+t,'Regular',9,165)+1
y+=6; text(x,y,'법규 확인 항목','SemiBold',13); y+=11
for t in ['토지이음 용도지역 · 국가유산(천연기념물) 보호구역 · 절대보전지역','지하층 인정 여부 (남측 노출 시 지상층 산정 가능)','거실 채광 1/10 · 환기 1/20 (건축법 시행령)']:
    y=wrap(x,y,'□  '+t,'Regular',9,165,SUB)+1
end()

# 4 section
begin(); header(4,'Site Section  N — S'); tag(15,31)
base=165; sc=9
def L(lv): return base-lv*sc
ter=[(25,L(0.3)),(205,L(0.3)),(215,L(-3.6)),(255,L(-3.6)),(268,L(-7.4)),(330,L(-8.6)),(W-15,L(-9.4))]
poly(ter+[(W-15,H-25),(25,H-25)],(214,206,194)); line(ter,INK,0.7)
rect(330,L(-9.0),W-15,H-25,fill=SEA); text(372,L(-9.0)+14,'바다 (해수면)','Medium',10,(255,255,255),'mm')
bx0=70
for name,lv,h,col,b in [('1F  숨',0,3.3,SAND,200),('B1  쉼',-3.6,3.3,(196,206,212),255),('B2  깊음',-7.6,4.0,(150,150,150),268)]:
    rect(bx0,L(lv+h),b,L(lv),fill=col,stroke=INK,lw=0.7); text(bx0+5,L(lv+h)+5,name,'SemiBold',12)
    text(bx0-3,L(lv),f'FL {lv:+.1f}','Regular',7.5,SUB,'rm')
for lv,b in ((3.3,200),(-0.3,200),(-3.6,255),(-7.6,268)): line([(bx0,L(lv)),(b,L(lv))],INK,1.6)
text(25,L(0.3)-6,'북측 도로','Medium',9)
text(258,L(-3.6)-6,'곡선 테라스 · 오션 자쿠지','Medium',8)
text(272,L(-7.4)-9,'수영장 수평창','Medium',8)
for lv in (1.5,-2.0,-6.0): arrow((150,L(lv)),(325 if lv>-5 else 320,L(lv)-2),SONGI,0.8,3.5)
text(150,L(1.5)-8,'조망','SemiBold',8,SONGI)
for xx in (215,230): arrow((xx+20,L(6)),(xx,L(-2.5)),GOLD,0.7,3)
text(242,L(6)-3,'남측 채광','Regular',7.5,GOLD)
line([(bx0-3,L(0)),(bx0-3,L(-7.8))],BLUE,1.0)
text(bx0-5,L(-5),'외방수 + 배수판','Regular',7.5,BLUE,'rm'); text(bx0-5,L(-6.3),'+ 드라이에어리어','Regular',7.5,BLUE,'rm')
wrap(W-15,36,"북측 도로에서 바다로 내려가는 지형을 따라 세 개의 층이 계단처럼 물러나며,\n각 층은 남쪽 바다를 향해 한 번씩 숨을 내쉽니다.",'Regular',9.5,220,right=True)
text(15,H-18,'※ 레벨 · 층고는 도면 수령 전 가정값입니다 (1F 3.3m / B1 3.3m / B2 4.0m, 슬래브 300mm).','Regular',7.5,SUB)
end()

# 5 stack
begin(); header(5,'Vertical Layers')
def axo(r,s):
    r=r.resize((int(r.width*s),int(r.height*s)),Image.LANCZOS).rotate(45,expand=True,resample=Image.BICUBIC)
    r=r.resize((r.width,int(r.height*0.55)),Image.LANCZOS)
    pad=40; out=Image.new('RGBA',(r.width+pad*2,r.height+pad*2),(0,0,0,0))
    sh=Image.new('RGBA',out.size,(90,80,70,0)); a=Image.new('L',out.size,0); a.paste(r.getchannel('A').point(lambda v:int(v*0.28)),(pad+8,pad+12))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(14))); out=Image.alpha_composite(out,sh); out.alpha_composite(r,(pad,pad)); return out
pxmm=0.135  # mm per px of axo image
for i,(n,t1,t2) in enumerate([(3,'B2  깊음','차고 · 바이크 갤러리 · 실내수영장'),(2,'B1  쉼','침실 · 거실 · 곡선 테라스 · 오션 자쿠지'),(1,'1F  숨','주방 · 다이닝 · 테라스 · 잔디마당')]):
    a=axo(alpha_cut(n),0.62); w,h=a.width*pxmm,a.height*pxmm; ly=225-i*72
    img(a,125-w/2,ly-h/2,w,h)
    line([(125+w/2-14,ly),(255,ly)],LINE,0.4); text(260,ly-7,t1,'SemiBold',15); text(260,ly+4,t2,'Regular',9,SUB)
wrap(260,36,"공용 → 사적 → 몰입.\n내려갈수록 사람은 줄고, 소리는 낮아지고, 바다와의 거리는 가까워집니다.",'Regular',10,145)
end()

# 6-8 zoning
def zoning(no,title,n,pts,t,iso=None):
    begin(); header(no,title)
    cx0,cy0,cx1,cy1=CROP[n]; ox,oy,s=place(load(n).crop(CROP[n]),12,33,235,245)
    for i,(x,y,_) in enumerate(pts,1): marker(ox+(x-cx0)*s,oy+(y-cy0)*s,i,3.4)
    x=260; y=40
    if iso: _,_,si=place(load(iso).crop((150,0,1900,1450)),W-15,y,145,95,'r'); y+=1450*si+8
    text(x,y,'Zoning Plan','SemiBold',14); y+=11
    y=wrap(x,y,t,'Regular',8.8,145,SUB)+6
    for i,(_,_,nm) in enumerate(pts):
        lx=x+3+(i//7)*72; ly=y+(i%7)*8.5; circ(lx,ly,2.6,BASALT); text(lx,ly,str(i+1),'SemiBold',6.5,(255,255,255),'mm'); text(lx+5,ly,nm,'Regular',9,INK,'lm')
    north(30,H-30); end()
zoning(6,'1F  숨 · Breath',1,P1,"동측 현관으로 들어서면 주방과 다이닝을 지나 폴딩도어 너머 테라스와 잔디마당, 그리고 바다가 한 번에 열립니다. 손님 · 가족 · 반려동물이 모이는 환대의 층입니다.",4)
zoning(7,'B1  쉼 · Rest',2,P2,"침실과 거실을 모은 사적인 층. 지형이 내려가는 남측을 곡선 테라스로 열어 땅속에서도 빛과 바다를 들이고, 끝단의 오션 자쿠지는 몸을 물에 담근 채 수평선을 마주하는, 이 집의 가장 고요한 순간입니다.",5)
zoning(8,'B2  깊음 · Depth',3,P3,"차 · 바이크 · 수영장이 모인 몰입의 층. 차고는 동측 경사로로 진입하며, 라운지와 차고 사이를 유리벽으로 계획해 컬렉션을 감상하는 갤러리로 만듭니다. 차고는 방화구획과 기계 배기로 생활공간과 분리합니다.")

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
      ('lime','라임 플라스터','내벽 · 외벽','베이지 타일 외벽'),('oak','화이트오크 원목마루','1F · B1 바닥','회색 우드 (전 층 동일)'),
      ('concrete','폴리싱 콘크리트','B2 차고 · 라운지 바닥','패턴 석재 차고'),('terrazzo','테라조 (송이 골재)','욕실 · 파우더룸','회색 욕실 타일 (전 층)')]
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
begin(); header(10,'Detail 01 · 지하 외벽 방수 (B2)')
text(15,34,'해안 지하 = 지하수 · 염분 · 결로. 하자 1순위인 지하 누수를 외방수 + 배수 + 내부 결로 방지의 3단 구조로 막습니다.','Regular',9,SUB)
hatch(20,60,99,262,'earth',EARTH)
hatch(99,60,104,252,'drain',(225,225,225))
rect(104,60,107,252,fill=(150,150,150))
rect(107,60,110,252,fill=WP)
hatch(110,60,140,232,'conc',CONC)
hatch(140,60,150,220,'ins',INS)
rect(153,60,156,220,fill=(238,238,236),stroke=SUB,lw=0.2)
hatch(60,232,250,252,'conc',CONC)
line([(60,252),(250,252)],WP,1.2); line([(107,252),(107,60)],WP,0.0)
rect(60,252,250,258,fill=(180,176,170))
hatch(78,236,99,252,'gravel',(214,206,194))
circ(89,244,4,(255,255,255),INK,0.5)
hatch(156,222,250,232,'conc',(222,219,214)); line([(140,232),(250,232)],WP,0.9)
line([(156,220),(250,220)],INK,0.6)
for xx in (20,250):
    pass
line([(95,58),(100,55),(105,61),(110,55),(115,61),(120,55),(125,61),(130,55),(135,61),(140,55),(145,61),(150,55),(158,58)],INK,0.4)
text(200,140,'B2 실내','Medium',11,SUB,'mm'); text(55,140,'되메우기 흙','Medium',9,INK,'mm')
for i,(x,y) in enumerate([(102,100),(105.5,120),(108.5,140),(125,170),(145,100),(154.5,120),(200,244),(170,226),(89,234),(160,256)],1): marker(x,y,i,2.6)
notes(262,42,[('배수판 (드레인보드)','흙 속 물을 아래로 흘려 방수층에 수압이 걸리지 않게 함'),
    ('보호판','되메우기 시 돌·장비로부터 방수층 보호'),
    ('외방수 복합시트 2겹','구조체 바깥에서 1차 차단. 바닥 → 벽까지 끊김 없이 감쌈'),
    ('수밀 콘크리트 400','방수제 혼입 · 시공이음에 지수판'),
    ('단열재 (XPS 50)','외기 · 지중 냉기 차단 → 실내 결로 방지'),
    ('띄움벽 + 마감','벽과 마감 사이 공기층 → 곰팡이 방지'),
    ('기초 매트 슬래브','하부 방수층 위 타설, 버림콘크리트 위'),
    ('바닥 누름 콘크리트 + 폴리싱 마감','바닥 방수층 보호, B2 차고 · 라운지'),
    ('ø100 유공관 + 자갈','벽 하단 물을 모아 집수정 → 배수펌프'),
    ('버림 콘크리트','지반 정리 · 하부 방수 바탕면')],140)
site_check(262,236,'현장 체크 (하자 포인트)',['방수층 겹침 100mm 이상 · 모서리 보강','시공이음 지수판 누락 확인','집수정 펌프 2대 (예비) · 정전 대비'],140)
text(15,H-14,'N.S. (Not to Scale) · 개념 디테일','Regular',7.5,SUB)
end()

# ---------- Detail 02 jacuzzi
begin(); header(11,'Detail 02 · B1 오션 자쿠지 단면')
text(15,34,'수면이 바다 쪽 수평선과 이어지는 인피니티 엣지. 바로 아래가 B2 바이크 갤러리라서 방수 · 하중 · 점검을 가장 먼저 해결합니다.','Regular',9,SUB)
rect(150,140,250,153,fill=(214,226,232)); text(248,136,'바다 · 수평선 →','Medium',8.5,SEA,'ra')
hatch(20,150,72,165,'conc',CONC); hatch(226,150,250,165,'conc',CONC)
hatch(72,150,82,220,'conc',CONC); hatch(214,165,226,220,'conc',CONC); hatch(72,205,226,220,'conc',CONC)
line([(82,150),(82,203),(212,203),(212,156)],WP,1.0)
rect(83,153,211,202,fill=WATER)
for a_,b_,cc in [(83,95,165),(95,107,177),(107,119,189)]: rect(a_,cc,b_,202,fill=TILE)
rect(20,145,72,150,fill=DECK); 
for xx in range(24,72,8): rect(xx,150,xx+1.5,150.01,fill=DECK)
rect(212,156,214,203,fill=TILE); line([(212,156),(214,156)],INK,0.4)
rect(226,160,240,170,fill=(225,225,225),stroke=INK,lw=0.3); rect(227,161,239,169,fill=WATER)
line([(245,150),(245,112)],(120,150,170),1.4); line([(245,112),(245,112)],INK,0.3)
line([(80,153),(212,153)],(60,120,160),0.5,([2,1],0))
rect(140,203,150,206,fill=(90,90,90))
line([(145,206),(145,232),(232,232)],(90,90,90),1.0); line([(233,170),(233,232)],(90,90,90),1.0)
rect(232,226,250,242,fill=(250,248,244),stroke=INK,lw=0.3); text(241,234,'M','SemiBold',8,INK,'mm')
line([(20,245),(250,245)],INK,0.5); rect(160,244,175,246,fill=BG)
text(135,262,'B2 바이크 갤러리','Medium',10,SUB,'mm')
circ(110,250,1.5,(200,60,50)); 
line([(60,153),(60,203)],INK,0.3); text(57,178,'수심 ≈ 900','Regular',7.5,INK,'rm')
for i,(x,y) in enumerate([(46,141),(77,185),(82,196),(150,176),(100,196),(219,186),(233,156),(245,118),(145,200),(241,220),(167,250),(110,256)],1): marker(x,y,i,2.6)
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
    ('B2 천장 점검구','배관 누수 확인 · 교체 동선'),
    ('누수 감지 센서','B2 천장 내 · 스마트폰 알림')],140)
site_check(262,255,'현장 체크 (하자 포인트)',['방수 후 48시간 담수 테스트 (2회)','바닥 배수 기울기 1/100 이상'],140)
text(15,H-14,'N.S. (Not to Scale) · 개념 디테일','Regular',7.5,SUB)
end()

# 10 scene plan
begin(); header(12,'Scene Plan · 추가 렌더 6컷')
shots=[(1,(1000,420),(1000,780),'1F 주방 → 폴딩도어 너머 잔디 · 바다','환대'),(1,(1150,880),(1150,1240),'1F 잔디 끝, 석양의 수평선','숨'),
       (2,(1150,430),(1110,800),'B1 거실 → 곡선 테라스','쉼 · 땅속의 빛'),(2,(1380,760),(1580,980),'B1 오션 자쿠지 → 수평선 (클라이맥스)','고요'),
       (3,(680,980),(680,1230),'B2 수영장 → 남측 수평창','깊음'),(3,(700,700),(1060,700),'B2 라운지 → 유리벽 너머 차고 (야간)','갤러리')]
pw=124
for j,n in enumerate((1,2,3)):
    cx0,cy0,_,_=CROP[n]; x0=15+j*(pw+9); ox,oy,s=place(load(n).crop(CROP[n]),x0,36,pw,120)
    text(x0,36+(CROP[n][3]-cy0)*s+3,['1F','B1','B2'][j],'SemiBold',10)
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
