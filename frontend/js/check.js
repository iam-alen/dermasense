async function ocr(){const fd=new FormData();fd.append('file',$('label').files[0]);
 try{const d=await api('/api/product/ocr',{method:'POST',body:fd});$('ings').value=d.ingredients}catch(e){err('checkOut',e)}}
async function check(){if(!$('ings').value.trim())return err('checkOut',{message:'Paste an ingredient list first.'});
 try{const d=await post('/api/product/analyze',{ingredients:$('ings').value,profile:profile()});
  $('checkOut').innerHTML=`<div class="score">${d.score}</div><h3>${d.verdict}</h3>
  ${d.why_good.length?'<p><b>Working for you</b></p>'+li(d.why_good):''}${d.why_not.length?'<p><b>Watch out for</b></p>'+li(d.why_not):''}
  ${!d.why_good.length&&!d.why_not.length?'<p class="muted">No known ingredients matched. Add more of the list for a better read.</p>':''}`}catch(e){err('checkOut',e)}}
async function clash(){try{const d=await post('/api/conflicts',{products:$('stack').value.split('\n').filter(Boolean)});
 $('clashOut').innerHTML=d.conflicts.length?li(d.conflicts):'<p class="muted">No clashes found. Nice stack.</p>'}catch(e){err('clashOut',e)}}
