/* All travel entry points share physical adjacency; no map fast travel. */
(function(){
'use strict';
const edge=(from,to)=>Object.keys(D).find(id=>D[id].a===from&&D[id].b===to||D[id].b===from&&D[id].a===to);
window.WardNavigation={edge,isDark:room=>!!R[room]?.dark&&!(S.f.power&&!S.f.powerOut&&WARD_POWERED.has(room)),until:0};
const baseLight=toggleLight;toggleLight=function(){if(S?.f.hidingRoom)return interaction('Keep the flashlight off while concealed.');return baseLight()};
const baseGo=go;
go=function(to,confirmed=false){
 if(!S||S.hp<=0||S.f.chapter1Complete||!R[to]||!edge(S.room,to))return;
 if(S.f.hidingRoom)return interaction('Leave your hiding place before moving.');
 const from=S.room,result=baseGo(to,confirmed);
 if(S.room===from&&S.msg){const reason=S.msg;S.msg=null;modal('Door closed','<p>'+htmlSafe(reason)+'</p><button class="btn" onclick="closeModal()">Stay here</button>');}
 if(S.room!==from){S.sceneFocus=null;S.sceneFocusRoom=S.room;WardNavigation.until=performance.now()+300;renderScene();}
 return result;
};
sceneDoorTravel=function(to,event){if(event?.detail>1||performance.now()<WardNavigation.until)return;go(to)};
mapTravel=function(to){if(!S||!edge(S.room,to)||performance.now()<WardNavigation.until)return;closeModal();go(to)};
})();
