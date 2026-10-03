async function sos(){if(!$('sosQ').value.trim())return err('sosOut',{message:'Describe what you\'re seeing, like "red and itchy".'});
 try{const d=await api(`/api/remedies?q=${encodeURIComponent($('sosQ').value)}&product=${encodeURIComponent($('sosP').value)}`);
  let h=`<div class="alert"><b>${d.stop_product}</b></div>`;
  h+=d.matches.length?d.matches.map(m=>`<h3 style="margin-top:20px">For ${m.concern}</h3>`+m.remedies.map(r=>`<p><b>${r.name}.</b> ${r.how}<br><span class="muted">${r.why}</span></p>`).join('')).join(''):'<p class="muted">No exact match. Try words like red, itchy, burning, dry or pimples.</p>';
  h+=`<p>${d.avoid}</p><h3>See a doctor if you have</h3>${chips(d.see_doctor_if,'r')}<p class="muted">${d.disclaimer}</p>`;$('sosOut').innerHTML=h}catch(e){err('sosOut',e)}}
