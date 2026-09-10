import re,json,subprocess,sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
slugs=["al-olaya","as-sulaymaniyah","al-wurud","al-mathar-ash-shamali","king-fahd","al-murooj","al-muhammadiyah","ar-rahmaniyah","al-wizarat","at-taawun","al-masif","an-nakheel","al-sulimaniyah","al-muruj","an-nakhil","al-malik-fahd","ar-rahmaniyah-riyadh"]
found={}
for sl in slugs:
    for page in (1,2,3):
        url=f"https://www.propertyfinder.sa/en/rent/ar-riyadh/apartments-for-rent-{sl}.html?fu=1&page={page}"
        r=subprocess.run(["curl","-s","-L","--max-time","60","-A",UA,"-w","\n%{http_code} %{url_effective}",url],capture_output=True,text=True)
        body,_,tail=r.stdout.rpartition('\n'); code,eff=tail.split(' ',1)
        m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',body,re.S)
        if not m or code!='200' or sl not in eff: print(sl,page,code,'redirect->',eff[-60:]); break
        d=json.loads(m.group(1)); sr=d['props']['pageProps'].get('searchResult',{}); L=[l['property'] for l in sr.get('listings',[]) if 'property' in l]
        mon=[p for p in L if p['price']['period']!='yearly']
        print(sl,page,'n',len(L),'nonyearly',len(mon),'periods',sorted(set(p['price']['period'] for p in L)))
        for p in mon: found[p['id']]=p
        if len(L)<25: break
json.dump(found,open('pf_monthly.json','w'),ensure_ascii=False,indent=1)
print('TOTAL non-yearly',len(found))
for p in found.values(): print(p['id'],p['price']['period'],p['price']['value'],p['bedrooms'],p['location']['full_name'],p['furnished'],p['listed_date'],p['share_url'])
