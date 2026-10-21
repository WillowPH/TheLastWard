/* Earned horror and recoverable environmental danger share the live game clock. */
(function(){
'use strict';
const WW=WardWinter;
const living=()=>!!(S&&S.hp>0&&!S.f.dead&&!S.f.chapter1Complete&&!WW.isPaused?.());
const activeWindows=()=>{const w=WW.windowState();return S.room==='wardnorth'&&w.triggered&&!w.resolved&&w.closed.some(v=>!v);};
const activeSpray=()=>S.room==='eastcorridor'&&S.f.sprinklerTriggered&&!S.f.sprinklerStopped;

// Exposure remains local and fully recoverable. A warm room stops continuing
// injury, but only its explicit recovery action dries the soaked clothing.
WW.advanceExposure=function(value){
 if(!living()||WW.isSurvivalPaused?.()||WW.hallActive?.())return;
 const n=Math.max(0,Number(value)||0);if(!n)return;
 const w=WW.windowState(),open=w.closed.filter(v=>!v).length;
 const windows=activeWindows(),spray=activeSpray(),coldRoom=S.room==='coldstore';
 const warm=WW.isWarm();
 if(spray)S.f.wet=1;
 if(windows){
  w.exposure+=n;S.f.coldExposure=(S.f.coldExposure||0)+n*open/3;
  if(w.exposure>=2&&!S.f.coldWarning){S.f.coldWarning=1;WW.sceneWarning?.('The open windows are freezing the corridor.');WW.think?.('The purge handle opened three windows. Close each brass catch before searching the released compartment.','warm');}
 }
 if(coldRoom)S.f.coldExposure=(S.f.coldExposure||0)+n*.55;
 if(S.f.wet){
  S.f.wetTurns=(S.f.wetTurns||0)+n;
  if(!warm)S.f.coldExposure=(S.f.coldExposure||0)+n*(spray?.9:.6);
  if(S.f.wetTurns>=2&&!S.f.wetWarning){S.f.wetWarning=1;WW.think?.('My soaked clothes are taking my strength. Stop the water, recover the flashlight and dry off at the laundry stove or a powered warm room.','dry');}
 }else if(!windows&&!coldRoom)S.f.coldExposure=Math.max(0,(S.f.coldExposure||0)-n*(warm?2:.35));
 const exposure=S.f.coldExposure||0;
 S.f.shivering=exposure>=4;
 const exposed=windows||spray||coldRoom||(S.f.wet&&!warm);
 if(exposed&&exposure>=4){
  const mode=S.m<1?.72:S.m>1?1.18:1;
  const rate=spray?1.8:windows?1.45:coldRoom?.8:1.1;
  S.hp=Math.max(0,S.hp-n*rate*S.m*mode);
  S.san=Math.max(0,S.san-n*(spray?.85:windows?.7:.55)*mode);
  if(!S.f.exposureWarning){S.f.exposureWarning=1;WW.sceneWarning?.('The cold is hurting me. Find warmth.');soundEffect('hit');}
 }
 if(S.hp<=0)die();
};

const sprinkler=wardSprinkler;
wardSprinkler=function(...args){
 if(!living())return;
 const first=S.room==='eastcorridor'&&!S.f.sprinklerTriggered,hp=S.hp;
 const result=sprinkler.apply(this,args);
 if(first&&S.f.sprinklerTriggered){
  // The scripted shock cannot take a living player straight to a fatal screen;
  // the persistent, warned hazard can. Its existing once-per-run flag is shared.
  const shock=S.m<1?8:S.m>1?18:14;
  S.hp=Math.max(1,hp-shock);S.f.coldExposure=Math.max(4,S.f.coldExposure||0);
  S.f.waterInjuryV8=1;WW.updateStatus?.();render();
 }
 return result;
};
const openWindows=wardOpenWindows;
wardOpenWindows=function(...args){
 if(!living())return;
 const first=S.room==='wardnorth'&&!WW.windowState().triggered,result=openWindows.apply(this,args);
 if(first&&WW.windowState().triggered){
  S.hp=Math.max(1,S.hp-Math.max(2,Math.round(4*S.m)));
  S.san=Math.max(0,S.san-3);S.f.coldExposure=Math.max(3.5,S.f.coldExposure||0);
  WW.think?.('The freezing gust is already numbing my fingers. Shut all three window catches before searching the trolley.');
  render();
 }
 return result;
};

function canShowEpisode(){
 if(!living()||WW.isSurvivalPaused?.()||WW.travelling||WW.orbit?.busy||WW.hallActive?.()||S.sceneFocus||alive(S.room)||S.f.pursuerEncounter||S.f.hidingRoom||SAFE_FROM_PURSUER.has(S.room)||$('m').children.length)return false;
 if(S.pursuer?.active&&S.pursuer.room===S.room)return false;
 return !activeWindows()&&!activeSpray();
}
function quietOver(){
 const clock=WW.readingClock?.();if(clock?.paused)return false;
 const turn=S.f.nextSanityEpisodeAt||0,real=S.f.sanityEpisodeDeadline||0;
 if(!turn&&!real)return true;
 return turn>0&&S.t>=turn||real>0&&(clock?.now||Date.now())>=real;
}
function quiet(turns=16,seconds=35){
 S.f.nextSanityEpisodeAt=S.t+turns;S.f.sanityEpisodeDeadline=Date.now()+seconds*1000;
}
function rememberTrauma(){
 const stress=WW.incidentStress();
 if(stress>(S.f.recordedIncidentStress||0)){
  S.f.recordedIncidentStress=stress;
  S.f.pendingSanityEpisode=(!S.f.falseEncounterSeen||(S.f.visualEpisodes||0)<2)?1:0;
 }
 return stress;
}
WW.sanityEpisode=function(){
 if(!living())return false;
 const stress=rememberTrauma();
 if(!canShowEpisode()||!quietOver()||S.sceneDisturbance)return false;
 // A witnessed second major incident remains consequential after a little
 // composure recovery. Severe current distress can also earn the encounter.
 const falseEligible=stress>=24&&S.san<=82||stress>0&&S.san<=50;
 if(!S.f.falseEncounterSeen&&falseEligible){
  const shown=wardFalseEncounter();
  if(shown){S.f.pendingSanityEpisode=0;quiet(20,45);}
  return shown;
 }
 const count=S.f.visualEpisodes||0;
 const visualEligible=stress>=12&&S.san<=74;
 if(count<2&&visualEligible&&(!count||S.t>=(S.f.nextVisualEpisodeAt||0)||Date.now()>=(S.f.sanityVisualDeadline||Infinity))){
  S.f.visualEpisodes=count+1;S.f.nextVisualEpisodeAt=S.t+30;
  S.f.sanityVisualDeadline=Date.now()+60000;S.f.pendingSanityEpisode=0;
  S.sceneDisturbance={room:S.room,view:S.roomView||'front',kind:count===0?'hanged':'body',deadline:Date.now()+15000};
  quiet(16,35);
  const memory=S.f.beggingPatientChoice==='killed'?'Mercer’s last breath':S.f.doctorWallSeen?'those impacts against the tiles':'the scene behind the observation glass';
  const thought=count===0?'I keep hearing '+memory+'. Something moved at the edge of my sight.':'My hands are shaking. The patients’ faces keep following me into other rooms.';
  (S.th2||(S.th2=[])).push(thought);WW.think?.(thought,'sanity');
  renderScene();return true;
 }
 return false;
};

const resolveHall=WW.resolveHall;
WW.resolveHall=function(...args){const active=!!S?.hallCombat,result=resolveHall.apply(this,args);if(active&&S&&!S.hallCombat){quiet(20,45);S.f.pendingSanityEpisode=0;}return result;};

// Story arrivals frequently end with a document or decision modal, so the old
// single arrival-only attempt was lost. Re-check after the player closes it and
// during quiet exploration. All bounds are saved, not tied to room re-entry.
setInterval(()=>{if(living())WW.sanityEpisode();},650);
})();
