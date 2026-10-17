/* Chapter 1 cinematic stage. Room art is local; online artwork is optional. No UI mask buttons. */
(function(){
const ROOM_ANCHORS={
 lobby:{doors:[[35,52,12,38],[78,52,13,38],[7,51,10,38],[94,51,8,38]],props:{'Reception desk':[72,78],'Staff locker':[92,55],'Payphone':[49,48],'Field cache':[89,78],'Continuity Terminal':[92,78],'Rain-streaked windows':[14,48],'Main entrance':[15,46]}},
 security:{doors:[[31,51,13,39],[79,51,13,39],[92,51,8,39]],props:{'Monitor wall':[17,39],'Security desk':[50,68],'Equipment cabinet':[88,57],'Floor plan rack':[60,49],'Staff portraits':[61,31]}},
 eastcorridor:{doors:[[12,51,12,39],[85,51,12,39],[48,51,12,39]],props:{'Emergency lighting':[55,24],'Broken trolley':[67,69],'Old wall directory':[30,48],'Portable staff radio':[43,58],'Cracked ward window':[72,43]}},
 ward:{doors:[[8,52,10,39],[27,52,10,39],[48,52,10,39],[70,52,10,39],[92,52,10,39]],props:{'Patient name boards':[22,44],'Nurses station':[63,67],'Pharmacy entry panel':[84,46]}},
 generator:{doors:[[18,51,11,39],[82,51,11,39],[49,51,10,39]],props:{'Generator controls':[50,56],'Maintenance tools':[32,72],'Continuity station':[76,60],'Abandoned equipment':[18,65],'Regulator housing':[39,48]}},
 pharmacy:{doors:[[18,51,13,39],[80,51,13,39]],props:{'Dispensing counter':[54,67],'Medicine fridge':[75,49],'Storage shelves':[26,52],'Maintenance shelf':[88,70]}},
 room12:{doors:[[16,51,11,39],[86,51,11,39]],props:{'Patient bed':[49,66],'Medical cabinets':[76,46],'Instrument tray':[65,73]}},
 observation:{doors:[[15,51,12,38],[88,51,12,38]],props:{'Observation window':[51,43],'Records terminal':[70,69]}}
};

// Original recovered journal: ordinary staff notes become progressively fractured across the floor.
DOCS['Attendant Journal — Page I']="NIGHT ATTENDANT — SEPTEMBER 12, 1998\n\nThe evening shift ran long again. Shaw thinks I should report the barred emergency doors, but Security says the locks are temporary. Someone left a patient's shoes beneath the stairs. I put them in Lost Property.\n\nI am too tired to worry about it.";
DOCS['Attendant Journal — Page II']="SEPTEMBER 15, 1998\n\nThe floor is quieter. I cannot remember taking my medication, though the packet is empty. I heard somebody moving in the supply wall. Maybe pipes. Maybe not.\n\nI went into the corridor for water. Came back holding a patient's wristband. I don't know whose it is.";
DOCS['Attendant Journal — Last Page']="17\n\nnot sleeping.\n\ndoor says stay. door says i work here.\n\nshoe under stairs still there. no feet.\n\nplease don't call my name.\n\ni can hear it when i don't.";
R.security.o.push(['attendantDiary1','Night attendant journal — first page','▤','A carefully dated personal notebook.',{doc:'Attendant Journal — Page I'}]);
R.laundry.o.push(['attendantDiary2','Night attendant journal — loose page','▤','Writing grows uneven and hurried.',{doc:'Attendant Journal — Page II'}]);
R.records.o.push(['attendantDiary3','Night attendant journal — final page','▤','Words barely form a sentence.',{doc:'Attendant Journal — Last Page'}]);

// Correct old site misclassification: a payphone, window, directory and radio are never one object.
if(typeof SCENE_CONFIG!=='undefined'){
 const lobby=SCENE_CONFIG.lobby?.sites||[];
 for(const s of lobby){if(s[0]==='Payphone')s.splice(3,s.length-3);}
 if(lobby.length)lobby.push(['Rain-streaked windows','glass','win']);
 const east=SCENE_CONFIG.eastcorridor?.sites||[];
 for(const s of east){if(s[0]==='Old wall directory')s.splice(3,s.length-3);}
 east.push(['Portable staff radio','screen','radioHall']);east.push(['Cracked ward window','glass','windowBoard']);
}
function escapeText(s){return htmlSafe(String(s||''))}
function listSites(){
 // Explicit object-to-fixture mapping. No automatic dumping of 'unmatched' items into desks, phones or directories.
 const conf=SCENE_CONFIG[S.room]||{sites:[]},visible=availableRoomObjects(),byID=new Map(visible.map(o=>[o[0],o]));
 const out=[];const used=new Set();
 const kindFrom=(obj)=>{const sp=obj[4]||{};return sp.doc?'paper':sp.act==='payphone'?'phone':sp.act==='save'?'screen':sp.act==='box'?'crate':sp.give?'locker':sp.look?'glass':'desk'};
 for(const [n,site] of (conf.sites||[]).entries()){
  const members=site.slice(2).filter(id=>byID.has(id)&&!used.has(id)).map(id=>{used.add(id);return byID.get(id)});
  if(!members.length)continue;
  if(members.length<=2){out.push({id:'site_'+n,label:site[0],kind:site[1],objects:members});continue;}
  // Large fixtures can have multiple independent inspection points, each max two sensible contents.
  for(let i=0;i<members.length;i+=2){const chunk=members.slice(i,i+2);out.push({id:'site_'+n+'_'+i,label:i===0?site[0]:chunk.length===1?chunk[0][1]:site[0]+' — '+(i/2+1),kind:i===0?site[1]:kindFrom(chunk[0]),objects:chunk});}
 }
 // Late scripted additions must NEVER be silently attached to the first desk or to a payphone.
 for(const obj of visible){if(used.has(obj[0]))continue;out.push({id:'fixture_'+obj[0],label:obj[1],kind:kindFrom(obj),objects:[obj]});used.add(obj[0]);}
 return out;
}
function doorSlots(n,room,connections){
 if(room==='lobby'&&connections)return connections.map(d=>d.to==='security'?[35,52,12,38]:d.to==='eastcorridor'?[78,52,13,38]:d.to==='records'?[7,51,10,38]:[94,51,8,38]);

 const prescribed=ROOM_ANCHORS[room]?.doors;
 if(prescribed&&prescribed.length>=n)return prescribed.slice(0,n);
 // All doorframes share the same floor. Additional connections go in a continuous, evenly spaced row.
 const count=Math.max(n,1),width=Math.min(14,Math.max(7.5,88/count-3));
 return Array.from({length:count},(_,i)=>[count===1?50:8+i*84/(count-1),51,width,39]);
}
function propSlots(groups,doors,room){
 // Hit regions are authored where available; a collision-free search is used only for overflow.
 const presets=ROOM_ANCHORS[room]?.props||{};
 const candidates=[[49,49],[14,49],[70,75],[91,57],[31,75],[55,73],[16,74],[82,73],[42,28],[68,29],[52,31],[27,28],[77,32],[8,28],[93,27],[36,61],[63,65],[50,66],[25,66],[76,62],[11,68],[90,69],[59,45],[42,46]];
 const used=[];
 const collides=(pt)=>doors.some(([x,y,w,h])=>Math.abs(pt[0]-x)<w/2+4.5&&Math.abs(pt[1]-y)<h/2+5.5)||used.some(q=>Math.abs(pt[0]-q[0])<6.8&&Math.abs(pt[1]-q[1])<7.5)||pt[1]>79;
 return groups.map((g,i)=>{
  const desired=presets[g.label]||presets[g.label.split(' — ')[0]];
  const tries=[...(desired?[desired]:[]),...candidates.slice(i%candidates.length),...candidates.slice(0,i%candidates.length)];
  let chosen=tries.find(p=>!collides(p));
  if(!chosen){for(let y=18;y<=77&&!chosen;y+=7)for(let x=9;x<=92&&!chosen;x+=7){if(!collides([x,y]))chosen=[x,y]}}
  chosen=chosen||[10+((i*13)%82),75];used.push(chosen);return chosen;
 });
}
function roomPicture(room){return 'assets/rooms/'+room+'.jpg'}
function sceneSrc(room){const path=roomPicture(room);if(window.WardEmbeddedAssets&&WardEmbeddedAssets[path])return WardEmbeddedAssets[path];return /^https?:\/\//.test(path)||/^assets\/rooms\/[a-z0-9_-]+\.jpg$/.test(path)?path:'assets/rooms/lobby.jpg'}
let recentTip='';
sceneTooltip=function(t){const el=$('sceneTooltip');if(el){el.textContent=t;el.classList.add('visible')}recentTip=t};
sceneTooltipClear=function(){const el=$('sceneTooltip');if(el)el.classList.remove('visible')};
function visualInspect(id){if(!S)return;
 if(R[S.room].dark&&!lit()){
  interaction('There is not enough light to search here. Switch on the flashlight to examine the room.');return;
 }
 S.sceneFocus=S.sceneFocus===id?null:id;S.f['seen_site_'+S.room+'_'+id]=1;renderScene();
}
sceneInspect=visualInspect;
function v3Drawer(){const overlay=$('sceneFocusOverlay');if(!overlay||!S)return;
 const group=listSites().find(g=>g.id===S.sceneFocus);
 if(!group){overlay.classList.add('hid');overlay.innerHTML='';return;}
 overlay.classList.remove('hid');
 // Fixed-size closeup in the same scene. No unrelated items and no permanently visible list.
 const zoom=ROOM_ANCHORS[S.room]?.props?.[group.label]||[50,48];const actions=group.objects.map(o=>{const [id,name,,description,sp]=o,state=S.ob[id],done=state==='done'||state==='read';
  const verb=done?'Examined':sp.doc?'Read':sp.give?'Take':sp.act==='payphone'?S.f.phoneRinging&&S.f.ringingPhoneRoom===S.room?'Answer':'Check line':sp.act==='npc'?'Speak':sp.act==='hide'?'Hide':sp.act==='map'?'Copy map':sp.look?'Examine':'Use';
  const icon=sp.give&&sp.give[0]?itemIconMarkup(sp.give[0][0]):'';
  const click=`wardSceneAction('${id}')`;
  return `<div class="v3-find"><div class="v3-icon">${icon||'<span class="v3-doc-icon">'+(sp.doc?'▤':sp.act==='payphone'?'☎':'◈')+'</span>'}</div><div class="v3-find-text"><strong>${escapeText(name)}</strong><small>${escapeText(description)}</small></div><button class="btn ${done?'':'p'}" ${done?'disabled':''} onclick="${click}">${verb}</button></div>`;
 }).join('');
 overlay.innerHTML=`<div class="v3-inspect"><div class="v3-inspect-top"><span>EXAMINING · ${escapeText(group.label)}</span><button class="btn" onclick="wardCloseFocus()">Return to room ×</button></div><div class="v3-inspect-image" style="background-image:linear-gradient(180deg,transparent,#0a0d12cc),url('${sceneSrc(S.room)}');background-size:cover,195% 175%;background-position:center,${zoom[0]}% ${zoom[1]}%"><span>${escapeText(group.label)}</span></div><div class="v3-findings">${actions}</div></div>`;
}
renderSceneDrawer=v3Drawer;
function centerShot(src,room){const fallback=(window.WardEmbeddedAssets?.['assets/rooms/'+room+'.jpg']||'assets/rooms/'+room+'.jpg');return `<img class="v3-background" src="${escapeText(src)}" alt="" onerror="this.onerror=null;this.src='${escapeText(fallback)}'">`}
renderScene=function(){if(!S)return;const host=$('interactiveScene');if(!host)return;
 if(S.sceneFocusRoom!==S.room){S.sceneFocus=null;S.sceneFocusRoom=S.room}
 const room=S.room,groups=listSites(),doors=roomConnections().filter(d=>!(room==='lobby'&&['serviceReturn','sl'].includes(d.id)&&!doorOpen(d.id))&&!(room==='security'&&d.id==='es'&&!doorOpen(d.id))),slots=doorSlots(doors.length,room,doors),objects=propSlots(groups,slots,room),torch=!!S.lightOn&&S.bat>0,unpowered=!!R[room].dark&&!(S.f.power&&!S.f.powerOut&&WARD_POWERED.has(room)),dark=unpowered&&!torch;
 const live=window.WardArt?.urlFor?.(room)||'';const images=centerShot(sceneSrc(room),room)+(live?`<img class="v3-ai-overlay" alt="" src="${escapeText(live)}" onerror="this.remove()">`:'');
 const doorButtons=doors.map((d,i)=>{const [x,y,w,h]=slots[i],open=doorOpen(d.id),entry=S.prev===d.to&&S.room!==d.to;
  const full=sceneDoorLabel(d.to,d),title=(R[d.to]?.short||R[d.to]?.n||'PASSAGE').replace(/\s+/g,' ').toUpperCase();
  // Sign above doorway. Never wrap into SECUR / ITY / OFFICE.
  const sign=title.length>19?title.slice(0,18)+'…':title;
  const picture='no-sprite';
  return `<button class="v3-door ${open?'':'locked'} ${entry?'entry':''} ${picture}" style="--x:${x}%;--y:${y}%;--w:${w}%;--h:${h}%;" aria-label="${escapeText(full)}" title="${escapeText(full)}" data-tip="${escapeText(full)}" onmouseenter="sceneTooltip(this.dataset.tip)" onmouseleave="sceneTooltipClear()" onfocus="sceneTooltip(this.dataset.tip)" onblur="sceneTooltipClear()" onclick="sceneDoorTravel('${d.to}')"><span class="v3-door-plaque">${escapeText(sign)}</span>${!open?'<span class="v3-locked">▣</span>':''}</button>`;
 }).join('');
 const sites=groups.map((g,i)=>{const [x,y]=objects[i];return `<button class="v3-prop" style="--x:${x}%;--y:${y}%;" aria-label="Inspect ${escapeText(g.label)}" title="${escapeText(g.label)}" data-tip="${escapeText(g.label)}" onmouseenter="sceneTooltip(this.dataset.tip)" onmouseleave="sceneTooltipClear()" onfocus="sceneTooltip(this.dataset.tip)" onblur="sceneTooltipClear()" onclick="sceneInspect('${g.id}')"><span class="v3-hotspot-label">${escapeText(g.label)}</span></button>`}).join('');
 const floor=R[room].ch;
 host.innerHTML=`<div class="v3-room-art ${unpowered?'is-dark':''} ${torch?'torch-on':''} ${S.f.power?'generator-on':''}" role="group" aria-label="${escapeText(R[room].n)} illustrated scene">${images}<div class="v3-film"></div><div class="v3-scrim"></div>${doorButtons}${sites}<div class="v3-lighting" aria-hidden="true"></div><div id="sceneTooltip" class="v3-tooltip" role="status"></div><span class="v3-room-stamp">${floor===1?'FIRST FLOOR':'BLACKRIDGE'} · ${escapeText(R[room].n)}</span></div><div id="sceneFocusOverlay" class="scene-focus-overlay hid"></div>`;
 v3Drawer();
 const phase=$('stagePower');if(phase)phase.textContent=dark?'DARK · USE FLASHLIGHT':unpowered?'FLASHLIGHT BEAM':S.f.power?'PARTIAL POWER RESTORED':'EMERGENCY LIGHTING';
};
// Previous implementation moved these controls back into the old top and bottom sections.
wardPrepareUi=function(){const rail=$('survivalControls'),buttons=document.querySelector('.story-actions');if(rail&&buttons&&buttons.parentElement!==rail)rail.appendChild(buttons);};
const prevRender=render;
render=function(){prevRender();if(!S)return;const el=$('mentalLabel'),sanity=san();const bar=$('mentalBar');if(bar)bar.style.width=Math.max(0,Math.min(100,sanity))+'%';
 if(el){el.textContent=sanity>=75?'STABLE':sanity>=50?'UNEASY':sanity>=25?'DISTRESSED':'FRACTURED';el.className=sanity>=75?'mind-stable':sanity>=50?'mind-uneasy':'mind-fractured';}
 document.body.classList.toggle('ward-playing',!$('game').classList.contains('hid'));
 const ci=$('stagePower');if(ci&&S.f.power&&ROOM_ANCHORS[S.room])ci.textContent=R[S.room].dark&&!lit()?'DARK · USE FLASHLIGHT':'PARTIAL POWER RESTORED';
 const msgs=document.querySelector('.message-stream');if(msgs){const observation=$('interactionText'),combat=$('combatText');msgs.classList.toggle('has-feedback',!!(observation?.textContent?.trim()||combat?.textContent?.trim()));}
 if($('lightBtn'))$('lightBtn').classList.toggle('torch-active',!!S.lightOn);const ml=$('mobileLight');if(ml){ml.textContent=S.lightOn?'LIGHT ON · '+S.bat:'LIGHT OFF';ml.classList.toggle('on',!!S.lightOn)}const hide=$('hideBtn');if(hide)hide.classList.toggle('hid',!HIDING_AREAS.has(S.room));
};
// Contextual narrative feedback is visible inside the single scene, not in another row.
const oldInteraction=interaction;
interaction=function(x){oldInteraction(x);const msgs=document.querySelector('.message-stream');msgs?.classList.toggle('has-feedback',!!String(x||'').trim());};
// Focus view is a scene-layer, never a new panel below the scene.
wardCloseFocus=function(){if(S)S.sceneFocus=null;renderScene();};
const oldRenderInv=renderUnifiedInventory;
renderUnifiedInventory=function(){oldRenderInv();};
// Player's first-floor ethical decision must remain exclusive after being made.
const patientLegacy=beggingPatient;
beggingPatient=function(){if(S?.f?.beggingPatientChoice)return interaction(S.f.beggingPatientChoice==='killed'?'The patient is dead. The decision cannot be undone.':S.f.beggingPatientChoice==='helped'?'He is receiving the treatment you gave him.':'He remains alive. I walked away from his plea.');return patientLegacy()};
// Collecting something visible in the focused close-up is one action: no second Take-confirmation modal.
window.wardSceneAction=function(id){
 const obj=R[S.room]?.o?.find(o=>o[0]===id);
 if(!obj)return;
 if(obj[4]?.give&&S.ob[id]!=='done'){
  S.cf=id;
  try{act(id)}finally{S.cf=null}
 }else act(id);
 S.sceneFocus=null;renderScene();
};
// Keep combat concise inside the stage, with an accuracy-versus-time decision.
const legacyCombat=combat;
combat=function(note){
 if(!S||!alive(S.room))return;
 cm=1;
 const e=E[S.room],w=W[S.eq]&&has(S.eq)?W[S.eq]:null;
 const descriptor=R[S.room].dark&&!lit()?'A shape in the dark':e.n;
 const cond=enemyCondition(S.en[S.room],e.hp);
 const loaded=w?(S.ld[S.eq]||0):0;
 const remaining=w?cnt(w.ammo):0;
 const actionNote=escapeText(note||'It is approaching. Every shot and every second matters.');
 const shotDisabled=!w||!loaded?'disabled':'';
 const fast=`<button class="btn p" ${shotDisabled} onclick="shoot()">Quick shot · ${loaded} loaded</button>`;
 const steady=`<button class="btn" ${shotDisabled} onclick="wardSteadyShot()">Steady shot · better accuracy</button>`;
 modal(descriptor,`<div class="v3-combat"><div class="v3-combat-card"><span>ENCOUNTER · ${escapeText(R[S.room].n)}</span><strong>${escapeText(cond)}</strong><p>${actionNote}</p><small>Condition: ${escapeText(conditionInfo(S.hp)[1])} · ${w?escapeText(S.eq)+' · '+loaded+'/'+w.mag+' · Reserve '+remaining:'UNARMED'}</small></div><div class="v3-combat-actions">${fast}${steady}<button class="btn" onclick="flee()" ${e.boss?'disabled':''}>Retreat</button><button class="btn" onclick="knifeAttack()">Struggle</button><button class="btn" onclick="reload()" ${!w?'disabled':''}>Reload</button><button class="btn" onclick="combatHeal()">Treat wounds</button></div></div>`);
};
const legacyShoot=shoot;
shoot=function(){let w=W[S?.eq],old=w?.hit;try{if(w&&S?.f?.steadyAim){w.hit=Math.min(.97,old+.18);S.f.steadyAim=false;}return legacyShoot()}finally{if(w&&old!==undefined)w.hit=old;}};
window.wardSteadyShot=function(){if(!S||!W[S.eq]||!has(S.eq))return;if((S.ld[S.eq]||0)<=0)return combat('The chamber is empty.');S.f.steadyAim=true;advanceTime(2);if(S.hp<=25&&rnd()<.22){S.f.steadyAim=false;return foe('Pain throws your aim off before you can fire.');}shoot()};

// Start menu artwork modes are preferences, never a network requirement.
function chosenArtMode(){return document.querySelector('input[name="artMode"]:checked')?.value||'auto'}
function artModeApply(){let m=chosenArtMode();try{localStorage.setItem('lw_art_mode',m)}catch(e){};if(window.WardArt)WardArt.update(m!=='offline')}
for(const i of document.querySelectorAll('input[name="artMode"]'))i.addEventListener('change',artModeApply);
try{const v=localStorage.getItem('lw_art_mode');const choice=document.querySelector(`input[name="artMode"][value="${v}"]`);if(choice)choice.checked=true;}catch(e){}
artModeApply();
const stageWorld=document.querySelector('.stage-world');if(stageWorld&&$('m'))stageWorld.appendChild($('m'));
const oldNewGame=newGame;
newGame=function(){artModeApply();oldNewGame();document.body.classList.add('ward-playing');};
const oldLoadGame=loadGame;
loadGame=function(...args){artModeApply();oldLoadGame(...args);if(S)document.body.classList.add('ward-playing');};
window.wardListSites=listSites;
// Fix visual state on low-light scene entry without moving narration.
document.addEventListener('pointermove',e=>{const scene=e.target.closest?.('.v3-room-art');if(!scene)return;const r=scene.getBoundingClientRect();scene.style.setProperty('--beam-x',(100*(e.clientX-r.x)/r.width).toFixed(1)+'%');scene.style.setProperty('--beam-y',(100*(e.clientY-r.y)/r.height).toFixed(1)+'%')},{passive:true});
})();
