/* Weather and CRT effects are clipped in room coordinates, never screen coordinates. */
(function(){
'use strict';
const WW=WardWinter;
const glass={
 lobby:{front:[[[0,2],[7,4],[7,21],[0,20]],[[17,13],[23,17],[23,32],[17,29]],[[25,18],[31,21],[31,35],[25,32]],[[33,23],[39,26],[39,39],[33,36]],[[0,27],[7,29],[7,48],[0,49]],[[17,35],[23,38],[23,56],[17,59]],[[25,39],[31,40],[31,55],[25,56]]],rear:[[[84,1],[97,1],[97,7],[84,12]],[[84,18],[97,11],[97,37],[84,38]],[[85,44],[97,43],[97,62],[85,57]]]},
 security:{front:[[[0,3],[8,9],[8,24],[0,22]],[[0,28],[8,31],[8,48],[0,49]],[[18,9],[23,16],[23,27],[18,23]],[[18,27],[23,30],[23,43],[18,45]]]},
 wardnorth:{rear:[[[14,23],[22,23],[22,32],[14,32]],[[14,36],[22,36],[22,45],[14,45]],[[27,23],[36,23],[36,32],[27,32]],[[27,36],[36,36],[36,45],[27,45]],[[74,23],[81,23],[81,32],[74,32]],[[74,36],[81,36],[81,45],[74,45]]]}
};
WW.glass=glass;
let raf=0,frames=0,running=false,currentRoom='';const images=new Map();
function load(path){const src=WW.asset(path);if(!images.has(src)){const im=new Image();im.src=src;images.set(src,im);}return images.get(src);}
function path(polys,w,h){const p=new Path2D();for(const poly of polys){p.moveTo(poly[0][0]/100*w,poly[0][1]/100*h);for(const [x,y]of poly.slice(1))p.lineTo(x/100*w,y/100*h);p.closePath();}return p;}
const enabled=o=>o.motion!==false&&(!matchMedia('(prefers-reduced-motion: reduce)').matches||o.motionOverride===true);
function mount(host,room,options){cancelAnimationFrame(raf);running=false;host.querySelectorAll('.c1-motion-canvas,.c1-weather-rain,.winter-screen-canvas').forEach(n=>n.remove());if(!S||S.hp<=0||S.f.chapter1Complete||S.f.hidingRoom)return;const view=S.sceneView,plane=host.querySelector(view==='rear'?'.c1-reverse-plane':'.c1-plane');if(!plane)return;const ratio=plane.clientWidth/Math.max(1,plane.clientHeight),canvas=document.createElement('canvas');canvas.width=1400;canvas.height=Math.round(1400/ratio);canvas.className='winter-screen-canvas';canvas.setAttribute('aria-hidden','true');plane.append(canvas);const c=canvas.getContext('2d'),w=canvas.width,h=canvas.height,polys=S.f.lobbyShutters&&room==='lobby'?null:glass[room]?.[view],clip=polys?path(polys,w,h):null,motion=enabled(options);currentRoom=room;
 const screens=[];
 if(room==='security'&&view==='front')for(let row=0;row<2;row++)for(let col=0;col<3;col++)screens.push({x:(42.35+col*5.45)/100*w,y:(30.2+row*9.4)/100*h,width:.042*w,height:.058*h,feed:['eastcorridor','ward','room12','laundry','observation','wardnorth'][row*3+col]});
 const tv=WardScenes[room].fixtures.find(f=>f.television&&(f.view||'front')===view);if(tv){const [x,y,fw,fh]=tv.rect;screens.push({x:(x-fw*.42)/100*w,y:(y-fh*.37)/100*h,width:fw*.68/100*w,height:fh*.68/100*h,feed:null});}
 function draw(now){if(!canvas.isConnected){running=false;return;}frames++;const t=now/1000;c.clearRect(0,0,w,h);
  if(clip){c.save();c.clip(clip);c.fillStyle='rgba(222,234,232,.7)';for(let i=0;i<160;i++){const x=((i*117.2+t*(13+i%5*4)+Math.sin(t*.8+i)*12)%w+w)%w,y=((i*61.8+t*(15+i%7*3))%h+h)%h;c.beginPath();c.arc(x,y,.7+i%3*.55,0,Math.PI*2);c.fill();}c.restore();}
  for(let i=0;i<screens.length;i++){const s=screens[i];c.save();c.beginPath();c.roundRect(s.x,s.y,s.width,s.height,Math.max(2,s.width*.06));c.clip();c.fillStyle='#08100d';c.fillRect(s.x,s.y,s.width,s.height);const online=!!(s.feed&&(S.f.power&&!S.f.powerOut||i<2));if(online){const image=load(WW.roomArt(s.feed,'front'));if(image.complete&&image.naturalWidth){c.filter='grayscale(1) contrast(1.15) brightness(.8)';c.drawImage(image,s.x,s.y,s.width,s.height);c.filter='none';}}
   for(let n=0;n<90;n++){const a=((Math.sin(n*66.4+(motion?t*14:0))+1)/2)*.15;c.fillStyle='rgba(207,225,213,'+a+')';const x=s.x+(n*29.7)%s.width,y=s.y+((n*17+(motion?t*24:0))%s.height);c.fillRect(x,y,1+n%3,1);}
   c.fillStyle='rgba(146,187,161,.12)';for(let y=s.y;y<s.y+s.height;y+=3)c.fillRect(s.x,y,s.width,.5);
   if(motion){c.fillStyle='rgba(196,228,207,.12)';c.fillRect(s.x,s.y+(t*12)%s.height,s.width,1.3);}
   if(S.sceneDisturbance?.room===room&&S.san<65){c.fillStyle='#0b100fe8';c.fillRect(s.x,s.y,s.width,s.height);c.fillStyle='#d2d9bd';c.font=Math.max(6,s.width*.1)+'px monospace';c.textAlign='center';c.fillText(['YOU WERE AWAKE','NO ADMISSION','WE REMEMBER'][i%3],s.x+s.width/2,s.y+s.height/2);}
   if(online){c.fillStyle='#b8c7b3';c.font=Math.max(4,s.width*.07)+'px monospace';c.textAlign='left';c.fillText('CAM '+String(i+1).padStart(2,'0')+' 1998',s.x+2,s.y+s.height-2);}c.restore();
  }
  const phase=(t+hashSeed(room)%23)%29;if(motion&&phase>27.8){const light=WardScenes[room].fixtures.find(f=>/light/.test(f.id)),x=(light?.rect[0]||50)/100*w,y=(light?.rect[1]||8)/100*h,r=w*.2,g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,'rgba(192,188,132,'+(.08+.06*Math.sin(t*27))+')');g.addColorStop(1,'transparent');c.fillStyle=g;c.fillRect(x-r,y-r,r*2,r*2);}
  if(room==='eastcorridor'&&view==='front'&&S.f.sprinklerTriggered&&!S.f.sprinklerStopped){c.strokeStyle='rgba(180,216,224,.42)';c.lineWidth=1;for(let i=0;i<60;i++){const travel=((t*.9+i/60)%1),x=w*(.59+(i%11-5)*.025*travel),y=h*(.16+travel*.7);c.beginPath();c.moveTo(x,y);c.lineTo(x+(i%11-5)*.8,y+h*.025);c.stroke();}}
  if(room==='laundry'&&view==='rear'&&S.f.stoveLit){const f=WardScenes.laundry.fixtures.find(f=>f.id==='stove'),x=f.rect[0]/100*w,y=f.rect[1]/100*h,r=w*.12,g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,'rgba(219,127,39,'+(.22+(motion?.05*Math.sin(t*9):0))+')');g.addColorStop(1,'transparent');c.fillStyle=g;c.fillRect(x-r,y-r,2*r,2*r);}
  if(motion){running=true;raf=requestAnimationFrame(draw);}else running=false;
 }
 draw(performance.now());
 if(!motion)for(const im of images.values())if(!im.complete)im.addEventListener('load',()=>{if(canvas.isConnected)draw(0);},{once:true});
}
WardMotion.mount=mount;WardMotion.enabled=enabled;WardMotion.glazing=glass;WardMotion.snapshot=()=>({room:currentRoom,frames,running});
})();
