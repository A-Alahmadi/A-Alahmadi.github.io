import re
import json,html,datetime
L=json.load(open('data.json')); C=json.load(open('imgcache.json'))
REMOVED=json.load(open('removed.json'))
EMO=re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200d\U0001F900-\U0001F9FF\u2190-\u21FF\u2500-\u25FF\u2700-\u27BF\U0001F300-\U0001F5FF\u2013\u2014\u2015\u2012\u2e3a\u2e3b]')
def clean(t):
    if not isinstance(t,str): return t
    t=EMO.sub(' ',t); t=re.sub(r'[\u2013\u2014]',' ',t); return re.sub(r'\s{2,}',' ',t).strip()
for i,o in enumerate(L):
    for k in ('note','street','title','incl','furn','area','per','priceText','date','type'): o[k]=clean(o.get(k))
    o['i']=i+1; o['imgd']=C.get(o['img']) if o.get('img') else None
    for k in ('img','lat','lng','title'): o.pop(k,None) if k in ('lat','lng') else None
def esc(s): return html.escape(str(s),quote=True)
n=len(L); nnew=sum(1 for o in L if o['status']=='new'); nkept=n-nnew
plats=sorted({o['plat'] for o in L}, key=lambda p:['بيوت','حراج','عقار','Airbnb','مبيت'].index(p) if p in ['بيوت','حراج','عقار','Airbnb','مبيت'] else 9)
priced=sum(1 for o in L if o['price'])
data_js=json.dumps(L,ensure_ascii=False,separators=(',',':'))
removed_rows=''.join(f"<tr><td class=num>{r['old']}</td><td>{esc(r['plat'])}</td><td>{esc(r['what'])}</td><td>{esc(r['why'])}</td><td><a href='{esc(r['url'])}' target=_blank rel=noopener>الرابط</a></td></tr>" for r in REMOVED)
page=f'''<title>رادار شقق العليا</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;800&display=swap">
<style>
:root{{--bg:#F2F4F3;--surface:#FFFFFF;--surface-2:#E9EDEB;--line:#D3DAD6;--ink:#171D1B;--ink-2:#4A5450;--ink-3:#77827D;--accent:#1E4F6E;--accent-ink:#FFFFFF;--accent-soft:#DCE8F0;--ok:#25704A;--ok-soft:#DFF0E6;--warn:#9A6A12;--warn-soft:#F6EBD2;--bad:#9B3B2E;--bad-soft:#F5E1DD;--radius:10px;--shadow:0 1px 2px rgba(23,29,27,.06),0 6px 20px rgba(23,29,27,.06)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#111615;--surface:#1A201E;--surface-2:#232B28;--line:#334039;--ink:#ECF1EE;--ink-2:#B4BFB9;--ink-3:#7F8B85;--accent:#7FB3D3;--accent-ink:#0E1F2A;--accent-soft:#1B2E3B;--ok:#7FD0A2;--ok-soft:#1B332A;--warn:#E3B95F;--warn-soft:#3A2F16;--bad:#F09A8C;--bad-soft:#3B211C;--shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.25)}}}}
:root[data-theme="dark"]{{--bg:#111615;--surface:#1A201E;--surface-2:#232B28;--line:#334039;--ink:#ECF1EE;--ink-2:#B4BFB9;--ink-3:#7F8B85;--accent:#7FB3D3;--accent-ink:#0E1F2A;--accent-soft:#1B2E3B;--ok:#7FD0A2;--ok-soft:#1B332A;--warn:#E3B95F;--warn-soft:#3A2F16;--bad:#F09A8C;--bad-soft:#3B211C;--shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.25)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans Arabic",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;font-size:15px;line-height:1.65}}
.wrap{{direction:rtl;text-align:right;max-width:820px;margin:0 auto;padding-inline:16px;padding-block:20px 56px;display:flex;flex-direction:column;gap:26px}}
h1,h2,h3{{font-family:"Noto Kufi Arabic","IBM Plex Sans Arabic",system-ui,sans-serif;margin:0;text-wrap:balance;line-height:1.35}}
h1{{font-size:1.7rem;font-weight:800}} h2{{font-size:1.15rem;font-weight:800}} h3{{font-size:1rem;font-weight:700}}
p{{margin:0}} a{{color:var(--accent)}}
.eyebrow{{font-size:.74rem;letter-spacing:.06em;color:var(--ink-3);font-weight:600}}
.num{{font-variant-numeric:tabular-nums}}
header{{display:flex;flex-direction:column;gap:10px}}
.anchor{{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:baseline;color:var(--ink-2);font-size:.9rem}} .anchor b{{color:var(--ink)}}
.status{{border:1px solid var(--line);border-inline-start:4px solid var(--ok);background:var(--surface);border-radius:var(--radius);padding:12px 14px;display:flex;flex-direction:column;gap:6px;font-size:.92rem}} .status b{{color:var(--ok)}}
section{{display:flex;flex-direction:column;gap:12px}}
.sec-head{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}}
.hint{{color:var(--ink-3);font-size:.84rem}}
.summary{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.tile{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:10px 12px}}
.tile .v{{font-size:1.25rem;font-weight:700;font-family:"Noto Kufi Arabic",sans-serif}} .tile .k{{font-size:.76rem;color:var(--ink-3)}}
.fbar{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;align-items:end}}
.fbar label{{display:flex;flex-direction:column;gap:3px;font-size:.78rem;color:var(--ink-2)}}
.fbar .chk{{flex-direction:row;align-items:center;gap:6px;font-size:.84rem;padding-bottom:8px}}
input,select{{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 10px;width:100%;min-width:0}}
input[type=checkbox]{{width:auto}}
button{{font:inherit;cursor:pointer}}
.count{{font-size:.84rem;color:var(--ink-2)}}
.cards{{display:flex;flex-direction:column;gap:12px}}
.lcard{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px;display:grid;grid-template-columns:120px 1fr auto;gap:6px 12px;box-shadow:var(--shadow)}}
.lcard .ph{{grid-row:1/4;width:120px;height:90px;border-radius:8px;object-fit:cover;background:var(--surface-2);display:block}}
.lcard .noph{{grid-row:1/4;width:120px;height:90px;border-radius:8px;background:var(--surface-2);color:var(--ink-3);font-size:.72rem;display:flex;align-items:center;justify-content:center;text-align:center;padding:6px}}
.lcard .t{{font-weight:700}}
.lcard .p{{font-family:"Noto Kufi Arabic",sans-serif;font-weight:800;font-size:1.15rem;white-space:nowrap;text-align:left}}
.lcard .p small{{display:block;font-size:.68rem;font-weight:500;color:var(--ink-3);font-family:"IBM Plex Sans Arabic",sans-serif;white-space:normal;max-width:170px}}
.lcard .p.unk{{font-size:.85rem;font-weight:600;color:var(--ink-3)}}
.lcard .chips{{grid-column:2/4;display:flex;flex-wrap:wrap;gap:6px}}
.chip{{display:inline-flex;align-items:center;gap:4px;font-size:.74rem;padding:2px 8px;border-radius:999px;background:var(--surface-2);color:var(--ink-2)}}
.chip.ok{{background:var(--ok-soft);color:var(--ok)}} .chip.warn{{background:var(--warn-soft);color:var(--warn)}} .chip.bad{{background:var(--bad-soft);color:var(--bad)}} .chip.new{{background:var(--accent-soft);color:var(--accent)}}
.lcard .d{{grid-column:1/4;display:grid;grid-template-columns:auto 1fr;gap:2px 10px;font-size:.84rem;color:var(--ink-2)}}
.lcard .d b{{color:var(--ink-3);font-weight:600;white-space:nowrap}}
.lcard .n{{grid-column:1/4;font-size:.84rem;color:var(--ink-2)}}
.lcard .r{{grid-column:1/4;display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.btn{{display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);color:var(--ink);text-decoration:none;font-size:.86rem;font-weight:500}}
.btn.primary{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
.btn:focus-visible,input:focus-visible,select:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.more{{align-self:center}}
.dgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.dtile{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:10px 12px;text-align:right;cursor:pointer;display:flex;flex-direction:column;gap:2px;color:var(--ink);font:inherit}}
.dtile:hover{{background:var(--surface-2)}}
.dtile[aria-pressed="true"]{{border-color:var(--accent);background:var(--accent-soft);box-shadow:inset 0 0 0 1px var(--accent)}}
.dtile .nm{{font-weight:700;font-family:"Noto Kufi Arabic",sans-serif}}
.dtile .ct{{font-size:.8rem;color:var(--ink-2)}}
.dtile .mn{{font-size:.76rem;color:var(--ink-3)}}
.seg{{display:flex;flex-wrap:wrap;gap:6px}}
.seg button{{padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font-size:.86rem}}
.seg button[aria-pressed="true"]{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
.seg button:disabled{{opacity:.45;cursor:default}}
.crumb{{font-size:.9rem;color:var(--ink-2);display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline}} .crumb b{{color:var(--ink)}}
.ghead{{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:6px 2px 0;border-bottom:2px solid var(--line);margin-top:6px}}
.ghead h3{{font-size:.98rem}} .ghead span{{font-size:.8rem;color:var(--ink-3)}}
.fbar{{grid-template-columns:repeat(4,1fr)}}
@media (max-width:560px){{.dgrid{{grid-template-columns:1fr 1fr}} .fbar{{grid-template-columns:1fr 1fr}}}}
.prov{{border:1px solid var(--line);border-inline-start:4px solid var(--accent);background:var(--surface);border-radius:var(--radius);padding:10px 14px;font-size:.86rem;color:var(--ink-2)}}
table{{border-collapse:collapse;width:100%;font-size:.82rem;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius)}}
th,td{{padding:7px 9px;border-top:1px solid var(--line);text-align:right;vertical-align:top}} th{{background:var(--surface-2);border-top:0;font-weight:600;color:var(--ink-2)}}
.tbl{{overflow-x:auto}}
details{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:10px 14px}} summary{{cursor:pointer;font-weight:600}}
.check{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px;display:grid;gap:6px;font-size:.9rem}} .check label{{display:flex;gap:8px;align-items:flex-start}} .check input{{margin-top:5px}}
footer{{color:var(--ink-3);font-size:.78rem;display:flex;flex-direction:column;gap:4px}}
@media (max-width:560px){{.summary{{grid-template-columns:1fr 1fr}} .fbar{{grid-template-columns:1fr 1fr}} .lcard{{grid-template-columns:96px 1fr}} .lcard .ph,.lcard .noph{{width:96px;height:72px;grid-row:1/3}} .lcard .p{{grid-column:2;text-align:right}} .lcard .chips{{grid-column:1/3}} .lcard .d,.lcard .n,.lcard .r{{grid-column:1/3}}}}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">استديو أو غرفة وصالة · إيجار شهري · عزاب · الرياض</div>
  <h1>رادار شقق العليا</h1>
  <div class="anchor">
    <span>نقطة القياس: <b>برج المملكة، طريق الملك فهد</b></span>
    <span class="num">24.7114° N, 46.6745° E</span>
    <span>النطاق: 10 إلى 15 دقيقة بالسيارة</span>
    <span class="num">آخر تحديث: 2026-09-10</span>
  </div>
  <div class="status">
    <b>وضع البيانات: {n} إعلاناً مفتوحاً فعلياً، كل حقل منقول من صفحة الإعلان نفسها.</b>
    <p>فُتح كل إعلان مباشرة بتاريخ 2026-09-09 و2026-09-10، وكل بطاقة تحمل سطر "التحقق" الذي يذكر كيف ثبت أن الإعلان قائم. من قائمة الجلسة السابقة (47 إعلاناً) بقي {nkept} وحُذف {len(REMOVED)} بأسبابها (منها 6 إعلانات حراج تُفتح صفحاتها لكنها غائبة عن البحث الحي، أي منتهية) في جدول أسفل الصفحة، وأُضيف {nnew} إعلاناً جديداً من بحث مباشر في 12 حياً. أي حقل لم يظهر في الصفحة كُتب "غير مذكور". الصور مصغّرة من الصورة الأولى لكل إعلان، والرابط يفتح الإعلان الأصلي بكل صوره.</p>
  </div>
</header>
<section id="zones">
  <div class="sec-head"><h2>اختر الحي</h2><span class="hint">مرتبة من الأقرب للبرج. الضغط على الحي يفتح إعلاناته مصنفة</span></div>
  <div class="dgrid" id="dgrid"></div>
</section>
<section id="found">
  <div class="crumb" id="crumb"></div>
  <div class="sec-head"><h3>النوع</h3></div>
  <div class="seg" id="segType"></div>
  <div class="sec-head"><h3>المنصة</h3></div>
  <div class="seg" id="segPlat"></div>
  <div class="summary">
    <div class="tile"><div class="v num" id="tN">0</div><div class="k">إعلان في هذا القسم</div></div>
    <div class="tile"><div class="v num" id="tP">0</div><div class="k">بسعر شهري ظاهر</div></div>
    <div class="tile"><div class="v num" id="tMin">0</div><div class="k">أقل سعر (ريال)</div></div>
    <div class="tile"><div class="v num" id="tMed">0</div><div class="k">الوسيط (ريال)</div></div>
  </div>
  <div class="fbar">
    <label>الحد الأعلى للشهر (ريال)<input id="qMax" type="number" inputmode="numeric" min="0" step="100" placeholder="مثال 5000"></label>
    <label>الفرش<select id="qFurn"><option value="">الكل</option><option value="مفروش">مفروش</option><option value="غير مفروش">غير مفروش</option></select></label>
    <label>الترتيب<select id="qSort"><option value="price">الأرخص أولاً</option><option value="dist">الأقرب للبرج</option><option value="date">الأحدث نشراً</option></select></label>
    <label>العرض<select id="qGroup"><option value="plat">مجموعات حسب المنصة</option><option value="type">مجموعات حسب النوع</option><option value="flat">قائمة واحدة</option></select></label>
    <label class="chk"><input type="checkbox" id="qPriced"> بسعر ظاهر فقط</label>
    <label class="chk"><input type="checkbox" id="qNoFam" checked> استبعاد "عوائل فقط"</label>
    <label class="chk"><input type="checkbox" id="qNew"> الجديد فقط</label>
    <label class="chk"><input type="checkbox" id="qTrust"> الموثوق فقط (تقييم عالٍ أو رقم ورخصة)</label>
  </div>
  <div class="cards" id="cards"></div>
  <button type="button" class="btn more" id="more">عرض المزيد</button>
  <p class="prov">السعر "شهري" كما كتبه المعلن. إعلانات Airbnb تعرض سعر إقامة كاملة من 1 إلى 31 أكتوبر 2026 بعد خصم الشهر كما ظهر عند الفتح، وقد تُضاف رسوم عند الحجز. إعلانات عقار المعلمة "عقد سنوي بدفع شهري" هي عقود سنوية يقسّط إيجارها شهرياً. المسافة على الخط المستقيم من إحداثيات الإعلان إن وُجدت، وإلا من مركز الحي تقريباً.</p>
</section>
<section id="removed">
  <div class="sec-head"><h2>ما حُذف من القائمة السابقة</h2><span class="count">{len(REMOVED)} من 47</span></div>
  <details><summary>عرض الجدول</summary>
  <div class="tbl"><table><thead><tr><th>#</th><th>المنصة</th><th>الإعلان</th><th>سبب الحذف</th><th></th></tr></thead><tbody>{removed_rows}</tbody></table></div>
  </details>
</section>
<section id="checklist">
  <h2>قبل ما تدفع</h2>
  <div class="check">
    <label><input type="checkbox"> السعر المعلن شهري فعلاً وليس سنوياً مقسوماً؛ بعض المنصات تعرض السنوي افتراضياً.</label>
    <label><input type="checkbox"> الكهرباء والماء والإنترنت: مشمولة أم لا، والحد الأقصى إن كانت مشمولة.</label>
    <label><input type="checkbox"> التأمين وقيمته وشروط استرداده، ومدة الإشعار قبل المغادرة.</label>
    <label><input type="checkbox"> العقد موثق في منصة إيجار باسمك، حتى لو كان شهرياً.</label>
    <label><input type="checkbox"> موقف سيارة، ومدخل مستقل، وسياسة الزوار للعزاب.</label>
    <label><input type="checkbox"> زيارة فعلية أو مكالمة فيديو قبل أي تحويل، ولا تحويل لحساب شخصي بدون عقد.</label>
    <label><input type="checkbox"> جرّب المشوار للبرج في وقت ذروتك الحقيقي قبل التوقيع.</label>
  </div>
</section>
<footer>
  <p>المصادر: صفحات الإعلانات نفسها في بيوت وحراج وعقار وAirbnb ومبيت، فُتحت مباشرة بتاريخ 2026-09-09 و2026-09-10. بروبرتي فايندر: الإعلانات الأربعة السابقة انتهت ولم يظهر في صفحات الأحياء أي إعلان شهري. الصور مصغّرة من الصورة الأولى في كل إعلان.</p>
  <p>المسافات محسوبة برمجياً على الخط المستقيم وليست أزمنة قيادة مقاسة.</p>
</footer>
</div>
<script>
(function(){{
var L={data_js};
var $=function(id){{return document.getElementById(id)}};
var KM={{"العليا": 2.1, "السليمانية": 2.7, "الورود": 1.8, "المعذر الشمالي": 1.6, "الملك فهد": 3.7, "المروج": 3.9, "المحمدية": 3.6, "الرحمانية": 3.8, "الوزارات": 4.3, "التعاون": 6.5, "المصيف": 6.0, "النخيل": 5.8}};
var dgrid=$("dgrid"),segType=$("segType"),segPlat=$("segPlat"),crumb=$("crumb"),cards=$("cards"),more=$("more");
var qMax=$("qMax"),qFurn=$("qFurn"),qSort=$("qSort"),qGroup=$("qGroup"),qPriced=$("qPriced"),qNoFam=$("qNoFam"),qNew=$("qNew"),qTrust=$("qTrust");
var S={{dist:"",type:"",plat:""}};
var TYPES=["استديو","غرفة وصالة","غير محدد"], PLATS=["بيوت","حراج","عقار","Airbnb","مبيت"];
function esc(t){{return String(t==null?"":t).replace(/[&<>"']/g,function(m){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[m]}})}}
function fmt(n){{return Number(n).toLocaleString("en-US")}}
function base(x){{
  var mx=Number(qMax.value)||0;
  if(qFurn.value&&(x.furn||"").indexOf(qFurn.value)!==0)return false;
  if(qFurn.value==="مفروش"&&(x.furn||"").indexOf("غير مفروش")===0)return false;
  if(mx&&(!x.price||x.price>mx))return false;
  if(qPriced.checked&&!x.price)return false;
  if(qNoFam.checked&&x.flags.indexOf("عوائل فقط")>-1)return false;
  if(qNew.checked&&x.status!=="new")return false;
  if(qTrust.checked&&!x.trust)return false;
  return true}}
function pool(){{return L.filter(base)}}
function renderD(){{
  var P=pool(),c={{}},mn={{}};
  P.forEach(function(x){{c[x.dist]=(c[x.dist]||0)+1;if(x.price&&(!mn[x.dist]||x.price<mn[x.dist]))mn[x.dist]=x.price}});
  var names=Object.keys(KM).sort(function(a,b){{return KM[a]-KM[b]}});
  Object.keys(c).forEach(function(d){{if(names.indexOf(d)<0)names.push(d)}});
  dgrid.innerHTML="";
  var all=document.createElement("button");all.type="button";all.className="dtile";all.setAttribute("aria-pressed",S.dist===""?"true":"false");
  all.innerHTML='<span class="nm">كل الأحياء</span><span class="ct num">'+P.length+' إعلاناً</span><span class="mn">12 حياً حول البرج</span>';
  all.addEventListener("click",function(){{S.dist="";S.plat="";update(true)}});dgrid.appendChild(all);
  names.forEach(function(d){{
    var b=document.createElement("button");b.type="button";b.className="dtile";b.setAttribute("aria-pressed",S.dist===d?"true":"false");
    b.innerHTML='<span class="nm">'+esc(d)+'</span><span class="ct num">'+(c[d]||0)+' إعلاناً'+(KM[d]!=null?' · '+KM[d]+' كم':'')+'</span><span class="mn">'+(mn[d]?'يبدأ من '+fmt(mn[d])+' ريال':'لا سعر ظاهر')+'</span>';
    b.addEventListener("click",function(){{S.dist=d;S.plat="";update(true)}});dgrid.appendChild(b)}});
}}
function seg(el,opts,cur,cnt,set){{
  el.innerHTML="";
  var a=document.createElement("button");a.type="button";a.setAttribute("aria-pressed",cur===""?"true":"false");a.textContent="الكل ("+cnt[""]+")";a.addEventListener("click",function(){{set("")}});el.appendChild(a);
  opts.forEach(function(o){{var b=document.createElement("button");b.type="button";b.setAttribute("aria-pressed",cur===o?"true":"false");b.textContent=o+" ("+(cnt[o]||0)+")";b.disabled=!cnt[o];b.addEventListener("click",function(){{set(o)}});el.appendChild(b)}});
}}
var list=[],shown=40;
function update(scroll){{
  renderD();
  var P=pool().filter(function(x){{return !S.dist||x.dist===S.dist}});
  var ct={{"":P.length}};P.forEach(function(x){{ct[x.type]=(ct[x.type]||0)+1}});
  seg(segType,TYPES,S.type,ct,function(v){{S.type=v;update(false)}});
  var P2=P.filter(function(x){{return !S.type||x.type===S.type}});
  var cp={{"":P2.length}};P2.forEach(function(x){{cp[x.plat]=(cp[x.plat]||0)+1}});
  seg(segPlat,PLATS,S.plat,cp,function(v){{S.plat=v;update(false)}});
  list=P2.filter(function(x){{return !S.plat||x.plat===S.plat}});
  var s=qSort.value;
  list.sort(function(a,b){{
    if(s==="price")return (a.price?0:1)-(b.price?0:1)||(a.price||0)-(b.price||0)||(a.km||99)-(b.km||99);
    if(s==="dist")return (a.km||99)-(b.km||99)||(a.price||1e9)-(b.price||1e9);
    return String(b.date).localeCompare(String(a.date))||(a.price||1e9)-(b.price||1e9)}});
  crumb.innerHTML='<span>القسم: <b>'+esc(S.dist||"كل الأحياء")+'</b></span><span>النوع: <b>'+esc(S.type||"الكل")+'</b></span><span>المنصة: <b>'+esc(S.plat||"الكل")+'</b></span><span class="num"><b>'+list.length+'</b> إعلاناً</span>';
  shown=40;render();
  if(scroll){{$("found").scrollIntoView({{behavior:"smooth",block:"start"}})}}
}}
function card(x){{
  var c=document.createElement("article");c.className="lcard";
  var price=x.price?'<div class="p num">'+fmt(x.price)+' <small>ر.س، '+esc(x.per)+'</small></div>':'<div class="p unk">'+esc(x.priceText||"السعر عند الفتح")+(x.per&&x.per!=="شهري"?'<small>'+esc(x.per)+'</small>':'')+'</div>';
  var chips='<span class="chip">'+esc(x.plat)+'</span>'+(x.status==="new"?'<span class="chip new">جديد</span>':'<span class="chip">من القائمة السابقة #'+x.old+'</span>')+(x.furn&&x.furn!=="غير مذكور"?'<span class="chip">'+esc(x.furn)+'</span>':'')+(x.incl&&x.incl!=="غير مذكور"&&x.incl.indexOf("حسب")!==0&&x.incl.indexOf("غير شامل")!==0?'<span class="chip ok">شامل: '+esc(x.incl)+'</span>':'')+(x.trust?'<span class="chip ok">موثوق: '+esc(x.trustWhy)+'</span>':'')+x.flags.map(function(f){{return '<span class="chip '+(f==="عوائل فقط"?"bad":"warn")+'">'+esc(f)+'</span>'}}).join('')+(x.km!=null?'<span class="chip num">'+x.km+' كم من البرج'+(x.kmSrc==="مركز الحي تقريباً"?" (تقريبي)":"")+'</span>':'');
  var img=x.imgd?'<img class="ph" loading="lazy" alt="" src="'+x.imgd+'">':'<div class="noph">'+(x.plat==="حراج"?"الصورة داخل الإعلان":"لا صورة")+'</div>';
  var d='<div class="d"><b>المساحة</b><span>'+esc(x.area)+(typeof x.area==="number"?" م²":"")+'</span><b>الدور</b><span>'+esc(x.floor)+'</span><b>يشمل</b><span>'+esc(x.incl)+'</span><b>الحي والشارع</b><span>'+esc(x.dist)+(x.street&&x.street!=="غير مذكور"?"، "+esc(x.street):"")+'</span><b>التواصل</b><span>'+(/^[+0-9]/.test(x.phone)?'<a href="tel:'+esc(x.phone.replace(/\s/g,""))+'">'+esc(x.phone)+'</a>':esc(x.phone))+'</span><b>تاريخ النشر</b><span>'+esc(x.date)+'</span></div>';
  c.innerHTML=img+'<div class="t">'+esc(x.type)+' في '+esc(x.dist)+'</div>'+price+'<div class="chips">'+chips+'</div>'+d+(x.note?'<div class="n">'+esc(x.note)+'</div>':'')+'<div class="r"><a class="btn primary" href="'+esc(x.url)+'" target="_blank" rel="noopener">فتح الإعلان وكل الصور</a>'+(x.img?'<a class="btn" href="'+esc(x.img)+'" target="_blank" rel="noopener">الصورة الأولى بالحجم الكامل</a>':'')+'</div>';
  return c}}
function render(){{
  var ps=list.filter(function(x){{return x.price}}).map(function(x){{return x.price}}).sort(function(a,b){{return a-b}});
  $("tN").textContent=list.length;$("tP").textContent=ps.length;$("tMin").textContent=ps.length?fmt(ps[0]):"0";$("tMed").textContent=ps.length?fmt(ps[Math.floor(ps.length/2)]):"0";
  cards.innerHTML="";
  var g=qGroup.value, sub=list.slice(0,shown);
  if(g==="flat"){{sub.forEach(function(x){{cards.appendChild(card(x))}})}}
  else{{
    var key=g==="plat"?"plat":"type", order=g==="plat"?PLATS:TYPES, groups={{}};
    list.forEach(function(x){{(groups[x[key]]=groups[x[key]]||[]).push(x)}});
    var left=shown;
    order.filter(function(k){{return groups[k]}}).forEach(function(k){{
      if(left<=0)return;
      var h=document.createElement("div");h.className="ghead";h.innerHTML='<h3>'+esc(k)+'</h3><span class="num">'+groups[k].length+' إعلاناً</span>';cards.appendChild(h);
      groups[k].slice(0,left).forEach(function(x){{cards.appendChild(card(x))}});left-=groups[k].length}});
  }}
  more.hidden=list.length<=shown;more.textContent="عرض المزيد ("+Math.max(0,list.length-shown)+" متبقية)"}}
[qMax,qFurn,qSort,qGroup,qPriced,qNoFam,qNew,qTrust].forEach(function(el){{el.addEventListener("change",function(){{update(false)}});el.addEventListener("input",function(){{update(false)}})}});
more.addEventListener("click",function(){{shown+=40;render()}});
update(false);
}})();
</script>
'''
open('radar.html','w',encoding='utf-8').write(page)
print('bytes',len(page.encode()),'listings',n)
