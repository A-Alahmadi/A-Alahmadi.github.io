const { chromium } = require('playwright'); const fs=require('fs');
const [,, listFile, outFile] = process.argv;
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium', headless:true, args:['--no-sandbox','--disable-features=PostQuantumKyber,UseMLKEM,EncryptedClientHello','--disable-quic','--ssl-version-max=tls1.2'], proxy:{server:process.env.HTTPS_PROXY} });
  const ctx = await b.newContext({ locale:'ar-SA', viewport:{width:1280,height:900}, ignoreHTTPSErrors:true, userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' });
  const out={};
  for (const line of fs.readFileSync(listFile,'utf8').split('\n').filter(Boolean)) {
    const [key,q]=line.split('\t'); const p=await ctx.newPage();
    try {
      await p.goto('https://haraj.com.sa/search/'+encodeURIComponent(q)+'/',{waitUntil:'domcontentloaded',timeout:90000});
      await p.waitForTimeout(6000);
      for(let i=0;i<4;i++){ await p.mouse.wheel(0,3000); await p.waitForTimeout(2000); }
      const items = await p.evaluate(()=>{
        const seen={}; const res=[];
        document.querySelectorAll('a[href]').forEach(a=>{
          const m=a.getAttribute('href').match(/^\/(\d{8,12})\//); if(!m) return; const id=m[1]; if(seen[id]) return;
          const card=a.closest('article')||a.closest('li')||a.closest('div'); const txt=(card?card.innerText:a.innerText)||'';
          seen[id]=1; res.push({id, href:a.getAttribute('href'), text:txt.replace(/\s+/g,' ').slice(0,260)});
        }); return res; });
      out[key]=items; console.log(key, items.length);
    } catch(e){ console.log(key,'ERR',e.message.slice(0,100)); out[key]=[]; }
    await p.close();
  }
  fs.writeFileSync(outFile, JSON.stringify(out,null,1)); await b.close();
})();
