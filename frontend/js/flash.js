const item=()=>({name:$('fN').value,category:$('fC').value,packaging:$('fP').value,uses:+$('fU').value,original_price:+$('fO').value,months_left:+$('fM').value,ingredients:$('fI').value});
async function est(){try{const d=await post('/api/price-estimate',item());
 $('fOut').innerHTML=d.eligible?`<p>Suggested price: <b>₹${d.price}</b></p>`:`<div class="alert">${d.reason}</div>`}catch(e){err('fOut',e)}}
async function list(){try{const d=await post('/api/listings',item());$('fOut').innerHTML=`<p>Listed <b>${d.name}</b> for ₹${d.price}.</p>`}catch(e){err('fOut',e)}}
async function market(){try{const d=await post('/api/listings/match',profile());
 $('mkt').innerHTML=d.length?d.sort((a,b)=>b.match.score-a.match.score).map(i=>`<div class="card"><h3>${i.name}</h3><p>₹${i.price} · ${i.packaging}, used ${i.uses}×</p>${chips([i.match.score+'/100 · '+i.match.verdict],i.match.score>=75?'g':i.match.score<50?'r':'')}</div>`).join(''):'<p class="empty">Nothing listed yet. Be the first to list a product.</p>'}catch(e){err('mkt',e)}}
