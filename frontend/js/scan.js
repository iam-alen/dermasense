async function scan(){const f=$('face').files[0];if(!f)return err('scanOut',{message:'Choose a photo first.'});
 $('scanOut').innerHTML='<p class="empty">Reading your skin…</p>';const fd=new FormData();fd.append('file',f);
 try{const d=await api('/api/skin/analyze',{method:'POST',body:fd});
  $('stype').value=d.skin_type;$('conc').value=d.concerns.join(', ');
  $('scanOut').innerHTML=`<br>${chips([d.skin_tone+' tone',d.skin_type+' skin',d.face_shape+' face'])}${chips(d.concerns,'r')}<p class="muted">${d.note} Your profile below is filled in. Edit anything that looks off.</p>`}
 catch(e){err('scanOut',e)}}
async function routine(){try{const d=await post('/api/routine',profile());
 $('routineOut').innerHTML=`<h3 style="margin-top:18px">Morning</h3>${li(d.morning)}<h3>Night</h3>${li(d.night)}`}catch(e){err('routineOut',e)}}
