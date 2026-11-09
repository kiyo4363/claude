import re, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

src='/home/user/claude/notes/紹介文の案.md'
t=open(src,encoding='utf-8').read()
sec=t.split('## 投稿済みの紹介文（全文が分かっているもの）')[1].split('## 反応のよかった')[0]
heads=[l[4:] for l in sec.splitlines() if l.startswith('### ')]

def genre(n):
    rules=[
     ('眉・顔まわり',['眉','アイブロウ','フェリエ']),
     ('ウィッグ',['ウィッグ']),
     ('帽子・小物',['帽子','キャスケット','ニット帽','手袋','ストール','靴下',]),
     ('靴・サポーター',['ニューバランス']),
     ('手もと・からだ',['ハンドクリーム','ボディバター']),
     ('シルク・夜ケア',['ナイトキャップ','ピローケース','ヘアゴム']),
     ('スキンケア',['化粧水','美容液','クリーム','オールインワン','アイクリーム','メラノCC','肌美精']),
     ('白髪ケア',['白髪','カラー','ビゲン','利尻','ルプルプ','カバーグレイ','プリオール','サロンドプロ']),
     ('道具・家電',['ドライヤー','アイロン','ブラシ','ヘッドケア','タオル','クリップ','タングルティーザー','つげ']),
     ('薄毛・ボリューム・頭皮',['スカルプ','頭皮','ボリューム','haru','セグレタ シャンプー 根元','フォンダン','for all hair']),
    ]
    for g,ks in rules:
        if any(k in n for k in ks):
            # skin exclusions
            if g=='スキンケア' and ('頭皮' in n or 'ヘア' in n or 'ケラスターゼ' in n or 'シャンプー' in n): continue
            if g=='白髪ケア' and ('カラーヘアメンテナンス' in n): continue
            return g
    return 'パサつき・ツヤ・まとまり'

rows=[]
for h in heads:
    end=h.rfind('）')
    if end<0:
        name,inside,tail=h,'',''
    else:
        d=0;st=None
        for k in range(end,-1,-1):
            if h[k]=='）': d+=1
            elif h[k]=='（':
                d-=1
                if d==0: st=k;break
        name,inside,tail=h[:st],h[st+1:end],h[end+1:]
    # nested paren in name like "ヘアオイル（...）" handled: take outermost last paren
    toks=[x.strip() for x in inside.split('、')]
    date=None; price=None; pricenote=''; shop=''
    dm=re.search(r'(2026-\d\d-\d\d)',inside)
    if dm: date=datetime.date.fromisoformat(dm.group(1))
    pm=re.search(r'¥([\d,]+)(〜)?',inside)
    if pm:
        price=int(pm.group(1).replace(',','')); pricenote='〜（選べる）' if pm.group(2) else ''
    if toks and not toks[0].startswith('¥') and not re.match(r'2026',toks[0]) and toks[0] not in ('帽子',):
        shop=toks[0]
    shop=shop.split('＝')[0]
    if shop.startswith('お試し'): shop=''
    if shop.startswith('グロス アブソリュ'): shop='Tiara888 楽天市場店'
    if shop.startswith('選べる単品'): shop='BEAUTE DE MODE'
    memo=[]
    if '削除' in inside: memo.append('送料が高いので同じ日に削除')
    if '別の会話' in inside: memo.append('別の会話で投稿')
    if '送料無料' in inside: memo.append('送料無料')
    sm=re.search(r'送料 ?([\d,]+) ?円',inside)
    if sm: memo.append(f'送料 {sm.group(1)} 円')
    if tail.strip(): memo.append(tail.strip().lstrip('★').replace(' ',''))
    rows.append([date,name.strip(),shop,price,pricenote,genre(name),'、'.join(memo)])

extra=[
 ('VALANROSE KURO クリームシャンプー','白髪ケア',None),
 ('アルガネーゼ カラートリートメント','白髪ケア',None),
 ('アルガネーゼ グレイヘア','白髪ケア',None),
 ('スカルプD ボーテ シャンプー','薄毛・ボリューム・頭皮',None),
 ('セラプリエ','薄毛・ボリューム・頭皮',None),
 ('uka スカルプブラシ','道具・家電',None),
 ('パナソニック ナノケア（ドライヤー）','道具・家電',None),
 ('頭皮エステ','道具・家電',None),
 ('ORBIS エッセンスインヘアミルク','パサつき・ツヤ・まとまり',None),
 ('帽子のコンヌ キルティング帽子','帽子・小物',None),
 ('ダンロップ リファインド ウォーキングシューズ','靴・サポーター',3990),
 ('アサヒ 快歩主義 L011','靴・サポーター',5499),
 ('アシックス ハダシウォーカー 1292A066','靴・サポーター',11880),
 ('ファイテン サポーター 腰用','靴・サポーター',7920),
 ('ファイテン サポーター ひざ用','靴・サポーター',4400),
]
for n,g,pr in extra:
    rows.append([None,n,'',pr,'〜' if n.startswith('アサヒ') else '',g,'最初のころ・ほかの会話の投稿（日付・お店はメモになし）'])
rows.sort(key=lambda r:(r[0] or datetime.date(2026,9,30)))

wb=Workbook(); ws=wb.active; ws.title='投稿一覧'
F='Arial'
title=Font(name=F,bold=True,size=14); hdr=Font(name=F,bold=True,color='FFFFFF'); body=Font(name=F,size=11)
fill=PatternFill('solid',fgColor='8E5A7A'); alt=PatternFill('solid',fgColor='F7EEF3'); red=PatternFill('solid',fgColor='EEEEEE')
thin=Side(style='thin',color='DDDDDD'); bd=Border(top=thin,bottom=thin,left=thin,right=thin)
ws['A1']='YOMI 大人のご褒美ケア　投稿した商品の一覧'; ws['A1'].font=title
ws['A2']='メモ（notes/紹介文の案.md）に記録した投稿から作りました。投稿日が空いているものは、最初のころ・ほかの会話の投稿で、日付やお店がメモにないものです。'; ws['A2'].font=Font(name=F,size=10,color='666666')
heads_=['No.','投稿日','商品名','お店','値段（円）','値段のメモ','ジャンル','メモ']
for i,hh in enumerate(heads_,1):
    c=ws.cell(row=4,column=i,value=hh); c.font=hdr; c.fill=fill; c.alignment=Alignment(horizontal='center',vertical='center'); c.border=bd
r0=5
for i,row in enumerate(rows):
    r=r0+i
    ws.cell(row=r,column=1,value=i+1)
    vals=row
    for j,v in enumerate(vals,2):
        ws.cell(row=r,column=j,value=v)
    for j in range(1,9):
        c=ws.cell(row=r,column=j); c.font=body; c.border=bd; c.alignment=Alignment(vertical='center',wrap_text=(j in (3,8)))
        if i%2: c.fill=alt
        if '削除' in (row[6] or ''): c.fill=red; c.font=Font(name=F,size=11,color='999999')
    ws.cell(row=r,column=2).number_format='yyyy/m/d'
    ws.cell(row=r,column=5).number_format='#,##0'
last=r0+len(rows)-1
widths=[6,12,46,30,12,14,22,34]
for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
ws.freeze_panes='A5'
ws.auto_filter.ref=f'A4:H{last}'

s=wb.create_sheet('まとめ')
s['A1']='まとめ'; s['A1'].font=title
s['A3']='記録している投稿の数'; s['B3']=f'=COUNTA(投稿一覧!C5:C{last})'
s['A4']='そのうち削除したもの'; s['B4']=f'=COUNTIF(投稿一覧!H5:H{last},"*削除*")'
s['A5']='値段の平均（円）'; s['B5']=f'=ROUND(AVERAGE(投稿一覧!E5:E{last}),0)'; s['B5'].number_format='#,##0'
s['A7']='ジャンル'; s['B7']='投稿の数'
for c in ('A7','B7'): s[c].font=hdr; s[c].fill=fill
genres=['パサつき・ツヤ・まとまり','白髪ケア','薄毛・ボリューム・頭皮','スキンケア','道具・家電','帽子・小物','手もと・からだ','シルク・夜ケア','眉・顔まわり','ウィッグ','靴・サポーター']
for i,g in enumerate(genres):
    r=8+i; s.cell(row=r,column=1,value=g); s.cell(row=r,column=2,value=f'=COUNTIF(投稿一覧!G$5:G${last},A{r})')
for row in s.iter_rows(min_row=3,max_row=8+len(genres)):
    for c in row:
        if c.font!=hdr: c.font=Font(name=F,size=11,bold=c.font.bold)
s['A1'].font=title
for c in ('A7','B7'): s[c].font=hdr
s.column_dimensions['A'].width=28; s.column_dimensions['B'].width=12
out='/home/user/claude/notes/ROOM投稿一覧.xlsx'
wb.save(out); print(len(rows), out)
from collections import Counter; print(Counter(r[5] for r in rows))
