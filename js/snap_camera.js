/* Renderer-independent, time-based angle interpolation. No game state or DOM required. */
(function(root){
'use strict';
const normalize=angle=>((angle%360)+360)%360;
const shortestDelta=(from,to)=>{const d=normalize(to-from+180)-180;return d===-180?180:d;};
function create({getAngle,getPitch=()=>0,onUpdate,onState=()=>{},onComplete=()=>{},snapSpeed=10,epsilon=.02,automatic=true,requestFrame=cb=>requestAnimationFrame(cb),cancelFrame=id=>cancelAnimationFrame(id)}={}){
 if(typeof getAngle!=='function'||typeof onUpdate!=='function')throw new TypeError('getAngle and onUpdate are required');
 let speed=Number(snapSpeed),active=false,current=0,target=0,goal=0,currentPitch=0,targetPitch=0,raf=null,last=null;
 if(!Number.isFinite(speed)||speed<=0)throw new RangeError('snapSpeed must be positive');
 if(!Number.isFinite(epsilon)||epsilon<=0)throw new RangeError('epsilon must be positive');
 function stopFrame(){if(raf!==null)cancelFrame(raf);raf=null;last=null;}
 function finish(){stopFrame();current=goal;currentPitch=targetPitch;active=false;onUpdate(goal,targetPitch);onState(false);onComplete(goal,targetPitch);}
 function step(deltaSeconds){if(!active)return false;if(!Number.isFinite(deltaSeconds)||deltaSeconds<0)return true;
  // The exponential factor gives the same position at a given elapsed time at any FPS.
  const factor=Math.exp(-speed*deltaSeconds);current=target+(current-target)*factor;currentPitch=targetPitch+(currentPitch-targetPitch)*factor;
  if(Math.abs(target-current)<=epsilon&&Math.abs(targetPitch-currentPitch)<=epsilon){finish();return false;}
  onUpdate(current,currentPitch);return true;
 }
 function frame(now){raf=null;if(!active)return;const dt=last===null?0:Math.max(0,(now-last)/1000);last=now;if(step(dt)&&automatic)raf=requestFrame(frame);}
 function snapTo(angle,{immediate=false,pitch=0}={}){if(active||!Number.isFinite(angle)||!Number.isFinite(pitch))return false;current=Number(getAngle());if(!Number.isFinite(current))return false;currentPitch=Number(getPitch())||0;targetPitch=Math.max(-45,Math.min(45,pitch));goal=normalize(angle);target=current+shortestDelta(current,goal);active=true;onState(true);
  if(immediate||Math.abs(target-current)<=epsilon&&Math.abs(targetPitch-currentPitch)<=epsilon){finish();return true;}
  if(automatic)raf=requestFrame(frame);return true;
 }
 function cancel({complete=false}={}){if(!active)return;if(complete)return finish();stopFrame();active=false;onState(false);}
 return {snapTo,step,cancel,get busy(){return active;},get targetAngle(){return goal;},get snapSpeed(){return speed;},set snapSpeed(value){value=Number(value);if(!Number.isFinite(value)||value<=0)throw new RangeError('snapSpeed must be positive');speed=value;}};
}
const api={create,normalize,shortestDelta};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.WardSnapCamera=api;
})(typeof window!=='undefined'?window:globalThis);
