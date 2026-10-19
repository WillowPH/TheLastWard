let S=null;
function violenceMode(){return S?.presentation?.violence==='reduced'?'reduced':'full'}
function sceneDetail(full,reduced){return violenceMode()==='reduced'?reduced:full}
function applyViolenceAppearance(){document.documentElement.dataset.violence=violenceMode()}

function hashSeed(seed){let h=2166136261;for(let i=0;i<seed.length;i++){h^=seed.charCodeAt(i);h=Math.imul(h,16777619)}return (h>>>0)||1}
function rnd(){if(!S)return Math.random();let state=S.rngState>>>0;state=(state+0x6D2B79F5)>>>0;let t=state;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);S.rngState=state;return ((t^(t>>>14))>>>0)/4294967296}
function generatePuzzles(){const wards=[1,2,3,4,5,6,7,8];for(let i=wards.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[wards[i],wards[j]]=[wards[j],wards[i]]}const wardOrder=wards.slice(0,4);const colors=['R','G','B','Y'];for(let i=colors.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[colors[i],colors[j]]=[colors[j],colors[i]]}const breaker=colors.slice(0,3);const hour=String(Math.floor(rnd()*24)).padStart(2,'0'),minute=String(Math.floor(rnd()*60)).padStart(2,'0');const day=String(1+Math.floor(rnd()*28)).padStart(2,'0'),month=String(1+Math.floor(rnd()*12)).padStart(2,'0');return {wardOrder,pharmacyCode:wardOrder.join(''),breaker,safeCode:hour+minute,memorialCode:day+month,memorialDate:day+'/'+month+'/1998'}}
function puzzleCode(id,sp){if(id==='kp')return S.puzzles.pharmacyCode;if(id==='sf')return S.puzzles.safeCode;if(id==='memDoor')return S.puzzles.memorialCode;if(id==='cat')return S.puzzles.memorialCode;return sp.code}
function puzzleSeq(id,sp){if(id==='brk'||id==='echoConsole')return S.puzzles.breaker.join('');return sp.seq}
function docText(t){let text=DOCS[t]||'';if(!S||!S.puzzles)return text;if(t==='Duty Roster')text='WARD ROTATION — NIGHT SHIFT\n\nThe pharmacy lock was reset after the thefts. Staff are to remember the order the wards lost power: '+S.puzzles.wardOrder.map(n=>'Ward '+n).join(', then ')+'.\n\nDo not write the code down anywhere else.';if(t==='Memory Vault Docket')text+='\n\nThe recorded dedication date is '+S.puzzles.memorialDate+'.';if(t==='Continuity Calibration Note')text+='\n\nThe alignment colours read '+S.puzzles.breaker.map(c=>({R:'red',G:'green',B:'blue',Y:'yellow'}[c])).join(', then ')+'.';if(t==='Resident Diary')text='Staff Residence, night shift\n\nThe breaker panel keeps tripping. Maintenance told me to restart it in the order shown by the colored exit signs: '+S.puzzles.breaker.map(c=>({R:'red',G:'green',B:'blue',Y:'yellow'}[c])).join(', then ')+'. Get it wrong and it bites.\n\nI left the winch crank in the panel cupboard.';if(t==='Maintenance Log')text+='\n\nHandwritten addendum: Failure logged at '+S.puzzles.safeCode.slice(0,2)+':'+S.puzzles.safeCode.slice(2)+'.';if(t==='Memorial Ledger')text='MEMORIAL PLAQUE REGISTER\n\nThe dedication date is '+(S.puzzles.memorialDate||((S.puzzles.memorialCode||'1710').slice(0,2)+'/'+(S.puzzles.memorialCode||'1710').slice(2)+'/1998'))+'. A matching brass plate in Archives is marked ‘Dedication’. The year has been struck through in pencil.';return text}
function conditionInfo(hp){if(hp>75)return ['●','Breathing controlled',''];if(hp>50)return ['◉','Your movements feel heavier','wounded'];if(hp>25)return ['◉','Breathing is ragged','badly'];return ['●','You can barely stay upright','critical']}
const HAL=['Behind you the floor creaks. Nothing is there.','A whisper, almost words: Someone is wearing your patient gown.','The shadows sit a half-step closer than they did.','A voice tries to say your name, then stops at the missing part.'];
const san=()=>S.san??100,lit=()=>!!(S&&((has('Flashlight')&&S.lightOn&&(S.bat||0)>0&&!S.f.flashlightDropped)||(window.WardNavigation?!WardNavigation.isDark(S.room):!R[S.room]?.dark)));
const has=n=>S.inv.some(s=>canonicalItem(s.n)===canonicalItem(n)),cnt=n=>S.inv.filter(s=>canonicalItem(s.n)===canonicalItem(n)).reduce((a,s)=>a+s.c,0);
const HEALS={'Trauma Dressing':20,'Field Medkit':45,'Emergency Trauma Kit':75,'Vitality Reconstructor':100};
function toast(x){$('t').innerHTML='<div class="tst">'+x+'</div>';setTimeout(()=>$('t').innerHTML='',2600)}
function lg(x){S.log.unshift(x);S.log=S.log.slice(0,6)}
function interaction(x){const n=$('interactionText');if(n)n.textContent=x;const e=$('ev');if(e){e.textContent=x;e.className='ev'}}
function combatNote(x){const n=$('combatText');if(n)n.textContent=x}
function contextualThought(){const pool=['I should be terrified. Instead I feel expected.','The dust says years. My hands say minutes. I do not know which to trust.','If I cannot trust my memory, I had better trust the evidence.','Everything here is lying politely.','I know the shape of this corridor. I do not know how.','A name rises in my throat and stops before it becomes a sound.','Someone cleaned this patch of floor. The rest of the room was left to rot.'];S.usedThoughts=S.usedThoughts||[];let choices=pool.filter(x=>!S.usedThoughts.includes(x));if(!choices.length){S.usedThoughts=[];choices=pool.slice()}const line=choices[Math.floor(rnd()*choices.length)];S.usedThoughts.push(line);return line}
function maybeAmbientHorror(){if(!S||S.f.pausedEvents||($('m')&&$('m').querySelector('.md')))return;S.f=S.f||{};S.eventClock=(S.eventClock||0)+1;if(S.eventClock<6)return;S.eventClock=0;const roll=rnd();if(roll<.16&&!S.f.screamSeenThisVisit){S.f.screamSeenThisVisit=1;lg('A distant scream cuts off before the echo returns.');interaction('A scream tears through the ward somewhere far away. No direction you can trust.');return}if(roll<.29&&!S.f.doctorMumbleSeen){const lines=['“The patient is awake. The patient is— the patient is the room.”','“Do not chart the second heartbeat. It belongs to the first one.”','“If she asks for the man in the mirror, do not tell her he is already here.”'];S.f.doctorMumbleSeen=1;lg('An infected doctor murmurs to an empty bed: '+lines[Math.floor(rnd()*lines.length)]);interaction('An infected doctor in a torn coat murmurs to an empty bed, not noticing you. It does not attack.');return}if(roll<.50&&san()<55&&!S.f['shadow_'+S.room]){S.f['shadow_'+S.room]=1;lg('A shadow passed under an empty doorway.');interaction('A human shadow slips beneath a locked door, then vanishes when the flickering light returns. There are no footsteps. I cannot tell whether anyone was there.');return}if(roll>.88&&!S.f.powerOut&&S.f.power&&S.room!=='core'&&!alive(S.room)){S.f.powerOut=1;S.f.powerOutTicks=0;lg('The overhead lights fail.');interaction('The lights die with a relay click. Your flashlight may be necessary until power returns.');if(!lit())toast('Power outage. The flashlight is your only light.')}}
function advancePowerOutage(){if(!S||!S.f.powerOut)return;S.f.powerOutTicks=(S.f.powerOutTicks||0)+1;if(S.f.powerOutTicks>=3){S.f.powerOut=0;S.f.powerOutTicks=0;lg('The overhead lights sputter back on.');interaction('Power returns in a sickly flicker. Something has moved while the lights were out.')}}
function maybeGlassHunter(){return false} // The glass encounter is discovered by inspection, never an automatic pop-up.
function inspectObservationGlass(){
 if(S.f.glassHunterDone)return toast('Nothing moves behind the glass now.');
 if(S.f.glassHunterEligible===undefined)S.f.glassHunterEligible=true;
 if(!S.f.glassHunterEligible){
  S.f.glassHunterDone=1;S.ob.glasssound='read';
  interaction('An air duct rattles behind the glass. The room beyond is empty.');
  lg('The sealed cell was empty.');render();return;
 }
 S.f.glassHunterTriggered=1;
 const step=S.f.glassHunterStep||0;
 if(step===0){
  S.f.glassHunterStep=1;advanceTime(1);
  try{localStorage.setItem('lw_ch1_cinematic_glass_checkpoint',JSON.stringify(S));S.f.glassHunterCheckpoint=1}catch(e){}
  modal('Something behind the glass',
   '<div class="unique-event"><p>Three slow scratches cross the reinforced pane. A wide, hooked claw rests against the far side. Each movement leaves a new crack. Whatever owns it is close enough to reach you if the glass fails.</p><p class="scene-warning"><b>WARNING:</b> Inspecting this window again is extremely dangerous. Back away.</p><p class="unique-thought">I can leave. Right now. Why am I still looking?</p></div><button class="btn p" onclick="retreatGlassHunter()">Back away permanently</button><button class="btn" onclick="closeGlassStage()">Step back for now</button>');
  return;
 }
 // The SECOND deliberate inspection is fatal. Both violence modes keep the same consequence.
 S.f.glassHunterStep=2;S.f.glassHunterDone=1;S.ob.glasssound='read';S.hp=0;
 soundEffect('kill');lg('The observation glass explodes. There is no time to escape.');
 modal('The glass breaks','<div class="unique-event">'+sceneDetail(
  '<p>The creature punches through the plexiglass. The protagonist jerks backward, but its hooked limb catches his neck. One savage motion severs his head; it strikes the tiles as the emergency lights go out.</p>',
  '<p>The pane explodes. A hooked silhouette crosses the light. There is a single impact and the world falls silent as the emergency lights go out.</p>')+
  '<p class="scene-warning">You died. The observation checkpoint is available.</p></div><button class="btn p" onclick="die()">Continue</button>');
 const close=$('m').querySelector('.mh button');if(close)close.remove();
}
function closeGlassStage(){if($('m'))$('m').innerHTML='';interaction('The scratching has stopped. You can leave it alone.');render()}
function retreatGlassHunter(){S.f.glassHunterDone=1;S.f.glassHunterRetreated=1;S.ob.glasssound='read';if($('m'))$('m').innerHTML='';interaction('You back away. Whatever was behind the glass stays there.');lg('You chose not to risk a second inspection.');render()}
function loadCheckpoint(){try{const snap=localStorage.getItem('lw_ch1_cinematic_glass_checkpoint');if(!snap)return loadGame();S=JSON.parse(snap);S.presentation=S.presentation||{violence:localViolenceChoice()};applyViolenceAppearance();$('m').innerHTML='';$('setup').classList.add('hid');$('game').classList.remove('hid');S.hp=Math.max(35,S.hp||35);S.f.glassHunterDone=1;S.f.glassHunterTriggered=1;S.f.glassHunterRetreated=1;S.ob.glasssound='read';render();toast('Checkpoint restored at the observation glass.')}catch(e){toast('Checkpoint could not be loaded.')}}
function advanceTime(n=1){
 S.t+=n;
 if(S.lightOn&&S.bat>0){
  S.noise=(S.noise||0)+n;
  if(S.noise>=6){S.noise=0;const nearby=Object.keys(D).map(k=>D[k].a===S.room?D[k].b:D[k].b===S.room?D[k].a:null).find(r=>r&&alive(r)&&!E[r].boss);if(nearby){S.f.lightAlert=Math.max(2,S.f.lightAlert||0);lg('The flashlight beam catches the corridor. Something nearby turns toward the light.');}}
  S.lightTicks=(S.lightTicks||0)+n;
  while(S.lightTicks>=8&&S.bat>0){S.lightTicks-=8;S.bat--;}
  if(S.bat<=0){S.bat=0;S.lightOn=false;lg('The flashlight dies. Its beam gutters out.');}
 }
 advancePowerOutage();maybeAmbientHorror();
}
function itemCue(n){if(['Power Fuse','Battery'].includes(n))return 'cue-power';if(HEALS[n])return 'cue-medical';if(['Cabinet Key','Staff Access Card','Archive Key','Crank Handle','Boiler Key','Bolt Cutters','Encrypted Drive'].includes(n))return 'cue-access';if(['Chapel Seal','Morgue Seal','Lab Seal','Boiler Seal'].includes(n))return 'cue-puzzle';return ''}
function objectCue(id,sp){if(sp.need)return itemCue(sp.need);if(sp.code||sp.seq||sp.need3)return 'cue-puzzle';if(sp.expand)return 'cue-access';if(sp.give&&sp.give[0])return itemCue(sp.give[0][0]);if(['pan','brk','fus','bt2'].includes(id))return 'cue-power';return ''}
function doorCue(d){if(d.need)return itemCue(d.need);if(d.flag==='power')return 'cue-power';if(d.flag)return 'cue-puzzle';return ''}
function canonicalItem(n){return ({'Ink Ribbon':'Floppy Disk','Medkit':'Field Medkit','Magnum Ammo':'Magnum Rounds','Magnum Ammunition':'Magnum Rounds','.44 Magnum Rounds':'Magnum Rounds','Magnum Bullets':'Magnum Rounds','Reinforced Cell':'Reinforced Battery'})[n]||n}
function carryLimit(){return S&&Number.isFinite(S.slots)?Math.max(8,Math.min(12,S.slots)):8}
function add(n,c=1,inv=S.inv,slotLimit=null){
 if(slotLimit===null)slotLimit=inv===S.inv?carryLimit():16;
 n=canonicalItem(n);const cap=STK[n]||1;let remaining=Math.max(0,Number(c)||0);
 const space=inv.filter(x=>x.n===n).reduce((sum,x)=>sum+Math.max(0,cap-x.c),0)+(slotLimit-inv.length)*cap;
 if(space<remaining)return false;
 for(const slot of inv)if(slot.n===n&&slot.c<cap){const take=Math.min(cap-slot.c,remaining);slot.c+=take;remaining-=take;if(!remaining)break;}
 while(remaining>0){const take=Math.min(cap,remaining);inv.push({n,c:take});remaining-=take;}
 return true;
}
function rem(n,c=1){n=canonicalItem(n);for(let i=S.inv.length-1;i>=0&&c>0;i--){const s=S.inv[i];if(s.n==n){const t=Math.min(c,s.c);s.c-=t;c-=t;if(!s.c)S.inv.splice(i,1)}}}
const alive=r=>!!(E[r]&&S.en&&S.en[r]>0);
function configureWorld(seed,preserve=true){const old=S.en||{};for(const k in R)R[k].o=R[k].o.filter(o=>!String(o[0]).startsWith('seedloot_'));let z=hashSeed(seed+'::world');const rr=()=>{z=(Math.imul(z,1664525)+1013904223)>>>0;return z/4294967296};const candidates=['ward','morgue','lab','observation','tunnel','boiler','laundry','children','surgery','isolation','specimen','powercontrol','stafflounge'];for(let i=candidates.length-1;i>0;i--){const j=Math.floor(rr()*(i+1));[candidates[i],candidates[j]]=[candidates[j],candidates[i]]}const regular=candidates.filter(r=>!['ward','lab','observation'].includes(r)).slice(0,3);S.spawnRooms=[...regular];S.en={};for(const room of S.spawnRooms)S.en[room]=preserve&&Number.isFinite(old[room])?Math.max(0,Math.min(E[room].hp,old[room])):E[room].hp;S.enemySeed=seed;
 const lootRooms=['security','ward','archive','generator','observation','pharmacy','chapel','morgue','lab','residence','tunnel','boiler','laundry','children','records','surgery','isolation','specimen','powercontrol','stafflounge'];for(let i=lootRooms.length-1;i>0;i--){const j=Math.floor(rr()*(i+1));[lootRooms[i],lootRooms[j]]=[lootRooms[j],lootRooms[i]]}const pool=[['Handgun Ammo',3],['Trauma Dressing',1],['Battery',1],['Ink Ribbon',1]];for(let i=0;i<1;i++){const room=lootRooms[i],item=pool[Math.floor(rr()*pool.length)];R[room].o.push(['seedloot_'+i,'Unmarked supply cache','📦','A sealed cache. Its contents vary from run to run.',{give:[[item[0],item[1]]]}])}}
function normalizeItems(items){const out=[];for(const s of (items||[])){const n=canonicalItem(s.n);let left=Math.max(1,Number(s.c)||1),cap=STK[n]||1;while(left>0){const take=Math.min(cap,left);let existing=out.find(x=>x.n===n&&x.c<cap);if(existing){const addn=Math.min(cap-existing.c,take);existing.c+=addn;left-=addn}else{out.push({n,c:Math.min(cap,left)});left-=Math.min(cap,left)}}}return out.slice(0,24)}
