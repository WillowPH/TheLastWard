/* Chapter 1 story events. All one-time encounters persist in S.f through save/load.
   The pursuer moves only along traversable first-floor links, never teleports. */
const FIRST_FLOOR=new Set(['lobby','security','eastcorridor','ward','isoward','room12','archive','laundry','children','surgery','records','residence','stafflounge','chapel','pharmacy']);
const SAFE_FROM_PURSUER=new Set(['lobby','chapel','generator','lift','sublevel','containment']);
const HIDING_AREAS=new Set(['security','room12','isoward','archive','laundry','surgery','records','residence','stafflounge','pharmacy']);
function initPursuer(){if(!S.pursuer)S.pursuer={active:false,room:'laundry',steps:0,cooldown:0,noise:0};return S.pursuer}
function makePursuerCheckpoint(){try{localStorage.setItem('lw_chapter1_pursuer_checkpoint',JSON.stringify(S));S.f.pursuerCheckpoint=1}catch(e){/* Browsers may disable storage. Player can still evade. */}}
function awakenPursuer(){
 const p=initPursuer();if(S.f.pursuerStarted)return false;
 S.f.pursuerStarted=1;p.active=true;p.room='laundry';p.steps=0;p.cooldown=2;
 makePursuerCheckpoint();
 S.th2=S.th2||[];S.th2.push('The security shutters did not malfunction. Something is walking the floor, and I think it is looking for me.');
 lg('Three heavy impacts buckle a service shutter. The footsteps begin.');
 soundEffect('door');
 modal('Something has been released',
  '<div class="unique-event"><p>From the laundry wing: <b>THUD. THUD. THUD.</b></p><p>A reinforced service door bends outward. A large figure in torn clinical restraints stoops through the opening. Its face is hidden by an opaque recovery mask. It pauses, listening.</p><p class="unique-thought">That thing is not wandering. It is looking for someone. I think it knows where I am.</p><p>Stay quiet, change routes, or hide behind room furnishings. Its heavy steps give you warning. You are not expected to kill it.</p></div><button class="btn p" onclick="closeModal();pursuerEncounter()">Move carefully</button>');
 render();return true;
}
// Telephone system lives in chapter_events.js; no duplicate handlers here.
function inspectLiftControlsLegacy(){
 if(S.f.liftDescended){interaction('The B2 button remains lit. The doors can now reach the underground complex.');return}
 if(!S.f.power)return interaction('Without the generator, the elevator has no power.');
 modal('Restricted elevator', '<div class="unique-event"><p>The floor selector has an extra position beneath the label B1. It reads <b>B2 — CONTAINMENT</b>.</p><p>The emergency brake is already released. A thumbprint sits in the dust beside the lower button. It is the same size as yours.</p><p class="unique-thought">Why does my hand know which button to press?</p></div><button class="btn p" onclick="beginDescent()">Descend to B2</button><button class="btn" onclick="closeModal()">Stay upstairs</button>');
}
function beginDescent(){
 if(S.f.liftDescended)return;
 S.f.liftDescended=1;S.f.liftRideDone=1;
 lg('The restricted elevator falls silent halfway down, then sinks below the public basement.');
 S.th2=S.th2||[];S.th2.push('There is another hospital underneath this one. Someone erased it from every map.');
 soundEffect('door');advanceTime(2);
 render();modal('Below the hospital','<div class="unique-event lift-ride"><p>The cage rattles down past the public basement.</p><p>Then it stops. The lights die. Something crawls slowly across the elevator roof.</p><p>One long scrape.</p><p>Without warning, the motor starts again. The descent continues far deeper than it should.</p><p class="unique-thought">How far down does this place go?</p></div><button class="btn p" onclick="closeModal()">Wait for the doors to open</button>');
}
function oneTimeSpeaker(){
 if(S.f.lowerSpeakerHeard)return toast('The speaker has been quiet since you stood beneath it.');
 S.f.lowerSpeakerHeard=1;S.ob.lowervoice='read';
 const line='The ceiling speaker clicks. A woman begins to say your name, then stops before the first syllable. After a pause, a recording of your own footsteps plays back from a hallway you have not entered.';
 interaction(line);S.th2.push('They recorded my footsteps before I walked down here.');lg('An underground speaker played footsteps you have not made yet.');
 render();modal('Ceiling speaker','<div class="unique-event"><p>'+line+'</p><p class="unique-thought">No. This has to be a tape.</p><small>This recording plays only once.</small></div><button class="btn p" onclick="closeModal()">Continue</button>');
}
// One-time first-floor encounters. Their consequences never depend on the presentation setting.
function doctorAtWall(){
 if(S.f.doctorWallSeen)return false;
 S.f.doctorWallSeen=1;
 S.san=Math.max(0,(S.san??100)-14);
 S.th2=S.th2||[];
 const clue='A doctor in the surgical corridor repeated a warning: “You were awake the first time.”';
 if(!S.th2.includes(clue))S.th2.push(clue);
 lg('The doctor in the surgical corridor stopped moving. The encounter will not repeat.');
 const scene=sceneDetail(
  '<p><b>THUD. THUD. THUD.</b> A doctor in a bloodstained coat drives his forehead into the tiled wall again and again. Each impact leaves another crimson mark. He does not seem to feel it.</p><div class="doctor-stain" aria-hidden="true"></div><p>He stops, turns a blood-smeared face toward you and whispers, “You were awake the first time.” Then his knees buckle.</p>',
  '<p><b>THUD. THUD. THUD.</b> Hard impacts echo from a tiled alcove. A doctor stands facing the wall. You call out. The sounds stop.</p><p>Without turning, he whispers, “You were awake the first time.” He sinks out of sight behind the examination curtain.</p>');
 render();modal('The doctor at the wall','<div class="doctor-wall-scene"><div class="doctor-vignette" role="img" aria-label="A silhouetted doctor repeatedly strikes a tiled wall"><div class="doctor-wall-tiles"></div><div class="doctor-figure"><span class="doctor-head"></span><span class="doctor-body"></span></div><div class="doctor-impact"></div></div>'+scene+'<p class="unique-thought">Stop. Please stop. What is happening to these people?</p><p class="micro">Composure shaken.</p></div><button class="btn p" onclick="finishWallDoctor()">Back away</button>');
 const close=$('m').querySelector('.mh button');if(close)close.remove();return true;
}
function finishWallDoctor(){$('m').innerHTML='';render();if(alive(S.room))combat()}
function researcherLastRoom(){
 if(S.f.researcherLastRoomSeen)return false;
 S.f.researcherLastRoomSeen=1;
 S.san=Math.max(0,(S.san??100)-10);
 S.th2=S.th2||[];
 const clue='A researcher left a final entry describing the LULLABY procedure as something that could not be stopped by forgetting.';
 if(!S.th2.includes(clue))S.th2.push(clue);
 if(!S.docs.includes('Final Research Entry'))S.docs.push('Final Research Entry');
 lg('Discovered a researcher’s final journal. The room is unchanged on return.');
 const scene=sceneDetail(
  '<p>The room is too warm. Beneath the smell of antiseptic is the sour odor of decomposition. A researcher hangs motionless beyond an overturned chair; the body has begun to decay. Flies gather at the window.</p>',
  '<p>The door opens on stale, sour air and an overturned chair. A researcher has died here. You look away from the body, toward a notebook left on the desk.</p>');
 render();modal('The last room','<div class="unique-event">'+scene+'<p>On the desk lies a final journal entry. It is filed automatically under Files, not carried as an item.</p><p class="unique-thought">There was no help left in this building. What made him think this was his only way out?</p><p class="micro">Composure shaken · New file: Final Research Entry</p></div><button class="btn p" onclick="showFinalResearchEntry()">Read the entry</button><button class="btn" onclick="closeModal()">Leave the room</button>');return true;
}
function showFinalResearchEntry(){doc('Final Research Entry')}
function connectedOnFirstFloor(room){const next=[];for(const id in D){const d=D[id],to=d.a===room?d.b:d.b===room?d.a:null;if(to&&FIRST_FLOOR.has(to)&&doorOpen(id))next.push(to)}return next}
function pursuerPath(source,target){
 if(source===target)return [source];
 const queue=[[source]],seen=new Set([source]);
 while(queue.length){const path=queue.shift(),tail=path[path.length-1];for(const dest of connectedOnFirstFloor(tail)){if(seen.has(dest))continue;const n=[...path,dest];if(dest===target)return n;seen.add(dest);queue.push(n)}}return [];
}
function pursuerApproach(to){
 const p=initPursuer();if(!p.active||SAFE_FROM_PURSUER.has(to)||!FIRST_FLOOR.has(to))return false;
 if(p.cooldown>0){p.cooldown--;return false}
 if(p.room===to&&S.f.hidingRoom===to&&S.f.hidingUntil>=S.t){S.f.hidingRoom=null;p.cooldown=3;const route=connectedOnFirstFloor(p.room).find(x=>x!==to);if(route)p.room=route;interaction('The heavy steps approach your hiding place, stop, and eventually move away. You stay silent.');lg('Avoided Subject X while hidden.');return false;}
 if(p.room===to)return pursuerEncounter();
 p.steps=(p.steps||0)+1;
 const accelerate=p.noise>0;
 if(!accelerate&&p.steps<2){const distance=pursuerPath(p.room,to).length-1;if(distance===1)interaction('An irregular metallic footstep sounds behind the next door. It pauses, listening.');return false}
 p.steps=0;p.noise=Math.max(0,(p.noise||0)-1);
 const path=pursuerPath(p.room,to);
 if(path.length>1)p.room=path[1];
 if(p.room===to&&S.f.hidingRoom===to&&S.f.hidingUntil>=S.t){S.f.hidingRoom=null;p.cooldown=3;const route=connectedOnFirstFloor(p.room).find(x=>x!==to);if(route)p.room=route;interaction('The heavy steps approach your hiding place, stop, and eventually move away. You stay silent.');lg('Avoided Subject X while hidden.');return false;}
 if(p.room===to)return pursuerEncounter();
 if(path.length>0&&path.length<=3)interaction('Heavy footsteps draw closer through the service corridors. Find a quieter route.');
 return false;
}
function pursuerEncounter(){
 const p=initPursuer();if(S.f.pursuerEncounter)return true;
 S.f.pursuerEncounter=1;p.encounters=(p.encounters||0)+1;
 lg('Subject X enters '+R[S.room].n+' and searches the room.');
 soundEffect('door');
 const w=W[S.eq],loaded=w?(S.ld[S.eq]||0):0;
 const hide=HIDING_AREAS.has(S.room)?'<button class="btn p" onclick="escapePursuer(\'hide\')">Hide quietly</button>':'';
 modal('Heavy footsteps', '<div class="unique-event"><p>The figure in the opaque recovery mask fills the doorway. It stops. A slow breath rattles behind the plastic.</p><p class="unique-thought">It has seen the light. Don’t move. Don’t breathe.</p><p>It can be delayed, not defeated. Retreat, hide, or force your way past.</p></div>'+hide+'<button class="btn p" onclick="escapePursuer(\'retreat\')">Retreat through an open door</button><button class="btn" onclick="escapePursuer(\'push\')">Push past (risk injury)</button>'+(loaded?'<button class="btn" onclick="escapePursuer(\'shoot\')">Fire once to stagger ('+loaded+' loaded)</button>':'') );
 // No generic Close control to bypass this encounter.
 const x=$('m').querySelector('.mh button');if(x)x.remove();
 return true;
}
function escapePursuer(how){
 if(!S.f.pursuerEncounter)return;
 const p=initPursuer();S.f.pursuerEncounter=0;
 let description='';
 if(how==='shoot'){
  const w=W[S.eq];if(!w||!has(S.eq)||(S.ld[S.eq]||0)<=0)return pursuerEncounter();
  S.ld[S.eq]--;soundEffect('shot');p.noise=1;
  description='Your shot staggers the masked figure against a trolley. It rises again, but you have a head start. Ammo: '+S.ld[S.eq]+' / '+w.mag+'.';
 }else if(how==='hide'){
  description='You slip behind the furniture and stop breathing. The heavy steps pass, then fade into the corridor.';
 }else if(how==='push'){
  S.hp=Math.max(1,S.hp-8);description='You squeeze through a gap as it grabs your sleeve. You tear free, bruised but alive. Condition: '+conditionInfo(S.hp)[1]+'.';soundEffect('hit');
 }else{
  const before=S.room,opts=connectedOnFirstFloor(before);
  const to=opts.includes(S.prev)?S.prev:opts.find(x=>x!==p.room)||opts[0];
  if(to){S.room=to;S.prev=before;S.vis[to]=1;S.searchArea=null;S.searchAreaRoom=to;description='You retreat into '+R[to].n+' and pull the door shut behind you.';soundEffect('door')}
  else description='Every nearby door is locked. You duck under its arm and stagger away.';
 }
 p.cooldown=3;p.steps=0;const neighboring=connectedOnFirstFloor(p.room);const next=neighboring.find(r=>r!==S.room)||neighboring[0];if(next)p.room=next;
 S.f.pursuerEscapes=(S.f.pursuerEscapes||0)+1;
 $('m').innerHTML='';advanceTime(1);lg(description);interaction(description);combatNote('');render();
}
// Story arrivals are resolved once, separately from ordinary repeated room narration.
function chapterArrival(from,to){
 if(to==='surgery'&&!S.f.doctorWallSeen)return doctorAtWall();
 if(to==='b2sleep'&&!S.f.researcherLastRoomSeen)return researcherLastRoom();
 maybeRingRoomPhone(to);
 if(S.f.power&&S.f.photoPuzzleSolved&&S.f.plexiIncidentSeen&&S.f.researcherLastRoomSeen&&!S.f.pursuerStarted&&['archive','ward','laundry','security'].includes(to))return awakenPursuer();
 if(to==='lift'&&!S.f.liftSeen){S.f.liftSeen=1;inspectLiftControls();return true}
 if(to==='sublevel'&&!S.f.underground){
  S.f.underground=1;const p=initPursuer();p.active=false;S.f.pursuerEscaped=1;
  lg('Reached Blackridge B2. Heavy footsteps remain on the floor above.');
  S.th2=S.th2||[];S.th2.push('The underground hospital is cleaner than the one above. It was not abandoned.');
  render();modal('SUBLEVEL B2', '<div class="unique-event"><p>The elevator opens onto a spotless hospital corridor. Somewhere, a machine stamps a medical form. Nobody is there to collect it.</p><p>Behind you, the elevator door closes on the heavy footsteps far above.</p><p class="unique-thought">This place is still running. Who the hell is running it?</p></div><button class="btn p" onclick="closeModal()">Enter the underground facility</button>');return true;
 }
 if(to==='eastcorridor'&&S.f.pursuerStarted&&!S.f.windowThreatResolved){
  S.f.windowThreatResolved=1;
  if(S.f.windowBarricaded){
   lg('A heavy shape struck the boarded ward window, but the plank held.');
   interaction('Something slams against the planks. They shudder and hold. The corridor remains safe from the window.');
  }else{
   S.f.windowBroken=1;S.en.eastcorridor=E.eastcorridor.hp;
   lg('A window-breach infected forced its way into the East Corridor.');
   render();modal('The unprotected window', '<div class="unique-event"><p>The cracked window explodes inward. A hospital patient crawls through the glass, dragging a ruined IV pole behind it.</p><p class="unique-thought">I could have secured that opening. I can still retreat through a door.</p></div><button class="btn p" onclick="closeModal()">Keep moving</button>');
   return true;
  }
 }
 if(to==='containment'&&!S.f.lowerConveyor){
  S.f.lowerConveyor=1;S.th2=S.th2||[];S.th2.push('An empty gurney moved through the lower corridor, as though a patient had just been transferred.');
  interaction('An empty gurney rolls behind reinforced glass. Its restraints pull tight around nobody.');lg('An empty gurney moved along the underground conveyor.');
 }
 return pursuerApproach(to);
}

// The powered cradle prevents a resource softlock without scattering batteries everywhere.
function rechargeAtGenerator(){
 if(!S.f.power)return interaction('The generator is off. The charger has no power.');
 if(!has('Flashlight'))return interaction('The flashlight is in storage. Bring it here to recharge.');
 if(S.bat>=6)return toast('The flashlight is already fully charged.');
 const uses=S.f.generatorChargeUses||0;
 if(uses>=2)return interaction('The maintenance charger has burned out. Its last spare cell is exhausted.');
 S.f.generatorChargeUses=uses+1;S.bat=6;S.lightTicks=0;
 soundEffect('pickup');lg('Recharged the flashlight at the generator ('+S.f.generatorChargeUses+'/2 charges).');
 interaction('The cradle whines softly. The flashlight reaches full charge. One of the old capacitors goes dark.');
 render();
}

function loadFirstFloorCheckpoint(){
 try{
  const snap=localStorage.getItem('lw_chapter1_pursuer_checkpoint');if(!snap)return toast('No checkpoint is available.');
  const state=JSON.parse(snap);if(!valid(state))return toast('This checkpoint is invalid.');
  S=state;S.presentation=S.presentation||{violence:localViolenceChoice()};applyViolenceAppearance();S.hp=Math.max(S.hp,45);S.f.pursuerStarted=1;S.f.pursuerEncounter=0;
  S.pursuer=initPursuer();S.pursuer.active=true;S.pursuer.cooldown=3;
  S.mapMode='overview';S.searchArea=null;S.searchAreaRoom=null;
  configureWorld(S.seed,true);$('setup').classList.add('hid');$('game').classList.remove('hid');$('m').innerHTML='';
  lg('Recovered at the first-floor checkpoint. The footsteps are still somewhere nearby.');render();toast('First-floor checkpoint restored.');
 }catch(e){console.warn('[The Last Ward] Checkpoint failure',e);toast('Could not restore checkpoint.')}
}
