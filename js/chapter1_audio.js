/* Local recorded sound bus. No oscillators or generated electronic fallback tones.
   Positional cues follow the same graph as the pursuer, not random timers. */
(function(){
'use strict';
const clips={door:'door_open',doorClose:'door_close',shot:'gunshot',reload:'reload',phone:'phone_ring',generator:'generator_start',elevator:'elevator',relay:'relay',metal:'metal',mechanism:'mechanism',impact:'impact',kill:'impact',hit:'impact',knife:'metal',pickup:'cloth',click:'switch',combine:'cloth',heal:'cloth',escape:'step_tile_1',glass:'glass'};
const active=new Set(),loops=new Map(),history=[];let ctx=null,stepAt=0,ringAt=0,infectedAt=0,lastRoom='',variant=0;
const paths=p=>window.WardEmbeddedAssets?.['audio/chapter1/'+p+'.ogg']||'audio/chapter1/'+p+'.ogg';
function context(){if(!ctx){const A=window.AudioContext||window.webkitAudioContext;if(A)try{ctx=new A()}catch(e){}}if(ctx?.state==='suspended')ctx.resume().catch(()=>{});return ctx;}
function caption(text){if(!window.WardScene?.options.soundCaptions)return;const el=$('c1SoundCaption');if(el){el.textContent=text;clearTimeout(el._clear);el._clear=setTimeout(()=>{if(el.isConnected)el.textContent=''},4500)}}
function play(name,{volume=.45,pan=0,rate=1,bus='fx',loop=false}={}){if(!audio.enabled||document.hidden)return null;const a=new Audio(paths(name));a.dataset.clip=name;if(name==='elevator')a.dataset.ending='true';a.volume=Math.max(0,Math.min(.8,volume*(S?.audio?.[bus]??.45)));a.playbackRate=rate;a.loop=loop;a.preload='auto';const c=context();if(c)try{const source=c.createMediaElementSource(a),node=c.createStereoPanner();node.pan.value=Math.max(-1,Math.min(1,pan));source.connect(node);node.connect(c.destination)}catch(e){}
 if(active.size>=12&&!loop){const first=[...active].find(a=>!a.loop);first?.pause();if(first)active.delete(first)}active.add(a);a.addEventListener('ended',()=>active.delete(a),{once:true});a.addEventListener('error',()=>{active.delete(a);console.warn('Missing local recording',name)},{once:true});a.play().catch(()=>active.delete(a));history.push({name,pan,rate,bus});if(history.length>80)history.shift();return a;}
function loop(key,name,volume){const old=loops.get(key);if(old?.name===name){old.audio.volume=Math.min(.5,volume*(S?.audio?.amb??.3));return;}if(old){old.audio.pause();active.delete(old.audio);loops.delete(key)}if(!name)return;const a=play(name,{volume,bus:'amb',loop:true});if(a)loops.set(key,{name,audio:a});}
function stop(keepEnding=false){for(const a of [...active])if(!keepEnding||a.dataset.ending!=='true'){a.pause();active.delete(a)}loops.clear();}
function distance(){if(!S?.pursuer?.active)return {distance:99,pan:0};if(S.pursuer.room===S.room)return {distance:0,pan:0};const path=pursuerPath(S.pursuer.room,S.room);if(!path.length)return {distance:99,pan:0};const reverse=pursuerPath(S.room,S.pursuer.room),next=reverse[1],door=roomConnections().find(d=>d.to===next),rect=door&&window.WardScenes?.[S.room]?.doors[door.id];return {distance:path.length-1,pan:rect?(rect[0]-50)/60:0};}
function sync(){if(!S||!audio.enabled||S.hp<=0){stop();return;}if(S.f.chapter1Complete){stop(true);return;}const r=S.room;
 if(r!==lastRoom){lastRoom=r;ringAt=0;stepAt=0;infectedAt=0;}
 const water=['lobby','eastcorridor','tunnel','coldstore'].includes(r),machine=['generator','powercontrol','boiler','laundry'].includes(r);
 const ambience=water?(r==='lobby'?'rain':'water'):machine?(S.f.power||r==='boiler'?'machine':null):['security','observation'].includes(r)?'room_hum':null;
 loop('room',ambience,water?.22:.16);loop('intro',S.f.introComplete?null:'room_hum',.12);
 if(S.f.sprinklerTriggered&&!S.f.sprinklerStopped&&r==='eastcorridor')loop('sprinkler','water',.4);else loop('sprinkler',null,0);
 if(S.hp<=50)loop('breathing','breathing',S.hp<=25?.25:.12);else loop('breathing',null,0);
 const now=performance.now(),d=distance();
 if(d.distance<=3&&!SAFE_FROM_PURSUER.has(r)&&now>=stepAt){variant=1-variant;play('subject_step_'+(variant+1),{volume:[.85,.55,.28,.13][d.distance],pan:d.pan,rate:.96});stepAt=now+(S.f.pursuerEncounter?1050:1650);caption(d.distance===0?'Heavy boots inside this room':d.distance===1?'Heavy boots beyond the '+(d.pan<0?'left':'right')+' doorway':'Heavy footsteps farther along the passage');}
 if(alive(r)&&now>=infectedAt){play('infected_step',{volume:.22,pan:.3,rate:.88});infectedAt=now+2600;caption('Uneven footsteps nearby');}
 if(S.f.phoneRinging&&S.f.ringingPhoneRoom===r&&now>=ringAt){play('phone_ring',{volume:.65});ringAt=now+5700;caption('A telephone rings in this room');}
}
window.WardSound={play,sync,stop,distance,history,paths,snapshot:()=>[...active].map(a=>({clip:a.dataset.clip,paused:a.paused,time:a.currentTime,ready:a.readyState}))};
initAudio=function(){audio.enabled=true;context();setAudioUI();sync()};
toggleAudio=function(){audio.enabled=!audio.enabled;if(audio.enabled){context();sync()}else stop();setAudioUI()};
soundEffect=function(kind){if(kind==='phone')ringAt=performance.now()+5700;const name=clips[kind];if(name)play(name,{volume:kind==='shot'?.65:kind==='phone'?.55:.4,bus:kind==='click'?'ui':'fx'});if(kind==='shot'&&window.WardScene?.options.flashes){document.body.classList.add('c1-shot-flash');setTimeout(()=>document.body.classList.remove('c1-shot-flash'),160)};};
const baseGo=go;go=function(...args){const before=S?.room,result=baseGo(...args);if(S&&S.room!==before){if(S.hp<=50&&window.WardScene?.options.shake){document.body.classList.add('c1-camera-limp');setTimeout(()=>document.body.classList.remove('c1-camera-limp'),550)}const name=S.f.wet?'step_wet':['chapel','residence','stafflounge'].includes(S.room)?'step_wood':'step_tile_1';play(name,{rate:S.hp<=25?.72:S.hp<=50?.86:1,volume:.4});setTimeout(()=>{if(S?.room!==before)play(S.f.wet?'step_wet':'step_tile_2',{rate:S.hp<=50?.85:1,volume:.3})},520);sync()}return result};
document.addEventListener('visibilitychange',()=>document.hidden?stop():sync());
setInterval(sync,350);
})();
