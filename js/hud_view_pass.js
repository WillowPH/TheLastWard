/* Mouse-first HUD, physical hiding apertures and hinged door presentation. */
(function(){
'use strict';
const WW=WardWinter,e=htmlSafe;
// A fresh installation uses subtle affordances. Explicit choices persist in
// Options; no scene control silently promotes the hint strength.
if(typeof WardScene.options.hints!=='boolean')WardScene.options.hints=false;
const options=optionsModal;
optionsModal=function(...args){const result=options(...args);for(const button of document.querySelectorAll('#m button'))if(/saveMenu\s*\(/.test(button.getAttribute('onclick')||''))button.remove();return result;};
const menu=saveMenu;
saveMenu=function(...args){const result=menu(...args),title=document.querySelector('#m .mh h2');if(title)title.textContent='Save records';return result;};

// A camera recording is a room image, not a generic document or supply pouch.
// Reuse the same authored Lobby painting that is sent to the surveillance CRTs.
const findingIcon=WW.findingIcon;
WW.findingIcon=function(object){const id=object?.[0];if(id==='cam'||id==='rep2')return '<img class="item-art surveillance-finding-preview" src="'+e(WW.asset(WW.roomViewAsset('lobby','front')))+'" alt="Monochrome Emergency Lobby camera feed">';if(id==='clara')return '<img class="item-art" src="'+e(WW.asset('assets/props/terminal.png'))+'" alt="Security message recorder">';return findingIcon(object);};

// The old focus overlay was opaque even when its child SVG had transparent
// slits. Openings now show the live room canvas and actors behind the mask.
WW.sceneUI.locker=function(){
 const root=$('sceneFocusOverlay');if(!root||!S)return;
 const peek=!!S.f.lockerPeeking,type=S.f.hidingType||'locker',p=initPursuer();
 // Openings are authored relative to the fitted room, rather than the whole
 // HUD. The old high, hairline vents looked onto ceiling/matte and missed a
 // threat's body. These remain physical slits, not a miniature full-room view.
 const native=type==='crates'?[[40,25,4,48],[49,25,6,48],[60,28,4,42]]:type==='desk'?[[16,48,68,21]]:[[23,24,54,6],[23,40,54,6],[23,56,54,6]];
 const host=$('interactiveScene').getBoundingClientRect(),frame=document.querySelector('.room-view-frame'),art=frame?.getBoundingClientRect()||host;
 const gaps=native.map(([x,y,w,h])=>[(art.left-host.left+art.width*x/100)/host.width*100,(art.top-host.top+art.height*y/100)/host.height*100,w*art.width/host.width,h*art.height/host.height]);
 WW.peekApertures=peek?gaps.map(v=>v.slice()):[];
 WW.roomViewRenderer?.()?.peek(peek);frame?.classList.toggle('peek-adapted',peek);
 const holes=peek?gaps.map(([x,y,w,h])=>'M'+x+' '+y+'h'+w+'v'+h+'h-'+w+'Z').join(' '):'';
 const rims=peek?gaps.map(([x,y,w,h])=>'<path d="M'+x+' '+(y+h)+'h'+w+'" stroke="#8e877b" stroke-opacity=".4" stroke-width=".22"/>').join(''):'';
 root.classList.remove('hid');root.innerHTML='<div class="c1-locker panorama-locker hiding-physical '+(peek?'peeking':'closed')+'" data-cover="'+e(type)+'"><svg class="panorama-hiding-mask" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path fill="#020202" fill-rule="evenodd" d="M0 0H100V100H0Z '+holes+'"/>'+rims+'</svg><footer><h3>'+(peek?'Through the '+(type==='locker'?'locker vents':type==='crates'?'gaps between the crates':'gap beneath the desk'):'Inside the hiding place')+'</h3><p>'+e(p.active&&p.room===S.room?'Heavy boots are in this room.':'Listen beyond the door.')+'</p><div><button class="btn" onclick="wardStayHidden()">Stay hidden</button><button class="btn" onclick="wardPeek()">'+(peek?'Stop peeking':'Peek')+'</button><button class="btn" onclick="wardExitHiding()">Exit</button></div></footer></div>';
 const targets=document.querySelector('.room-view-targets');if(targets)targets.inert=true;
};
const focusWithoutPeek=WW.sceneUI.focus;
WW.sceneUI.focus=function(...args){WW.roomViewRenderer?.()?.peek(false);document.querySelector('.room-view-frame')?.classList.remove('peek-adapted');WW.peekApertures=[];return focusWithoutPeek.apply(this,args);};

// UI-only animation: movement and combat authorization stay in sceneDoorTravel.
// No timers finish a doorway while paused, and a pause preserves animation time.
let activeDoorTransition=null;
WW.playDoorTransition=function({from,to,duration=1500,onComplete}={}){
 if(activeDoorTransition||WW.travelling)return false;
 const host=document.querySelector('.room-view-frame');
 if(!host||!S){onComplete?.();return {cancel(){}};}
 const reduced=WardScene.options.motion===false||matchMedia('(prefers-reduced-motion: reduce)').matches;
 const exposure=S.f.wet?1.65:S.f.shivering||S.f.coldExposure>=4?1.35:1;
 const total=reduced?100:Math.max(900,duration)*exposure;
 const overlay=document.createElement('div');overlay.className='ward-door-passage';overlay.style.setProperty('--door-time',total+'ms');overlay.dataset.exposure=exposure>1?'cold':'normal';
 const edge=WardNavigation.edge(from||S.room,to),view=Object.entries(WardRoomViews[to]?.views||{}).find(([name,v])=>v.doors?.[edge])?.[0]||'front',path=WardRoomViews[to]?.views[view]?.asset;
 const targetDark=WardNavigation.isDark(to),source=path?'<img class="ward-door-next-room" src="'+e(WW.asset(path))+'" alt="">':'';
 overlay.innerHTML='<div class="ward-door-depth" style="--destination-light:'+(targetDark?.32:.78)+'">'+source+'</div><div class="ward-door-casing"><div class="ward-door-slab"><div class="ward-door-upper-panel"></div><div class="ward-door-lower-panel"></div><div class="ward-door-handle"><i></i></div></div></div><div class="ward-door-blackout"></div><div class="ward-door-label">'+e(R[to]?.n||'')+(exposure>1?'<small>Cold hands slow the latch.</small>':'')+'</div>';
 host.append(overlay);
 let last=performance.now(),elapsed=0,done=false,raf=0;
 const release=()=>{if(done)return false;done=true;cancelAnimationFrame(raf);overlay.remove();if(activeDoorTransition===handle){activeDoorTransition=null;WW.travelling=false;}return true;};
 const finish=()=>{if(release())onComplete?.();};
 const frame=now=>{if(done)return;const paused=!!WW.isPaused?.();overlay.classList.toggle('animation-paused',paused);for(const animation of overlay.getAnimations({subtree:true})){if(paused&&animation.playState==='running')animation.pause();else if(!paused&&animation.playState==='paused')animation.play();}if(!paused)elapsed+=Math.max(0,now-last);last=now;if(elapsed>=total)return finish();raf=requestAnimationFrame(frame);};
 const handle={duration:total,cancel(){release();}};activeDoorTransition=handle;WW.travelling=true;
 raf=requestAnimationFrame(frame);return handle;
};

WW.cancelDoorTransition=()=>activeDoorTransition?.cancel();
// The animation owns the movement latch. Every user-facing command and both
// physical/map travel entries wait for it; its completion releases the latch
// before calling the authorized travel function. Pause is handled at window
// capture and remains available throughout this document-level input lock.
const travelCommands=['act','exam','go','mapTravel','mapModal','invModal','storage','doc','evidenceModal','journal','optionsModal','saveMenu','saveGame','confirmSave','toggleLight','useInventorySlot','heal','reload','combineItems','combat','shoot','knifeAttack'];
for(const name of Object.keys(window))if(/^ward[A-Z]/.test(name)&&!/^ward(?:Pause|Resume|TogglePause|Load)/.test(name))travelCommands.push(name);
for(const name of new Set(travelCommands)){const action=window[name];if(typeof action==='function')window[name]=function(...args){if(WW.travelling)return false;return action.apply(this,args);};}
for(const name of ['setView','snapTo','look','reveal','face','pointOfInterest']){const action=WW.orbit?.[name];if(typeof action==='function')WW.orbit[name]=function(...args){if(WW.travelling)return false;return action.apply(this,args);};}
for(const name of ['newGame','loadGame','loadCheckpoint','loadFirstFloorCheckpoint','wardLoadFinale']){const action=window[name];if(typeof action==='function')window[name]=function(...args){WW.cancelDoorTransition();return action.apply(this,args);};}
for(const eventType of ['click','pointerdown','keydown'])document.addEventListener(eventType,event=>{if(!WW.travelling||event.target.closest?.('[data-pause-action],#wardPauseOverlay'))return;if(event.target.closest?.('#game,#m')){event.preventDefault();event.stopImmediatePropagation();}},true);

// Remove abandoned drawer focus containers once their fixture is resolved. A
// notice must stay a local card; it must never paint a full-screen colour wash.
const renderHudScene=renderScene;
renderScene=function(...args){const result=renderHudScene(...args);WW.floorplan?.syncBearing?.();const root=$('sceneFocusOverlay');if(root&&!S?.f.hidingRoom&&!S?.sceneFocus&&!root.querySelector('.winter-ending,.c1-ending')){root.innerHTML='';root.classList.add('hid');}return result;};
})();
