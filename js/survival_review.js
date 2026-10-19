/* Final command boundary: a fatal outcome ends this run until a saved run is loaded. */
(function(){
'use strict';
const WW=WardWinter;
const dead=()=>!!(S&&(S.f.dead||S.hp<=0||(S.f.glassHunterStep>=2&&!S.f.glassHunterRetreated)));
function latch(){if(!dead())return false;S.f.dead=true;S.hp=0;S.lightOn=false;cm=0;return true;}
WW.isDead=dead;
WW.canAct=()=>!!(S&&!dead()&&!S.f.chapter1Complete);
WW.guardAction=function(action){return function(...args){if(!S)return;if(latch()){die();return false;}const result=action.apply(this,args);latch();return result;};};
const deathScreen=die;
die=function(...args){if(S){S.hp=0;S.f.dead=true;S.lightOn=false;cm=0;}return deathScreen(...args);};
const switchLight=toggleLight;
toggleLight=function(){
 if(!S)return;if(dead())return die();
 if(!S.lightOn&&has('Flashlight')&&!WW.needsFlashlight()){
  WW.think?.('There is enough light here. I can save the flashlight battery for the dark rooms.');
  return false;
 }
 return switchLight();
};

// These are the public commands used by the HUD, scene, inventory, puzzles and
// combat. Guard the final wrappers, after every feature module has loaded.
const commands=[
 'act','exam','go','sceneDoorTravel','mapTravel','mapModal','wardMapSelect',
 'heal','combatHeal','useInventoryHeal','chooseMedical','useInventorySlot',
 'equipWeapon','reload','useBat','rechargeAtGenerator','upgrade','combineItems','invModal','storage',
 'store','take','storageTab','storagePage','toggleLight','saveGame','confirmSave',
 'combat','shoot','knifeAttack','foe','flee','sneak','noise','advanceTime',
 'wardInspectFixture','wardFixtureAction','wardInspectInventory','wardUseManagedItem',
 'wardRequestDiscard','wardConfirmDiscard','wardCombineLighter','wardWarmUp',
 'wardOpenWindows','wardCloseColdWindow','wardSprinkler','wardRecoverFlashlight',
 'reinforceWindow','wardPlacePlank','triggerServiceTrap','wardConfirmTrap',
 'wardSteadyShot','wardStruggle','wardResolveFalseEncounter','wardFalseEncounter',
 'pursuerEncounter','escapePursuer','awakenPursuer','hideInRoom','wardConfirmHide',
 'wardStayHidden','wardExitHiding','wardPeek','choosePatientFate','wardConfirmPatient',
 'doctorAtWall','wardFinishKessler','researcherLastRoom','plexiIncident',
 'inspectObservationGlass','retreatGlassHunter','closeGlassStage',
 'portraitPuzzle','portraitChoice','wardInspectPortrait','wardWirePanel',
 'wardConnectWire','wardElevatorBoard','wardFitElevatorFuse','wardTuneRadio',
 'wardListenRadio','code','seq','tryCode','trySeq','unlockCode','inspectLiftControls',
 'beginDescent','answerPayphone','ringPayphone','doc','evidenceModal','journal'
];
for(const name of commands)if(typeof window[name]==='function')window[name]=WW.guardAction(window[name]);
for(const name of ['ignite','inspectObject'])if(typeof WW[name]==='function')WW[name]=WW.guardAction(WW[name]);

const renderRun=render;
render=function(...args){latch();return renderRun(...args);};
// Loading replaces the state object. A valid living save can leave the death
// screen; a saved zero-health state must remain terminal rather than be healed.
for(const name of ['loadGame','loadCheckpoint','loadFirstFloorCheckpoint','wardLoadFinale','newGame']){
 const original=window[name];if(typeof original!=='function')continue;
 window[name]=function(...args){const result=original.apply(this,args);if(S?.hp>0){delete S.f.dead;}else if(S)die();return result;};
}

// Prevent stale controls, keyboard shortcuts or a delayed click from opening an
// inventory over the death screen. Only explicit restart/load commands pass.
function terminalInput(event){
 if(!latch())return;
 const button=event.target.closest?.('button,a');
 const command=button?.getAttribute('onclick')||'';
 if(/^(?:loadGame|loadCheckpoint|loadFirstFloorCheckpoint|wardLoadFinale|newGame|die|location\.reload)\s*\(/.test(command))return;
 if(event.target.closest?.('#game,#m')){event.preventDefault();event.stopImmediatePropagation();}
}
document.addEventListener('click',terminalInput,true);
document.addEventListener('keydown',terminalInput,true);

// Retreats have their own cost and already validate an unlocked adjacent door.
// Run the same arrival story once, without charging for a second walk or opening
// the door a second time. The serial also protects future handlers that already
// call chapterArrival internally.
let arrivalSerial=0;
const arrive=chapterArrival;
chapterArrival=function(...args){arrivalSerial++;return arrive(...args);};
for(const name of ['flee','escapePursuer']){
 const retreat=window[name];
 window[name]=function(...args){
  const from=S?.room,before=arrivalSerial,escaping=!!S?.f.pursuerEncounter,result=retreat.apply(this,args);
  if(name==='escapePursuer'&&escaping&&S&&!dead()&&!S.f.pursuerEncounter){
   const p=initPursuer();p.evadeUntil=S.t+(S.m<1?16:S.m>1?8:12);p.lastMoveAt=S.t;
  }
  if(S&&S.room!==from&&!dead()&&before===arrivalSerial){
   S.sceneFocus=null;S.searchArea=null;S.searchAreaRoom=S.room;combatNote('');
   const handled=chapterArrival(from,S.room);
   if(!handled&&alive(S.room)&&!S.f.pursuerEncounter)combat();
  }
  return result;
 };
}

// Successfully waiting out a search must also buy time to leave the room.
const hideWait=wardStayHidden;
wardStayHidden=function(...args){const escapes=S?.f.pursuerEscapes||0,result=hideWait.apply(this,args);if(S&&!dead()&&(S.f.pursuerEscapes||0)>escapes){const p=initPursuer();p.evadeUntil=S.t+(S.m<1?16:S.m>1?8:12);p.lastMoveAt=S.t;}return result;};

// More finite ammunition, on the same authored shelves and drawers. A loaded
// save retains collected flags; configuring the world never replenishes a cache.
const ammoBase=new Map();
for(const [room,r]of Object.entries(R))for(const o of r.o){const give=o[4].give;if(!give)continue;give.forEach(([name,count],i)=>{if(/Ammo|Shells|Rounds/.test(name))ammoBase.set(room+'/'+o[0]+'/'+i,count);});}
const configure=configureWorld;
configureWorld=function(...args){const result=configure(...args);if(!S)return result;
 for(const [room,r]of Object.entries(R))for(const o of r.o){
  const give=o[4].give;if(!give)continue;
  give.forEach((entry,i)=>{if(!/Ammo|Shells|Rounds/.test(entry[0]))return;const key=room+'/'+o[0]+'/'+i;if(!ammoBase.has(key))ammoBase.set(key,entry[1]);const base=ammoBase.get(key);entry[1]=Math.max(base,Math.ceil(base*(S.m<1?2:S.m>1?1.25:1.65)));});
  if(give.length===1&&/Ammo|Shells|Rounds/.test(give[0][0]))o[3]='A sealed supply of '+give[0][1]+' '+give[0][0].toLowerCase()+'. Take it now or leave it for later.';
 }
 return result;
};
})();
