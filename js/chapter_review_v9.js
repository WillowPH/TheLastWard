/* Presentation hooks keep online atmosphere and earned memories out of logic. */
(function(){'use strict';const WW=WardWinter;
WW.visionMarkup=function(){
 const d=S?.sceneDisturbance;if(!d||d.room!==S.room||(d.view||'rear')!==S.roomView||S.san>74||WW.incidentStress()<12)return '';
 if(S.room==='eastcorridor'&&S.f.sprinklerTriggered&&!S.f.sprinklerStopped)return '';
 const stage=WW.enemyStaging?.(S.room,false,{aspect:2/3})||{left:58,bottom:3,boxHeight:70};
 const source=WW.asset(d.kind==='body'?'assets/room_views/infected_orderly.png':'assets/characters/infected_patient.png'),art=WardRoomViewRenderer.opaqueSource(source);
 return '<div class="winter-hallucinated-body sanity-memory" data-sanity-vision="true" aria-label="A fleeting figure at the edge of sight" style="left:'+stage.left+'%;bottom:'+stage.bottom+'%;height:'+stage.boxHeight+'%;width:auto;pointer-events:none;z-index:5;--enemy-light:'+Math.max(.5,WW.enemyLight?.()||.6)+';animation-delay:-'+Math.max(0,(Date.now()-(d.deadline-15000))/1000)+'s"><img data-solid-source="'+htmlSafe(source)+'" src="'+htmlSafe(art)+'" alt="A fleeting infected figure"></div>';
};
const scene=renderScene;renderScene=function(...args){const result=scene.apply(this,args);if(S?.hp>0&&!S.f.dead&&!S.f.chapter1Complete)WardArt.prepare(S.room);return result;};
})();
