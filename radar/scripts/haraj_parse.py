import re,json,html,datetime,sys
old={x['id']:x for x in json.load(open('old.json'))}
def unesc(t):
    # payload is JSON-escaped inside a JS string; decode twice
    try: return json.loads('"'+t+'"')
    except Exception: return t
def grab(s,key,kind='str'):
    if kind=='str':
        m=re.search(r'\\"'+key+r'\\",\\"((?:[^"\\]|\\\\.|\\\\\\\\)*?)\\"',s)
        return unesc(unesc(m.group(1))) if m else None
    m=re.search(r'\\"'+key+r'\\",(-?\d+)',s); return int(m.group(1)) if m else None
out=[]
for i,x in old.items():
    if x['plat']!='حراج': continue
    s=open(f'pages/{i}.html',encoding='utf-8').read()
    d={'id':i,'url':x['url']}
    d['title']=grab(s,'title'); d['body']=grab(s,'bodyTEXT'); d['author']=grab(s,'authorUsername')
    d['postDate']=grab(s,'postDate','int'); d['updateDate']=grab(s,'updateDate','int')
    d['city']=grab(s,'city'); d['nb']=grab(s,'geoNeighborhood'); d['thumb']=grab(s,'thumbURL')
    m=re.search(r'maps\.google\.com/\?q=([0-9.]+),([0-9.]+)',s); d['geo']=[float(m.group(1)),float(m.group(2))] if m else None
    m=re.search(r'\\"imagesList\\",\[([^\]]*)\]',s); d['images']=re.findall(r'\\"([^"\\]+)\\"',m.group(1)) if m else []
    d['status']=grab(s,'status')
    for k in ['postDate','updateDate']:
        if d[k]: d[k+'_h']=datetime.datetime.utcfromtimestamp(d[k]).strftime('%Y-%m-%d')
    m=re.search(r'\\"realEstateInfo\\",\{(.{0,200})',s); d['reInfo']=m.group(1) if m else None
    out.append(d)
json.dump(out,open('haraj.json','w'),ensure_ascii=False,indent=1)
for d in out:
    print(d['id'],d['postDate_h'] if d.get('postDate_h') else None,d['updateDate_h'] if d.get('updateDate_h') else None,'|',d['nb'],'|',d['author'],'|',(d['title'] or '')[:70])
