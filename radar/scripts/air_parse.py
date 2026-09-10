import json,re,glob,math,base64
K=(24.7114,46.6745)
def hav(a,b):
    R=6371;dl=math.radians(b[0]-a[0]);dg=math.radians(b[1]-a[1]);h=math.sin(dl/2)**2+math.cos(math.radians(a[0]))*math.cos(math.radians(b[0]))*math.sin(dg/2)**2;return 2*R*math.asin(math.sqrt(h))
out={}
files=glob.glob('render_air_d/*.json')+['render_srch/air_olaya.json']
for f in files:
    try: js=json.load(open(f))
    except Exception: continue
    for j in js:
        if 'airbnb.com/api/v3' not in j['url'] or '"searchResults"' not in j['body']: continue
        d=json.loads(j['body'])
        def walk(o):
            if isinstance(o,dict):
                if o.get('__typename')=='StaySearchResult': yield o
                for v in o.values(): yield from walk(v)
            elif isinstance(o,list):
                for v in o: yield from walk(v)
        for r in walk(d):
            l=r.get('demandStayListing') or {}
            try: lid=base64.b64decode(l.get('id','')).decode().split(':')[-1]
            except Exception: lid=None
            if not lid or not lid.isdigit(): continue
            sp=(r.get('structuredDisplayPrice') or {}).get('primaryLine') or {}
            co=((l.get('location') or {}).get('coordinate')) or {}
            lat,lng=co.get('latitude'),co.get('longitude')
            name=(((l.get('description') or {}).get('name')) or {}).get('localizedStringWithTranslationPreference')
            pic=((r.get('contextualPictures') or [{}])[0]).get('picture')
            o={'id':lid,'name':name,'title':r.get('title'),'subtitle':r.get('subtitle'),'lat':lat,'lng':lng,'km':round(hav(K,(lat,lng)),2) if lat else None,'price':sp.get('discountedPrice') or sp.get('price'),'orig':sp.get('originalPrice'),'qual':sp.get('qualifier'),'label':sp.get('accessibilityLabel'),'pic':pic,'rating':r.get('avgRatingLocalized'),'url':f'https://ar.airbnb.com/rooms/{lid}','src':f.split('/')[-1]}
            if lid not in out or (o['price'] and not out[lid]['price']): out[lid]=o
json.dump(out,open('air_search.json','w'),ensure_ascii=False,indent=1)
print('airbnb unique',len(out))
for o in sorted(out.values(),key=lambda x:(x['km'] or 99))[:80]: print(o['id'],o['km'],o['price'],o['qual'],'|',(o['title'] or '')[:35],'|',(o['name'] or '')[:45],'|',o['src'])
