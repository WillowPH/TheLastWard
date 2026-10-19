/* Room-facing atmosphere: every effect shares the native image's 1448 × 1086 coordinates. */
(function(){
'use strict';
const WW=WardWinter,W=1448,H=1086,fx=document.createElement('canvas'),snow=document.createElement('canvas');
fx.width=snow.width=W;fx.height=snow.height=H;
const ctx=fx.getContext('2d'),flakes=snow.getContext('2d'),images=new Map();
let data={},raf=0,revision=0,frames=0,running=false;
const state=()=>typeof S==='undefined'?null:S;
const renderer=()=>WW.roomViewRenderer?.();
function image(path){
 if(!images.has(path)){
  const im=new Image();
  im.onload=()=>{if(renderer()?.loaded)draw(performance.now());};
  im.src=WW.asset(path);images.set(path,im);
 }
 return images.get(path);
}
function polygons(paths){
 const p=new Path2D();
 for(const poly of paths||[]){p.moveTo(poly[0][0]/100*W,poly[0][1]/100*H);for(const [x,y]of poly.slice(1))p.lineTo(x/100*W,y/100*H);p.closePath();}
 return p;
}
function bounds(rect){return [(rect[0]-rect[2]/2)/100*W,(rect[1]-rect[3]/2)/100*H,rect[2]/100*W,rect[3]/100*H];}
function motionEnabled(){return WardMotion.enabled(WardScene.options);}
function shutterSurface(spec){
 // Both shutter states are full-resolution painted room states with rails,
 // perspective and foreground occlusion. Never stretch a material over glass.
 if(!spec?.asset)return null;
 const native=image(spec.asset);return native.complete&&native.naturalWidth?native:null;
}
function paintSnow(glass,time,moving){
 flakes.clearRect(0,0,W,H);if(!glass.length)return;
 flakes.save();flakes.clip(polygons(glass));
 for(let pane=0;pane<glass.length;pane++){
  const poly=glass[pane],xs=poly.map(p=>p[0]/100*W),ys=poly.map(p=>p[1]/100*H),left=Math.min(...xs),top=Math.min(...ys),width=Math.max(...xs)-left,height=Math.max(...ys)-top;
  const count=Math.max(2,Math.min(36,Math.round(width*height/500)));
  for(let i=0;i<count;i++){
   const depth=.35+i%4*.14,t=moving?time:0,x=left+((i*17.71+pane*11+t*(.5+depth))%width+width)%width,y=top+((i*11.19+pane*5+t*(2+depth*2))%height+height)%height;
   flakes.fillStyle='rgba(214,225,235,'+(.18+depth*.25)+')';flakes.beginPath();flakes.ellipse(x,y,.3+depth*.35,.45+depth*.55,.12,0,Math.PI*2);flakes.fill();
  }
 }
 flakes.restore();
}
function paintScreens(screens,time,moving){
 for(const [i,screen]of (screens||[]).entries()){
  const [x,y,w,h]=bounds(screen.rect),s=state(),online=screen.feed&&(s.f.power&&!s.f.powerOut||i<2);
  ctx.save();ctx.beginPath();ctx.roundRect(x,y,w,h,Math.max(2,w*.06));ctx.clip();ctx.fillStyle='#080908';ctx.fillRect(x,y,w,h);
  if(online){
   const source=WW.roomViewAsset?.(screen.feed,'front')||data[screen.feed]?.front?.source;
   if(source){const im=image(source);if(im.complete&&im.naturalWidth){ctx.filter='grayscale(1) brightness(.66) contrast(1.12)';ctx.drawImage(im,0,0,im.naturalWidth,im.naturalHeight,x,y,w,h);ctx.filter='none';}}
  }
  for(let n=0;n<60;n++){ctx.fillStyle='rgba(192,198,190,'+(.025+.055*Math.abs(Math.sin(n*7+(moving?time*13:0))))+')';ctx.fillRect(x+(n*13.7)%w,y+(n*7.7+(moving?time*15:0))%h,1,1);}
  ctx.fillStyle='#c1c7bc16';for(let line=0;line<h;line+=3)ctx.fillRect(x,y+line,w,.5);
  if(moving){ctx.fillStyle='#c1c7bc22';ctx.fillRect(x,y+(time*7)%h,w,1);}
  if(s.sceneDisturbance?.room===s.room&&s.san<65){
   ctx.fillStyle='#070807';ctx.fillRect(x,y,w,h);ctx.fillStyle='#cdd3c4';ctx.font=Math.max(6,w*.075)+'px monospace';ctx.textAlign='center';ctx.fillText(['WE REMEMBER','YOU WERE AWAKE','DO NOT LOOK AWAY'][i%3],x+w/2,y+h/2);
  }else if(online){ctx.fillStyle='#b7bdb0';ctx.font=Math.max(5,w*.065)+'px monospace';ctx.fillText('CAM '+(i+1)+' 1998',x+3,y+h-3);}
  ctx.restore();
 }
}
function paintFire(rect,time,moving){
 if(!rect)return;const [x,y,w,h]=bounds(rect);ctx.save();ctx.beginPath();ctx.roundRect(x,y,w,h,Math.min(w,h)*.07);ctx.clip();
 // Keep the painted smoky firebox visible under a restrained ember glow.
 const glow=ctx.createRadialGradient(x+w*.5,y+h*.87,1,x+w*.5,y+h*.87,h*.7);glow.addColorStop(0,'#ef742a42');glow.addColorStop(.45,'#b84d1926');glow.addColorStop(1,'#1c100a00');ctx.fillStyle=glow;ctx.fillRect(x,y,w,h);
 for(let i=0;i<24;i++){const ex=x+w*(.08+(i*17.3%83)/100),ey=y+h*(.78+(i*11.9%16)/100),pulse=.35+.25*Math.sin(i*3.1+(moving?time*2:0));ctx.fillStyle='rgba(202,86,34,'+pulse+')';ctx.beginPath();ctx.ellipse(ex,ey,w*(.025+i%3*.01),h*.014,i*.1,0,Math.PI*2);ctx.fill();}
 for(let i=0;i<8;i++){
  const phase=i*2.37+(moving?time*4:0),cx=x+w*(.1+i*.115),height=h*(.25+.35*(.5+.5*Math.sin(phase))),bend=w*.08*Math.sin(phase*.7),flame=ctx.createLinearGradient(0,y+h,0,y+h-height);
  flame.addColorStop(0,'#f7ac5b72');flame.addColorStop(.5,'#d47b333b');flame.addColorStop(1,'#d54b1700');ctx.fillStyle=flame;ctx.beginPath();ctx.moveTo(cx-w*.07,y+h*.92);ctx.bezierCurveTo(cx-w*.09,y+h-height*.35,cx+bend-w*.035,y+h-height*.85,cx+bend,y+h-height);ctx.bezierCurveTo(cx+bend+w*.025,y+h-height*.45,cx+w*.08,y+h-height*.3,cx+w*.065,y+h*.92);ctx.fill();
 }
 ctx.restore();
}
function draw(now){
 const s=state(),r=renderer();if(!s||!r?.loaded||r.room!==s.room)return;
 const view=r.view||s.roomView||'front',spec=data[s.room]?.[view];ctx.clearRect(0,0,W,H);flakes.clearRect(0,0,W,H);if(!spec){r.effects(fx);return;}
 const t=now/1000,moving=motionEnabled(),closed=s.room==='lobby'&&s.f.lobbyShutters;
 const windows=spec.windowGlass&&WW.windowState?.(),physicalGlass=windows?.triggered?spec.windowGlass.flatMap((pane,i)=>pane[windows.closed[i]?'closed':'open']):spec.glass||[],glass=closed?[]:physicalGlass;
 if(windows?.triggered&&spec.windowState){
  const opening=image(spec.windowState.asset);
  if(opening.complete&&opening.naturalWidth)for(let i=0;i<3;i++)if(!windows.closed[i]){
   ctx.save();ctx.clip(polygons(spec.windowState.masks[i]));ctx.drawImage(opening,0,0,W,H);ctx.restore();
  }
 }
 if(closed){const surface=shutterSurface(spec.shutters);if(surface)ctx.drawImage(surface,0,0,W,H);}
 const dip=moving&&WardScene.options.flashes!==false?WW.flicker(s.room,t):0;
 if(dip){const interior=new Path2D();interior.rect(0,0,W,H);interior.addPath(polygons(physicalGlass));ctx.save();ctx.clip(interior,'evenodd');ctx.fillStyle='rgba(0,0,0,'+dip+')';ctx.fillRect(0,0,W,H);ctx.restore();}
 paintSnow(glass,t,moving);ctx.drawImage(snow,0,0);paintScreens(spec.screens,t,moving);
 if(s.room==='laundry'&&s.f.stoveLit)paintFire(spec.firebox,t,moving);
 if(s.room==='eastcorridor'&&s.f.sprinklerTriggered&&!s.f.sprinklerStopped&&spec.sprinkler){
  const p=spec.sprinkler,x=p.origin[0]/100*W,y=p.origin[1]/100*H;ctx.save();ctx.strokeStyle='rgba(182,215,223,.25)';
  for(let i=0;i<35;i++){const a=(i%9-4)/9,travel=((moving?t:0)*.9+i/35)%1,px=x+a*travel*W*p.width/100,py=y+travel*H*p.length/100;ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px+a*2,py+6);ctx.stroke();}ctx.restore();
 }
 r.effects(fx);frames++;
}
function stop(){cancelAnimationFrame(raf);raf=0;revision++;running=false;}
function mount(){
 stop();const own=revision,s=state();if(!s||s.hp<=0||s.f.chapter1Complete)return;
 let last=-Infinity;
 function frame(now){if(own!==revision||!renderer()?.loaded)return;if(now-last>=1000/24){draw(now);last=now;}if(motionEnabled()){running=true;raf=requestAnimationFrame(frame);}else running=false;}
 frame(performance.now());
}
const api={mount,stop,draw,canvas:fx,snowCanvas:snow,get frames(){return frames;},get data(){return data;}};
WW.roomViewEffects=api;
api.ready=fetch(WW.asset('data/room_view_effects.json')).then(response=>{if(!response.ok)throw Error('Room effect definitions could not load.');return response.json();}).then(value=>{data=value;WardMotion.glazing=data;mount();return data;}).catch(error=>{console.error(error);return null;});
WardMotion.mount=mount;
WardMotion.snapshot=()=>({room:state()?.room,view:renderer()?.view||state()?.roomView,frames,running});
})();
