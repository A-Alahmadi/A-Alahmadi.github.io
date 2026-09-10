// usage: node pw_fetch.js <listfile: id<TAB>url per line> <outdir> [waitTitleRegex] [extraWaitMs]
const { chromium } = require('playwright'); const fs=require('fs');
const [,, listFile, outDir, badTitle='Security check', extraWait='6000'] = process.argv;
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium', headless:true,
    args:['--no-sandbox','--disable-features=PostQuantumKyber,UseMLKEM,EncryptedClientHello','--disable-quic','--ssl-version-max=tls1.2'],
    proxy:{server:process.env.HTTPS_PROXY} });
  const ctx = await b.newContext({ locale:'ar-SA', viewport:{width:1280,height:900}, ignoreHTTPSErrors:true,
    userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' });
  fs.mkdirSync(outDir,{recursive:true});
  const lines = fs.readFileSync(listFile,'utf8').split('\n').filter(Boolean);
  for (const line of lines) {
    const [id,url] = line.split('\t'); const p = await ctx.newPage(); const jsons=[];
    p.on('response', async r => { try { const ct=r.headers()['content-type']||''; if(/json/.test(ct) && r.status()===200){ const t=await r.text(); if(t.length<3000000) jsons.push({url:r.url(),body:t}); } } catch(e){} });
    let status='ERR', title='';
    try {
      const r = await p.goto(url,{waitUntil:'domcontentloaded',timeout:90000}); status=r?r.status():'nil';
      for (let i=0;i<10;i++){ await p.waitForTimeout(3000); title=await p.title(); if(!(new RegExp(badTitle,'i')).test(title)) break; }
      await p.waitForTimeout(Number(extraWait));
      title=await p.title();
      fs.writeFileSync(`${outDir}/${id}.html`, await p.content());
      fs.writeFileSync(`${outDir}/${id}.json`, JSON.stringify(jsons));
      try { await p.screenshot({path:`${outDir}/${id}.png`, fullPage:false}); } catch(e){}
    } catch(e){ title='ERR '+e.message.slice(0,120); }
    console.log(`${id}\t${status}\t${p.url()}\t${title.slice(0,90)}\tjson=${jsons.length}`);
    await p.close();
  }
  await b.close();
})().catch(e=>{console.error('FATAL',e.message);process.exit(1)});
