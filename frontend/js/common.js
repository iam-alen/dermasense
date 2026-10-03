const $=id=>document.getElementById(id),csv=v=>v.split(',').map(s=>s.trim()).filter(Boolean);
const chips=(a,c='')=>a.map(x=>`<span class="chip ${c}">${x}</span>`).join('');
const li=a=>a.length?'<ul>'+a.map(x=>`<li>${x}</li>`).join('')+'</ul>':'';
const token=()=>localStorage.getItem('ds_token');
if(document.body.dataset.protected&&!token())location.replace('login.html');
async function api(url,opt={}){opt.headers={...(opt.headers||{}),...(token()?{Authorization:'Bearer '+token()}:{})};
 try{const r=await fetch(url,opt),d=await r.json();
  if(!r.ok)throw new Error(typeof d.detail=='string'?d.detail:'Please check your entries and try again.');return d}
 catch(e){throw new Error(e.message=='Failed to fetch'?"Can't reach the server. Start it with: uvicorn main:app":e.message)}}
const post=(u,b)=>api(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});
const err=(id,e)=>$(id).innerHTML=`<div class="alert">${e.message}</div>`;
// Profile is saved so every page can use what the scan found.
const DEF={skin_type:'Combination',concerns:[],allergies:[],avoid:[]};
function profile(){if($('stype')){const p={skin_type:$('stype').value,concerns:csv($('conc').value),allergies:csv($('alg').value),avoid:csv($('avd').value)};
 localStorage.setItem('ds_profile',JSON.stringify(p));return p}
 try{return JSON.parse(localStorage.getItem('ds_profile'))||DEF}catch{return DEF}}
if($('stype')){const p=profile();$('stype').value=p.skin_type;$('conc').value=p.concerns.join(', ');$('alg').value=p.allergies.join(', ');$('avd').value=p.avoid.join(', ')}
// Shared navigation and footer: edit links here once.
const here=location.pathname.split('/').pop()||'index.html';
const L=[['index.html','Home'],['scan.html','Skin scan'],['check.html','Product check'],['sos.html','Skin SOS'],['flash.html','DermaFlash']];
const user=token()?localStorage.getItem('ds_name'):null;
$('nav').innerHTML=`<a class="logo" href="index.html" style="font:700 1.7rem 'Cormorant Garamond',serif">Derma<i style="color:var(--rose)">Sense</i></a>`+
 L.map(([h,t])=>`<a href="${h}" class="${h==here?'on':''}">${t}</a>`).join('')+
 (user?`<a href="#" id="out">Log out (${user})</a>`:`<a href="login.html" class="${here=='login.html'?'on':''}">Log in</a><a href="signup.html" class="cta">Sign up</a>`);
if($('out'))$('out').onclick=e=>{e.preventDefault();localStorage.removeItem('ds_token');localStorage.removeItem('ds_name');location='index.html'};
$('foot').textContent='DermaSense gives general skincare guidance, not medical advice.';
