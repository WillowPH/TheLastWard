/* Finite authored pressure: ammunition is a route resource, not an enemy spawner. */
(function(){
'use strict';
const WW=WardWinter;
const living=()=>!!(S&&S.hp>0&&!S.f.dead&&!S.f.chapter1Complete&&!WW.isPaused?.());
const homes={story:['laundry','stafflounge','morgue','specimen','coldstore'],normal:['wardnorth','laundry','archive','stafflounge','children','morgue','specimen','isolation','coldstore'],nightmare:['wardnorth','wardservice','laundry','archive','stafflounge','children','morgue','boiler','specimen','isolation','coldstore']};
const names=['Infected orderly','Infected laundry attendant','Infected archivist','Screaming infected attendant','Infected ward patient','Infected mortuary attendant','Infected laboratory orderly','Infected isolation patient','Infected cold-store orderly','Infected service orderly','Infected maintenance worker'];
const mode=()=>S.m<1?'story':S.m>1?'nightmare':'normal';
WW.pursuerKnockdownThreshold=()=>S.m<1?2:S.m>1?4:3;
WW.pursuerCounterDamage=()=>S.m<1?3:4;
function newActor(room,index,migrated=false){const m=mode(),hp=m==='story'?9+index%3:m==='nightmare'?14+index%3:11+index%3;return {id:'infected-'+(migrated?30+index:index),room,home:room,hp,maxHp:hp,name:room==='stafflounge'?'Screaming infected attendant':names[index%names.length],dmg:m==='story'?[4,7]:m==='nightmare'?[6,10]:[5,8],type:'infected_patient',screamer:room==='stafflounge',nextCry:S.t+16,lastMove:S.t,alert:null};}
function applyAmmo(){
 const factor=S.m<1?1.25:S.m>1?.8:1,counts={pistolRounds:18,am:12,serviceAmmo:12,recordsAmmo:18,purgeSupplies:12,shotShells:6};
 for(const r of Object.values(R))for(const object of r.o||[]){for(const give of object[4].give||[]){if(object[0] in counts&&/^(Handgun Ammo|Shotgun Shells)$/.test(give[0]))give[1]=Math.max(1,Math.round(counts[object[0]]*factor));else if(/^seedloot_/.test(object[0])&&give[0]==='Handgun Ammo')give[1]=S.m<1?8:S.m>1?4:6;}if(object[4].give?.length===1&&/^(Handgun Ammo|Shotgun Shells)$/.test(object[4].give[0][0]))object[3]='A sealed supply contains '+object[4].give[0][1]+' '+object[4].give[0][0].toLowerCase()+'. Take it now or leave it for a later return.';}
}
function configurePopulation(preserve){
 const list=homes[mode()];
 if(!preserve){const breach=S.enemyActors?.find(a=>a.id==='window-breach');S.enemyActors=list.map((room,i)=>newActor(room,i));if(breach)S.enemyActors.push(breach);}
 else if(S.balanceVersion!==8){
  if(['last-ward-ch1-survival-review-5','last-ward-ch1-chapter-review-6','last-ward-ch1-chapter-review-7'].includes(S.buildId)&&(S.f.finalSecurityClearance||S.f.liftSeen)&&(S.f.pursuerEscapes||0)>0)S.f.legacyPursuitProof=1;
  // Existing deaths, down states and IDs are retained. A continued old run can
  // gain encounters only in unvisited, unoccupied rooms, never at a cleared home.
  const occupied=new Set((S.enemyActors||[]).flatMap(a=>[a.home,a.room]));
  let remaining=Math.max(0,list.length-S.enemyActors.filter(a=>a.id!=='window-breach').length);list.forEach((room,i)=>{if(remaining>0&&!S.vis[room]&&!occupied.has(room)){S.enemyActors.push(newActor(room,i,true));occupied.add(room);remaining--;}});
 }
 S.balanceVersion=8;S.spawnRooms=[...new Set(S.enemyActors.filter(a=>a.id!=='window-breach').map(a=>a.home))];
 WW.enemies.project();
 W.Handgun.dmg=[3,4];W.Handgun.hit=.82;W.Shotgun.dmg=[7,10];W.Shotgun.hit=.8;
 applyAmmo();
 if(S.f.finalPursuitActive){SAFE_FROM_PURSUER.delete('generator');R.generator.safe=0;}else{SAFE_FROM_PURSUER.add('generator');R.generator.safe=1;}
}
const configure=configureWorld;configureWorld=function(seed,preserve=true){const result=configure(seed,preserve);if(S)configurePopulation(preserve);return result;};

// Close-range blade work is a dangerous finishing tactic, not a cheap primary.
const knife=knifeAttack;
knifeAttack=function(){
 if(!living())return;if(WW.hallActive?.()||WW.pursuerPresent?.())return knife();
 const actor=WW.enemies.actorAt();if(!actor)return knife();
 const armed=has('Utility Knife'),weakened=actor.hp<=actor.maxHp*.4;
 advanceTime(1);if(!living())return;
 const damage=armed?(weakened?4+Math.floor(rnd()*3):2+Math.floor(rnd()*2)):1;
 actor.hp=Math.max(0,actor.hp-damage);S.en[S.room]=actor.hp;S.f.knifeCuts=(S.f.knifeCuts||0)+1;soundEffect('knife');
 if(actor.hp<=0){cm=0;WW.pendingExit=null;if(!S.f.pursuerEncounter)$('m').innerHTML='';lg(actor.name+' finished at close range.');soundEffect('kill');render();return interaction('The blade finishes it. I had to get dangerously close.');}
 S.stag=armed&&weakened&&rnd()<.15?1:0;WW.enemies.project();render();return foe(armed?'The small blade wounds it, but I am inside its reach.':'My unarmed strike barely slows it.');
};
const struggle=wardStruggle;
wardStruggle=function(){
 if(!living())return;if(WW.hallActive?.())return struggle();const actor=WW.enemies.actorAt();if(!actor)return struggle();
 const base=Math.max(3,Math.round(6*S.m)),fresh=actor.hp>actor.maxHp*.4;
 const cost=Math.round((fresh?14:9)*S.m),extra=Math.max(0,cost-base);
 if(extra){S.hp=Math.max(0,S.hp-extra);if(S.hp<=0)return die();}
 S.f.forcedInfectedGaps=(S.f.forcedInfectedGaps||0)+1;return struggle();
};

// Deliberate aim gives a useful tradeoff: extra world time, a reliable hit and a
// chance to interrupt the approach. Quick shots remain faster, less certain.
const priorShoot=shoot;
window.shoot=function(){
 if(!living())return;if(WW.hallActive?.()||WW.pursuerPresent?.()){S.f.steadyAim=false;return priorShoot();}
 const actor=WW.enemies.actorAt(),weapon=W[S.eq];if(!actor||!weapon||!has(S.eq)||!(S.ld[S.eq]>0))return priorShoot();
 const aimed=!!S.f.steadyAim;S.f.steadyAim=false;S.ld[S.eq]--;S.f.firearmRoundsSpent=(S.f.firearmRoundsSpent||0)+1;
 advanceTime(1);if(!living())return;noise();soundEffect('shot');
 const hit=rnd()<Math.min(.97,weapon.hit+(aimed?.13:0)-(san()<40?.06:0));let note;
 if(hit){const damage=weapon.dmg[0]+Math.floor(rnd()*(weapon.dmg[1]-weapon.dmg[0]+1))+(S.up[S.eq]||0)+(aimed?1:0);actor.hp=Math.max(0,actor.hp-damage);S.en[S.room]=actor.hp;S.stag=rnd()<(aimed?.55:.18)?1:0;note=aimed?'The aimed shot hits.':'The shot hits.';}else{S.stag=0;note='The shot misses. The report carries down the corridors.';}
 if(actor.hp<=0){cm=0;WW.pendingExit=null;if(!S.f.pursuerEncounter)$('m').innerHTML='';S.f.infectedDefeated=(S.f.infectedDefeated||0)+1;lg(actor.name+' defeated.');soundEffect('kill');WW.enemies.project();render();return interaction(note+' It falls and stays down.');}
 WW.enemies.project();render();return foe(note+' '+enemyCondition(actor.hp,actor.maxHp)+'.');
};
const steady=wardSteadyShot;wardSteadyShot=function(){if(!living())return;return steady();};

function strategy(){return !!(S.f.legacyPursuitProof||(S.f.pursuerStaggers||0)>0||S.f.pursuerTrapCaught||(S.f.trapUsed&&(S.pursuer?.trappedUntil||0)>0)||(S.f.pursuerCoverEscapes||0)>0);}
const tripTrap=wardTripTrap;wardTripTrap=function(...args){const caught=tripTrap.apply(this,args);if(caught&&S?.pursuer?.trappedUntil>S.t)S.f.pursuerTrapCaught=1;return caught;};
const confirmTrap=wardConfirmTrap;wardConfirmTrap=function(...args){const result=confirmTrap.apply(this,args);if(S?.f.trapUsed&&S.pursuer?.trappedUntil>S.t)S.f.pursuerTrapCaught=1;return result;};
function transferReady(){return !!(S.f.power&&S.f.photoPuzzleSolved&&S.f.plexiIncidentSeen&&S.f.researcherLastRoomSeen&&S.f.doctorWallSeen&&S.f.finalSecurityClearance&&S.f.elevatorFusesInstalled&&S.f.drained&&S.f.transferBusReady);}
function endIntercept(){
 if(!living()||S.room!=='generator')return false;
 S.f.finalPursuitActive=1;SAFE_FROM_PURSUER.delete('generator');R.generator.safe=0;
 const p=initPursuer();p.active=true;p.room='generator';p.cooldown=0;p.lastMoveAt=S.t;p.openingUntil=0;p.evadeUntil=0;S.f.pursuerStarted=1;
 interaction('The service door crashes open. Subject X steps between me and the lift gate. I need a real opening; falling back alone will not clear the transfer route.');
 return pursuerEncounter('Subject X has breached the generator shelter and blocks the lift gate. I can stagger it, draw it into the laundry trap, or lose it using real cover.');
}
const requirements=WardChapter.requirements;WardChapter.requirements=function(){let missing=requirements();if(S?.f.finalPursuitActive&&S.room==='generator'&&WW.pursuerDown?.()&&strategy())missing=missing.filter(value=>value!=='escape Subject X');if(S&&!strategy())missing.push('create a safe opening past Subject X');return missing;};
// A genuine hide-and-evade is an alternative to gunfire. Merely backing through
// a door and receiving the legacy retreat counter does not satisfy this gate.
const hiddenWait=wardStayHidden;wardStayHidden=function(...args){if(!living())return;const before=S.f.pursuerEscapes||0,hidden=!!S.f.hidingRoom,result=hiddenWait.apply(this,args);if(hidden&&!S.f.lockerSeenEntering&&(S.f.pursuerEscapes||0)>before)S.f.pursuerCoverEscapes=(S.f.pursuerCoverEscapes||0)+1;return result;};
const priorGo=go;
window.go=function(to,confirmed=false){
 if(!living())return;const from=S.room;
 if(to==='lift'&&transferReady()&&(!strategy()||!(S.f.pursuerEscapes>0))){
  if(from==='generator'&&WW.pursuerPresent?.()&&WW.pursuerDown?.()&&strategy()){
   // The existing engine checks its escape flag before moving. Reserve this
   // earned opening for that one move; roll it back if travel cannot complete.
   const old=S.f.pursuerEscapes||0;S.f.pursuerEscapes=Math.max(1,old);const result=priorGo(to,confirmed);
   if(S.room===from)S.f.pursuerEscapes=old;else{S.f.pursuerEscapes=Math.max(old+1,(S.f.pursuerEscapes||1)-(old?0:1));S.f.finalPursuitActive=0;SAFE_FROM_PURSUER.add('generator');R.generator.safe=1;}return result;
  }
  if(from==='generator')return endIntercept();
 }
 // The native door/map controls already call this normally. Do not let a
 // confirmed forward transition silently pass a standing ordinary infected.
 const a=WW.enemies.actorAt();if(a&&to!==S.prev&&confirmed)confirmed=false;
 const result=priorGo(to,confirmed);
 if(S.room!==from&&S.f.finalPursuitActive&&strategy()&&S.room==='lift'){S.f.finalPursuitActive=0;SAFE_FROM_PURSUER.add('generator');R.generator.safe=1;}
 return result;
};
const priorAct=act;window.act=function(id){const held=has('Handgun'),result=priorAct(id);if(!held&&has('Handgun'))WW.think?.('I have a sidearm, but I need to ration it. The medicine cupboard behind the Patient Wing entry and the service trolley hold patrol ammunition. Security’s ammunition log lists the later stores.','ammo');return result;};
setInterval(()=>{if(living()&&S.room==='generator'&&transferReady()&&!strategy()&&!S.f.finalPursuitActive&&!WW.travelling&&!WW.orbit?.busy&&!$('m').children.length)endIntercept();},350);
WW.balance8={homes,mode,strategy,transferReady,ensureFinalIntercept:endIntercept,ammoBudget:()=>Object.values(R).flatMap(r=>r.o||[]).flatMap(o=>o[4].give||[]).filter(g=>g[0]==='Handgun Ammo').reduce((n,g)=>n+g[1],0)};
})();
