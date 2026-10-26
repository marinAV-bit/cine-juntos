from PIL import Image, ImageDraw, ImageFont
import os
S=1024; K=2; W=S*K
os.makedirs('assets',exist_ok=True)
def P(x,y): return (x*K,y*K)
def grad(w,h):
    im=Image.new('RGB',(w,h)); d=ImageDraw.Draw(im)
    a=(240,101,149); b=(194,37,92)
    for y in range(h):
        t=y/(h-1)
        d.line([(0,y),(w,y)],fill=tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3)))
    return im
def fg():
    im=Image.new('RGBA',(W,W),(0,0,0,0)); d=ImageDraw.Draw(im)
    cream=(255,244,214,255); edge=(255,212,59,255)
    for cx,cy,r in [(400,470,62),(624,470,62),(512,380,80),(430,420,70),(594,420,70),(350,520,56),(674,520,56),(512,470,70)]:
        d.ellipse([(cx-r)*K,(cy-r)*K,(cx+r)*K,(cy+r)*K],fill=cream,outline=edge,width=6*K)
    topw,botw,y0,y1,n=460,350,500,800,7
    def xs(y,f):
        t=(y-y0)/(y1-y0); w=topw+(botw-topw)*t
        return 512-w/2+w*f
    for i in range(n):
        f0,f1=i/n,(i+1)/n
        d.polygon([P(xs(y0,f0),y0),P(xs(y0,f1),y0),P(xs(y1,f1),y1),P(xs(y1,f0),y1)],
                  fill=(224,49,49,255) if i%2==0 else (255,255,255,255))
    d.rounded_rectangle([(512-topw/2-14)*K,(y0-22)*K,(512+topw/2+14)*K,(y0+14)*K],radius=14*K,fill=(255,255,255,255))
    return im
bg=grad(W,W); f=fg()
full=bg.convert('RGBA'); full.alpha_composite(f)
bg.resize((S,S),Image.LANCZOS).save('assets/icon-background.png')
f.resize((S,S),Image.LANCZOS).save('assets/icon-foreground.png')
full.resize((S,S),Image.LANCZOS).convert('RGB').save('assets/icon-only.png')
b=grad(1280,720)
ic=f.resize((620,620),Image.LANCZOS)
b.paste(ic,(30,27),ic)
d=ImageDraw.Draw(b)
try:
    ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',96)
    d.text((620,250),'Cine',font=ft,fill='white')
    d.text((620,370),'Juntos MR',font=ft,fill='white')
except Exception:
    pass
os.makedirs('android/app/src/main/res/drawable',exist_ok=True)
b.resize((640,360),Image.LANCZOS).save('android/app/src/main/res/drawable/tv_banner.png')
print('OK iconos')
