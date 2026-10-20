/* Captions sit over the authored artwork, without a second opaque footer. */
(function(){'use strict';const WW=WardWinter;let frame=null,queued=false;
// A status or apparition refresh must not reset a live mouse gesture. The
// completed turn performs the pending render, or a cancelled/short drag replays it.
const scene=renderScene;let pendingScene=false;
renderScene=function(...args){if(WW.orbit?.holding){pendingScene=true;return;}pendingScene=false;return scene.apply(this,args);};
document.addEventListener('ward:look-gesture-end',()=>{if(pendingScene)requestAnimationFrame(()=>{if(pendingScene&&!WW.orbit?.busy)renderScene();});});
// A remaining ammunition sleeve gets a brighter etched bracket on its actual
// container. It retires with the pickup, even if a record remains inside.
const fixture=WW.sceneUI.fixture;
WW.sceneUI.fixture=function(f){const html=fixture(f),ammo=f.objects.some(o=>S.ob[o[0]]!=='done'&&(o[4].give||[]).some(([name])=>/Ammo|Shells|Rounds/.test(name)));return ammo?html.replace('class="c1-target important','data-supply="ammo" class="c1-target important'):html;};
function place(){queued=false;const stage=$('wardStage'),art=document.querySelector('.room-view-frame'),cards=document.querySelector('.narrative-focus');if(!stage||!art||!cards)return;if(frame!==art){if(frame)observer.unobserve(frame);frame=art;observer.observe(frame);}if(innerWidth<=700)return;const s=stage.getBoundingClientRect(),r=art.getBoundingClientRect();if(!r.width||!r.height)return;const left=Math.max(10,r.left-s.left+12),right=Math.max(10,s.right-r.right+12),bottom=Math.max(12,s.bottom-r.bottom+14);for(const [name,value]of Object.entries({'--caption-left':left,'--caption-right':right,'--caption-bottom':bottom})){const v=Math.round(value)+'px';if(cards.style.getPropertyValue(name)!==v)cards.style.setProperty(name,v);}}
function schedule(){if(!queued){queued=true;requestAnimationFrame(place);}}
const observer=new ResizeObserver(schedule);observer.observe($('wardStage'));
new MutationObserver(schedule).observe($('interactiveScene'),{childList:true,subtree:true});
window.addEventListener('resize',schedule);document.addEventListener('ward:resume',schedule);WW.placeCaptions=place;schedule();
})();
