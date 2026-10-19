/* A physical pursuer must be dealt with before any travel command can pass it. */
(function(){
'use strict';
const WW=WardWinter,escape=htmlSafe;
const paused=()=>!!WW.isPaused?.();
const actionable=()=>!!(S&&S.hp>0&&!S.f.dead&&!WW.isDead?.()&&!S.f.chapter1Complete&&!paused());
function present(){return !!(S?.pursuer?.active&&S.pursuer.room===S.room&&!SAFE_FROM_PURSUER.has(S.room));}
function down(){const p=S?.pursuer;return !!(p&&((p.trappedUntil||0)>S.t||((p.staggerUntil||0)>S.t&&(p.staggerDeadline||0)>Date.now())));}
function opening(){return !!(S?.pursuer&&(S.pursuer.openingUntil||0)>S.t);}
WW.pursuerDown=down;
WW.pursuerPresent=present;
WW.pursuerBlocksExit=to=>!!(actionable()&&WardNavigation.edge(S.room,to)&&present()&&!down()&&!opening());
WW.enemyVisual=function(actor){
 const i=Number(String(actor?.id||'').match(/\d+/)?.[0]||0)%3;
 if(actor?.id==='window-breach')return {image:'assets/characters/infected_patient.png',variant:'breach',sheet:false};
 return i===0?{image:'assets/room_views/infected_orderly.png',variant:'orderly',sheet:false}:i===1?{image:'assets/characters/nurse_walk.webp',variant:'nurse',sheet:true,still:'assets/characters/infected_nurse.png'}:{image:'assets/characters/patient_walk.webp',variant:'patient',sheet:true,still:'assets/characters/infected_patient.png'};
};
// Correct the near-opaque source alpha in the renderer, without filling the
// surrounding transparent cutout or fading a real enemy into the room artwork.
const filters=document.createElementNS('http://www.w3.org/2000/svg','svg');
filters.setAttribute('width','0');filters.setAttribute('height','0');filters.setAttribute('aria-hidden','true');
filters.style.position='absolute';
filters.innerHTML='<defs><filter id="ward-solid-enemy" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncA type="discrete" tableValues="0 0 0 .6 1 1 1 1"/></feComponentTransfer></filter></defs>';
document.body.append(filters);

function clearEncounter(){S.f.pursuerEncounter=0;cm=0;$('m').innerHTML='';}
function stagger(){const p=initPursuer(),turns=S.m<1?15:S.m>1?9:12;p.staggerUntil=S.t+turns;p.staggerDeadline=Date.now()+30000;p.evadeUntil=p.staggerUntil;p.lastMoveAt=S.t;p.posture=0;p.cooldown=0;S.f.pursuerStaggers=(S.f.pursuerStaggers||0)+1;clearEncounter();soundEffect('impact');interaction('Subject X drops to one knee. It is still moving. I have a brief opening to leave.');render();}
function recover(){if(!actionable())return false;const p=S?.pursuer;if(!p?.staggerUntil||down())return false;delete p.staggerUntil;delete p.staggerDeadline;p.evadeUntil=0;p.posture=0;p.lastMoveAt=S.t;S.f.pursuerEncounter=0;if(present()){interaction('The heavy boots scrape the tiles. Subject X is standing again.');renderScene();}return true;}
WW.updatePursuerRecovery=recover;

pursuerEncounter=function(note){
 if(!actionable()||!present()||down()||opening())return false;
 if(wardTripTrap())return false;
 const p=initPursuer();if(!S.f.pursuerEncounter)p.encounters=(p.encounters||0)+1;
 S.f.pursuerEncounter=1;cm=0;S.sceneFocus=null;renderScene();
 const weapon=W[S.eq]&&has(S.eq)?W[S.eq]:null,loaded=weapon?(S.ld[S.eq]||0):0;
 modal('Subject X · blocking the passage','<div class="c1-encounter"><div><p>'+escape(note||'The broad figure turns with me, cutting off the door. I cannot simply walk past it.')+'</p><p>'+(p.posture?'The last impact shook its balance. Another solid hit may bring it down.':'A concentrated burst can knock it down. It will recover.')+'</p><p>'+(weapon?escape(S.eq)+' · '+loaded+' loaded · '+cnt(weapon.ammo)+' reserve':'No firearm equipped. Cover or a risky retreat may be safer.')+'</p></div></div><div class="c1-encounter-actions"><button class="btn p" '+(!loaded?'disabled':'')+' onclick="escapePursuer(\'shoot\')">Shoot Subject X</button><button class="btn" '+(!weapon?'disabled':'')+' onclick="reload()">Reload</button>'+(HIDING_AREAS.has(S.room)?'<button class="btn" onclick="escapePursuer(\'hide\')">Enter cover · it may see you</button>':'')+'<button class="btn" onclick="escapePursuer(\'retreat\')">Retreat through an unlocked door</button><button class="btn" onclick="escapePursuer(\'push\')">Force a gap · risk injury</button></div>');
 document.querySelector('#m .mh button')?.remove();document.querySelector('#m .md')?.classList.add('winter-combat-modal');WW.orbit?.face('front');WardSound?.sync();return true;
};
function shootPursuer(){
 if(!actionable()||!present()||down())return;
 const weapon=W[S.eq];if(!weapon||!has(S.eq))return pursuerEncounter('I need a firearm. Cover or retreat are still possible.');
 if(!(S.ld[S.eq]>0))return pursuerEncounter('Click. The chamber is empty. I need to reload.');
 const p=initPursuer();S.ld[S.eq]--;soundEffect('shot');noise();advanceTime(1);
 if(!actionable())return;
 // At this range the large target can reliably be hit: two handgun rounds or
 // one heavier shell create a finite opening, rather than a lethal boss fight.
 p.posture=(p.posture||0)+(S.eq==='Handgun'?1:2);
 if(p.posture>=2)return stagger();
 S.hp=Math.max(0,S.hp-Math.max(1,Math.round(3*S.m)));soundEffect('hit');
 if(S.hp<=0)return die();render();pursuerEncounter('The shot drives its shoulder back, but it catches me before I can pass. One more solid impact should break its balance.');
}
const priorShoot=shoot;shoot=function(){if(!actionable())return;if(present()&&!down())return shootPursuer();return priorShoot();};
const priorReload=reload;reload=function(){if(!actionable())return;if(!present()||down())return priorReload();const w=W[S.eq];if(!w||!has(S.eq))return pursuerEncounter('There is no firearm to reload.');const amount=Math.min(w.mag-(S.ld[S.eq]||0),cnt(w.ammo));if(amount<=0)return pursuerEncounter('No reserve rounds are available for this weapon.');rem(w.ammo,amount);S.ld[S.eq]=(S.ld[S.eq]||0)+amount;advanceTime(1);soundEffect('reload');pursuerEncounter('The magazine locks into place. It is still between me and the door.');};
const priorCombat=combat;combat=function(note){if(!actionable())return;if(present()&&!down())return pursuerEncounter(note);return priorCombat(note);};
const priorSteady=wardSteadyShot;wardSteadyShot=function(){if(!actionable())return;if(present()&&!down())return shootPursuer();return priorSteady();};
const priorEscape=escapePursuer;
escapePursuer=function(how){
 if(!actionable()||!present()||!S.f.pursuerEncounter)return;
 if(how==='shoot')return shootPursuer();
 if(how==='hide')return hideInRoom();
 if(how==='retreat'){
  // Retreat means the doorway behind us. Passing deeper through the room
  // requires a stagger, a trap, or the explicit injury-cost action below.
  const target=S.prev,id=WardNavigation.edge(S.room,target);
  if(!id||!doorOpen(id))return pursuerEncounter('The way behind me is locked. I need cover, a stagger, or a forced opening.');
  const p=initPursuer(),from=S.room,escapes=S.f.pursuerEscapes||0;p.openingUntil=S.t+6;p.evadeUntil=S.t+(S.m<1?16:S.m>1?8:12);p.lastMoveAt=S.t;
  clearEncounter();const result=go(target,true);
  if(S.room!==from){S.f.pursuerEscapes=escapes+1;S.f.pursuerChaseComplete=1;interaction('I fall back through the door I came from. Subject X remains behind me.');}
  return result;
 }
 if(how==='push'){
  const p=initPursuer();S.hp=Math.max(0,S.hp-Math.round((9+rnd()*5)*S.m));soundEffect('hit');if(S.hp<=0)return die();
  clearEncounter();p.openingUntil=S.t+6;p.evadeUntil=S.t+6;p.lastMoveAt=S.t;advanceTime(1);interaction('I tear free from its grip. My shoulder is burning. I have a moment to reach a door.');render();return;
 }
 return priorEscape(how);
};
const priorGo=go;go=function(to,confirmed=false){if(!actionable())return;if(WW.pursuerBlocksExit(to))return pursuerEncounter();const before=S.room,result=priorGo(to,confirmed);if(S.room!==before&&S.pursuer?.active){const p=S.pursuer;if(p.room===before&&(down()||opening())){S.f.pursuerEscapes=(S.f.pursuerEscapes||0)+1;S.f.pursuerChaseComplete=1;p.lastMoveAt=S.t;}}return result;};
const priorFlee=flee;flee=function(){if(!actionable())return;if(present()&&!down()&&!opening())return pursuerEncounter('I cannot run through its reach. I need to create an opening or retreat behind me.');return priorFlee();};
const priorSneak=sneak;sneak=function(){if(!actionable())return;if(present()&&!down()&&!opening())return pursuerEncounter('It has already seen me. I cannot sneak through the doorway.');return priorSneak();};
sceneDoorTravel=function(to,event){
 if(!actionable()||event?.detail>1||WW.travelling||WW.orbit?.busy)return;
 const id=WardNavigation.edge(S.room,to);if(!id)return;
 if(WW.pursuerBlocksExit(to))return pursuerEncounter();
 if(!doorOpen(id)&&!(D[id].need&&has(D[id].need)))return go(to);
 if(alive(S.room)&&to!==S.prev)return go(to);
 if(to==='lift'&&WardChapter.requirements().length)return go(to);
 const from=S.room,finish=()=>{if(S?.room===from&&actionable())go(to,true);};
 if(WW.playDoorTransition)return WW.playDoorTransition({from,to,duration:1050,onComplete:finish});
 return finish();
};
mapTravel=function(to){if(!actionable()||!WardNavigation.edge(S.room,to))return;if(WW.pursuerBlocksExit(to))return pursuerEncounter();$('m').innerHTML='';return sceneDoorTravel(to);};
const priorApproach=pursuerApproach;pursuerApproach=function(to){if(!actionable())return false;recover();if(down()||opening())return false;return priorApproach(to);};
// A modest, fixed addition to authored ammunition caches covers the new cost.
// This is recalculated from the preceding configuration, never spawned or
// granted on a room visit, and completed pickups retain their saved flags.
const configure=configureWorld;configureWorld=function(...args){const result=configure(...args);if(!S)return result;for(const [room,r]of Object.entries(R))for(const o of r.o){for(const give of o[4].give||[]){if(give[0]==='Handgun Ammo')give[1]+=S.m<1?4:S.m>1?1:3;}}return result;};
setInterval(()=>{if(actionable())recover();},350);
})();
