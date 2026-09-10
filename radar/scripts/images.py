import json,os,hashlib,subprocess,base64,io,sys
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
L=json.load(open('data.json'))
cache={}
if os.path.exists('imgcache.json'): cache=json.load(open('imgcache.json'))
def fix(u):
    if 'images.bayut.sa/thumbnails/' in u: return u.replace('-800x600','-400x300')
    if 'images.aqar.fm/webp/750x0' in u: return u.replace('/webp/750x0/','/webp/300x0/')
    if 'muscache.com' in u and 'im_w=' not in u: return u+('&' if '?' in u else '?')+'im_w=320'
    return u
def fetch(u):
    if u in cache: return u,cache[u]
    fu=fix(u); fn='imgs/'+hashlib.md5(u.encode()).hexdigest()
    r=subprocess.run(["curl","-s","-L","--max-time","40","-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0","-o",fn,"-w","%{http_code}",fu],capture_output=True,text=True)
    if r.stdout!='200' or not os.path.exists(fn) or os.path.getsize(fn)<500: return u,None
    try:
        im=Image.open(fn); im=im.convert('RGB'); w,h=im.size
        if w>320: im=im.resize((320,int(h*320/w)))
        b=io.BytesIO(); im.save(b,'JPEG',quality=62,optimize=True)
        return u,'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    except Exception as e: return u,None
urls=sorted({o['img'] for o in L if o.get('img')})
with ThreadPoolExecutor(10) as ex:
    for u,d in ex.map(fetch,urls): cache[u]=d
json.dump(cache,open('imgcache.json','w'))
ok=sum(1 for u in urls if cache.get(u)); tot=sum(len(cache[u]) for u in urls if cache.get(u))
print('images',len(urls),'ok',ok,'total KB',tot//1024)
