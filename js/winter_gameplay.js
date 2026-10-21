/* One authoritative exploration clock for charge, local exposure and recovery. */
(function(){
'use strict';
const WW=WardWinter,e=htmlSafe;
const warmRooms=new Set(['lobby','generator','chapel','stafflounge']);
WW.isWarm=()=>!!(S.f.power&&!S.f.powerOut&&warmRooms.has(S.room)||S.room==='laundry'&&S.f.stoveLit);
// This is the same darkness test used by the renderer and authored interaction targets.
WW.needsFlashlight=()=>!!(S&&WardNavigation.isDark(S.room));
WW.isSurvivalPaused=()=>!!(WW.isReadingRecord?.()||document.querySelector('#m .winter-document-modal,#m .winter-object-modal,#m .winter-portrait-grid,#m .winter-wire-panel,#m .winter-radio,#m .winter-fuse-board'));
WW.windowState=()=>S.windows||(S.windows={triggered:false,closed:[true,true,true],resolved:false,exposure:0});
WW.ignitionCapacity=()=>S?Math.max(0,2-Number(!!S.f.stoveLit)-Number(!!S.f.chapelCandles)):0;
WW.fuel=()=>Math.max(0,Math.min(WW.ignitionCapacity(),Math.floor(Number(S?.lighterFuel)||0)));
const configureFuel=configureWorld;configureWorld=function(...args){const result=configureFuel.apply(this,args);if(S)S.lighterFuel=WW.fuel();return result;};
WW.ignite=function(){if(!has('Lighter')){interaction('I need the petrol lighter from Security.');return false;}if(WW.fuel()<=0){interaction('The lighter is empty. Combine it with Lighter Fluid in Inventory.');return false;}S.lighterFuel=WW.fuel()-1;soundEffect('click');return true;};
window.wardCombineLighter=function(){if(!S||S.hp<=0||S.f.dead||S.f.chapter1Complete||WW.isPaused?.())return false;if(!has('Lighter')||!has('Lighter Fluid'))return toast('Carry the lighter and fluid together.');const remaining=WW.ignitionCapacity();if(!remaining)return toast('Both permanent ignition points are already lit.');if(WW.fuel()>=remaining)return toast('The lighter already has enough fuel for its remaining ignition points.');rem('Lighter Fluid');S.lighterFuel=remaining;advanceTime(1);soundEffect('combine');render();toast('Lighter prepared · '+remaining+' ignition'+(remaining===1?'':'s')+' remaining.');};
const combine=combineItems;combineItems=function(){const a=S.inv[Number($('combineA')?.value)]?.n,b=S.inv[Number($('combineB')?.value)]?.n;if(new Set([a,b]).has('Lighter')&&new Set([a,b]).has('Lighter Fluid')){wardCombineLighter();return invModal();}return combine();};
const slot=useInventorySlot;useInventorySlot=function(i){const n=S.inv[i]?.n;if(n==='Lighter'||n==='Lighter Fluid')return modal(e(n),`<div class="c1-item-examine">${itemIconMarkup(n)}<p>${e(desc(n))}</p>${n==='Lighter'?'<p>Ignitions remaining · '+WW.fuel()+'</p>':''}</div>${has('Lighter')&&has('Lighter Fluid')?'<button class="btn p" onclick="wardCombineLighter();closeModal()">Combine lighter + fluid</button>':''}<button class="btn" onclick="invModal()">Inventory / combine</button>`);return slot(i);};
window.wardWarmUp=function(){if(!WW.isWarm())return interaction('This room is not warm enough. Find a powered safe room or light the laundry stove.');const affected=!!(S.f.wet||S.f.shivering||(S.f.coldExposure||0)>0);S.f.wet=0;S.f.wetTurns=0;S.f.coldExposure=0;S.f.shivering=0;S.f.wetWarning=0;S.f.exposureWarning=0;S.f.sprinklerRecovered=!!(S.f.sprinklerStopped&&!S.f.flashlightDropped);const w=WW.windowState();w.exposure=0;if(affected&&S.san<85&&S.t-(S.f.lastWarmRecovery??-100)>25){S.san=Math.min(85,S.san+8);S.f.lastWarmRecovery=S.t;}advanceTime(3);interaction('I dry my clothes and warm my hands. My grip steadies. The cold is passing.');render();};
window.wardOpenWindows=function(){const w=WW.windowState();if(S.room!=='wardnorth'||w.triggered)return;w.triggered=true;w.closed=[false,false,false];w.exposure=0;w.startedAt=S.t;S.f.coldWarning=0;S.sceneView='rear';$('m').innerHTML='';soundEffect('mechanism');S.f.windowOpenedOnce=1;interaction('Three sashes jerk open. Snow blows past the catches. I must close each window before the cold reaches my hands.');render();};
window.wardCloseColdWindow=function(i){const w=WW.windowState();if(S.room!=='wardnorth'||!Number.isInteger(i)||i<0||i>2||!w.triggered||w.closed[i])return;w.closed[i]=true;S.ob['coldWindow'+i]='done';S.sceneFocus=null;advanceTime(1);soundEffect('doorClose');if(w.closed.every(Boolean)){w.resolved=true;S.f.windowHazardResolved=1;S.ob.windowLever='done';for(let k=0;k<3;k++)S.ob['coldWindow'+k]='done';interaction('The final catch holds. The linkage snaps harmlessly back. These windows will not open again. I need warmth if I stayed too long.');}else interaction('Window '+(i+1)+' is shut. '+w.closed.filter(v=>!v).length+' still open.');render();};
wardSprinkler=function(){if(S.room!=='eastcorridor')return;if(S.f.sprinklerStopped)return interaction('The valve stays shut. No water is falling.');if(!S.f.sprinklerTriggered){S.f.sprinklerTriggered=1;S.f.wet=1;S.f.wetTurns=0;S.f.coldExposure=Math.max(4,S.f.coldExposure||0);S.f.flashlightDropped=!!has('Flashlight');S.lightOn=false;S.hp=Math.max(1,S.hp-Math.max(4,Math.round(7*S.m)));S.san=Math.max(0,S.san-6);soundEffect('metal');render();modal('The suppression line bursts','<p>Freezing water crashes against my shoulders. My foot slips. The flashlight hits the tiles beneath the pipe.</p><p>The impact has bruised my shoulder. The overhead valve stops the water; the flashlight must be picked up separately. Afterward I need the laundry drying stove or a powered warm room. Wet clothes will not dry just by walking around.</p><button class="btn p" onclick="closeModal()">Reach for the shutoff</button>');return;}S.f.sprinklerStopped=1;S.ob.staffSprinkler='done';advanceTime(1);soundEffect('mechanism');interaction('The valve closes. The sprinkler stops.'+(S.f.flashlightDropped?' My flashlight is still on the floor.':''));WW.think?.('My clothes are soaked. I need to dry them at the laundry stove, or warm up in a powered safe room.','dry');render();};
wardRecoverFlashlight=function(){if(S.room!=='eastcorridor'||!S.f.flashlightDropped)return;S.f.flashlightDropped=0;S.f.flashlightRecovered=1;advanceTime(1);soundEffect('pickup');interaction('I recover the flashlight and wipe its lens. My sleeves are soaked.');render();};
reinforceWindow=function(){if(S.f.windowBarricaded)return interaction('The barricade is secure.');if(!has('Wooden Plank'))return interaction('One substantial wooden plank would secure this opening. Laundry stores dry timber.');modal('Place the plank here?','<p>Secure the cracked opening with your wooden plank? The plank will be used here.</p><button class="btn p" onclick="wardPlacePlank()">Place plank</button><button class="btn" onclick="closeModal()">Cancel</button>');};
window.wardPlacePlank=function(){if(S.room!=='eastcorridor'||S.f.windowBarricaded||!has('Wooden Plank'))return;rem('Wooden Plank');S.f.windowBarricaded=1;S.ob.windowBoard='done';advanceTime(2);$('m').innerHTML='';soundEffect('metal');interaction('I brace the timber across the broken frame. It bears against both sides of the opening.');render();};
window.wardFitElevatorFuse=function(name,index){if(S.room!=='powercontrol'||!WW.fuses.includes(name)||!has(name))return;if(WW.fuses.indexOf(name)!==index)return toast('The shaped contacts do not fit. Nothing was used.');S.f.elevatorInserted=S.f.elevatorInserted||[];if(S.f.elevatorInserted.includes(name))return;rem(name);S.f.elevatorInserted.push(name);soundEffect('relay');advanceTime(1);if(S.f.elevatorInserted.length===4){S.f.elevatorFusesInstalled=1;S.ob.elevatorBoard='done';lg('All four elevator interlock plugs installed.');interaction('Four continuity lamps settle. The final elevator interlock is ready.');}wardElevatorBoard();render();};
window.wardElevatorBoard=function(){const inserted=S.f.elevatorInserted||[];modal('Elevator transfer interlock',`<p>The four sockets have different contact shapes. Select a carried plug, then its matching socket. The motor still needs generator power and transfer clearance.</p><div class="winter-fuse-plugs">${WW.fuses.filter(has).map(n=>`<button class="btn" onclick="WardWinter.selectedFuse='${n}';document.querySelectorAll('.winter-fuse-plugs .btn').forEach(b=>b.classList.remove('active'));this.classList.add('active')">${itemIconMarkup(n)}${e(n)}</button>`).join('')}</div><div class="winter-fuse-board">${WW.fuses.map((n,i)=>`<button class="winter-fuse-socket ${inserted.includes(n)?'fitted':''}" onclick="wardFitElevatorFuse(WardWinter.selectedFuse,${i})" aria-label="${e(n)} socket">${['♜','♝','♞','♚'][i]}<small>${inserted.includes(n)?'CONNECTED':n.replace(' Interlock Fuse','')}</small></button>`).join('')}</div><p>${inserted.length} / 4 connected</p><button class="btn" onclick="closeModal()">Leave the board</button>`);};
const actBase=act;
act=function(id){const o=R[S.room]?.o.find(o=>o[0]===id);if(!o||S.ob[id]==='done')return;const availability=WW.chargerStatus?.(id);if(availability&&!availability.available)return interaction(availability.reason);const sp=o[4];
 if(sp.act==='windowLever'){const w=WW.windowState();if(w.triggered)return interaction(w.resolved?'The one-use linkage has sheared. The windows stay shut.':'Close the three windows by their individual catches.');return modal('Release emergency supplies?','<p>The purge shaft frees a seized linen-return supply compartment containing sealed patrol ammunition. It also opens three windows into the snowstorm. Close all three brass catches before collecting the supplies. This reserve is optional; leave the handle alone if you do not need it.</p><button class="btn" onclick="wardOpenWindows()">Pull the handle</button><button class="btn p" onclick="closeModal()">Leave it alone</button>');}
 if(sp.act==='coldWindow')return wardCloseColdWindow(sp.index);
 if(sp.act==='warmStove'){if(!S.f.stoveLit){if(!WW.ignite())return;S.f.stoveLit=1;lg('Lit the enclosed laundry drying stove.');}wardWarmUp();return;}
 if(sp.act==='shutters'){S.f.lobbyShutters=!S.f.lobbyShutters;soundEffect('mechanism');advanceTime(1);interaction(S.f.lobbyShutters?'The steel shutters close over the three upper panes. The furniture barricade remains below.':'The upper shutters roll up, revealing snow beyond the glass.');return render();}
 if(sp.act==='candles'){if(!S.f.chapelCandles){if(!WW.ignite())return;S.f.chapelCandles=1;S.ob[id]='done';S.san=Math.max(S.san,Math.min(90,S.san+4));advanceTime(1);interaction('The three candles catch. Warm light reaches the opening-day photograph.');}return render();}
 if(sp.act==='elevatorBoard')return wardElevatorBoard();
 if(sp.act==='egg'){S.ob[id]='read';if(sp.egg==='sopranos'){if(!S.docs.includes('A note beside the sandwich bag'))S.docs.push('A note beside the sandwich bag');return doc('A note beside the sandwich bag');}return WW.inspectObject?.('icecreamToy');}
 if(sp.act==='photoInspect')return WW.inspectObject?.('openingPhoto');
 if(id==='regulator'){if(S.f.maintenancePrepared)return interaction('All four generator contacts are repaired.');if(!has('Maintenance Tools'))return interaction('The fused contacts require the insulated Maintenance Tools from Pharmacy.');return wardWirePanel();}
 if(id==='handCharge'||id==='emergencyDynamo'){if(!has('Flashlight'))return interaction('Bring the flashlight here.');if(S.bat>=12)return interaction('The emergency handle only supplies a little reserve charge.');if(S.t-(S.f.lastDynamo??-100)<50)return interaction('The dynamo needs to cool before another emergency charge. Find spare batteries.');S.f.lastDynamo=S.t;advanceTime(5);S.bat=12;S.lightTicks=0;interaction('Slow turns recover 12% emergency charge. The handle is hot now.');return render();}
 const powered=!!S.f.power,result=actBase(id);if(!powered&&S.f.power){S.f.lastBlackoutAt=S.t;S.f.blackoutCount=0;}return result;
};
window.wardWirePanel=function(){S.f.wires=S.f.wires||[];const labels=['A','B','C','D'],right=labels.slice().sort((a,b)=>hashSeed(S.seed+'wire'+a)-hashSeed(S.seed+'wire'+b));modal('Generator regulator contacts',`<p>Follow each lettered lead to its matching terminal. The insulated tools keep your hands clear of the damaged bus.</p><div class="winter-wire-panel"><div>${labels.map(c=>`<button class="winter-wire ${S.f.wires.includes(c)?'connected':''}" onclick="WardWinter.wireLead='${c}';this.classList.add('selected')">Lead ${c} ${S.f.wires.includes(c)?'✓':''}</button>`).join('')}</div><svg viewBox="0 0 100 180" aria-hidden="true">${S.f.wires.map(c=>`<path d="M0 ${labels.indexOf(c)*43+20} C70 ${labels.indexOf(c)*43+20},30 ${right.indexOf(c)*43+20},100 ${right.indexOf(c)*43+20}" stroke="${['#b36454','#6b9c8b','#c4ab65','#7798b8'][labels.indexOf(c)]}" stroke-width="3" fill="none"/>`).join('')}</svg><div>${right.map(c=>`<button class="winter-wire" onclick="wardConnectWire('${c}')">Terminal ${c}</button>`).join('')}</div></div><button class="btn" onclick="closeModal()">Leave the panel</button>`);};
window.wardConnectWire=function(c){if(S.room!=='generator'||!has('Maintenance Tools'))return;if(WW.wireLead!==c)return toast('The terminal marking does not match. Nothing is connected.');if(!S.f.wires.includes(c)){S.f.wires.push(c);soundEffect('relay');advanceTime(1);}WW.wireLead=null;if(S.f.wires.length===4){S.f.maintenancePrepared=1;S.ob.regulator='done';$('m').innerHTML='';interaction('Four lettered leads are seated. The repaired regulator can accept the ceramic fuse.');render();return;}wardWirePanel();};
const originalBattery=useBat;
const batteryDescription=desc;desc=function(name){return ({Battery:'Restores 40 percentage points of flashlight charge. Use from Inventory.','Reinforced Battery':'Restores 65 percentage points of flashlight charge. Combine a Battery with a Wire Spool to make one.'})[name]||batteryDescription(name);};
useBat=function(which,reopen=true){if(S.f.flashlightDropped)return interaction('Recover the flashlight from the East Corridor floor before replacing its battery.');which=which||(has('Reinforced Battery')?'Reinforced Battery':'Battery');if(!has(which))return toast('No spare battery.');if(S.bat>=100)return toast('The flashlight is fully charged.');rem(which);S.bat=Math.min(100,S.bat+(which==='Reinforced Battery'?65:40));soundEffect('pickup');advanceTime(1);render();if(cm&&alive(S.room))return foe('You replace the flashlight battery.');if(reopen)invModal('materials');};
rechargeAtGenerator=function(){const availability=WW.chargerStatus?.('charger');if(availability&&!availability.available)return interaction(availability.reason);if(!has('Flashlight')||!S.f.power)return interaction('The powered cradle needs the flashlight and generator power.');if(S.bat>=90)return interaction('The charge is already sufficient.');if((S.f.generatorChargeUses||0)>=2)return interaction('The cradle’s two spare cells are exhausted. Find batteries or use the emergency dynamo for a little charge.');S.f.generatorChargeUses=(S.f.generatorChargeUses||0)+1;S.bat=Math.min(100,S.bat+65);advanceTime(2);soundEffect('relay');interaction('A spare cradle cell restores charge. '+(2-S.f.generatorChargeUses)+' spare cells remain.');render();};
maybeAmbientHorror=function(){};
advancePowerOutage=function(){if(S.f.powerOut&&(S.t>=S.f.powerRestoreAt||Date.now()>=S.f.powerRestoreReal)){S.f.powerOut=0;S.f.lastBlackoutAt=S.t;interaction('The emergency relay catches. Hospital power returns.');soundEffect('relay');}};
// Exposure advances through deliberate actions and short real-time exploration ticks.
// Reading records and solving an open puzzle pause these survival costs.
WW.advanceExposure=function(n){
 if(!S||S.hp<=0||S.f.dead||S.f.chapter1Complete||WW.isSurvivalPaused())return;
 n=Math.max(0,Number(n)||0);if(!n)return;
 const w=WW.windowState(),open=w.closed.filter(v=>!v).length;
 const openWindows=S.room==='wardnorth'&&w.triggered&&!w.resolved&&open>0;
 const spray=S.room==='eastcorridor'&&S.f.sprinklerTriggered&&!S.f.sprinklerStopped;
 const coldRoom=S.room==='coldstore';
 if(spray)S.f.wet=1;
 if(openWindows){
  w.exposure+=n;S.f.coldExposure=(S.f.coldExposure||0)+n*open/3;
  if(w.exposure>=3&&!S.f.coldWarning){S.f.coldWarning=1;WW.sceneWarning?.('The open windows are freezing the corridor.');WW.think?.('The purge handle has opened three windows. I need to close each brass catch, then get warm.');}
 }
 if(coldRoom)S.f.coldExposure=(S.f.coldExposure||0)+n*.45;
 if(S.f.wet){
  S.f.wetTurns=(S.f.wetTurns||0)+n;
  // A warm room is shelter, not an automatic cure: choose its Warm up action.
  if(!WW.isWarm())S.f.coldExposure=(S.f.coldExposure||0)+n*(spray?.65:.3);
  if(S.f.wetTurns>=3&&!S.f.wetWarning){S.f.wetWarning=1;WW.think?.('My soaked clothes are making me shake. Stop the sprinkler, recover my flashlight and dry off at the laundry stove or a powered warm room.');}
 }else if(!openWindows&&!coldRoom)S.f.coldExposure=Math.max(0,(S.f.coldExposure||0)-n*(WW.isWarm()?2:.3));
 const exposure=S.f.coldExposure||0;
 S.f.shivering=exposure>=4;
 const activelyCold=openWindows||spray||coldRoom||(S.f.wet&&!WW.isWarm());
 if(activelyCold&&exposure>=4){
  const damage=n*(spray?1.2:openWindows?.9:.55)*S.m;
  S.hp=Math.max(0,S.hp-damage);S.san=Math.max(0,S.san-n*(spray?.45:.3));
  if(!S.f.exposureWarning){S.f.exposureWarning=1;WW.sceneWarning?.('The cold is hurting me. Find warmth.');soundEffect('hit');}
 }
 if(S.hp<=0)die();
};
WW.consumeFlashlight=function(n){
 if(!S||S.hp<=0||S.f.dead||WW.isSurvivalPaused())return;
 if(!WW.needsFlashlight()){if(S.lightOn){S.lightOn=false;WW.updateStatus?.();}return;}
 if(!S.lightOn||!has('Flashlight')||S.f.flashlightDropped)return;
 S.bat=Math.max(0,S.bat-Math.max(0,n));
 if(!S.bat){S.lightOn=false;WW.sceneWarning?.('The flashlight has run out of charge.');WW.think?.('The flashlight fades. I need a battery.','charge');renderScene();}
};
advanceTime=function(n=1){
 if(!S||S.hp<=0||S.f.dead||S.f.chapter1Complete||WW.isSurvivalPaused())return;
 n=Math.max(0,Number(n)||0);S.t+=n;
 WW.consumeFlashlight(n*(S.m<1?.38:S.m>1?1.1:.75));
 advancePowerOutage();WW.advanceExposure(n);if(S.hp<=0||S.f.dead)return;
 if(S.f.power&&!S.f.powerOut&&S.t-(S.f.lastBlackoutAt||S.t)>75&&(S.f.blackoutCount||0)<2&&!cm&&!S.f.pursuerEncounter&&!S.hallCombat&&rnd()<.09){S.f.powerOut=1;S.f.powerRestoreAt=S.t+6;S.f.powerRestoreReal=Date.now()+35000;S.f.blackoutCount=(S.f.blackoutCount||0)+1;soundEffect('relay');interaction('A relay trips. The overhead lights go out. The backup circuit is trying to reset.');}
 WW.enemies?.advance(n);
 if(S.pursuer?.active&&!S.hallCombat&&!S.f.hidingRoom&&!S.f.pursuerEncounter)pursuerApproach(S.room);
 wardTripTrap();
};
const arrival=chapterArrival;chapterArrival=function(from,to){if(S.hallCombat)WW.resolveHall?.('retreat');if(WW.isWarm()&&S.san<85&&S.t-(S.f.lastSafeComposure??-100)>40){S.san=Math.min(85,S.san+5);S.f.lastSafeComposure=S.t;}return arrival(from,to);};
const awaken=awakenPursuer;awakenPursuer=function(){if(!S.f.power||!S.f.photoPuzzleSolved||!S.f.plexiIncidentSeen||!S.f.researcherLastRoomSeen||Object.keys(S.vis).length<14)return false;return awaken();};
// Local exposure costs about one exploration turn per four seconds. Modal decisions
// pause it, giving the player time to read the warning and select the right control.
WW.survivalTick=function(){
 if(!S||!S.f.introComplete||S.hp<=0||S.f.dead||S.f.chapter1Complete||document.hidden||WW.isSurvivalPaused())return;
 if(S.f.powerOut&&Date.now()>=S.f.powerRestoreReal){advancePowerOutage();render();}
 if($('m').children.length||S.f.hidingRoom)return;
 WW.consumeFlashlight(S.m<1?.045:S.m>1?.16:.12);
 WW.advanceExposure(.25);
 $('interactiveScene')?.classList.toggle('winter-cold',!!S.f.shivering);
 WW.updateStatus?.();
};
setInterval(WW.survivalTick,1000);
})();
