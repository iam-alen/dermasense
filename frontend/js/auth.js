const mode=document.body.dataset.mode;
$('f').onsubmit=async e=>{e.preventDefault();
 const b={email:$('email').value,password:$('pw').value};if(mode=='signup')b.name=$('name').value;
 try{const d=await post('/api/auth/'+mode,b);localStorage.setItem('ds_token',d.token);localStorage.setItem('ds_name',d.name);location='scan.html'}
 catch(x){err('msg',x)}};
