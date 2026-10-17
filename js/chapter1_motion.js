/* Animated scene layers in artwork coordinates. No UI text or input capture. */
(function(){
'use strict';
let raf=0,frames=0,currentRoom='',running=false;
const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
function enabled(options){return options.motion!==false&&(!reduced()||options.motionOverride===true)}
function mount(host,room,options){cancelAnimationFrame(raf);running=false;host.querySelectorAll('.c1-motion-canvas').forEach(e=>e.remove());const rear=S.sceneView==='rear',plane=host.querySelector(rear?'.c1-reverse-plane':'.c1-plane');if(!plane||!enabled(options)||S.hp<=0||S.f.hidingRoom||S.f.chapter1Complete)return;
 const canvas=document.createElement('canvas');canvas.width=1000;canvas.height=750;canvas.className='c1-motion-canvas';canvas.setAttribute('aria-hidden','true');plane.append(canvas);const c=canvas.getContext('2d');currentRoom=room;running=true;
 const dust=Array.from({length:32},(_,i)=>({x:(i*137.7)%1000,y:(i*89.3)%750,s:5+(i%7)*2}));
 function glow(x,y,r,color){const g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,color);g.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=g;c.fillRect(x-r,y-r,r*2,r*2)}
 function draw(now){if(!canvas.isConnected){running=false;return;}frames++;const t=now/1000;c.clearRect(0,0,1000,750);
  // Rain tracks the actual window, with moving reflected street light on the floor.
  if(room==='lobby'){c.save();c.beginPath();c.rect(0,0,rear?330:340,450);c.clip();c.strokeStyle='rgba(180,211,228,.27)';c.lineWidth=1.3;for(let i=0;i<75;i++){const x=(i*43.7)%340,y=(i*97+t*(110+i%9*14))%520-70;c.beginPath();c.moveTo(x,y);c.lineTo(x-3,y+22+i%17);c.stroke();}c.restore();glow(290,660,260,`rgba(115,139,168,${.055+.04*Math.sin(t*2)})`);glow(140,630,190,`rgba(157,49,31,${.05+.045*Math.sin(t*1.4)})`);}
  if(room==='security'&&!rear){c.save();c.beginPath();c.rect(386,220,250,130);c.clip();c.fillStyle='rgba(156,221,214,.13)';c.fillRect(386,220+(t*45)%130,250,4);for(let i=0;i<18;i++){c.fillStyle=`rgba(175,218,211,${.025+(Math.sin(t*8+i)*.025)})`;c.fillRect(386,220+i*8,250,1);}c.restore();}
  if(room==='eastcorridor'){const flicker=.05+.035*Math.sin(t*4.7)+.022*Math.sin(t*17);glow(510,95,230,`rgba(227,222,175,${Math.max(.008,flicker)})`);glow(520,610,250,`rgba(199,208,187,${.035+.025*Math.sin(t*4.7)})`);}
  if(room==='ward'){glow(rear?750:440,rear?420:290,210,`rgba(239,199,115,${.055+.035*Math.sin(t*2.1)})`);}
  if(room==='room12'){glow(rear?220:330,rear?350:250,180,`rgba(151,190,218,${.065+.035*Math.sin(t*.9)})`);glow(810,280,180,`rgba(230,182,98,${.04+.025*Math.sin(t*3.1)})`);}
  // Slow airborne dust catches the local light; it does not move the background or targets.
  for(let i=0;i<dust.length;i++){const d=dust[i],x=(d.x+t*d.s)%1000,y=(d.y+Math.sin(t*.5+i)*12+750)%750;c.fillStyle=`rgba(212,212,186,${.08+(i%5)*.025})`;c.beginPath();c.arc(x,y,.65+i%3*.35,0,Math.PI*2);c.fill();}
  raf=requestAnimationFrame(draw);
 }
 raf=requestAnimationFrame(draw);
}
window.WardMotion={mount,enabled,snapshot:()=>({room:currentRoom,frames,running})};
})();
