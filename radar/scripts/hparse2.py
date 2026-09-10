import re,json,datetime,glob,math,subprocess
K=(24.7114,46.6745)
def hav(a,b):
    R=6371;dl=math.radians(b[0]-a[0]);dg=math.radians(b[1]-a[1]);h=math.sin(dl/2)**2+math.cos(math.radians(a[0]))*math.cos(math.radians(b[0]))*math.sin(dg/2)**2;return 2*R*math.asin(math.sqrt(h))
def unesc(t):
    try: return json.loads('"'+t+'"')
    except Exception: return t
def grab(s,key,kind='str'):
    if kind=='str':
        m=re.search(r'\\"'+key+r'\\",\\"((?:[^"\\]|\\\\.|\\\\\\\\)*?)\\"',s); return unesc(unesc(m.group(1))) if m else None
    m=re.search(r'\\"'+key+r'\\",(-?\d+)',s); return int(m.group(1)) if m else None
T=["العليا","السليمانية","الورود","المروج","الملك فهد","المحمدية","الرحمانية","المعذر الشمالي","النخيل","التعاون","المصيف","الوزارات"]
S=json.load(open('h_search_ids.json'))
out=[]
for f in glob.glob('hpages/*.html'):
    pid=f.split('/')[-1][:-5]; s=open(f,encoding='utf-8').read()
    d={'id':pid,'url':f'https://haraj.com.sa/{pid}/','title':grab(s,'title'),'body':grab(s,'bodyTEXT'),'author':grab(s,'authorUsername'),'postDate':grab(s,'postDate','int'),'updateDate':grab(s,'updateDate','int'),'nb':grab(s,'geoNeighborhood'),'city':grab(s,'city'),'thumb':grab(s,'thumbURL'),'searchText':S.get(pid,{}).get('text')}
    m=re.search(r'maps\.google\.com/\?q=([0-9.]+),([0-9.]+)',s); d['geo']=[float(m.group(1)),float(m.group(2))] if m else None
    d['km']=round(hav(K,tuple(d['geo'])),2) if d['geo'] else None
    for k in ['postDate','updateDate']:
        d[k+'_h']=datetime.datetime.utcfromtimestamp(d[k]).strftime('%Y-%m-%d') if d[k] else None
    b=(d['body'] or '')
    m=re.search(r'(?:سعر الوحدة|السعر)\s*:\s*([0-9][0-9,\.]*)',b); d['licPrice']=m.group(1) if m else None
    m=re.search(r'مساحة العقار\s*:\s*([0-9][0-9\.]*)',b); d['licArea']=m.group(1) if m else None
    m=re.search(r'رقم جوال مسؤول الإعلان\s*:\s*(0?5\d{8})',b); d['phone']=m.group(1) if m else None
    m=re.search(r'نوع العقار\s*:\s*([^\n|]{2,40})',b); d['licType']=m.group(1).strip() if m else None
    m=re.search(r'تاريخ انتهاء رخصة الإعلان\s*:\s*([0-9-]+)',b); d['licExp']=m.group(1) if m else None
    tt=(d['title'] or '')+' '+(d['searchText'] or '')
    d['type']='استديو' if re.search('استديو|استوديو|ستوديو|ستديو',tt) else ('غرفة وصالة' if re.search('غرف[ةه] ?و ?صال[ةه]|غرفه وصاله|غرفة و صالة',tt) else 'غير محدد')
    d['inTarget']=d['nb'] in T
    last=max([x for x in [d['postDate'],d['updateDate']] if x] or [0])
    d['lastDate']=datetime.datetime.utcfromtimestamp(last).strftime('%Y-%m-%d') if last else None
    d['fresh']= last>= datetime.datetime(2026,3,9).timestamp()
    out.append(d)
out.sort(key=lambda x:(not x['inTarget'],x['nb'] or '',x['lastDate'] or ''),reverse=False)
json.dump(out,open('h_new.json','w'),ensure_ascii=False,indent=1)
keep=[d for d in out if d['inTarget'] and d['fresh'] and d['city']=='الرياض']
print('parsed',len(out),'inTarget',sum(d['inTarget'] for d in out),'fresh+target',len(keep))
for d in keep: print(d['id'],d['nb'],d['type'],'last',d['lastDate'],'lic',d['licPrice'],d['licArea'],'km',d['km'],'ph',bool(d['phone']),'|',(d['title'] or '')[:60])
