import json,re,math,datetime,subprocess,os
from concurrent.futures import ThreadPoolExecutor
K=(24.7114,46.6745)
def hav(a,b):
    R=6371;dl=math.radians(b[0]-a[0]);dg=math.radians(b[1]-a[1]);h=math.sin(dl/2)**2+math.cos(math.radians(a[0]))*math.cos(math.radians(b[0]))*math.sin(dg/2)**2;return 2*R*math.asin(math.sqrt(h))
D={"العليا":(24.695,46.685),"السليمانية":(24.705,46.700),"الورود":(24.727,46.672),"المعذر الشمالي":(24.705,46.660),"الملك فهد":(24.744,46.680),"المروج":(24.745,46.665),"المحمدية":(24.735,46.650),"الرحمانية":(24.725,46.640),"الوزارات":(24.680,46.700),"التعاون":(24.770,46.680),"المصيف":(24.760,46.700),"النخيل":(24.745,46.630)}
def nearest(lat,lng):
    return min(D.items(),key=lambda kv:hav((lat,lng),kv[1]))[0]
NA="غير مذكور"
L=[]
def add(**k):
    o={'plat':'','type':NA,'dist':'','price':None,'per':'شهري','priceText':'','area':NA,'floor':NA,'furn':NA,'incl':NA,'street':NA,'img':None,'phone':NA,'date':NA,'url':'','note':'','flags':[],'lat':None,'lng':None,'km':None,'kmSrc':'','status':'new','old':None,'title':''}
    o.update(k)
    if o['lat'] and o['lng']:
        o['km']=round(hav(K,(o['lat'],o['lng'])),1); o['kmSrc']='إحداثيات الإعلان'
    elif o['dist'] in D:
        o['km']=round(hav(K,D[o['dist']]),1); o['kmSrc']='مركز الحي تقريباً'
    if o['price'] and not o['priceText']: o['priceText']=f"{o['price']:,}"
    L.append(o); return o
# ---------- old kept: Haraj
H={d['id']:d for d in json.load(open('haraj.json'))}
def hg(i): d=H[i]; return dict(lat=d['geo'][0] if d['geo'] else None,lng=d['geo'][1] if d['geo'] else None,img=d.get('img'),url=d['url'],title=d['title'])
add(plat='حراج',type='استديو',dist='العليا',price=3500,area='672 حسب الرخصة (قد تكون للمبنى)',furn='مفروش',street='حي العليا، إحداثيات الإعلان قرب شارع التخصصي',date='2026-01-27، تحديث 2026-03-30',note='الإعلان معنون للعوائل. السعر من رخصة الإعلان: سعر الوحدة 3500. المعلن: شركة الفريح للعقارات، عرض H1030',flags=['عوائل'],status='kept',old=1,**hg(1))
add(plat='حراج',type='استديو',dist='المروج',price=None,priceText='السعر عند الفتح',area=NA,furn=NA,date='2024-10-21، تحديث 2025-09-20',note='الصفحة لا تظهر سعراً الآن، والفهرس السابق أظهر 3,600. آخر تحديث قبل 12 شهراً تقريباً، تحقق من التوفر',flags=['تحقق من التوفر'],status='kept',old=2,**hg(2))
add(plat='حراج',type='استديو',dist='العليا',price=5000,area='672 حسب الرخصة (قد تكون للمبنى)',furn='مفروش',street='حي العليا، إحداثيات الإعلان قرب شارع التخصصي',phone='0594100564',date='2025-12-29',note='الإعلان معنون للعوائل. السعر من رخصة الإعلان. شركة الفريح للعقارات، عرض H1041',flags=['عوائل'],status='kept',old=3,**hg(3))
add(plat='حراج',type='استديو',dist='العليا',price=3500,area='672 حسب الرخصة (قد تكون للمبنى)',furn='مفروش',street='حي العليا، إحداثيات الإعلان قرب شارع التخصصي',date='2025-11-15',note='الإعلان معنون للعوائل. السعر من رخصة الإعلان. شركة الفريح للعقارات، عرض H1028',flags=['عوائل'],status='kept',old=8,**hg(8))
add(plat='حراج',type='غرفة وصالة',dist='المحمدية',price=6500,area=80,furn='مفروش',street='حي المحمدية قرب محطة المترو',date='2025-09-22، تحديث 2025-10-18',note='السعر من رخصة الإعلان. شركة غالينا للوحدات المفروشة. آخر تحديث قبل 11 شهراً',flags=['تحقق من التوفر'],status='kept',old=37,**hg(37))
add(plat='حراج',type='غرفة وصالة',dist='العليا',price=4500,area='902 حسب الرخصة (قد تكون للمبنى)',furn='مفروش',incl='الكهرباء والماء والصيانة',street='مجمع ريم السكني بين شارع العليا العام وطريق الملك فهد',phone='0552098080',date='2025-12-28، تحديث 2026-03-10',note='السعر من رخصة الإعلان: 4500، عدد الغرف 1. المعلن: لا كاسا. الإعلان الأحدث لنفس المجمع مدرج أيضاً',status='kept',old=40,**hg(40))
# ---------- Bayut (old 30 + new)
for b in json.load(open('bayut.json')):
    add(plat='بيوت',type=b['type'],dist=b['dist'],price=b['price'],area=b['area'] if b['area'] else NA,floor=b['floor'] or NA,furn=b['furn'],incl=b['incl'],street=b['street'],img=b['img'],phone=b['phone'] or NA,date=b['date'],url=f"https://www.bayut.sa/en/property/details-{b['id']}.html",note=b['note'],flags=(['عوائل'] if b['fam'] else []),status='kept' if b.get('old') else 'new',old=b.get('old'))
# ---------- Airbnb old kept
AS=json.load(open('air_search.json'))
def ab(i):
    s=AS.get(i,{}); return dict(lat=s.get('lat'),lng=s.get('lng'))
add(plat='Airbnb',type='استديو',dist='العليا',price=6466,per='شهري لتواريخ 1 إلى 31 أكتوبر 2026',priceText='6,466',area=NA,furn='مفروش',incl='حسب صفحة Airbnb، تأكد من الرسوم قبل الحجز',street='مقابل التخصصي 101 حسب العنوان',date=NA,img='https://a0.muscache.com/im/pictures/hosting/Hosting-1435560123810132032/original/9c814142-51fa-4fb6-8ed8-dbfd6117637f.jpeg',url='https://ar.airbnb.com/rooms/1435560123810132032',note='كان 7,850 قبل خصم الشهر. 1 غرفة نوم، سرير واحد، حمام واحد، ضيفان. تقييم 4.92',status='kept',old=22,**ab('1435560123810132032'))
add(plat='Airbnb',type='استديو',dist='العليا',price=5766,per='شهري لتواريخ 1 إلى 31 أكتوبر 2026',priceText='5,766',area=NA,furn='مفروش',incl='حسب صفحة Airbnb، تأكد من الرسوم قبل الحجز',street='شارع التحلية حسب العنوان',date=NA,img='https://a0.muscache.com/im/pictures/ff1d6f3f-e101-40aa-a899-9caedb23f96e.jpg',url='https://ar.airbnb.com/rooms/1003011993846222550',note='كان 9,037 قبل خصم الشهر. 1 غرفة نوم، سرير واحد، حمام واحد. تقييم 4.74',status='kept',old=23,**ab('1003011993846222550'))
add(plat='Airbnb',type='غرفة وصالة',dist='السليمانية',price=8844,per='شهري لتواريخ 1 إلى 31 أكتوبر 2026',priceText='8,844',area=NA,furn='مفروش',incl='حسب صفحة Airbnb، تأكد من الرسوم قبل الحجز',street='السليمانية 114 حسب العنوان',date=NA,img='https://a0.muscache.com/im/pictures/hosting/Hosting-1555690148386070450/original/ee71095a-92b7-4f3d-8497-98fa1746863b.jpeg',url='https://ar.airbnb.com/rooms/1555690148386070450',note='1 غرفة نوم، سرير واحد، حمام واحد، 3 ضيوف. تقييم 5.0',status='kept',old=41,**ab('1555690148386070450'))
add(plat='Airbnb',type='غرفة وصالة',dist='العليا',price=None,priceText='غير متاح لأكتوبر',per='السعر يظهر عند اختيار تواريخ متاحة',area=NA,furn='مفروش',incl='حسب صفحة Airbnb',street='العليا حسب العنوان',date=NA,img='https://a0.muscache.com/im/pictures/hosting/Hosting-1395621662972284279/original/5bdb63f1-9daa-4e0a-9780-a4375a742734.jpeg',url='https://ar.airbnb.com/rooms/1395621662972284279',note='تواريخ 1 إلى 31 أكتوبر غير متاحة عند الفتح. 1 غرفة نوم، سريران، حمام واحد. تقييم 4.67',flags=['تحقق من التوفر'],status='kept',old=42,**ab('1395621662972284279'))
add(plat='Airbnb',type='غرفة وصالة',dist='الورود',price=4709,per='شهري لتواريخ 1 إلى 31 أكتوبر 2026',priceText='4,709',area=NA,furn='مفروش',incl='حسب صفحة Airbnb، تأكد من الرسوم قبل الحجز',street='حي الورود حسب العنوان',date=NA,img='https://a0.muscache.com/im/pictures/hosting/Hosting-1526803772794391562/original/d5b9fee4-5f2f-40d8-83a6-befe03bcb4b8.jpeg',url='https://ar.airbnb.com/rooms/1526803772794391562',note='كان 5,773 قبل خصم الشهر. صفحة Airbnb تسجل المدينة "الخرج" بينما العنوان يقول حي الورود، تأكد من الموقع قبل الحجز. 1 غرفة نوم، 4 ضيوف. تقييم 4.94',flags=['تحقق من الموقع'],status='kept',old=44,**ab('1526803772794391562'))
# ---------- Haraj new
HN={d['id']:d for d in json.load(open('h_new.json'))}
def hn(i,**k):
    d=HN[i]; base=dict(plat='حراج',url=d['url'],title=d['title'],lat=d['geo'][0] if d['geo'] else None,lng=d['geo'][1] if d['geo'] else None,img=d.get('img'),dist=d['nb'],date=d['postDate_h']+(('، تحديث '+d['updateDate_h']) if d['updateDate_h'] and d['updateDate_h']!=d['postDate_h'] else ''),phone=d['phone'] or NA)
    base.update(k); add(**base)
hn('11181965123',type='استديو',price=None,priceText='السعر عند الفتح',furn='مفروش بالكامل',street='طريق أبو بكر الصديق، دقيقتان من الريفر ووك',note='للإيجار الشهري والسنوي. المعلن fahad almg')
hn('11174163231',type='استديو',price=None,priceText='السعر عند الفتح',furn='مفروش (فندقي)',note='لا تفاصيل في نص الإعلان. مكتب إلهام وتمكين العقارية')
hn('11188110754',type='غرفة وصالة',price=3950,per='شهري بعقد سنوي أو نصف سنوي',furn='مفروش بالكامل',incl='الكهرباء',street='شارع الوطن متفرع من الدائري الشمالي بين مخرج 6 و7',area='625 حسب الرخصة (قد تكون للمبنى)',note='عمارة عوائل والسكان عوائل صغيرة فقط حسب الإعلان',flags=['عوائل فقط','عقد سنوي بدفع شهري'])
hn('11176319574',type='استديو',price=None,priceText='السعر عند الفتح',furn='مفروش',note='لا تفاصيل في نص الإعلان. أصول الخبرة العقارية')
hn('11176322553',type='استديو',price=3500,area=40,furn='مفروش',street='حي السليمانية قرب حديقة',note='غرفة نوم ومطبخ مجهز ودورة مياه ومكيف سبليت. أصول الخبرة العقارية')
hn('11184727260',type='غرفة وصالة',price=5000,per='شهري بحد أدنى 3 أشهر، أو 52,000 سنوي',area=80,floor='علوي',furn='مفروش',incl='غير شامل: الماء 500 ريال',note='مطبخ راكب ومكيفات وكاميرات وعامل نظافة')
hn('11180019518',type='استديو',price=None,priceText='السعر عند الفتح',furn='مفروش',area='580 حسب الرخصة (قد تكون للمبنى)',note='سعر الرخصة 42,000 وقد يكون سنوياً. لا نص في الإعلان',flags=['تحقق من الفترة'])
hn('11187424455',type='استديو',price=None,priceText='السعر عند الفتح',note='لا تفاصيل في نص الإعلان. المعلن التساهيل11')
hn('11187715875',type='غرفة وصالة',price=None,priceText='السعر عند الفتح',street='برج داماك، العليا',furn=NA,note='لا تفاصيل في نص الإعلان. سلسال السياحية')
hn('11187112515',type='غرفة وصالة',price=4500,area='902 حسب الرخصة (قد تكون للمبنى)',furn='مفروش',incl='الكهرباء والماء والصيانة',street='مجمع ريم السكني بين شارع العليا العام وطريق الملك فهد، خلف الدفاع المدني',note='إعادة نشر لإعلان لا كاسا المدرج سابقاً. السعر من رخصة الإعلان. مواقف وحراسة 24 ساعة')
hn('11179593953',type='استديو',price=4200,area=50,furn='مفروش',incl='الماء والكهرباء',street='حي المروج قرب المترو',note='تأمين 500. مؤسسة فايندر للعقارات، إعادة نشر لإعلان قديم')
hn('11158632519',type='استديو',price=2700,floor='الأول بدون مصعد',furn=NA,street='شارع عوف بن عبدالرحمن',note='قرب مغسلة ومحطة ومطاعم. رقم الترخيص 50011888')
hn('11187803215',type='استديو',price=None,priceText='السعر عند الفتح',furn=NA,note='الإعلان أساساً لدور أرضي ويذكر توفر استديو كبير شهري أو سنوي بمكيفات ومطبخ راكب')
hn('11184170740',type='غرفة وصالة',price=4000,area='390 حسب الرخصة (قد تكون للمبنى)',furn='مفروش بالكامل',per='شهري (الدفع شهري)',note='السعر من رخصة الإعلان. مجموعة أبو نواف العقارية')
hn('11185868470',type='استديو',price=4500,per='شهري، يبدأ من',area=60,furn='مفروش',street='حي النخيل قرب جامعة الملك سعود وخلف المدينة الرقمية',note='غرفة وصالة من 5,800 إلى 6,500، وغرفتان 8,000. غالينا للوحدات المفروشة')
hn('11185663838',type='استديو',price=4500,area=60,furn='مفروش بكامل التجهيزات',street='حي النخيل خلف المدينة الرقمية',note='السعر من رخصة الإعلان. غالينا للوحدات المفروشة')
hn('11185879248',type='غرفة وصالة',price=4700,per='شهري، يبدأ من',area='627 حسب الرخصة (قد تكون للمبنى)',furn='مفروش',incl='الإنترنت والماء والكهرباء والصيانة',street='شارع العروبة، حي الورود',note='غرفة ودورة مياه من 3,800، غرفة وصالة من 4,700 إلى 6,000 حسب المساحة. لا كاسا')
hn('11182629626',type='غرفة وصالة',price=None,priceText='السعر عند الفتح',furn='مفروش',note='لا تفاصيل في نص الإعلان. أصول الخبرة العقارية')
hn('11170836945',type='استديو',price=2500,area=40,furn='مفروش',incl='الماء والكهرباء',street='حي الوزارات، 5 دقائق مشياً من محطة القطار',note='نص الإعلان يقول 2,500 ورخصة الإعلان 2,300. قرب المستشفى العسكري')
hn('11185171750',type='غرفة وصالة',price=4000,area=50,furn='مفروش',incl='الماء والكهرباء والصيانة',street='حي الوزارات قرب المستشفى العسكري ومدينة الملك فهد الطبية',note='غرفة وصالة ومطبخ صغير 4,000، مطبخ كبير 4,500. شركة مئة للعقارات، ولها إعلانان مكرران 11184538658 و11180457905')
hn('11185739282',type='غرفة وصالة',price=None,priceText='السعر عند الفتح',furn='مفروش',street='خلف فندق الماريوت، حي الوزارات',note='وحدات: غرفة وحمام ومطبخ، غرفة وصالة، غرفتان. سعر الرخصة 6,000 لوحدة 150 م². شقق أسوار')
# ---------- Aqar
AQ=json.load(open('aqar_final.json'))
def aqdetail(o):
    r=subprocess.run(["curl","-s","-L","--max-time","40","-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0",o['url']],capture_output=True,text=True).stdout
    out={}
    m=re.search(r'\\"create_time\\":(\d{10})',r); out['created']=datetime.datetime.utcfromtimestamp(int(m.group(1))).strftime('%Y-%m-%d') if m else NA
    m=re.search(r'\\"last_update\\":(\d{10})',r); out['updated']=datetime.datetime.utcfromtimestamp(int(m.group(1))).strftime('%Y-%m-%d') if m else None
    m=re.search(r'\\"phone\\":\\"?(\+?9?6?6?0?5\d{8})',r); out['phone']=m.group(1) if m else NA
    out['alive']=bool(re.search(r'\\"published\\":true',r))
    return out
with ThreadPoolExecutor(8) as ex: det=list(ex.map(aqdetail,AQ))
for o,dt in zip(AQ,det):
    if not dt['alive']: continue
    txt=o['text']; typ='غرفة وصالة' if (o['livings'] not in (None,'0','null') or re.search('غرف[ةه] ?و ?صال[ةه]',txt)) else 'استديو'
    if re.search('غرفتين|غرفتان|2 ?غرف|٢ ?غرف',txt) and 'استديو' not in txt and 'استوديو' not in txt: typ='غرفة وصالة'
    listed=int(o['price']) if o['price'] and o['price'].isdigit() else None
    flags=[]; per='شهري (من نص الإعلان)'
    if listed and listed>=15000: flags.append('عقد سنوي بدفع شهري'); per=f"شهري بعقد سنوي، الإجمالي المعلن {listed:,}"
    if re.search('عوائل فقط|للعوائل فقط|عوايل فقط',txt): flags.append('عوائل فقط')
    elif re.search('عوائل|عوايل',txt): flags.append('عوائل')
    furn='مفروش' if re.search('مفروش|مؤثث|موثث',txt) else NA
    incl='الماء والكهرباء' if re.search('شامل[ةه]? (الماء|للماء|الكهرباء|للكهرباء|المويا|المياه)',txt) or re.search('شامل الكهرباء والماء|شامل الماء والكهرباء',txt) else NA
    add(plat='عقار',type=typ,dist=o['dist'],price=o['mon'],per=per,area=o['area'] or NA,furn=furn,incl=incl,street=(o['address'] or NA).replace(', مدينة الرياض, منطقة الرياض',''),img=o['img'],phone=dt['phone'] if dt['phone']!=NA else 'يظهر بزر الاتصال في عقار',date=dt['created']+(('، تحديث '+dt['updated']) if dt['updated'] and dt['updated']!=dt['created'] else ''),url=o['url'],note=('المعلن: '+(o['company'] or o['user'] or '')+'. ' if (o['company'] or o['user']) else '')+txt[:220],flags=flags,lat=float(o['lat']) if o['lat'] else None,lng=float(o['lng']) if o['lng'] else None,title=txt[:60])
# ---------- Airbnb search
seen_old={'1435560123810132032','1003011993846222550','1555690148386070450','1395621662972284279','1526803772794391562'}
for s in AS.values():
    if s['id'] in seen_old or not s['km'] or s['km']>9: continue
    t=(s['title'] or ''); n=(s['name'] or '')
    if re.search('فيلا|بيت|مزرعة|كوخ|إقامة',t.split(' في ')[0]) : continue
    if re.search('غرفتين|غرفتي|2 ?غرف|٢ ?غرف|3 ?غرف|ثلاث|2BR|2 bedroom',n,re.I): continue
    typ='استديو' if re.search('استديو|استوديو|ستوديو|studio',n,re.I) else ('غرفة وصالة' if re.search('غرف[ةه] ?و ?صال[ةه]|غرفة نوم|بغرفة|1BR|one bedroom|غرفة واحدة|جناح',n,re.I) else 'غير محدد')
    pr=int(re.sub(r'[^0-9]','',s['price'])) if s['price'] else None
    note=(f"كان {s['orig']} قبل خصم الشهر. " if s['orig'] else '')+(f"تقييم {s['rating']}. " if s['rating'] else '')+'الحي مستنتج من إحداثيات Airbnb: الأقرب هو '+nearest(s['lat'],s['lng'])
    add(plat='Airbnb',type=typ,dist=nearest(s['lat'],s['lng']),price=pr,per='شهري لتواريخ 1 إلى 31 أكتوبر 2026',priceText=(re.sub(r'[^0-9,]','',s['price']) if s['price'] else 'السعر عند الفتح'),furn='مفروش',incl='حسب صفحة Airbnb، تأكد من الرسوم قبل الحجز',street=NA,img=(s['pic']+'?im_w=320') if s['pic'] else None,url=s['url'],note=note,lat=s['lat'],lng=s['lng'],title=n)
# ---------- Mabet
if os.path.exists('mabet_final.json'):
    for u in json.load(open('mabet_final.json')): add(**u)
json.dump(L,open('data.json','w'),ensure_ascii=False,indent=1)
import collections
print('TOTAL',len(L),collections.Counter(o['plat'] for o in L),collections.Counter(o['status'] for o in L))
print('with price',sum(1 for o in L if o['price']),'with img',sum(1 for o in L if o['img']))
