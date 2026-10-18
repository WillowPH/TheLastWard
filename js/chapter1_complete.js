/* Chapter 1 production boundary and progression. The uploaded cinematic project is
   the baseline; no room, map or renderer from the rejected pilot is imported. */
(function(){
'use strict';
const BUILD='last-ward-ch1-roomviews-4';
const ROOMS=['lobby','security','eastcorridor','ward','wardnorth','wardservice','room12','isoward','archive','pharmacy','laundry','generator','powercontrol','boiler','tunnel','morgue','chapel','children','residence','stafflounge','records','surgery','observation','specimen','isolation','coldstore','lift'];
window.WardChapter={BUILD,rooms:ROOMS};
for(const id of Object.keys(R))if(!ROOMS.includes(id))delete R[id];
for(const id of ROOMS){R[id].ch=1;FIRST_FLOOR.add(id);}
for(const id of [...FIRST_FLOOR])if(!R[id])FIRST_FLOOR.delete(id);
// Observation and emergency electrical work are upstairs. B2 remains future content.
D.os={a:'observation',b:'specimen',need:'Encrypted Drive'};
D.spc={a:'specimen',b:'powercontrol',flag:'power'};
delete D.gp;D.oi={a:'powercontrol',b:'isolation',flag:'power'};
for(const id of Object.keys(D))if(!R[D[id].a]||!R[D[id].b])delete D[id];
// Return shortcuts use the same physical room entrances, not additional floating doors.
delete D.serviceReturn;delete D.sl;R.surgery.o.push(['surgeryExit','Bolted theatre exit','▥','A second theatre door is sealed by containment bolts.',{look:1,th:'The emergency release was deliberately disabled.'}]);
for(const id of Object.keys(E))if(!R[id])delete E[id];
for(const id of ['lobby','chapel','generator','lift']){R[id].safe=1;SAFE_FROM_PURSUER.add(id)}
SAFE_FROM_PURSUER.delete('sublevel');SAFE_FROM_PURSUER.delete('containment');
for(const id of ['wardnorth','wardservice','powercontrol','specimen','observation'])WARD_POWERED.add(id);
for(const id of ['wardservice','isoward','laundry','security','room12','archive','surgery','records','residence','stafflounge','pharmacy'])HIDING_AREAS.add(id);
const remove=(room,ids)=>R[room].o=R[room].o.filter(o=>!ids.includes(o[0]));
// The keypad is beside the pharmacy door, not in an unrelated wing.
const keypad=R.ward.o.find(o=>o[0]==='kp');remove('ward',['kp','drg']);R.wardservice.o.push(keypad);
R.wardservice.o.push(['serviceTrail','Drag marks','◈','Tracks emerge beneath the pharmacy door.',{look:1,after:'pharm',th:'Something crawled into the dispensary. It walked back out.'}]);
R.pharmacy.o.push(['maintenanceKit','Maintenance tool roll','⚒','Insulated contact tool and a small spanner, left for Martin Heller.',{give:[['Maintenance Tools',1]]}]);
ICON['Maintenance Tools']='⚒';ITEM_ART['Maintenance Tools']='assets/items/maintenance_tool.png';
// One logical fixture per object. Decoration and empty legacy weapon caches do not become loot.
remove('coldstore',['cacheammo']);
R.powercontrol.o.push(['clearance','Containment authorization console','▦','An executive clearance terminal. A removable archive drive fits its slot.',{act:'clearance'}]);
R.generator.o.push(['handCharge','Emergency hand charger','⚙','A manual dynamo beside the maintenance bench. Slow, but independent of mains power.',{act:'handCharge'}]);
R.lift.o.push(['finalTerminal','Continuity Terminal','▦','A final record station before the descent.',{act:'save'}],['finalRibbon','Emergency record spool','▥','One sealed Ink Ribbon beside the record station.',{give:[['Ink Ribbon',1]]}]);
R.lift.safe=1;
R.lift.o.push(['finalBox','Field cache','▣','Transfer storage for equipment you may need below.',{act:'box'}]);
R.surgery.o.push(['shotShells','Sealed shotgun shell sleeve','◉','Four shells beside the restricted shotgun case.',{give:[['Shotgun Shells',4]],after:'photoPuzzleSolved'}]);
R.isoward.n='Isolation Treatment Room';R.isolation.n='Restricted Isolation Room';
R.observation.d='Reinforced viewing windows separate the first-floor observation ward from sealed trial chambers. A records console remains under emergency power. The more heavily scratched pane is isolated behind a yellow floor line.';
R.records.d='The Records Annex smells of warm paper and stale antiseptic. A researcher’s final notes rest beside a field recorder. A carbon-copy cabinet conceals a photographic lock; no public exit leads through this room.';
DOCS['Maintenance Log']+='\n\nREGULATOR SERVICE — MARTIN HELLER\nUse the insulated maintenance tool roll from Pharmacy to reseat the contacts. Only then install the ceramic fuse. A manual dynamo can recover emergency flashlight charge.';
DOCS['Observation Safety Notice']='MONOLITH PHARMACEUTICALS\nPreserving Life. Securing Peace.\n\nRestricted viewing cell: do not approach scratched glass. A subject has broken the inner laminate. A second approach may provoke a lethal breach. This inspection is not required for clearance.';
R.observation.o.push(['glassNotice','Observation safety notice','▤','A plain warning secured to the viewing-room rail.',{doc:'Observation Safety Notice'}]);
DOCS['Isolation Patient Chart']=DOCS['Isolation Patient Chart'].replace('PATIENT 14','DANIEL MERCER — PATIENT 14');
// Retire carryover seal rewards whose only locks belonged to later chapters.
const reliquary=R.chapel.o.find(o=>o[0]==='rel');reliquary[3]='One sealed dressing rests inside the reliquary’s emergency aid compartment.';reliquary[4]={give:[['Trauma Dressing',1]]};
const mortuary=R.morgue.o.find(o=>o[0]==='dw');mortuary[3]='A transfer slip has been filed inside the empty drawer.';mortuary[4]={doc:'Mortuary Transfer Slip'};
DOCS['Mortuary Transfer Slip']=`BLACKRIDGE MORTUARY — THOMAS REED

The missing nurse was not among the admissions to this room. A personal locket was returned to Staff Residence. No authorized transfer appears in Strickland’s evacuation report.

Someone used the service elevator after exterior lockdown.`;
const furnace=R.boiler.o.find(o=>o[0]==='fur');furnace[3]='A heatproof service compartment holds one usable precision part.';furnace[4]={give:[['Stabilizer Part',1]]};
const previousDescription=desc;
desc=function(name){return ({'Maintenance Tools':'Insulated contact tools. Used to reseat the damaged generator regulator.','Encrypted Drive':'Observation archive drive. Used to verify final transfer clearance in Emergency Power Control.','Cabinet Key':'Reception cabinet key. Opens the nurse equipment box and Room 12 medical cabinet.','Power Fuse':'Ceramic generator fuse. Install only after repairing the regulator.'})[name]||previousDescription(name)};
const tunnelKey=R.tunnel.o.find(o=>o[0]==='tk');delete tunnelKey[4].after;tunnelKey[3]='A key suspended beyond the flooded working platform. The winch can bring it within reach.';
// An explicit final gate shared by map travel, doors and the elevator controls.
function requirements(){return [[S.f.power,'restore generator power'],[S.f.photoPuzzleSolved,'recover executive photograph clearance'],[S.f.plexiIncidentSeen,'investigate the observation incident'],[S.f.researcherLastRoomSeen,'recover Rourke’s final evidence'],[S.f.doctorWallSeen,'investigate the surgical theatre'],[S.f.finalSecurityClearance,'authorize the containment console'],[S.f.pursuerStarted&&(S.f.pursuerEscapes||0)>0,'escape Subject X']].filter(r=>!r[0]).map(r=>r[1]);}
WardChapter.requirements=requirements;
const previousDoor=doorOpen;
doorOpen=function(id){if(!D[id]||!S)return false;if(id==='liftEntry')return requirements().length===0;return previousDoor(id)};
const previousGo=go;
go=function(to,confirmed=false){if(!S||!R[to]||S.f.chapter1Complete)return;if(S.f.hidingRoom)return interaction('Leave your hiding place before moving.');if(to==='lift'){const missing=requirements();if(missing.length)return interaction('Containment elevator locked. I still need to '+missing.join(', ')+'.');S.f.chapter1Ready=1;}return previousGo(to,confirmed)};
// Stable seeded supplies without placing a random object on a blank wall.
configureWorld=function(seed,preserve=true){const old=S.en||{};for(const r of Object.values(R))r.o=r.o.filter(o=>!o[0].startsWith('seedloot_'));
 const candidates=['laundry','morgue','boiler','children','isolation','specimen','powercontrol','stafflounge'];candidates.sort((a,b)=>hashSeed(seed+'enemy'+a)-hashSeed(seed+'enemy'+b));S.spawnRooms=candidates.slice(0,S.m<1?2:3);S.en={};for(const id of S.spawnRooms)S.en[id]=preserve&&Number.isFinite(old[id])?Math.max(0,Math.min(E[id].hp,old[id])):E[id].hp;
 if(preserve&&old.eastcorridor!==undefined)S.en.eastcorridor=old.eastcorridor;
 S.enemySeed=seed;
 const candidatesLoot=['security','laundry','pharmacy','stafflounge'];const room=candidatesLoot[hashSeed(seed+'lootroom')%candidatesLoot.length];const pool=[['Handgun Ammo',S.m<1?6:3],['Trauma Dressing',1],['Battery',1],['Ink Ribbon',1]],item=pool[hashSeed(seed+'loot')%pool.length];R[room].o.push(['seedloot_0','Emergency supply pouch','▣','One sealed staff supply pouch.',{give:[item]}]);
};
placeTelephones=function(seed){for(const r of Object.values(R))r.o=r.o.filter(o=>!/^phone_(stage|decoy)_/.test(o[0]));S.phoneRooms=phoneRoomsForSeed(seed);
 S.phoneRooms.slice(1).forEach((room,i)=>R[room].o.push(['phone_stage_'+(i+2),'Wall telephone','☎','A hard-wired hospital telephone.',{act:'payphone'}]));
 ['security','chapel','isoward'].sort((a,b)=>hashSeed(seed+a)-hashSeed(seed+b)).slice(0,2).forEach((room,i)=>R[room].o.push(['phone_decoy_'+i,'Disconnected telephone','☎','A disconnected desk telephone.',{act:'payphone'}]));
};
rechargeAtGenerator=function(){if(!has('Flashlight'))return interaction('Retrieve the flashlight from storage first.');if(!S.f.power)return interaction('The charging cradle needs generator power.');S.bat=Math.max(S.bat,8);S.lightTicks=0;soundEffect('relay');interaction('The powered charging cradle restores the flashlight.');render()};
const inheritedAct=act;
act=function(id){const o=R[S.room]?.o.find(o=>o[0]===id);if(!o||S.f.chapter1Complete)return;
 if(id==='regulator'){if(S.f.maintenancePrepared)return interaction('The repaired regulator is seated correctly.');if(!has('Maintenance Tools'))return interaction('The contacts are fused. Martin Heller’s log calls for the insulated maintenance tool roll from Pharmacy.');S.f.maintenancePrepared=1;S.ob[id]='done';interaction('I clean and reseat the damaged regulator contacts with the insulated tool. It can accept the fuse now.');soundEffect('metal');lg('Repaired generator regulator with maintenance tools.');return render()}
 if(id==='handCharge'){if(!has('Flashlight'))return interaction('The flashlight is in storage.');if(S.bat>=3)return interaction('There is enough charge for emergency exploration.');advanceTime(4);S.bat=Math.max(S.bat,3);S.lightTicks=0;interaction('Four slow turns of the dynamo. The flashlight has enough charge to find the next safe route.');soundEffect('mechanism');return render()}
 if(id==='clearance'){if(S.f.finalSecurityClearance)return interaction('Executive transfer clearance is recorded. The service elevator can verify it.');if(!S.f.power||!S.f.photoPuzzleSolved||!S.f.researcherLastRoomSeen||!has('Encrypted Drive'))return interaction('The console needs power, executive portrait authorization, Rourke’s final record, and the archive drive from Observation.');S.f.finalSecurityClearance=1;S.ob[id]='done';S.docs.push('Containment Transfer Authorization');DOCS['Containment Transfer Authorization']='MONOLITH PHARMACEUTICALS\nPreserving Life. Securing Peace.\n\nOne surviving operator is cleared for the restricted service elevator. Exterior evacuation remains forbidden. Transfer is subject to containment pursuit protocol.';interaction('The drive verifies the executive record. The terminal authorizes a single downward transfer.');soundEffect('relay');lg('Authorized final service-elevator clearance.');return render()}
 if(id==='staffSprinkler')return wardSprinkler();
 if(id==='pan'&&S.f.power)return interaction('The diesel generator is already running.');
 // A physical pickup is atomic. Full inventory leaves it available in its own fixture.
 if(id==='tk'&&!S.f.drained)return interaction('The key hangs beyond the flooded working platform. The winch must release its chain before I can reach it.');
 const beforePower=S.f.power;const result=inheritedAct(id);if(!beforePower&&S.f.power){soundEffect('generator');S.f.powerOut=0;}return result;
};
// Replace the older contradictory pair of researchers with Rourke's one final room.
researcherEncounter=function(){return false};researcherAftermath=function(){return false};finishResearcherScene=function(){closeModal()};
const baseExam=exam;
exam=function(id){if(id==='glasssound')return inspectObservationGlass();return baseExam(id)};
// Never let a UI close button count as escaping a physical pursuer.
closeModal=function(){if(!S)return void($('m').innerHTML='');if(!S.f.introComplete)return introStep();if(S.hp<=0)return die();if(S.f.pursuerEncounter)return pursuerEncounter();$('m').innerHTML='';if(cm&&alive(S.room))combat()};
// The last room is the elevator. There is no Chapter 2 room to enter in this build.
inspectLiftControlsLegacy=function(){if(requirements().length)return interaction('The containment transfer is not authorized.');modal('The final descent','<div class="unique-event"><p>The cage gate closes around you. Below the public basement, an unmarked stop waits in darkness.</p><p class="unique-thought">If the recording is real, I helped build what is down there. I need to know why.</p></div><button class="btn p" onclick="beginDescent()">Descend · End Chapter 1</button><button class="btn" onclick="closeModal()">Stay on the first floor</button>')};
finishChapterOneReveal=function(){$('m').innerHTML='';inspectLiftControlsLegacy()};
beginDescent=function(){if(S.room!=='lift'||requirements().length||!S.f.chapter1Revelation||S.f.chapter1Complete)return;S.f.chapter1Complete=1;S.f.liftDescended=1;S.f.liftRideDone=1;S.pursuer.active=false;S.f.pursuerEncounter=0;S.sceneFocus=null;cm=0;advanceTime(2);lg('Chapter 1 complete. The elevator descends below Blackridge.');soundEffect('elevator');
 try{localStorage.setItem('lw_ch1_completion_v1',JSON.stringify({game:'The Last Ward',format:2,chapter:1,build:BUILD,record:S}));S.f.completionSaved=1}catch(e){S.f.completionSaved=0}
 $('m').innerHTML='';render();};
window.wardExportCompletion=function(){if(!S?.f.chapter1Complete)return;const blob=new Blob([JSON.stringify({game:'The Last Ward',format:2,chapter:1,build:BUILD,record:S})],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='The_Last_Ward_Chapter_1_Completed.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),3000)};
// The floor plan uses one fixed coordinate system for all 27 rooms.
const positions={lobby:[45,330],security:[45,280],eastcorridor:[110,300],ward:[170,300],wardnorth:[230,300],wardservice:[290,260],room12:[230,345],isoward:[290,345],residence:[170,345],stafflounge:[110,345],children:[350,345],archive:[220,210],records:[290,210],coldstore:[350,210],chapel:[150,210],generator:[220,145],lift:[150,145],pharmacy:[350,260],laundry:[290,145],surgery:[350,145],powercontrol:[290,80],specimen:[350,80],observation:[220,80],isolation:[290,30],morgue:[150,80],tunnel:[85,80],boiler:[150,30]};
for(const [id,[x,y]] of Object.entries(positions)){R[id].x=x;R[id].y=y;}
for(const id of ['wardnorth','wardservice'])FIRST_MAP.add(id);
// New topology gets separate save keys and rejects older records without overwriting them.
const baseValid=valid;valid=function(o){return !!(baseValid(o)&&o.buildId===BUILD&&R[o.room]&&o.inv.every(x=>x&&typeof x.n==='string'&&Number.isFinite(x.c)&&x.c>0))};
const baseNew=newGame;newGame=function(){baseNew();S.buildId=BUILD;S.bat=S.m<1?12:S.m>1?7:10;S.presentation.hints=false;render()};
// Capture a final-route checkpoint without consuming ribbons; explicit recovery stays separate from saves.
const baseArrival=chapterArrival;
chapterArrival=function(from,to){if(to==='lift'){S.f.liftSeen=1;try{localStorage.setItem('lw_ch1_finale_checkpoint',JSON.stringify(S))}catch(e){}inspectLiftControls();return true}return baseArrival(from,to)};
window.wardLoadFinale=function(){try{const data=JSON.parse(localStorage.getItem('lw_ch1_finale_checkpoint'));if(!valid(data))return toast('No compatible finale checkpoint.');S=data;S.hp=Math.max(35,S.hp);S.f.chapter1Complete=0;S.f.pursuerEncounter=0;S.pursuer.cooldown=3;configureWorld(S.seed,true);placeTelephones(S.seed);$('m').innerHTML='';$('setup').classList.add('hid');$('game').classList.remove('hid');render()}catch(e){toast('The finale checkpoint is unavailable.')}};
// Persistent journal leads reflect obstacles actually discovered, without exposing code solutions.
journal=function(){const leads=[];if(!S.mapParts)leads.push('An evacuation plan may be in Security.');if(S.vis.generator&&!S.f.power)leads.push('The generator needs its contacts repaired and a ceramic fuse. Read Heller’s maintenance notes.');if(S.f.power&&!S.f.photoPuzzleSolved)leads.push('The restored Security portrait lamp may reveal something new.');if(S.vis.observation&&!S.f.finalSecurityClearance)leads.push('The archive drive belongs in a containment authorization terminal.');if(S.f.pursuerStarted&&!(S.f.pursuerEscapes>0))leads.push('I need to break contact with the masked pursuer.');modal('Journal','<h3>Unresolved leads</h3>'+leads.map(x=>'<p>'+htmlSafe(x)+'</p>').join('')+'<h3>Thoughts and discoveries</h3>'+(S.th2||[]).slice(-12).map(x=>'<p>'+htmlSafe(x)+'</p>').join(''))};
})();
