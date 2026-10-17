/* Online environment enhancement. OPTIONAL. Gameplay and bundled scene art never use a remote resource. */
(function(){
 const SETTINGS={enabled:true,endpoint:'/api/ward-art'};
 const cache=new Map(),requests=new Set(),unavailable=new Set();let backendUnavailable=false;
 try{const o=JSON.parse(localStorage.getItem('lw_c1_atmosphere_cache_v1')||'{}');for(const [k,v] of Object.entries(o))if(typeof v==='string'&&/^https?:\/\//.test(v))cache.set(k,v)}catch(e){};
 function persistCache(){try{localStorage.setItem('lw_c1_atmosphere_cache_v1',JSON.stringify(Object.fromEntries([...cache].slice(-90))))}catch(e){}}
 function readSettings(){try{const v=localStorage.getItem('lw_online_art_settings');if(v){const x=JSON.parse(v);SETTINGS.enabled=!!x.enabled;if(typeof x.endpoint==='string'&&/^https?:\/\/|^\//.test(x.endpoint))SETTINGS.endpoint=x.endpoint}}catch(e){}}
 readSettings();
 function key(room){return `${S?.seed||'base'}::${room}::${S?.f?.power?'powered':'dark'}`;}
 function urlFor(room){const value=cache.get(key(room));if(!SETTINGS.enabled||!value)return '';try{return new URL(value,location.href).origin===location.origin?value:''}catch(e){return ''}}
 function prepare(room){if(!SETTINGS.enabled||backendUnavailable||navigator.onLine===false||!S||!/^https?:$/.test(location.protocol))return;const k=key(room);if(cache.has(k)||requests.has(k)||unavailable.has(k))return;requests.add(k);
  const timer=new AbortController(),timeout=setTimeout(()=>timer.abort(),9000);
  fetch(SETTINGS.endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({room,roomName:R[room].n,seed:S.seed,powered:!!S.f.power,chapter:1,style:'1998 analog cinematic medical horror; abstract dust and light texture only; NO environment, doors, objects or text'}),signal:timer.signal})
   .then(r=>{if(!r.ok){if([404,501,503].includes(r.status))backendUnavailable=true;throw Error('art service unavailable')}return r.json()})
   .then(data=>{if(!data||typeof data.image_url!=='string'||!/^https?:\/\//.test(data.image_url))throw Error('unexpected image response');const u=new URL(data.image_url,location.href);if(u.origin!==location.origin)throw Error('image must be same-origin');cache.set(k,u.href);persistCache();if(S.room===room)renderScene();})
   .catch(()=>{unavailable.add(k);/* bundled local room view continues uninterrupted */})
   .finally(()=>{requests.delete(k);clearTimeout(timeout)});
 }
 function update(enabled,endpoint){SETTINGS.enabled=!!enabled;backendUnavailable=false;if(endpoint)SETTINGS.endpoint=endpoint;try{localStorage.setItem('lw_online_art_settings',JSON.stringify(SETTINGS))}catch(e){}if(S&&enabled)prepare(S.room)}
 window.WardArt={urlFor,prepare,update,settings:SETTINGS};
 const baseRender=render;render=function(){baseRender();if(S)prepare(S.room)};
})();
