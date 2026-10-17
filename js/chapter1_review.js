/* Four-room visual review and shared player-facing corrections. */
(function(){
'use strict';
const e=htmlSafe;
R.security.d='Surveillance monitors hum above a cramped security desk. A cold coffee sits beside the controls. The outside locks answer to a remote operator; the local switches have been disabled.';
R.security.alt=['power','Restored power steadies the surveillance bank. The exterior locks remain under outside control.'];
R.ward.d='The Patient Wing opens around a tiled nurse station. An open night-shift equipment case rests on the counter. Heavy doors lead back to the East Corridor and onward to the North Patient Corridor. A toppled gurney blocks part of the floor.';
delete R.ward.alt;

R.security.o=R.security.o.filter(o=>o[0]!=='reva');const equipment=R.security.o.find(o=>o[0]==='rev');equipment[1]='Equipment cabinet';equipment[3]='The sidearm case and ammunition sleeve are both empty.';equipment[4].th='The pistol and its ammunition are gone. The night-shift equipment was taken toward the Patient Wing.';
const sidearm=R.ward.o.find(o=>o[0]==='nightPistol');sidearm[1]='Secured night-shift sidearm';sidearm[3]='A keyed retaining bracket holds the handgun inside the open equipment case.';

const patientChoice=choosePatientFate;
choosePatientFate=function(choice){if(!S||S.f.beggingPatientChoice||!['helped','left','killed'].includes(choice))return;
 let failure='';if(choice==='helped'&&!has('Trauma Dressing'))failure='You need a Trauma Dressing to treat him. Your choice has not been made.';
 if(choice==='killed'&&(!W[S.eq]||!has(S.eq)))failure='You need to equip a firearm before you can do this. Your choice has not been made.';
 else if(choice==='killed'&&!(S.ld[S.eq]>0))failure='Your firearm is empty. Reload it first. Your choice has not been made.';
 if(failure)return modal('The patient is still alive',`<p>${failure}</p><button class="btn p" onclick="beggingPatient()">Return to the patient</button><button class="btn" onclick="closeModal();invModal()">Check equipment</button>`);
 return patientChoice(choice);
};
const positions={lobby:[150,90],security:[400,90],eastcorridor:[275,230],ward:[275,370],wardnorth:[275,510],room12:[100,670],isoward:[350,670],wardservice:[850,510],residence:[100,840],stafflounge:[100,1010],children:[350,840],pharmacy:[1100,370],laundry:[1100,510],surgery:[1350,510],archive:[850,710],chapel:[600,850],records:[1100,710],coldstore:[1350,710],generator:[850,1010],lift:[600,1010],morgue:[1100,1010],tunnel:[1350,1010],boiler:[1100,1180],observation:[850,1180],specimen:[850,1350],powercontrol:[1100,1350],isolation:[1350,1350]};
for(const [id,[x,y]]of Object.entries(positions)){R[id].x=20+x/4;R[id].y=370-y/4;}
window.WardFloorPlan={positions,zoom:1};
function roomLines(name){const words=name.split(' '),lines=[''];for(const word of words){if((lines.at(-1)+' '+word).trim().length>21)lines.push(word);else lines[lines.length-1]=(lines.at(-1)+' '+word).trim()}return lines.slice(0,3)}
function largeMap(){const paths=Object.entries(D).map(([id,d])=>{const [x,y]=positions[d.a],[u,v]=positions[d.b];return `<path data-map-edge="${id}" class="${doorOpen(id)?'open':'sealed'}" d="M${x} ${y}L${u} ${v}"/>`}).join('');const nodes=Object.entries(positions).map(([id,[x,y]])=>{const adjacent=WardNavigation.edge(S.room,id),known=mappedRoom(id),name=known?R[id].n:'Unmapped room',lines=roomLines(name),cls=id===S.room?'here':adjacent?'adjacent':S.vis[id]?'visited':'unknown';return `<g transform="translate(${x},${y})" class="${cls}" ${adjacent?`role="button" tabindex="0" data-map-room="${id}" onclick="mapTravel('${id}')" onkeydown="if(event.key==='Enter'){mapTravel('${id}')}"`:''} aria-label="${e(name)}"><title>${e(name)}${adjacent?' · Connected to your room':''}</title><rect x="-96" y="-35" width="192" height="70" rx="7"/>${lines.map((line,i)=>`<text text-anchor="middle" y="${(i-(lines.length-1)/2)*20+5}">${e(line)}</text>`).join('')}${id===S.room?'<text class="map-you" y="-47" text-anchor="middle">YOU ARE HERE</text>':''}</g>`}).join('');return `<svg class="c1-large-map" viewBox="0 0 1470 1450" role="img" aria-label="Blackridge first-floor connections"><g class="c1-map-links">${paths}</g><g class="c1-map-rooms">${nodes}</g></svg>`}
mapModal=function(){if(!S)return;const exits=roomConnections().map(d=>`<button class="btn" onclick="mapTravel('${d.to}')">${e(R[d.to].n)}${doorOpen(d.id)?'':' · locked'}</button>`).join('');modal('Blackridge · First floor',`<div class="c1-map-controls"><button class="btn" onclick="wardMapZoom(-.2)">−</button><button class="btn" onclick="wardMapZoom(.2)">+</button><button class="btn" onclick="wardMapCenter()">Find my room</button><span>Drag the scrollbars or swipe to explore.</span></div><div class="c1-map-scroll">${largeMap()}</div><p class="c1-map-legend">Gold: your room · Blue: connected room · Grey: explored · Dashed line: locked passage. Lines show actual connections; proximity alone does not.</p><div class="c1-map-exits"><strong>Doors from here</strong>${exits}</div>`);document.querySelector('#m .md')?.classList.add('c1-map-modal');WardFloorPlan.zoom=1;wardMapZoom(0);wardMapCenter();};
window.wardMapZoom=function(delta){WardFloorPlan.zoom=Math.max(.5,Math.min(1.8,WardFloorPlan.zoom+delta));const svg=document.querySelector('.c1-large-map');if(svg){svg.style.width=(1470*WardFloorPlan.zoom)+'px';svg.style.height=(1450*WardFloorPlan.zoom)+'px'}};
window.wardMapCenter=function(){const host=document.querySelector('.c1-map-scroll');if(!host)return;const [x,y]=positions[S.room];host.scrollLeft=x*WardFloorPlan.zoom-host.clientWidth/2;host.scrollTop=y*WardFloorPlan.zoom-host.clientHeight/2};
})();
