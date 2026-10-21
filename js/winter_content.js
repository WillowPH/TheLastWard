/* Authored winter content. The seed selects authored slots, never room geometry. */
(function(){
'use strict';
const W=window.WardWinter={version:1};
W.asset=p=>window.WardEmbeddedAssets?.[p]||p;
W.completed=o=>S.ob[o[0]]==='done'||S.ob[o[0]]==='read';
W.find=id=>Object.values(R).flatMap(r=>r.o).find(o=>o[0]===id);
W.register=function(room,fixture,id,name,description,spec){
 R[room].o.push([id,name,'',description,spec]);
 const f=WardScenes[room].fixtures.find(f=>f.id===fixture);
 if(!f)throw Error('Missing authored fixture '+room+'/'+fixture);
 f.ids.push(id);
};
W.fixture=function(room,id,label,rect,view='front',extra={}){
 const f={id,label,rect,ids:[],view,...extra};WardScenes[room].fixtures.push(f);return f;
};
const documents={
 'Heller’s winter maintenance note':`MARTIN HELLER — NIGHT MAINTENANCE\n14 NOVEMBER 1998\n\nThe automatic window linkage is still connected to the purge handle in the North Patient Corridor. Pulling it opens all three sashes. Shut EACH sash by its brass catch. The linkage will shear after one opening. A seized linen-return flap is coupled to the same shaft; the purge releases its emergency supply compartment. Shut the windows before collecting the supplies.\n\nThere is a petrol lighter in Security and lighter fluid on the same early staff route. Refill the lighter before you need it. The laundry drying stove has a prepared bed of old cotton. Light it, then stand back and warm your hands. Powered safe rooms will also dry you.\n\nThe lift motor uses generator power, but its transfer interlock has FOUR shaped fuse plugs. The duty electrician left them at Archives, Pharmacy, Records and Emergency Power Control. They are circuit keys, not spare flashlight batteries. All four belong in the elevator control board.\n\nThe generator is not running. Any light you see now is a battery-backed emergency fitting.`,
 'Window linkage warning':`BLACKRIDGE MAINTENANCE\n\nPURGE HANDLE — THREE WINDOW LINKAGES\n\nThe purge shaft also releases the seized emergency linen-return compartment. Supplies are inside, but opening the windows during the snowstorm will expose the whole corridor. The old linkage cannot pull them shut again. Close the three brass catches individually before searching the trolley. Warm rooms are marked on the service plan.\n\nSomeone has written beneath it: The valve in East Corridor controls the sprinklers. It does NOT close these windows.`,
 'Laundry stove instructions':`M. HELLER\n\nThe drying stove is packed with discarded dry cotton. Use the petrol lighter to ignite it. Leave the flue open; the firebox is enclosed. You do not need to carry the cloth.\n\nSit beside the stove until your hands stop shaking. Do not waste fuel trying to warm yourself with the lighter alone.`,
 'Nursing personnel amendment':`MONOLITH PHARMACEUTICALS\nPERSONNEL AMENDMENT / INTERNAL ONLY\n\nEmployee name: ████████████████████\nAssignment: Nursing / lower clinical services\nPublic roster: REMOVED\n\nPersonal correspondence may use the nickname MIMI. Do not restore the legal name from carbon copies. All inquiries are to be forwarded below the public basement.\n\nHandwritten: She always remembered what each patient liked. I cannot understand why they took her off the ward.`,
 'Mimi’s unsigned note':`I put the clean dressings in the lower cabinet. Leave some for the night staff.\n\nThey keep changing my rota. Yesterday I was upstairs. Today the lift would not stop there. Nobody will tell me why my name is blacked out.\n\nIf you cannot find me, ask for Mimi.\n\nM.`,
 'Redacted treatment transfer':`MONOLITH / RESTRICTED CLINICAL TRANSFER\n\nName: ████████████████████\nFormer post: Nursing\nRecorded alias: MIMI\nDestination: Underground clinical research\n\nOccupational clearance withdrawn pending neurological observation. Experiment authorization and attending physician fields have been removed from this copy.\n\nThe lower staff are instructed to refer to her by nickname only.`,
 'Lower laboratory nursing addendum':`LULLABY / RESTRICTED ADDENDUM\n\nThe former nurse designated MIMI remains under Monolith observation. The public chart is not a reliable record of her condition.\n\nHer personal identity, treatment history and current assignment are held in the underground laboratory archive. Do not discuss them over the ward intercom.\n\nThe remainder of the page has been cut away.`,
 'A note beside the sandwich bag':`Tony,\n\nYour gabagool’s in the fridge.\n\n—Paulie\n\nSATRIALE’S PORK STORE\nNEW JERSEY`,
 'A postcard from a foggy town':`The lake disappeared into the fog this morning. The radio keeps hissing even when the batteries are out.\n\nI wish you were here.\n\nSILENT HILL`,
 'Chapel candle register':`The three votive candles still have good wicks. Heller left a lighter with the Security staff; there is enough dry cotton in the laundry stove to warm anyone who reaches it.\n\nThe photograph below the stand records the opening of Blackridge. Someone has kept it here all these years.`,
 'Opening day photograph':`BLACKRIDGE MEDICAL COMPLEX\nOPENING DAY\n\nOn the reverse, in the chaplain’s hand:\nDedication — {MEMORIAL_DATE}.\nFor everyone who came through these doors.`,
 'A note on the discarded radio':`The static starts before anyone comes through the door. I used to think it was the wiring.\n\nIt is not the wiring.`,
 'Archive component transfer':`ELEVATOR INTERLOCK COMPONENTS\n\nFour shaped fuse plugs were removed for isolation testing. One was left in Archives, one in Pharmacy, one in Records, and one in Emergency Power Control.\n\nThe generator powers the motor. These four plugs authorize the transfer circuit. They can be fitted only to the board outside the final elevator.`,
};
for(const [title,text]of Object.entries(documents))DOCS[title]=text;
const docBase=docText;
docText=function(title){return docBase(title).replaceAll('{MEMORIAL_DATE}',S?.puzzles?.memorialDate||'');};
const register=W.register;
register('security','diary','winterJournal','Heller’s folded winter note','A handwritten maintenance note beside the night journal.',{doc:'Heller’s winter maintenance note'});
register('security','cabinet','petrolLighter','Empty petrol lighter','A scratched brass lighter with an empty reservoir.',{give:[['Lighter',1]]});
register('security','drawer','lighterFluid','Lighter fluid tin','A small capped tin of petrol lighter fluid.',{give:[['Lighter Fluid',1]]});
register('security','cabinet','earlyBattery','Sealed flashlight cell','One sealed replacement battery remains behind the cabinet divider.',{give:[['Battery',1]]});
register('wardnorth','trolley','linenBattery','Battery in the linen trolley','A dry torch battery is tucked into the trolley pocket.',{give:[['Battery',1]]});
// Keep the collected-object ID for older saves; this reserve now supports saving.
register('pharmacy','returns','pharmacyBattery','Clerk’s unused record disk','A sealed blank disk was left in the pharmacy returns box.',{give:[['Floppy Disk',1]]});
register('security','roster','mimiPersonnel','Redacted nursing roster','One name has been heavily blacked out.',{doc:'Nursing personnel amendment'});
register('room12','drawer','mimiNote','Unsigned nursing note','A folded personal note tucked beneath the drawer lining.',{doc:'Mimi’s unsigned note'});
register('archive','folder','mimiTransfer','Restricted nursing transfer','A clinical transfer form with its name field removed.',{doc:'Redacted treatment transfer'});
register('records','journal','mimiResearch','Cut laboratory addendum','The bottom half of a restricted nursing report has been cut away.',{doc:'Lower laboratory nursing addendum'});
register('archive','memo','componentNote','Elevator component transfer','A maintenance carbon copy lists four component locations.',{doc:'Archive component transfer'});
register('wardnorth','notice','windowWarning','Window linkage warning','A warning is pinned beside the emergency window controls.',{doc:'Window linkage warning'});
register('laundry','journal','stoveNote','Drying stove instructions','An oil-stained instruction sheet from Heller.',{doc:'Laundry stove instructions'});
W.fixture('laundry','stove','Laundry drying stove',[84,72,13,20],'rear',{});
register('laundry','stove','dryingStove','Drying stove','The enclosed firebox holds dry discarded cotton. A petrol lighter can ignite it.',{act:'warmStove'});
W.fixture('wardnorth','windowLever','Window purge handle',[64,50,3,10],'rear',{art:'assets/props/window_lever.svg'});
register('wardnorth','windowLever','windowLever','Window purge handle','The purge shaft releases the seized linen-return supply compartment, but also opens three windows into the snowstorm.',{act:'windowLever'});
for(let i=0;i<3;i++){
 W.fixture('wardnorth','coldWindow'+i,'Window '+(i+1)+' brass catch',[[18,35,11,28],[32,35,11,28],[77,35,11,28]][i],'rear',{windowIndex:i});
 register('wardnorth','coldWindow'+i,'coldWindow'+i,'Window '+(i+1)+' catch','A brass catch closes this window independently.',{act:'coldWindow',index:i});
}
register('lobby','window','lobbyShutters','Upper window shutters','A rolling shutter handle closes the three clear upper panes. The lower windows remain barricaded.',{act:'shutters'});
register('chapel','letter','chapelRegister','Candle register','A page explains the memorial candles.',{doc:'Chapel candle register'});
W.fixture('chapel','candles','Memorial candles',[15,43,9,12],'rear',{art:'assets/props/candles.svg'});
register('chapel','candles','chapelCandles','Three votive candles','The sheltered wicks can be lit with a filled lighter.',{act:'candles'});
register('chapel','candles','openingPhoto','Opening-day photograph','A photograph rests below the candle stand. Its reverse contains a date.',{act:'photoInspect'});
register('stafflounge','thermos','satriales','Satriale’s sandwich bag','An old paper sandwich bag sits beneath a familiar handwritten note.',{act:'egg',egg:'sopranos'});
register('children','rabbit','icecreamToy','Clown ice-cream truck','A battered toy ice-cream truck has a painted grinning clown.',{act:'egg',egg:'twisted'});
register('residence','diary','fogPostcard','Postcard from a foggy town','The lake on this postcard has almost disappeared into fog.',{doc:'A postcard from a foggy town'});
register('eastcorridor','radio','staticNote','Note beneath the radio','Someone has taped a warning beneath the receiver.',{doc:'A note on the discarded radio'});
register('stafflounge','note','herbMemo','Medicinal herb memo','A staff note describes green and red medicinal herbs. Nothing usable remains.',{look:1,th:'The author signed only R.P.D. Someone has underlined “do not mix the red ones alone.”'});
register('security','cabinet','umbrella','Supplier insignia','A red-and-white segmented corporate badge is tucked inside a discarded supplier dossier on the rear staff table.',{look:1,th:'The supplier’s name has rubbed off. This was not a Monolith delivery.'});
W.fixture('powercontrol','markerGraffiti','Red wall graffiti',[28,35,12,24],'rear',{graffiti:true});
register('powercontrol','markerGraffiti','markerGraffiti','Red wall graffiti','MAKE US WHOLE is painted beside a twisted double-spire sketch.',{look:1,th:'Someone kept drawing the same shape until the paint ran out.'});
for(const [room,fixture,id,name]of [
 ['archive','fuse','elevatorFuseA','Rook Interlock Fuse'],
 ['pharmacy','ribbon','elevatorFuseB','Bishop Interlock Fuse'],
 ['records','cabinet','elevatorFuseC','Knight Interlock Fuse'],
 ['powercontrol','parts','elevatorFuseD','King Interlock Fuse']
])register(room,fixture,id,name,'A shaped ceramic fuse plug marked for the final elevator interlock.',{give:[[name,1]]});
ITEM_ART['Wooden Plank']='assets/items/wooden_plank.webp';
W.fuses=['Rook Interlock Fuse','Bishop Interlock Fuse','Knight Interlock Fuse','King Interlock Fuse'];
register('powercontrol','clearance','elevatorBoard','Elevator fuse interlock','Four different sockets stand beside the transfer console.',{act:'elevatorBoard'});
for(const [name,art]of Object.entries({Lighter:'lighter.png','Lighter Fluid':'lighter_fluid.png',...Object.fromEntries(W.fuses.map(n=>[n,'interlock_'+n.split(' ')[0].toLowerCase()+'.svg']))})){
 ITEM_ART[name]='assets/items/'+art;ICON[name]='';STK[name]=1;
}
const oldDesc=desc;
desc=function(n){if(n==='Lighter')return 'A petrol lighter. One measured fill provides two ignitions: the laundry drying stove and chapel candles.';if(n==='Lighter Fluid')return 'A measured refill for the lighter’s two ignition points. Combine the tin with the lighter.';if(W.fuses.includes(n))return 'One of four shaped plugs for the elevator interlock in Emergency Power Control. Reusable until installed.';return oldDesc(n);};
// Early objects stay on the accessible Security route. Later supplies use real containers.
W.fixture('stafflounge','television','Staff room television',[24,35,20,20],'rear',{art:'assets/props/crt.svg',television:true});
register('stafflounge','television','staffTV','Staff television','An old CRT television hisses with interference.',{look:1,th:'The antenna socket is empty. The static continues anyway.'});
const blockedExit=R.lobby.o.find(o=>o[0]==='sealedExit');if(blockedExit){blockedExit[1]='Barricaded main entrance';blockedExit[3]='A tipped filing cabinet and heavy waiting benches are wedged against the exterior entrance.';blockedExit[4].th='The furniture is jammed tight against the doors. The internal hospital passages are my only route.';}
// Presentation and equipment terminology are data, not labels pasted over legacy items.
ICON['Floppy Disk']='';STK['Floppy Disk']=3;ITEM_ART['Floppy Disk']='assets/items/floppy_disk.svg';
const equipmentName=text=>String(text).replace(/Continuity Terminal/gi,'Terminal').replace(/Ink Ribbons?/g,m=>m.endsWith('s')?'Floppy Disks':'Floppy Disk').replace(/Field cache/gi,'Storage box');
for(const [title,text]of Object.entries(DOCS))DOCS[title]=equipmentName(text);
DOCS['Evelyn Shaw’s handover']=`EVELYN SHAW — HANDOVER\n\nDaniel Mercer in Isolation Treatment was still conscious when the ward closed. He understood every word. Do not treat him like an empty bed.\n\nKessler kept accepting Graves’s instructions after the evacuation was cancelled. I am going to look for Marian. If I do not return, leave this with the night attendant.`;
DOCS['Judith Price’s medication record']=`JUDITH PRICE — DISPENSARY RECORD\n\n20:00 medication round suspended. The names on the charts no longer match the wristbands. I have locked the returned drugs away rather than administer an unverified dose.\n\nNo staff remain assigned to this dispensary. Do not follow an old rota into a closed ward.`;
DOCS['Chaplain Letter']=`I refused Blackwell’s request to bless the continuity trial. I can still leave clean dressings for whoever reaches this room.\n\nThe reliquary holds emergency aid. There is no staff rota left to keep; I will leave the candles and the opening-day photograph where anyone can find them.`;
DOCS['Staff Lounge Note']=DOCS['Staff Lounge Note'].replace('leave it with Evelyn Shaw','return it to her locker in Staff Residence');
for(const [room,id,fixture,title,name,description]of [
 ['stafflounge','shaw','note','Evelyn Shaw’s handover','Shaw’s abandoned handover','A nurse’s handwritten handover remains on the noticeboard. The lounge is empty.'],
 ['pharmacy','judith','ribbon','Judith Price’s medication record','Judith’s medication record','A signed medication record lies at the empty clerk’s desk.']
]){
 const object=R[room].o.find(o=>o[0]===id);object[0]=id==='shaw'?'shawHandover':'judithRecord';object.splice(1,4,name,'',description,{doc:title});
 WardScenes[room].fixtures=WardScenes[room].fixtures.filter(f=>f.id!==id);
 WardScenes[room].fixtures.find(f=>f.id===fixture).ids.push(object[0]);
}
const coat=R.lobby.o.find(o=>o[0]==='coat');coat[1]='Flashlight in the coat pocket';coat[3]='A scratched flashlight protrudes from the abandoned coat. I can take it, or leave it here.';coat[4]={give:[['Flashlight',1]]};
const plaque=R.archive.o.find(o=>o[0]==='cat');plaque[3]='A four-place brass lock marked “Dedication”. The year is crossed out on its small date plate.';
for(const [room,fixture,id]of [['stafflounge','harness','loungeStorage'],['pharmacy','returns','pharmacyStorage'],['records','cabinet','recordsStorage']]){
 register(room,fixture,id,'Storage box','An intact hospital storage compartment. Stored equipment can be retrieved at any storage box.',{act:'box'});
}
register('wardnorth','trolley','purgeSupplies','Emergency linen-return compartment','The purge shaft has released a sealed maintenance pouch. Close the windows before opening it.',{give:[['Handgun Ammo',8],['Battery',1]],after:'windowHazardResolved'});
W.chargerStatus=function(id){
 if(!['emergencyDynamo','handCharge','charger'].includes(id))return null;
 if(!S||!has('Flashlight'))return {available:false,label:'Battery charger · no flashlight',reason:S?.ob.coat==='done'?'Retrieve the flashlight from where you left it or from a Storage box before charging.':'Take the flashlight from the coat beside reception first.'};
 if(S.f.flashlightDropped)return {available:false,label:'Battery charger · flashlight dropped',reason:'Recover the flashlight from the East Corridor floor first.'};
 if(id==='charger'){
  if(!S.f.power||S.f.powerOut)return {available:false,label:'Battery charger · no power',reason:'The generator must be running.'};
  if((S.f.generatorChargeUses||0)>=2)return {available:false,label:'Battery charger · empty',reason:'Both reserve cells have been used.'};
  if(S.bat>=90)return {available:false,label:'Battery charger · charge sufficient',reason:'No recharge is needed.'};
 }else{
  if(S.bat>=12)return {available:false,label:'Emergency battery charger · reserve sufficient',reason:'This hand charger is only for a nearly empty flashlight.'};
  if(S.t-(S.f.lastDynamo??-100)<50)return {available:false,label:'Emergency battery charger · cooling',reason:'The charging handle must cool before another use.'};
 }
 return {available:true,label:id==='charger'?'Battery charger':'Emergency battery charger',reason:''};
};
W.objectAvailable=o=>W.chargerStatus(o[0])?.available!==false;
for(const [room,r]of Object.entries(R))for(const o of r.o){
 o[1]=equipmentName(o[1]);o[3]=equipmentName(o[3]);if(o[4].give)o[4].give=o[4].give.map(([name,count])=>[canonicalItem(name),count]);
 if(o[4].act==='save')o[1]='Terminal';if(o[4].act==='box')o[1]='Storage box';if(o[0]==='finalRibbon')o[1]='Emergency Floppy Disk';
 if(['emergencyDynamo','handCharge'].includes(o[0])){o[1]='Emergency battery charger';o[3]='A hand-powered charger for a nearly empty flashlight. Slow turns restore a small emergency reserve; the handle needs time to cool.';}
}
for(const bp of Object.values(WardScenes))for(const f of bp.fixtures){f.label=equipmentName(f.label);if(f.ids.some(id=>W.find(id)?.[4].act==='save'))f.label='Terminal';if(f.ids.length===1&&W.find(f.ids[0])?.[4].act==='box')f.label='Storage box';if(f.ids.some(id=>['emergencyDynamo','handCharge'].includes(id)))f.label='Emergency battery charger';}
const revisedDescription=desc;desc=function(name){if(canonicalItem(name)==='Floppy Disk')return 'One blank 3½-inch disk. Records your progress at a Terminal.';return revisedDescription(name);};
// Small, authored containers keep important equipment discoverable without a
// single cabinet becoming a shopping list. These all match painted furniture.
W.fixture('security','personalEffects','Personal effects cupboard',[82,56,14,13],'rear',{drawer:true});
W.fixture('security','winterNotice','Heller’s maintenance notice',[81,26,15,16],'rear',{});
W.fixture('records','researchBinder','Restricted research binder',[76,32,10,13],'rear',{});
W.fixture('residence','nightDesk','Night attendant’s desk',[80,45,9,5],'rear',{});
W.fixture('children','nightDrawer','Bedside supply drawer',[25,48,8,7],'rear',{drawer:true});
W.fixture('isolation','dressingShelf','Sealed dressing shelf',[4.5,51,7,10],'rear',{drawer:true});
W.fixture('coldstore','courierCrate','Insulated courier crate',[79,57,8,8],'rear',{drawer:true});
const relocate=(id,room,fixture)=>{
 let object;
 for(const r of Object.values(R)){const i=r.o.findIndex(o=>o[0]===id);if(i>=0)object=r.o.splice(i,1)[0];}
 if(!object)throw Error('Cannot relocate missing authored object '+id);
 for(const bp of Object.values(WardScenes))for(const f of bp.fixtures){f.ids=f.ids.filter(x=>x!==id);f.collectibles=(f.collectibles||[]).filter(p=>p.id!==id);}
 R[room].o.push(object);WardScenes[room].fixtures.find(f=>f.id===fixture).ids.push(id);
};
for(const [id,room,fixture]of [
 ['winterJournal','security','winterNotice'],['petrolLighter','security','personalEffects'],
 ['drw','security','personalEffects'],['lighterFluid','security','drawer'],
 ['earlyBattery','security','cache'],
 ['mimiResearch','records','researchBinder'],['attendantDiary3','residence','nightDesk']
])relocate(id,room,fixture);
W.find('attendantDiary3')[3]='The final loose page of the night attendant’s notebook, left on his quarters desk.';
W.find('earlyBattery')[3]='A sealed flashlight cell remains in the desk supply pouch.';
// Rear-facing furniture carries useful finds throughout the chapter. Moving the
// existing IDs preserves each run's pickup flags, resource totals and lock logic.
for(const [room,id,label,rect]of [
 ['lobby','returnStand','Cloakroom return counter',[7,55,12,18]],
 ['ward','rearMedicine','Rear medicine cupboard',[15,38,17,25]],
 ['laundry','rearShelf','Laundry supply shelves',[15,43,22,26]],
 ['generator','rearWorkbench','Maintenance charging bench',[92,53,14,18]],
 ['boiler','rearTrolley','Heatproof service trolley',[24,57,18,22]],
 ['morgue','rearTrolley','Mortuary work trolley',[17,57,21,15]],
 ['specimen','rearBench','Laboratory rear workbench',[87,48,21,14]],
 ['surgery','rearSupply','Theatre preparation drawer',[20,52,17,15]],
 ['stafflounge','rearTable','Staff recreation table',[11,70,18,13]],
 ['eastcorridor','rearTrolley','Rear linen and radio trolley',[90,66,18,44]],
 ['isoward','rearCabinet','Treatment chart cabinet',[19,30,18,26]],
 ['isoward','rearTrolley','Care equipment trolley',[21,55.5,23,25]],
 ['chapel','rearVestry','Chapel vestry cabinet',[10,49,16,11]]
])W.fixture(room,id,label,rect,'rear',{drawer:!['returnStand','rearWorkbench','rearTable'].includes(id)});
for(const [id,room,fixture]of [
 ['umbrella','stafflounge','rearTable'],['pistolRounds','ward','rearMedicine'],['gur','ward','rearMedicine'],
 ['pouch','laundry','rearShelf'],['attendantDiary2','laundry','rearShelf'],
 ['charger','generator','rearWorkbench'],['handCharge','generator','rearWorkbench'],
 ['fur','boiler','rearTrolley'],['aut','morgue','rearTrolley'],
 ['wire','specimen','rearBench'],['shotShells','surgery','rearSupply'],
 ['trolley','eastcorridor','rearTrolley'],['radioHall','eastcorridor','rearTrolley'],['staticNote','eastcorridor','rearTrolley'],
 ['patientFile','isoward','rearCabinet'],['patientTherapy','isoward','rearTrolley'],
 ['let','chapel','rearVestry'],['box3','chapel','rearVestry']
])relocate(id,room,fixture);
W.find('pistolRounds')[3]='A sealed ammunition sleeve is tucked inside the medicine cupboard behind the entry door.';
W.find('pouch')[3]='A compact belt-and-pouch kit is tucked inside the rear laundry supply shelves.';
W.find('charger')[3]='A battery charging cradle sits on the maintenance bench behind the generator.';
W.find('handCharge')[3]='A manual dynamo shares the rear charging bench. It can recover a nearly empty flashlight without mains power.';
W.find('fur')[1]='Heatproof service-part tin';W.find('fur')[3]='A heatproof tin on the boiler service trolley holds one usable precision part.';
W.find('aut')[3]='An autopsy report lies on the work trolley beside the mortuary sink.';
W.find('wire')[3]='A spool of dry insulated wire rests on the laboratory rear workbench.';
W.find('shotShells')[3]='A sealed shotgun shell sleeve remains in the theatre preparation drawer behind the operating table.';
register('stafflounge','rearTable','arcadeMedallion','Dragon tournament medallion','A brass dragon token rests on an old staff arcade-night flyer.',{look:1});
register('stafflounge','rearTable','heroMug','Heroes’ mug','A repaired ceramic mug bears a dark circular emblem and an orange arc.',{look:1});
W.find('umbrella')[3]='A red-and-white segmented corporate badge is tucked inside a discarded supplier dossier on the rear staff table.';
W.find('gur')[1]='Night-round record disk';W.find('gur')[3]='A sealed blank disk remains beside the patrol ammunition in the rear medicine cupboard.';
W.find('radioHall')[3]='A portable staff receiver sits on the rear linen trolley. A folded warning is tucked beneath it.';
W.find('staticNote')[3]='A warning is folded beneath the portable receiver on the rear linen trolley.';
W.find('patientFile')[3]='Daniel Mercer’s admission chart is filed in the glass-fronted cabinet behind the treatment bed.';
W.find('patientTherapy')[3]='A care trolley stands behind the treatment bed. Its clean equipment could support basic care, but no sedative remains.';
W.find('let')[3]='The chaplain’s folded letter is kept inside the vestry cabinet behind the pews.';
W.find('icecreamToy')[1]='Sweet Tooth ice-cream truck';W.find('icecreamToy')[3]='The battered toy carries a sculpted grinning clown head with flame-shaped hair.';
register('children','nightDrawer','childNightCell','Night-light battery','A sealed torch battery was set aside in the bedside drawer for night rounds.',{give:[['Battery',1]]});
register('isolation','dressingShelf','isolationDressing','Sealed isolation dressing','An unopened sterile dressing survived inside the glass-fronted cabinet.',{give:[['Trauma Dressing',1]]});
register('coldstore','courierCrate','courierCell','Courier’s spare battery','A spare torch cell is sealed in the insulated delivery crate beside the cold-room door.',{give:[['Battery',1]]});
// Progress-critical equipment and finite reserves also live behind the player.
// These are painted drawers/racks, not new icons laid over blank wall space.
for(const [room,id,label,rect]of [
 ['wardservice','rearTrolley','Ammunition service trolley',[90,55,16,27]],
 ['observation','rearDesk','Archive transfer drawer',[8,54,14,28]],
 ['archive','rearTransferCabinet','Component transfer cabinet',[26,44,11,30]],
 ['powercontrol','rearServiceRack','Transfer service rack',[82,45,15,42]]
])W.fixture(room,id,label,rect,'rear',{drawer:true});
relocate('dr','observation','rearDesk');
W.find('dr')[1]='Archive transfer drive';W.find('dr')[3]='The sealed archive drive is kept in the writing desk drawer behind the observation console.';
relocate('componentNote','archive','rearTransferCabinet');
relocate('pwrmemo','powercontrol','rearServiceRack');
register('wardservice','rearTrolley','serviceAmmo','Night patrol ammunition sleeve','An intact patrol sleeve is sealed in the rear service trolley beside the return door.',{give:[['Handgun Ammo',6]]});
register('records','cabinet','recordsAmmo','Records guard ammunition sleeve','A guard left a sealed ammunition sleeve in the rear filing cabinet.',{give:[['Handgun Ammo',8]]});
register('surgery','rearSupply','restrictedShotgun','Restricted surgical security shotgun','A pump shotgun remains inside the preparation drawer behind the theatre. The executive restriction has been released.',{give:[['Shotgun',1]],after:'photoPuzzleSolved'});
DOCS['Security ammunition issue log']='NIGHT SECURITY — AMMUNITION ISSUE\n\nPatrol pistol rounds were split between the Patient Wing medicine cupboard and the Ward Service trolley. Both are behind the entry doors, away from public view. Pharmacy keeps its own sealed reserve.\n\nThe North Corridor linen-return reserve is for emergencies; Heller warned that its release linkage also opens the windows. Do not pull it without reading the warning.\n\nThe theatre shotgun and shells are held together in the rear preparation drawer. Executive authorization releases that restriction. A late-shift guard signed a final sleeve into the Records filing cabinet.';
register('security','winterNotice','ammoIssueLog','Security ammunition issue log','A dated patrol issue sheet lists where the finite ammunition sleeves were distributed.',{doc:'Security ammunition issue log'});
WardScenes.records.fixtures.find(f=>f.id==='cabinet').label='Records security supply cabinet';
const beforeRestrictedTake=act;act=function(id){if(id==='restrictedShotgun'&&!S.f.photoPuzzleSolved)return W.think?.('The surgical security case is still under executive restriction.');return beforeRestrictedTake(id);};
// Chapter 1 only foreshadows Sister Mimi. Her real identity remains redacted;
// meeting her, the betrayal and the underground pursuit belong to Chapter 2.
DOCS['Nursing personnel amendment']=`MONOLITH PHARMACEUTICALS\nPERSONNEL AMENDMENT / INTERNAL ONLY\n\nLegal name: ████████████████████\nReligious title: SISTER\nRecorded name: SISTER MIMI\nAssignment: Hospital religious sister / ward medical duties\nPublic roster: REMOVED\n\nHer charitable order has not authorized this transfer. Do not restore the legal name from carbon copies. All inquiries are to be forwarded below the public basement.\n\nHandwritten: Sister Mimi sits with frightened patients until they sleep. She makes sure the night staff have clean dressings, even when supplies are short. Nobody has explained why she was transferred.`;
DOCS['Mimi’s unsigned note']=`I put the clean dressings in the lower cabinet. Leave some for the night staff.\n\nThey keep changing my rota. Yesterday I was upstairs. Today the lift would not stop there. Nobody will tell me why my name is blacked out.\n\nIf you cannot find me, ask for Sister Mimi. I still know how to take care of my patients.\n\nSister M.`;
DOCS['Redacted treatment transfer']=`MONOLITH / RESTRICTED CLINICAL TRANSFER\n\nLegal name: ████████████████████\nFormer post: Hospital religious sister / medical duties\nRecorded name: SISTER MIMI\nDestination: Underground clinical research\n\nThe sister’s medical clearance is withdrawn pending neurological observation. Infection markers and affective instability have been recorded after experimental treatment. Experiment authorization and attending physician fields have been removed from this copy.\n\nStaff are instructed to use her religious title and recorded name only.`;
DOCS['Lower laboratory nursing addendum']=`LULLABY / RESTRICTED ADDENDUM\n\nSister Mimi remains under Monolith observation following experimental treatment. Familiar voices briefly settle her, but her condition is unstable.\n\nHer personal identity, treatment history and current assignment are held in the underground laboratory archive. The charitable order’s inquiries have not been answered. Do not discuss her condition over the ward intercom.\n\nThe remainder of the page has been cut away.`;
W.find('mimiPersonnel')[1]='Redacted religious staff roster';W.find('mimiTransfer')[1]='Sister’s restricted transfer';W.find('mimiNote')[1]='Sister Mimi’s folded note';W.find('mimiResearch')[1]='Sister’s cut research addendum';
// Names follow the painted containers in the authored rear views.
for(const [room,id,label]of [['security','drawer','Security filing drawer'],['stafflounge','harness','Staff locker'],['pharmacy','returns','Returns box'],['pharmacy','ribbon','Clerk filing drawer'],['room12','drawer','Treatment cabinet drawer'],['archive','fuse','Equipment cabinet']])WardScenes[room].fixtures.find(f=>f.id===id).label=label;
R.stafflounge.o.find(o=>o[0]==='harness')[3]='A durable medical utility harness hangs inside the open staff locker.';
// A finite mid-route first-aid kit supports the longer authored encounter route.
register('stafflounge','harness','loungeFirstAid','Staff first-aid kit','A sealed first-aid kit remains in the rear staff locker beside the utility harness.',{give:[['Field Medkit',1]]});
// Recovery is spread across the route rather than bundled into the early locker.
relocate('loungeFirstAid','observation','rearDesk');
W.find('loungeFirstAid')[1]='Observation first-aid kit';W.find('loungeFirstAid')[3]='An unopened first-aid kit is sealed in the rear observation desk, beside the archive drive.';
register('ward','rearMedicine','clinicDressing','Night clinic dressing','A sealed dressing was kept with the night patrol equipment in the rear medicine cupboard.',{give:[['Trauma Dressing',1]]});
register('children','nightDrawer','childrenDressing','Pediatric night dressing','A small sealed dressing remains in the bedside night-round drawer.',{give:[['Trauma Dressing',1]]});
register('isolation','dressingShelf','isolationFirstAid','Isolation emergency kit','A sealed first-aid kit is stored behind the clean dressing shelf.',{give:[['Field Medkit',1]]});
register('lobby','returnStand','securityRecordDisks','Reception record disks','Unused blank disks remain on the cloakroom return counter behind reception, ready for a Terminal.',{give:[['Floppy Disk',1]]});
register('generator','rearWorkbench','generatorRecordDisks','Maintenance record disks','Unused blank disks are kept in the rear maintenance bench drawer beside the charging equipment.',{give:[['Floppy Disk',1]]});
register('residence','nightDesk','residenceRecordDisks','Night attendant’s blank disk','An unused blank disk lies inside the rear night attendant’s desk.',{give:[['Floppy Disk',1]]});
const baselineObjects=Object.fromEntries(Object.entries(R).map(([r,v])=>[r,structuredClone(v.o)]));
const baselineScenes=structuredClone(WardScenes);
const configure=configureWorld;
configureWorld=function(seed,preserve=true){
 for(const [r,objects]of Object.entries(baselineObjects))R[r].o=structuredClone(objects);
 for(const [r,bp]of Object.entries(baselineScenes))WardScenes[r]=structuredClone(bp);
 configure(seed,preserve);
 S.placements=preserve&&S.placements?.seed===seed?S.placements:{seed,items:{}};
 const slots={
  drw:['security',['personalEffects']],petrolLighter:['security',['personalEffects']],lighterFluid:['security',['drawer']],
  utilityKnife:['security',['cabinet']],cab:['room12',['cabinet','drawer']],drw12:['room12',['drawer','shelf']],
  elevatorFuseA:['archive',['fuse','rearTransferCabinet']],elevatorFuseB:['pharmacy',['ribbon','drawer']],
  elevatorFuseC:['records',['cabinet','ledger']],elevatorFuseD:['powercontrol',['rearServiceRack']]
 };
 for(const [id,[room,choices]]of Object.entries(slots)){
  const savedTarget=S.placements.items[id],target=choices.includes(savedTarget)?savedTarget:choices[hashSeed(seed+'::slot::'+id)%choices.length];S.placements.items[id]=target;
  for(const f of WardScenes[room].fixtures){f.ids=f.ids.filter(x=>x!==id);f.collectibles=(f.collectibles||[]).filter(x=>x.id!==id);}
  const f=WardScenes[room].fixtures.find(f=>f.id===target);f.ids.push(id);f.drawer=true;
 }
 // Every pickup has a removable visual or a container interior; never an icon block.
 for(const [room,bp]of Object.entries(WardScenes))for(const f of bp.fixtures){
  const objects=R[room].o.filter(o=>f.ids.includes(o[0]));
  if(objects.some(o=>o[4].give)&&!/key|negative|plank/.test(f.id))f.drawer=true;
  if(f.drawer)f.collectibles=[];
 }
 const coatFixture=WardScenes.lobby.fixtures.find(f=>f.id==='coat');coatFixture.drawer=false;coatFixture.label='Flashlight in the coat pocket';coatFixture.collectibles=[{id:'coat',asset:'assets/items/flashlight.png',rect:[97,39,2.8,5]}];
 for(const r of Object.values(R))for(const o of r.o){if(o[4].give)o[4].give=o[4].give.map(([name,count])=>[canonicalItem(name),count]);o[1]=equipmentName(o[1]);o[3]=equipmentName(o[3]);}
 S.inv=normalizeItems(S.inv);S.box=normalizeItems(S.box);
 for(const bp of Object.values(WardScenes))for(const f of bp.fixtures)f.label=f.label.replace(/Rain-streaked/gi,'Snow-covered');
 R.lobby.d='Snow drifts against the dark glass. Battery-backed emergency lamps pulse above abandoned reception. Black mould blooms around the vents; a dark drag trail ends beneath the desk.';
 for(const r of Object.values(R)){
  r.d=r.d.replace(/\brain\b/gi,m=>m[0]==='R'?'Snow':'snow');
  for(const o of r.o){o[1]=o[1].replace(/Rain-streaked/gi,'Snow-covered');o[3]=o[3].replace(/rain beats/gi,'snow blows').replace(/rain-streaked/gi,'snow-covered');}
 }
};
const previousRequirements=WardChapter.requirements;
WardChapter.requirements=function(){const missing=previousRequirements();if(!S.f.elevatorFusesInstalled)missing.push('install all four elevator interlock fuses in Emergency Power Control');return missing;};
const open=doorOpen;doorOpen=function(id){if(id==='liftEntry')return WardChapter.requirements().length===0;return open(id);};
const travel=go;go=function(to,confirmed=false){if(to==='lift'&&!S.f.elevatorFusesInstalled)return interaction('The elevator interlock needs four shaped fuse plugs. Heller’s winter note lists their service locations.');return travel(to,confirmed);};
const descent=beginDescent;beginDescent=function(){if(!S.f.elevatorFusesInstalled)return;return descent();};
const newRun=newGame;newGame=function(){newRun();S.winterVersion=1;S.lighterFuel=0;S.windows={triggered:false,closed:[true,true,true],resolved:false,exposure:0};S.f.lastBlackoutAt=S.t;S.f.nextHallucinationAt=S.t+90;S.batteryCapacity=100;S.bat=S.batteryCapacity;S.audio={amb:.65,fx:.8,ui:.45};render();};
})();
