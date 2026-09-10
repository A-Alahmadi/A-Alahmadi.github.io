const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium', headless:true, args:['--no-sandbox','--disable-features=PostQuantumKyber,UseMLKEM,EncryptedClientHello','--disable-quic','--ssl-version-max=tls1.2'], proxy:{server:process.env.HTTPS_PROXY} });
  const ctx = await b.newContext({ locale:'ar-SA', viewport:{width:1280,height:900}, ignoreHTTPSErrors:true, userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' });
  const out=[];
  for (const line of fs.readFileSync('list_hv.txt','utf8').split('\n').filter(Boolean)) {
    const [id,url]=line.split('\t'); const p=await ctx.newPage(); let r={id,url};
    try {
      const resp=await p.goto(url,{waitUntil:'domcontentloaded',timeout:90000}); r.status=resp?resp.status():null;
      await p.waitForTimeout(7000);
      r.final=p.url(); r.title=await p.title();
      const t=await p.evaluate(()=>document.body.innerText);
      r.markers=['غير موجود','تم حذف','محذوف','منتهي','غير متاح','لا يوجد إعلان','هذا الإعلان','404','تم البيع','مغلق','الصفحة غير موجودة'].filter(m=>t.includes(m));
      r.hasTitleInBody=t.includes((r.title||'').split('|')[0].trim().slice(0,25));
      r.snippet=t.replace(/\s+/g,' ').slice(0,300);
      r.dateText=(t.match(/(قبل [^\n]{2,20}|أمس|أول أمس|الأسبوع الماضي|منذ [^\n]{2,20})/)||[])[0]||null;
    } catch(e){ r.err=e.message.slice(0,120); }
    out.push(r); console.log(id,r.status,'|',r.markers,'|',r.hasTitleInBody,'|',r.dateText,'|',(r.title||'').slice(0,50)); await p.close();
  }
  fs.writeFileSync('hverify.json',JSON.stringify(out,null,1)); await b.close();
})();
