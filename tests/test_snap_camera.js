'use strict';
const assert=require('node:assert/strict');
const {create,normalize,shortestDelta}=require('../js/snap_camera.js');
function rig(start=0,speed=10){let angle=start,updates=0,states=[];const camera=create({getAngle:()=>angle,onUpdate:a=>{angle=a;updates++;},onState:v=>states.push(v),snapSpeed:speed,automatic:false});return {camera,get angle(){return angle;},get updates(){return updates;},states};}
for(const [from,to,delta]of [[350,10,20],[10,350,-20],[0,180,180],[359,0,1],[0,359,-1],[-10,730,20]])assert.equal(shortestDelta(from,to),delta);
for(const [from,to]of [[350,10],[10,350],[0,180],[359,0]]){const r=rig(from);r.camera.snapTo(to);const distance=shortestDelta(from,to);let previous=0;for(let frame=0;frame<240&&r.camera.busy;frame++){r.camera.step(1/60);const progress=shortestDelta(from,r.angle);assert(Math.abs(progress)>=Math.abs(previous)-1e-9);assert(Math.abs(progress)<=Math.abs(distance)+1e-9);previous=progress;}assert(!r.camera.busy);assert.equal(r.angle,normalize(to));const updates=r.updates;r.camera.step(100);assert.equal(r.updates,updates);assert.deepEqual(r.states,[true,false]);}
function at(rate){const r=rig(350);r.camera.snapTo(10);let t=0;while(t<.25){const dt=Math.min(1/rate,.25-t);r.camera.step(dt);t+=dt;}return r.angle;}
assert(Math.abs(at(30)-at(60))<1e-9);assert(Math.abs(at(60)-at(144))<1e-9);
const r=rig();assert(r.camera.snapTo(90));assert.equal(r.camera.snapTo(270),false);r.camera.step(10);assert.equal(r.angle,90);assert(!r.camera.busy);assert(r.camera.snapTo(270));r.camera.cancel({complete:true});assert.equal(r.angle,270);assert(!r.camera.busy);
const instant=rig(350);instant.camera.snapTo(10,{immediate:true});assert.equal(instant.angle,10);assert(!instant.camera.busy);assert.throws(()=>{instant.camera.snapSpeed=0;},RangeError);
console.log('PASS shortest wrap in both directions, no overshoot, exact stop, no idle jitter, 30/60/144 FPS equivalence, long frames, speed validation, input retarget lock and reduced-motion instant snap');

let yaw=350,pitch=-12;const vertical=create({getAngle:()=>yaw,getPitch:()=>pitch,onUpdate:(a,p)=>{yaw=a;pitch=p;},automatic:false});vertical.snapTo(10,{pitch:18});for(let i=0;i<200&&vertical.busy;i++)vertical.step(1/60);assert.equal(yaw,10);assert.equal(pitch,18);assert(!vertical.busy);console.log("PASS POI pitch and yaw stop together at their exact destinations");
