from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
F='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
def font(s): return ImageFont.truetype(F,s)
CREAM=(250,244,236); BROWN=(110,74,56); ROSE=(176,104,120); GOLD=(184,150,90)
src='/root/.claude/uploads/6329eea8-3d42-5fdc-a6f7-6294973fb194/32b8eb39-image.jpg'
im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
im=im.resize((1200,1600))
im=ImageEnhance.Brightness(im).enhance(1.25)
im=ImageEnhance.Color(im).enhance(0.6)
im=Image.blend(im,Image.new('RGB',im.size,(255,236,220)),0.18)
W=1600; canvas=Image.new('RGB',(W,1600),CREAM); canvas.paste(im,(W-1200,0))
d=ImageDraw.Draw(canvas)
def tc(cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
cx=200
tc(cx,110,'＼ 元美容師の ／',font(40),ROSE)
tc(cx,165,'愛用品',font(40),ROSE)
for i,t in enumerate(['シャンプー','タイムの','ご褒美']):
    tc(cx,300+i*110,t,font(66),BROWN)
d.line((70,650,330,650),fill=GOLD,width=4)
for i,(a,b) in enumerate([('ゴールドが','上品'),('シャンプー','のときに'),('手になじむ','かたち')]):
    y=760+i*250; r=105
    d.ellipse((cx-r,y-r+60,cx+r,y+r+60),outline=ROSE,width=5,fill=(255,250,245))
    tc(cx,y+12,a,font(36),BROWN); tc(cx,y+62,b,font(36),BROWN)
tc(cx,1520,'S-HEART-S スカルプブラシ',font(26),BROWN)
canvas.save('/home/user/claude/notes/写真/スカルプブラシ_1.jpg',quality=92)
