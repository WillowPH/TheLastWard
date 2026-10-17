/* Chapter 1 interaction and progression overhaul. No external dependency is required. */
const WARD_CHAPTER_BUILD='2026-10-17-Ch1';
const WARD_POWERED=new Set(['lobby','security','eastcorridor','ward','room12','pharmacy','archive','generator','laundry','stafflounge','records','residence','surgery','isoward','lift']);
// A location already seen in the world must not secretly become another category of object.
function siteGroups(){
 const conf=SCENE_CONFIG[S.room]||{style:'corridor',sites:[]},objects=availableRoomObjects();
 const slots=SCENE_ROOM_POS[S.room]||SCENE_STYLE_POS[conf.style]||SCENE_SITE_POS;
 const byId=new Map(objects.map(o=>[o[0],o])); const seen=new Set(),groups=[];
 for(const [i,s] of (conf.sites||[]).entries()){
  const listed=s.slice(2).filter(id=>byId.has(id));listed.forEach(id=>seen.add(id));
  if(!listed.length)continue;
  // Group only contents that logically belong in the same physical furnishing.
  const compatible=['desk','locker','books','cart','crate','rack','machine','bed','altar'].includes(s[1]);
  if(compatible){ groups.push({id:'site_'+i,label:s[0],kind:s[1],objects:listed.map(id=>byId.get(id)),x:slots[i]?.[0]||50,y:slots[i]?.[1]||70});}
  else listed.forEach((id,j)=>groups.push({id:'object_'+id,label:byId.get(id)[1],kind:s[1],objects:[byId.get(id)],x:slots[i]?.[0]||50,y:slots[i]?.[1]||70}));
 }
 const free=objects.filter(o=>!seen.has(o[0]));
 free.forEach((o,i)=>{
  const sp=o[4]||{},kind=sp.act==='payphone'?'phone':sp.doc?'paper':sp.give?'crate':sp.act==='save'?'screen':sp.look?'paper':'machine';
  groups.push({id:'object_'+o[0],label:o[1],kind,objects:[o],x:23+(i*23)%60,y:69+(i%2)*8});
 });
 return groups;
}
// Architectural doors are floor-anchored, not hovering in the upper half of the room.
function sceneLayout(doors,groups,room){
 const n=doors.length;const xs=n===1?[51]:n===2?[12,88]:n===3?[10,50,90]:n===4?[9,35,65,91]:Array.from({length:n},(_,i)=>8+i*84/(n-1));
 const doorPlaces=xs.map(x=>[x,69]);
 const locations=[[27,71],[72,71],[41,57],[60,57],[20,52],[80,52],[34,84],[65,84],[48,83],[18,86],[82,86],[49,43],[25,41],[75,41],[12,39],[88,39],[38,39],[63,39]];
 const itemPlaces=[];
 for(let i=0;i<groups.length;i++){
  const wish=[groups[i].x,groups[i].y];
  const sorted=[wish,...locations.slice((hashSeed(room+'f'+i)%locations.length)),...locations];
  const best=sorted.find(pt=>!doorPlaces.some(d=>Math.abs(d[0]-pt[0])<14&&Math.abs(d[1]-pt[1])<43)&&!itemPlaces.some(q=>Math.abs(q[0]-pt[0])<12&&Math.abs(q[1]-pt[1])<17));
  itemPlaces.push(best||[25+(i*17)%55,42+(i%3)*18]);
 }
 return {doorPlaces,itemPlaces};
}
function drawDoor(x,y,locked,entry=false){const X=x*8,Y=y*3.3;return `<g transform="translate(${X-37} ${Y-131})"><rect width="74" height="202" rx="3" fill="#11151b" stroke="${entry?'#d9ab82':locked?'#ab6267':'#697580'}" stroke-width="${entry?4:3}"/><rect x="7" y="8" width="60" height="185" fill="#252b31" stroke="#474950" stroke-width="2"/><rect x="14" y="24" width="46" height="29" fill="#12181e" stroke="#686b73" stroke-width="2"/><path d="M19 36H55M14 175H60" stroke="#8d8b86" opacity=".38"/><circle cx="59" cy="125" r="4" fill="#bdb3a7"/>${locked?'<path d="M29 116v-9a8 8 0 0 1 16 0v9m-20 0h24v19H25z" stroke="#bd7377" fill="none" stroke-width="3"/>':''}${entry?'<path d="M2 199h70" stroke="#f3c493" stroke-width="4"/>':''}</g>`}
// Real door signage is attached to the illustrated door. No generic DOOR button labels.
function renderScene(){const host=$('interactiveScene');if(!host||!S)return;const conf=SCENE_CONFIG[S.room]||{style:'corridor'};const doors=roomConnections(),groups=siteGroups();if(S.sceneFocusRoom!==S.room){S.sceneFocus=null;S.sceneFocusRoom=S.room;}
 const dark=!!R[S.room].dark&&!lit(),layout=sceneLayout(doors,groups,S.room);
 let doorArt='',doorButtons='',propArt='',propButtons='';
 doors.forEach((d,i)=>{const pos=layout.doorPlaces[i],open=doorOpen(d.id),entry=S.prev===d.to&&S.prev!==S.room,tip=sceneDoorLabel(d.to,d);const sign=(R[d.to]?.short||R[d.to]?.n||'ACCESS').slice(0,14).toUpperCase();doorArt+=drawDoor(...pos,!open,entry);doorButtons+=`<button class="hotspot door-hotspot ${open?'':'is-locked'} ${entry?'entry-door':''}" style="left:${pos[0]}%;top:${pos[1]}%" data-tip="${htmlSafe(tip)}" aria-label="${htmlSafe(tip)}" onmouseenter="sceneTooltip(this.dataset.tip)" onmouseleave="sceneTooltipClear()" onfocus="sceneTooltip(this.dataset.tip)" onblur="sceneTooltipClear()" onclick="sceneDoorTravel('${d.to}')"><span class="door-label">${htmlSafe(sign)}</span></button>`});
 groups.forEach((g,i)=>{const pos=layout.itemPlaces[i];propArt+=drawProp(g.kind,...pos);const active=S.sceneFocus===g.id;propButtons+=`<button class="hotspot prop-hotspot ${active?'is-active':''}" style="left:${pos[0]}%;top:${pos[1]}%" data-tip="${htmlSafe(g.label)}" aria-label="Examine ${htmlSafe(g.label)}" onmouseenter="sceneTooltip(this.dataset.tip)" onmouseleave="sceneTooltipClear()" onfocus="sceneTooltip(this.dataset.tip)" onblur="sceneTooltipClear()" onclick="sceneInspect('${g.id}')"></button>`});
 const background=window.WardArt?.urlFor?.(S.room)||'';
 const artTag=background?`<img class="online-room-art" alt="" src="${htmlSafe(background)}" onerror="this.remove()">`:'';
 host.innerHTML=`<div class="scene-image">${sceneArchitecture(conf.style)+roomSignature(S.room)}${artTag}<svg class="scene-overdraw" viewBox="0 0 800 330" preserveAspectRatio="none" aria-hidden="true">${propArt}${doorArt}</svg><div class="scene-haze"></div>${doorButtons}${propButtons}<div class="scene-darkness ${dark?'deep-dark':''}" aria-hidden="true"></div><div id="sceneTooltip" class="scene-tooltip" role="status"></div><div class="room-inset"><span>${htmlSafe(R[S.room].n)}</span> · ${dark?'FLASHLIGHT REQUIRED':S.f.power&&WARD_POWERED.has(S.room)?'POWERED':'EMERGENCY LIGHTING'}</div></div>`;
 document.getElementById('sceneFocusOverlay')?.remove();host.insertAdjacentHTML('beforeend','<div id="sceneFocusOverlay" class="scene-focus-overlay hid"></div>');
 renderSceneDrawer();
}
function sceneInspect(id){if(!S)return;if(R[S.room].dark&&!lit()){interaction('The room is too dark to inspect safely. Turn on your flashlight.');return;}S.sceneFocus=S.sceneFocus===id?null:id;renderScene()}
function renderSceneDrawer(){const host=$('sceneDrawer');if(!host||!S)return;const group=siteGroups().find(g=>g.id===S.sceneFocus);const area=$('sceneFocusOverlay');if(!area)return;
 if(!group){host.classList.add('hid');area.classList.add('hid');area.innerHTML='';return;}
 host.classList.add('hid');area.classList.remove('hid');
 const actions=group.objects.map(o=>{const [id,name,icon,description,sp]=o;const status=S.ob[id],done=status==='done'||status==='read';const verb=done?'Completed':sp.doc?'Read':sp.give?'Take':sp.act==='payphone'?'Use phone':sp.act==='hide'?'Hide':sp.look?'Examine':'Interact';return `<div class="focus-object"><div><strong>${htmlSafe(name)}</strong><small>${htmlSafe(description)}</small></div><button class="btn ${done?'':'p'}" ${done?'disabled':''} onclick="sceneAction('${id}');wardCloseFocus()">${verb}</button></div>`}).join('');
 area.innerHTML=`<div class="focus-inner"><div class="focus-top"><strong>${htmlSafe(group.label)}</strong><button class="btn" onclick="wardCloseFocus()" aria-label="Close inspection">Back to room ×</button></div><div class="focus-object-illustration"><svg viewBox="0 0 800 330" aria-hidden="true">${drawProp(group.kind,50,56)}</svg></div><div class="focus-objects">${actions}</div></div>`;
}
function wardCloseFocus(){S.sceneFocus=null;renderScene()}
function wardPrepareUi(){const controls=$('survivalControls'),actions=document.querySelector('.story-actions'),msgs=document.querySelector('.message-stream');if(controls&&actions&&!controls.contains(actions))controls.appendChild(actions);if(msgs&&!document.querySelector('.narrative-focus').contains(msgs))document.querySelector('.narrative-focus').appendChild(msgs);
 const btn=$('lightBtn');if(btn)btn.setAttribute('aria-label','Toggle flashlight');
 const heading=document.querySelector('.scene-title-row small');if(heading)heading.textContent='Click doors, furniture and objects directly';
}
const wardBaseRender=render;
render=function(){wardPrepareUi();wardBaseRender();if(S){const btn=$('lightBtn');if(btn)btn.classList.toggle('torch-active',S.lightOn);const body=$('game');body?.classList.toggle('world-blackout',!!R[S.room]?.dark&&!lit());}}
const wardBaseAct=act;
act=function(id){if(id==='regulator'){if(S.f.maintenancePrepared)return interaction('The regulator has been realigned.');if(!has('Archive Key'))return interaction('The regulator cabinet is bolted shut. I need the Archive Key to reach its adjustment assembly.');S.f.maintenancePrepared=1;S.ob.regulator='done';interaction('Using the Archive Key, I open the regulator housing, clean the contacts and reseat the coils. The generator can safely accept the fuse now.');lg('Generator regulator repaired with Archive Key.');return render()}
 if(id==='lateShotgun'){if(!S.f.power||!S.f.photoPuzzleSolved)return interaction('The shotgun case is locked behind an electronic authorization. Security must restore the staff photograph clearance first.');if(S.ob[id]==='done')return interaction('The case is empty.');if(!add('Shotgun',1))return interaction('Not enough inventory space. The shotgun remains safely in its case.');S.ob[id]='done';interaction('Retrieved the restricted security shotgun. It was held here under Monolith containment authority.');return render()}
 if(!S.f.ammoSnakeSeen&&S.san<55&&R[S.room].o.some(o=>o[0]===id&&o[4]?.give?.some(g=>/Ammo|Shells|Rounds/.test(g[0])))){S.f.ammoSnakeSeen=1;interaction('The cartridges twitch against one another. Something dark coils between them, and for a moment the open box seems full of living scales. When I look again, the ammunition is unchanged.');S.san=Math.max(0,S.san-2);return render()}
 if(S.f.wet&&!S.f.wetFumbled&&(R[S.room].o.find(o=>o[0]===id)?.[4]?.doc)){S.f.wetFumbled=1;advanceTime(2);interaction('My wet hands lose their grip on the pages. They slip to the floor. I crouch, retrieve the document, and steady my fingers.');return render();}
 if(id==='finalJournal'){if(!S.f.researcherLastRoomSeen)return researcherLastRoom();return doc('Final Research Entry')}
 if(id==='sprinkler')return wardSprinkler();
 return wardBaseAct(id);
}
function wardSprinkler(){if(S.f.sprinklerStopped)return interaction('The repaired pressure valve stays shut. The corridor is damp, but no more water falls.');if(!S.f.sprinklerTriggered){S.f.sprinklerTriggered=1;S.f.wet=1;S.f.wetTurns=0;S.f.flashlightDropped=1;S.lightOn=false;S.san=Math.max(0,S.san-3);modal('THE PRESSURE LINE',`<div class="unique-event"><p>A corroded suppression pipe bursts overhead. Freezing water drives you against the wall. The flashlight slips from your fingers and lands in the spray.</p><p class="unique-thought">My fingers are numb. I need to shut this valve and collect the light.</p></div><button class="btn p" onclick="closeModal()">Get out of the spray</button>`);render();return}
 if(!S.f.flashlightRecovered){S.f.flashlightRecovered=1;S.f.flashlightDropped=0;S.f.sprinklerStopped=1;interaction('I retrieve the flashlight from beneath the pipe and force the shutoff wheel closed. My clothes are soaked, and the metal is freezing against my palms.');return render()}
}
const wardBaseAdvance=advanceTime;
advanceTime=function(n=1){wardBaseAdvance(n);if(!S)return;if(S.f.wet){S.f.wetTurns=(S.f.wetTurns||0)+n;if(S.f.wetTurns>=18&&!S.f.wetNotice){S.f.wetNotice=1;interaction('My soaking clothes are turning cold. My hands shake when I try to steady them.');}if(S.f.wetTurns>=45||['lobby','chapel','generator'].includes(S.room)&&S.f.power){S.f.wet=0;interaction('The air is warm enough here. The shaking finally subsides.');}}}
// A late first-floor arc that cannot be skipped simply by pressing the elevator button.
const wardBaseArrival=chapterArrival;
chapterArrival=function(from,to){
 if(to==='records'&&!S.f.researcherLastRoomSeen&&S.f.power)return researcherLastRoom();
 if(to==='observation'&&!S.f.plexiIncidentSeen&&S.f.power){plexiIncident();return true}
 if(to==='surgery'&&!S.f.doctorWallSeen&&S.f.power)return doctorAtWall();
 if(S.f.power&&!S.f.pursuerStarted&&S.f.photoPuzzleSolved&&S.f.plexiIncidentSeen&&S.f.researcherLastRoomSeen&&['laundry','ward','security','archive'].includes(to))return awakenPursuer();
 return wardBaseArrival(from,to);
}
// Do not let chapter progression depend only on one visit to the elevator.
const wardBaseDoorOpen=doorOpen;
doorOpen=function(id){if(id==='liftEntry')return !!S.f.chapter1Ready;return wardBaseDoorOpen(id)}
// Check final gate on actual progression, not simply on discovery of one note.
const wardBaseGo=go;
go=function(to,confirmed=false){
 if(to==='lift'&&!S.f.chapter1Ready){const reasons=[];
  if(!S.f.power)reasons.push('restore the generator');if(!S.f.photoPuzzleSolved)reasons.push('recover corporate clearance');if(!S.f.plexiIncidentSeen)reasons.push('investigate the restricted observation ward');if(!S.f.pursuerStarted||!(S.f.pursuerEscapes>0))reasons.push('survive Subject X');
  if(!S.f.researcherLastRoomSeen)reasons.push('recover the researcher’s evidence');
  if(reasons.length)return interaction('The containment elevator is mechanically locked. I still need to '+reasons.join(', ')+'.');S.f.chapter1Ready=1;
 }
 return wardBaseGo(to,confirmed)
}
// Properly mark photo solve flag from the existing portrait interaction system.
const wardBasePortraitChoice=portraitChoice;
portraitChoice=function(name){wardBasePortraitChoice(name);if(S?.f?.photoPuzzleSolved)S.f.portraitSolved=1;}
const wardBasePursuerAction=escapePursuer; // current encounter resolution
escapePursuer=function(how){wardBasePursuerAction(how);if(S&&S.f.pursuerEscapes>0){S.f.pursuerChaseComplete=1;initPursuer().cooldown=Math.min(1,initPursuer().cooldown||1)}}
// Ensure old story nomenclature does not survive in newly generated journal entries.
DOCS['Monolith Executive Directive']=DOCS['Monolith Executive Directive']||'MONOLITH PHARMACEUTICALS\nPreserving Life. Securing Peace.\n\nAll exterior doors are to remain secured until executive clearance.';

// Situational effects remain in the scene, never as permanent HUD meters.
const wardBaseToggleLight=toggleLight;
toggleLight=function(){if(S?.f?.flashlightDropped)return interaction('The flashlight lies under the spraying pipe. I must retrieve it before I can switch it on.');return wardBaseToggleLight()};
const wardBaseGoInjured=go;
go=function(to,confirmed=false){if(S&&S.hp<=50&&to!==S.room){S.t+=S.hp<=25?3:1;if(!S.f.injuryWarning){S.f.injuryWarning=1;interaction('Pain catches in my leg as I move. I cannot run as steadily as before.')}}return wardBaseGoInjured(to,confirmed)};
function wardFalseEncounter(){if(S.f.falseEncounterSeen)return false;S.f.falseEncounterSeen=1;modal('An infected orderly',`<div class="unique-event"><p>A figure drags itself out of a dark alcove. Its arms hang at an unnatural angle. It advances as though it knows where you will move next.</p><p class="unique-thought">No. Stay back.</p><p>It is almost close enough to strike.</p></div><button class="btn p" onclick="wardResolveFalseEncounter('hold')">Hold position</button><button class="btn" onclick="wardResolveFalseEncounter('run')">Retreat quietly</button><button class="btn" onclick="wardResolveFalseEncounter('fire')">Fire a shot</button>`);return true}
function wardResolveFalseEncounter(choice){let text='';if(choice==='fire'){if(W[S.eq]&&(S.ld[S.eq]||0)>0){S.ld[S.eq]--;soundEffect('shot');noise();text='The shot strikes the tiled wall. A black silhouette hangs in the smoke. When the echoes fade, there is nobody there. One real round is gone.';}else text='I reach for a weapon, but there is nothing loaded. The figure sways, then disappears without a sound.';}else if(choice==='run'){text='I turn into the corridor and shut the door. There are no footsteps behind me. The next room is empty.';}else{text='I hold still. The orderly moves closer, then flickers like a reflection in uneven glass. Nothing remains where it stood.';}S.f.falseEncounterResolved=1;$('m').innerHTML='';interaction(text);lg('A threatening figure disappeared. No physical injuries were sustained.');render()}
const wardPreviousArrival=chapterArrival;
chapterArrival=function(from,to){const result=wardPreviousArrival(from,to);if(result)return result;if(S&&!S.f.falseEncounterSeen&&san()<52&&S.f.plexiIncidentSeen&&!S.f.pursuerStarted&&!alive(to)&&['eastcorridor','security','ward','laundry'].includes(to)){return wardFalseEncounter()}return result};
// Optional online AI graphics belong to the settings screen, not the main HUD.
const wardOriginalOptions=optionsModal;
optionsModal=function(){wardOriginalOptions();const body=document.querySelector('#m .mb');if(!body)return;const enabled=!!window.WardArt?.settings?.enabled;body.insertAdjacentHTML('beforeend',`<div class="options-online-art"><h3>Online environment art (optional)</h3><p class="micro">Hosted editions can request AI-enhanced backgrounds from a configured server. Bundled room art and gameplay work offline, including during connection loss.</p><label class="audio-label"><input type="checkbox" id="onlineArtSetting" ${enabled?'checked':''} onchange="WardArt.update(this.checked)"> Request online art when a server is available</label><p class="micro">A compatible generation server is required. This download does not include a paid AI service.</p></div>`)};
