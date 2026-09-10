import re,json,subprocess,html
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
D={"العليا":"شمال-الرياض/حي-العليا","السليمانية":"شمال-الرياض/حي-السليمانية","الورود":"شمال-الرياض/حي-الورود","المروج":"شمال-الرياض/حي-المروج","الملك فهد":"شمال-الرياض/حي-الملك-فهد","المحمدية":"شمال-الرياض/حي-المحمدية","الرحمانية":"شمال-الرياض/حي-الرحمانية","المعذر الشمالي":"شمال-الرياض/حي-المعذر-الشمالي","النخيل":"شمال-الرياض/حي-النخيل","التعاون":"شمال-الرياض/حي-التعاون","المصيف":"شمال-الرياض/حي-المصيف","الوزارات":"وسط-الرياض/حي-الوزارات"}
found={}
def get(url):
    r=subprocess.run(["curl","-s","-L","--max-time","60","-A",UA,"-w","\n%{http_code}",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition('\n'); return code,body
def objs(body):
    # RSC payload: find listing objects by "id":N,... "path":...
    out=[]
    for m in re.finditer(r'\{\\"id\\":(\d{6,8}),\\"(?:sov_campaign_id|area)\\"',body):
        seg=body[m.start():m.start()+6000]
        def g(k,typ='s'):
            mm=re.search(r'\\"'+k+r'\\":(?:\\"((?:[^"\\]|\\\\.)*?)\\"|([-0-9.a-z]+))',seg)
            if not mm: return None
            return mm.group(1) if mm.group(1) is not None else mm.group(2)
        o={'id':m.group(1),'area':g('area'),'beds':g('beds'),'livings':g('livings'),'price':g('price'),'rent_period':g('rent_period'),'daily':g('daily_rentable'),'content':g('content'),'address':g('address'),'district':g('district'),'path':g('path'),'furnished':g('furnished'),'rent_period_text':g('rent_period_text'),'mainImage':g('mainImage'),'lat':g('lat'),'lng':g('lng'),'user':g('name'),'company':g('company_name'),'family':g('family'),'singles':g('singles'),'floor':g('floor'),'published':g('published')}
        out.append(o)
    return out
for name,slug in D.items():
    for q in ["beds=eq,1","beds=eq,1&furnished=eq,1"]:
        for page in (1,2,3,4):
            url=f"https://sa.aqar.fm/شقق-للإيجار/الرياض/{slug}/{page}?{q}" if page>1 else f"https://sa.aqar.fm/شقق-للإيجار/الرياض/{slug}?{q}"
            code,body=get(url)
            if code!='200': print(name,q,page,code); break
            L=objs(body); cnt=re.search(r'\\"count\\":(\d+)',body)
            mon=[o for o in L if o['content'] and re.search('شهري|شهرى|شهريا|بالشهر|كل شهر',o['content'].replace('\\\\n',' '))]
            for o in mon: o['dist']=name; found[o['id']]=o
            print(name,q,page,'count',cnt.group(1) if cnt else None,'objs',len(L),'monthly-mention',len(mon))
            if len(L)<20: break
json.dump(found,open('aqar_monthly.json','w'),ensure_ascii=False,indent=1)
print('TOTAL',len(found))
for o in found.values(): print(o['id'],o['dist'],o['price'],o['rent_period_text'],o['beds'],o['area'],'|',(o['content'] or '')[:100].replace('\\\\n',' '))
