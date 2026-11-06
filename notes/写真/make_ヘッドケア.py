from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
F='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
def font(s): return ImageFont.truetype(F,s)
CREAM=(250,244,236); BROWN=(110,74,56); ROSE=(176,104,120)

def square(path, focus_y=0.5, focus_x=0.5):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    w,h=im.size; s=min(w,h)
    x=int((w-s)*focus_x); y=int((h-s)*focus_y)
    im=im.crop((x,y,x+s,y+s)).resize((1600,1600))
    im=ImageEnhance.Brightness(im).enhance(1.45)
    im=ImageEnhance.Color(im).enhance(0.55)
    im=ImageEnhance.Contrast(im).enhance(0.9)
    warm=Image.new('RGB',im.size,(255,236,220))
    im=Image.blend(im,warm,0.22)
    return im

def text_c(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)

def band(im,lines):
    ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.rounded_rectangle((60,50,1540,410),radius=40,fill=CREAM+(235,))
    im=Image.alpha_composite(im.convert('RGBA'),ov); d=ImageDraw.Draw(im)
    text_c(d,800,85,lines[0],font(64),ROSE)
    text_c(d,800,180,lines[1],font(120),BROWN)
    d.line((300,330,1300,330),fill=ROSE,width=4)
    text_c(d,800,345,lines[2],font(46),BROWN)
    return im

def badges(im,items,y=1240):
    d=ImageDraw.Draw(im); r=150; n=len(items)
    xs=[800+(i-(n-1)/2)*360 for i in range(n)]
    for x,(a,b) in zip(xs,items):
        d.ellipse((x-r,y-r,x+r,y+r),fill=CREAM+(240,),outline=ROSE,width=6)
        text_c(d,x,y-62,a,font(52),BROWN); text_c(d,x,y+8,b,font(52),BROWN)
    return im

a=square('/root/.claude/uploads/6329eea8-3d42-5fdc-a6f7-6294973fb194/75c2eabb-image.jpg',0.55)
a=band(a,['＼ 元美容師の愛用品 ／','毎日のご褒美ヘッドケア','気が向いたら すぐ手に取れる場所に'])
a=badges(a,[('お風呂でも','使える'),('力加減を','自分で'),('耳まわり・','首すじも')])
a.convert('RGB').save('/home/user/claude/notes/写真/ヘッドケア_1.jpg',quality=92)

b=square('/root/.claude/uploads/6329eea8-3d42-5fdc-a6f7-6294973fb194/29ff2612-image.jpg',0.62,0.3)
b=band(b,['＼ 元美容師が毎日使う ／','頭がスッキリ、気持ちいい','ツインバード 防水ヘッドケア機'])
b.convert('RGB').save('/home/user/claude/notes/写真/ヘッドケア_2.jpg',quality=92)
