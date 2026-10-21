/* Online is a preference, never a prerequisite for the authored hospital. */
(function(){'use strict';
const settings={enabled:true,endpoint:null,available:false},cache=new Map(),pending=new Map(),failed=new Set(),controllers=new Set(),decoding=new Set();
let mode='online',phase='checking',reason='Checking the connected artwork service.',capability=null,revision=0,modeEpoch=0;
try{if(localStorage.getItem('lw_art_mode')==='offline')mode='offline';}catch(e){}
settings.enabled=mode!=='offline';
function status(){return {mode,phase,available:settings.available,reason};}
function badge(){const node=document.querySelector('.hud-local-art');if(!node)return;node.replaceChildren();const icon=document.createElement('span');icon.setAttribute('aria-hidden','true');icon.textContent=phase==='active'?'◉':'○';node.append(icon,document.createTextNode(mode==='offline'?'Offline artwork':phase==='active'?'Online artwork':phase==='checking'?'Checking online artwork':'Online preferred · local art'));node.title=reason;node.dataset.artState=phase;}
function announce(){badge();const note=document.getElementById('onlineArtStatus'),toggle=document.getElementById('onlineArtSetting');if(note)note.textContent=reason;if(toggle)toggle.checked=settings.enabled;document.dispatchEvent(new CustomEvent('ward:art-status',{detail:status()}));}
function setStatus(value,text){if(phase===value&&reason===text)return;phase=value;reason=text;announce();}
async function capabilities(force=false){
 if(capability&&!force)return capability;
 const own=++revision;setStatus('checking','Checking the connected artwork service.');
 capability=(async()=>{const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),4000);controllers.add(controller);
  try{const response=await fetch('data/art_service.json'+(force?'?check='+Date.now():''),{cache:'no-store',signal:controller.signal});if(!response.ok)throw Error('Unavailable');const info=await response.json(),endpoint=info.endpoint?new URL(info.endpoint,location.href):null;if(own!==revision)return false;
   settings.available=info.available===true&&endpoint?.origin===location.origin;settings.endpoint=settings.available?endpoint.pathname+endpoint.search:null;
   if(!settings.available&&mode!=='offline')setStatus('local','No online artwork service is connected. The complete bundled artwork is active.');return settings.available;
  }catch(e){if(own===revision){settings.available=false;settings.endpoint=null;if(mode!=='offline')setStatus('local','The online artwork service could not be reached. Bundled artwork remains active.');}return false;}
  finally{clearTimeout(timer);controllers.delete(controller);}
 })();return capability;
}
function identity(room){return room+'|'+String(typeof S!=='undefined'&&S?.seed||'')+'|'+(typeof S!=='undefined'&&S?.f.power&&!S?.f.powerOut?'powered':'emergency');}
function sync(){
 const frame=document.querySelector('.room-view-frame');if(!frame)return;
 const room=typeof S!=='undefined'?S?.room:null,key=room?identity(room):'',url=mode!=='offline'?cache.get(key):null;let layer=frame.querySelector('.room-online-atmosphere');
 if(!url){layer?.remove();if(mode!=='offline'&&settings.available)setStatus(failed.has(key)?'local':'checking',failed.has(key)?'Online atmosphere is unavailable for this room. The complete bundled artwork is active.':'Loading optional online atmosphere. Bundled artwork remains active.');return;}if(window.WardWinter?.isPaused?.())return;
 if(!layer){layer=document.createElement('img');layer.className='room-online-atmosphere';layer.alt='';layer.setAttribute('aria-hidden','true');frame.append(layer);}
 if(layer.dataset.key!==key){layer.src=url;layer.dataset.key=key;}setStatus('active','Online atmosphere is active. Room artwork, doors and clues retain their authored positions.');
}
async function prepare(room){
 if(!room||mode==='offline')return sync();
 const key=identity(room),epoch=modeEpoch,seed=typeof S!=='undefined'?S?.seed:null,powered=typeof S!=='undefined'?!!S?.f.power&&!S?.f.powerOut:false;
 sync();if(!await capabilities()||mode==='offline'||epoch!==modeEpoch||typeof S==='undefined'||S?.room!==room||identity(room)!==key)return;
 if(cache.has(key))return sync();if(pending.has(key))return pending.get(key);if(failed.has(key))return;
 let task;task=(async()=>{const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),150000);controllers.add(controller);let image=null;
  try{const response=await fetch(settings.endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({room,seed,powered}),signal:controller.signal});if(!response.ok)throw Error('Unavailable');const value=await response.json();if(mode==='offline'||epoch!==modeEpoch||S?.seed!==seed)return;const url=new URL(value.image_url,location.href);if(url.origin!==location.origin||!/^https?:$/.test(url.protocol))throw Error('Invalid artwork origin');image=new Image();decoding.add(image);image.src=url.href;await image.decode();if(mode==='offline'||epoch!==modeEpoch||S?.seed!==seed)return;cache.set(key,url.href);if(cache.size>60)cache.delete(cache.keys().next().value);sync();
  }catch(e){if(epoch!==modeEpoch||mode==='offline')return;failed.add(key);if(S?.room&&identity(S.room)===key)setStatus('local','Online atmosphere is unavailable for this room. The complete bundled artwork is active.');}
  finally{clearTimeout(timer);controllers.delete(controller);if(image)decoding.delete(image);if(pending.get(key)===task)pending.delete(key);}
 })();pending.set(key,task);return task;
}
function setMode(value){const next=value==='offline'?'offline':'online';if(next!==mode)modeEpoch++;mode=next;settings.enabled=mode!=='offline';try{localStorage.setItem('lw_art_mode',mode);}catch(e){}for(const input of document.querySelectorAll('input[name="artMode"]'))input.checked=input.value===mode;
 if(mode==='offline'){revision++;capability=null;settings.available=false;settings.endpoint=null;for(const controller of controllers)controller.abort();controllers.clear();for(const image of decoding)image.src='';decoding.clear();pending.clear();setStatus('offline','All artwork is loaded from the downloaded game. No online artwork requests are made.');sync();return;}
 setStatus('checking','Checking the connected artwork service.');
 return capabilities().then(available=>{if(mode==='offline')return;if(!available)setStatus('local','No online artwork service is connected. The complete bundled artwork is active.');if(typeof S!=='undefined'&&S?.room)return prepare(S.room);});
}
window.WardArt={settings,status,refreshBadge:badge,setMode,update:enabled=>setMode(enabled?'online':'offline'),prepare,sync,urlFor:room=>cache.get(identity(room))||'',recheck:()=>{if(mode==='offline'||phase==='checking')return;failed.clear();return capabilities(true).then(()=>{if(typeof S!=='undefined'&&S?.room)prepare(S.room);});}};
document.addEventListener('ward:resume',sync);document.addEventListener('DOMContentLoaded',badge);
})();
