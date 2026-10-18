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
 'Heller’s winter maintenance note':`MARTIN HELLER — NIGHT MAINTENANCE\n14 NOVEMBER 1998\n\nThe automatic window linkage is still connected to the purge handle in the North Patient Corridor. Pulling it opens all three sashes. Shut EACH sash by its brass catch. The linkage will shear after one opening; do not try it for fun.\n\nThere is a petrol lighter in Security and lighter fluid on the same early staff route. Refill the lighter before you need it. The laundry drying stove has a prepared bed of old cotton. Light it, then stand back and warm your hands. Powered safe rooms will also dry you.\n\nThe lift motor uses generator power, but its transfer interlock has FOUR shaped fuse plugs. The duty electrician left them at Archives, Pharmacy, Records and Emergency Power Control. They are circuit keys, not spare flashlight batteries. All four belong in the elevator control board.\n\nThe generator is not running. Any light you see now is a battery-backed emergency fitting.`,
 'Window linkage warning':`BLACKRIDGE MAINTENANCE\n\nPURGE HANDLE — THREE WINDOW LINKAGES\n\nOpening the windows during the snowstorm will expose the whole corridor. The old linkage cannot pull them shut again. Close the three brass catches individually. Warm rooms are marked on the service plan.\n\nSomeone has written beneath it: The valve in East Corridor controls the sprinklers. It does NOT close these windows.`,
 'Laundry stove instructions':`M. HELLER\n\nThe drying stove is packed with discarded dry cotton. Use the petrol lighter to ignite it. Leave the flue open; the firebox is enclosed. You do not need to carry the cloth.\n\nSit beside the stove until your hands stop shaking. Do not waste fuel trying to warm yourself with the lighter alone.`,
 'Nursing personnel amendment':`MONOLITH PHARMACEUTICALS\nPERSONNEL AMENDMENT / INTERNAL ONLY\n\nEmployee name: ████████████████████\nAssignment: Nursing / lower clinical services\nPublic roster: REMOVED\n\nPersonal correspondence may use the nickname MIMI. Do not restore the legal name from carbon copies. All inquiries are to be forwarded below the public basement.\n\nHandwritten: She always remembered what each patient liked. I cannot understand why they took her off the ward.`,
 'Mimi’s unsigned note':`I put the clean dressings in the lower cabinet. Leave some for the night staff.\n\nThey keep changing my rota. Yesterday I was upstairs. Today the lift would not stop there. Nobody will tell me why my name is blacked out.\n\nIf you cannot find me, ask for Mimi.\n\nM.`,
 'Redacted treatment transfer':`MONOLITH / RESTRICTED CLINICAL TRANSFER\n\nName: ████████████████████\nFormer post: Nursing\nRecorded alias: MIMI\nDestination: Underground clinical research\n\nOccupational clearance withdrawn pending neurological observation. Experiment authorization and attending physician fields have been removed from this copy.\n\nThe lower staff are instructed to refer to her by nickname only.`,
 'Lower laboratory nursing addendum':`LULLABY / RESTRICTED ADDENDUM\n\nThe former nurse designated MIMI remains under Monolith observation. The public chart is not a reliable record of her condition.\n\nHer personal identity, treatment history and current assignment are held in the underground laboratory archive. Do not discuss them over the ward intercom.\n\nThe remainder of the page has been cut away.`,
 'A note beside the sandwich bag':`Tony,\n\nYour gabagool’s in the fridge.\n\n—Paulie\n\nSATRIALE’S PORK STORE\nNEW JERSEY`,
 'A postcard from a foggy town':`The lake disappeared into the fog this morning. The radio keeps hissing even when the batteries are out.\n\nI wish you were here.\n\nSILENT HILL`,
 'Chapel candle register':`The memorial inscription is difficult to read after the lamps fail. The three votive candles still have good wicks.\n\nThe photograph on the lower shelf is of the hospital's opening day. Someone wrote the dedication date on its reverse.`,
 'Opening day photograph':`BLACKRIDGE MEDICAL COMPLEX\nOPENING DAY\n\nOn the reverse, in the chaplain’s hand:\nThe dedication was held on {MEMORIAL_DATE}. Use the DAY, then the MONTH, in the old memorial lock.`,
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
register('pharmacy','returns','pharmacyBattery','Returned torch cell','A sealed replacement battery lies among the empty wrappers.',{give:[['Battery',1]]});
register('security','roster','mimiPersonnel','Redacted nursing roster','One name has been heavily blacked out.',{doc:'Nursing personnel amendment'});
register('room12','drawer','mimiNote','Unsigned nursing note','A folded personal note tucked beneath the drawer lining.',{doc:'Mimi’s unsigned note'});
register('archive','folder','mimiTransfer','Restricted nursing transfer','A clinical transfer form with its name field removed.',{doc:'Redacted treatment transfer'});
register('records','journal','mimiResearch','Cut laboratory addendum','The bottom half of a restricted nursing report has been cut away.',{doc:'Lower laboratory nursing addendum'});
register('archive','memo','componentNote','Elevator component transfer','A maintenance carbon copy lists four component locations.',{doc:'Archive component transfer'});
register('wardnorth','notice','windowWarning','Window linkage warning','A warning is pinned beside the emergency window controls.',{doc:'Window linkage warning'});
register('laundry','journal','stoveNote','Drying stove instructions','An oil-stained instruction sheet from Heller.',{doc:'Laundry stove instructions'});
W.fixture('laundry','stove','Laundry drying stove',[84,72,13,20],'rear',{art:'assets/props/drying_stove.svg'});
register('laundry','stove','dryingStove','Drying stove','The enclosed firebox holds dry discarded cotton. A petrol lighter can ignite it.',{act:'warmStove'});
W.fixture('wardnorth','windowLever','Window purge handle',[64,50,3,10],'rear',{art:'assets/props/window_lever.svg'});
register('wardnorth','windowLever','windowLever','Window purge handle','A mechanical handle links three window sashes. A warning explains the danger.',{act:'windowLever'});
for(let i=0;i<3;i++){
 W.fixture('wardnorth','coldWindow'+i,'Window '+(i+1)+' brass catch',[[18,35,11,28],[32,35,11,28],[77,35,11,28]][i],'rear',{windowIndex:i});
 register('wardnorth','coldWindow'+i,'coldWindow'+i,'Window '+(i+1)+' catch','A brass catch closes this window independently.',{act:'coldWindow',index:i});
}
register('lobby','window','lobbyShutters','Lobby window shutters','A rolling shutter handle controls the exterior glazing.',{act:'shutters'});
register('chapel','letter','chapelRegister','Candle register','A page explains the memorial candles.',{doc:'Chapel candle register'});
W.fixture('chapel','candles','Memorial candles',[15,43,9,12],'rear',{art:'assets/props/candles.svg'});
register('chapel','candles','chapelCandles','Three votive candles','The sheltered wicks can be lit with a filled lighter.',{act:'candles'});
register('chapel','candles','openingPhoto','Opening-day photograph','A photograph rests below the candle stand. Its reverse contains a date.',{act:'photoInspect'});
register('stafflounge','thermos','satriales','Satriale’s sandwich bag','An old paper sandwich bag sits beneath a familiar handwritten note.',{act:'egg',egg:'sopranos'});
register('children','rabbit','icecreamToy','Clown ice-cream truck','A battered toy ice-cream truck has a painted grinning clown.',{act:'egg',egg:'twisted'});
register('residence','diary','fogPostcard','Postcard from a foggy town','The lake on this postcard has almost disappeared into fog.',{doc:'A postcard from a foggy town'});
register('eastcorridor','radio','staticNote','Note beneath the radio','Someone has taped a warning beneath the receiver.',{doc:'A note on the discarded radio'});
register('stafflounge','note','herbMemo','Medicinal herb memo','A staff note describes green and red medicinal herbs. Nothing usable remains.',{look:1,th:'The author signed only R.P.D. Someone has underlined “do not mix the red ones alone.”'});
register('security','cabinet','umbrella','Red-and-white umbrella','An abandoned umbrella carries a red-and-white segmented emblem.',{look:1,th:'The supplier’s name has rubbed off. This was not a Monolith delivery.'});
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
desc=function(n){if(n==='Lighter')return 'Reusable petrol lighter. Combine with Lighter Fluid to refill; ignites the laundry drying stove and chapel candles.';if(n==='Lighter Fluid')return 'Refills the petrol lighter. Combine the two in Inventory.';if(W.fuses.includes(n))return 'One of four shaped plugs for the elevator interlock in Emergency Power Control. Reusable until installed.';return oldDesc(n);};
// Early objects stay on the accessible Security route. Later supplies use real containers.
W.fixture('stafflounge','television','Staff room television',[24,35,20,20],'rear',{art:'assets/props/crt.svg',television:true});
register('stafflounge','television','staffTV','Staff television','An old CRT television hisses with interference.',{look:1,th:'The antenna socket is empty. The static continues anyway.'});
const baselineObjects=Object.fromEntries(Object.entries(R).map(([r,v])=>[r,structuredClone(v.o)]));
const baselineScenes=structuredClone(WardScenes);
const configure=configureWorld;
configureWorld=function(seed,preserve=true){
 for(const [r,objects]of Object.entries(baselineObjects))R[r].o=structuredClone(objects);
 for(const [r,bp]of Object.entries(baselineScenes))WardScenes[r]=structuredClone(bp);
 configure(seed,preserve);
 S.placements=preserve&&S.placements?.seed===seed?S.placements:{seed,items:{}};
 const slots={
  drw:['security',['drawer','cabinet']],petrolLighter:['security',['cabinet','drawer']],lighterFluid:['security',['drawer','cabinet']],
  utilityKnife:['security',['cabinet','drawer']],cab:['room12',['cabinet','drawer']],drw12:['room12',['drawer','shelf']],
  elevatorFuseA:['archive',['fuse','drawer']],elevatorFuseB:['pharmacy',['ribbon','drawer']],
  elevatorFuseC:['records',['cabinet','ledger']],elevatorFuseD:['powercontrol',['parts','clearance']]
 };
 for(const [id,[room,choices]]of Object.entries(slots)){
  const target=S.placements.items[id]||choices[hashSeed(seed+'::slot::'+id)%choices.length];S.placements.items[id]=target;
  for(const f of WardScenes[room].fixtures){f.ids=f.ids.filter(x=>x!==id);f.collectibles=(f.collectibles||[]).filter(x=>x.id!==id);}
  const f=WardScenes[room].fixtures.find(f=>f.id===target);f.ids.push(id);f.drawer=true;
 }
 // Every pickup has a removable visual or a container interior; never an icon block.
 for(const [room,bp]of Object.entries(WardScenes))for(const f of bp.fixtures){
  const objects=R[room].o.filter(o=>f.ids.includes(o[0]));
  if(objects.some(o=>o[4].give)&&!/key|negative|plank/.test(f.id))f.drawer=true;
  if(f.drawer)f.collectibles=[];
 }
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
