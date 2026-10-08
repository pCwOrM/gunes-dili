const M=require('./motor.js'); const B=require('./beklenen.json');
let n=0,tokOk=0,gdOk=0; const hata=[];
const t0=Date.now();
for(const row of B){
  const rs=M.cozumleCumle(row.map(x=>x[0]));
  row.forEach(([w,tk,gd],i)=>{
    const r=rs[i]; n++;
    const t=(r.tokenlar||[]).map(([b,e])=>b+'/'+e.islev).join('+');
    const g=r.tokenlar&&r.tokenlar.length?M.turkceden(r):null;
    if(t===tk)tokOk++; else if(hata.length<15)hata.push([w,tk,t]);
    if((g?g.kelime:null)===gd)gdOk++; else if(hata.length<15)hata.push(['GD',w,gd,g&&g.kelime]);
  });
}
console.log(`kelime ${n}  Türkçe çözümleme eşleşme ${(100*tokOk/n).toFixed(2)}%  Güneş Dili eşleşme ${(100*gdOk/n).toFixed(2)}%  süre ${Date.now()-t0}ms`);
console.log(JSON.stringify(hata,null,0));
