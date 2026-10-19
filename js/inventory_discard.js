/* Carry management and practical thoughts. Progression items stay protected until their last use. */
(function(){
'use strict';
const WW=WardWinter,e=htmlSafe;
const accessItems=new Set(['Cabinet Key','Staff Access Card','Archive Key','Boiler Key','Bolt Cutters','Crank Handle','Maintenance Tools','Encrypted Drive']);
const resources=new Set(['Battery','Reinforced Battery','Floppy Disk','Ink Ribbon','Antiseptic','Wire Spool','Stabilizer Part','Wooden Plank']);
const keepsakes=new Set(['Silver Locket','Executive Photograph','Continuity Reel','Emergency Record Spool','Chapel Seal','Morgue Seal','Lab Seal','Boiler Seal']);
let pending=null,serial=0,selected=null,combineArmed=false;
const usable=()=>!!(S&&S.hp>0&&!S.f.dead&&!S.f.chapter1Complete&&!WW.orbit?.busy&&!WW.isPaused?.());
function unfinishedUse(name){
 for(const [id,d]of Object.entries(D))if(d.need===name&&!S.dr[id])return true;
 for(const r of Object.values(R))for(const o of r.o){const sp=o[4]||{};if(S.ob[o[0]]==='done'||S.ob[o[0]]==='read')continue;if(sp.need===name||sp.need3?.includes(name))return true;}
 return false;
}
function policy(name){
 if(!S)return {allowed:false,status:'Keep',reason:'No active investigation.'};
 name=canonicalItem(name);
 const protect=reason=>({allowed:false,status:'Keep',reason}),spent=reason=>({allowed:true,spent:true,status:'Spent',reason});
 if(name==='Flashlight')return protect('Keep the flashlight. Dark rooms and later blackouts still require it.');
 if(WW.fuses?.includes(name))return S.f.elevatorInserted?.includes(name)?spent('This interlock plug is already installed.'):protect('Keep this plug for the final elevator interlock.');
 if(name==='Power Fuse')return S.f.power?spent('The generator is already powered.'):protect('Keep the ceramic fuse until the generator is restored.');
 if(unfinishedUse(name))return protect('This item still opens a lock or completes an unfinished task.');
 if(name==='Maintenance Tools'&&!S.f.maintenancePrepared)return protect('The generator contacts still need these insulated tools.');
 if(name==='Encrypted Drive'&&!S.f.finalSecurityClearance)return protect('The archive drive is still needed for transfer authorization.');
 if(accessItems.has(name))return spent('All matching locks and tasks have been completed.');
 if(['Photographic Negative','Developing Fluid'].includes(name))return S.f.photo?spent('The photograph has already been developed.'):protect('Keep this until the hidden photograph has been developed.');
 if(name==='Developed Photograph')return S.f.photo&&S.vis.coldstore?spent('The photograph has revealed and opened its hidden route.'):protect('Keep the developed photograph until its hidden route has been used.');
 if(name==='Lighter')return S.f.stoveLit&&S.f.chapelCandles?spent('Both permanent ignition points are lit.'):protect('Keep the lighter for the laundry stove and chapel candles.');
 if(name==='Lighter Fluid'&&S.f.stoveLit&&S.f.chapelCandles)return spent('Both permanent ignition points are already lit.');
 if(name==='Wooden Plank'&&S.f.windowBarricaded)return spent('The service opening is already secured.');
 if(name==='Lighter Fluid'&&!S.lighterFuel&&!S.f.stoveLit&&!S.f.chapelCandles)return protect('Keep this first refill until the lighter has fuel.');
 if(name==='Lighter Fluid'||resources.has(name)||HEALS[name]||Object.values(W).some(w=>w.ammo===name))return {allowed:true,spent:false,status:'Supply',reason:'This supply can still be useful. Discarding it is permanent.'};
 if(keepsakes.has(name))return {allowed:true,spent:false,status:'Keepsake',reason:'This keepsake has no remaining lock or task in Chapter 1.'};
 return protect('Keep this equipment. It may still be needed. Use a storage box to store it safely.');
}
function actions(index){const slot=S.inv[index];if(!slot)return '';const p=policy(slot.n);return '<div class="inventory-discard-actions"><p class="inventory-discard-note">'+(p.spent?'<b>Spent item</b> · ':'')+e(p.reason)+'</p>'+(p.allowed?'<button type="button" class="btn" onclick="wardRequestDiscard('+index+')">Discard'+(slot.c>1?' stack':'')+'</button>':'<span class="inventory-protected" aria-label="Protected item">Keep</span>')+'</div>';}
window.wardInspectInventory=function(index){
 if(!usable())return;pending=null;const slot=S.inv[index];if(!slot)return;clearSelection();
 const n=slot.n,p=policy(n),uses=W[n]?'Equip':HEALS[n]?'Use':n==='Flashlight'?'Toggle flashlight':['Battery','Reinforced Battery'].includes(n)?'Recharge':Object.values(W).some(w=>w.ammo===n)?'Load compatible weapon':n==='Stabilizer Part'?'Upgrade equipped weapon':null;
 modal(e(n),'<div class="c1-item-examine">'+itemIconMarkup(n)+'<p>'+e(desc(n))+'</p>'+(slot.c>1?'<p>Quantity · '+slot.c+'</p>':'')+(n==='Lighter'?'<p>Fuel · '+WW.fuel()+' / 6 ignitions</p>':'')+'</div>'+(uses?'<button class="btn p" onclick="wardUseManagedItem('+index+')">'+e(uses)+'</button>':'')+(has('Lighter')&&has('Lighter Fluid')&&['Lighter','Lighter Fluid'].includes(n)?'<button class="btn p" onclick="wardCombineLighter();closeModal()">Combine lighter + fluid</button>':'')+actions(index)+'<button class="btn" onclick="invModal()">All carried items</button>');
};
window.wardUseManagedItem=function(index){if(!usable()||!S.inv[index])return;$('m').innerHTML='';useInventorySlot(index);};
window.wardRequestDiscard=function(index){
 if(!usable())return;const slot=S.inv[index];if(!slot)return;const p=policy(slot.n);
 if(!p.allowed){WW.think(p.reason);return;}
 clearSelection();
 pending={slot,index,room:S.room,token:++serial};
 modal('Discard '+e(slot.n)+'?', '<div class="c1-item-examine">'+itemIconMarkup(slot.n)+'<p>'+e(slot.n)+(slot.c>1?' × '+slot.c:'')+'</p></div><p>'+e(p.spent?'This item has no remaining use. Discard it to free one carry slot?':'Discard this whole stack to free one carry slot? You may want to store it in a storage box instead.')+'</p><p><b>This is permanent. It cannot be picked up again.</b></p><button class="btn" onclick="wardInspectInventory('+index+')">Keep item</button><button class="btn p" onclick="wardConfirmDiscard('+pending.token+')">Discard permanently</button>');
 pending.modal=document.querySelector('#m .md');
};
window.wardConfirmDiscard=function(token){
 const request=pending;pending=null;
 if(!usable()||!request||request.token!==token||request.modal!==document.querySelector('#m .md')||request.room!==S.room||S.inv[request.index]!==request.slot||!policy(request.slot.n).allowed)return;
 const slot=request.slot;S.inv.splice(request.index,1);S.discardedItems=S.discardedItems||[];S.discardedItems.push({n:slot.n,c:slot.c,room:S.room,time:S.t});S.discardedItems=S.discardedItems.slice(-100);
 selected=null;combineArmed=false;lg('Discarded '+slot.n+(slot.c>1?' ×'+slot.c:'')+'.');soundEffect('pickup');$('m').innerHTML='';render();WW.think('I leave '+(slot.c>1?'the remaining ':'the ')+slot.n.toLowerCase()+' behind. There is space in my pack now.');
};
const baseInventory=invModal;
invModal=function(category='all'){
 pending=null;const result=baseInventory(category);if(!S)return result;
 const rows=S.inv.map((slot,index)=>({slot,index})).filter(({slot})=>category==='all'||itemCategory(slot.n)===category);
 document.querySelectorAll('#m .inventory-item-row').forEach((row,i)=>{const entry=rows[i];if(!entry)return;const controls=row.lastElementChild;const detail=document.createElement('button');detail.type='button';detail.className='btn';detail.textContent='Inspect / manage';detail.onclick=()=>wardInspectInventory(entry.index);controls.append(detail);const p=policy(entry.slot.n);if(p.spent){const label=document.createElement('small');label.className='inventory-spent-label';label.textContent='Spent · safe to discard';row.querySelector('.inventory-menu-copy').append(document.createElement('br'),label);}});
 return result;
};
const baseSlot=useInventorySlot;
useInventorySlot=function(index){if(!usable())return;const slot=S?.inv[index],result=baseSlot(index);if(!slot)return result;const body=document.querySelector('#m .mb');if(body&&document.querySelector('#m .c1-item-examine')&&!body.querySelector('.inventory-discard-actions'))body.insertAdjacentHTML('beforeend',actions(index));return result;};
const baseBattery=useBat;
useBat=function(...args){if(!usable())return;if(!has('Flashlight'))return WW.think('I need to find the flashlight before installing a battery.','torch');return baseBattery(...args);};
const notificationStyle=document.createElement('style');notificationStyle.textContent='.ward-playing .tst{pointer-events:none!important}.ward-playing .inventory-cell .inv-meta:empty{display:none!important}';document.head.append(notificationStyle);

// The carry grid is an action surface. Combining never requires the inventory modal.
function selectionIndex(){if(!selected||selected.room!==S?.room)return -1;return S.inv.indexOf(selected.slot);}
function pairAction(a,b){
 if(!a||!b||a===b)return null;
 const recipe=RECIPES.find(r=>(r.a===a.n&&r.b===b.n)||(r.b===a.n&&r.a===b.n));
 if(recipe)return {kind:'recipe',recipe};
 if([a.n,b.n].includes('Lighter')&&[a.n,b.n].includes('Lighter Fluid'))return {kind:'lighter'};
 if([a.n,b.n].includes('Flashlight')){const battery=[a,b].find(slot=>['Battery','Reinforced Battery'].includes(slot.n));if(battery)return {kind:'battery',battery};}
 const weapon=W[a.n]?a:W[b.n]?b:null,other=weapon===a?b:a;
 if(weapon&&W[weapon.n].ammo===other.n)return {kind:'reload',weapon};
 if(weapon&&other.n==='Stabilizer Part')return {kind:'upgrade',weapon};
 return null;
}
function selectedUse(name){return W[name]?'Equip':HEALS[name]?'Use':name==='Flashlight'?'Toggle flashlight':['Battery','Reinforced Battery'].includes(name)?'Recharge':Object.values(W).some(w=>w.ammo===name)?'Load weapon':name==='Stabilizer Part'?'Upgrade weapon':null;}
function clearSelection(){selected=null;combineArmed=false;syncCarryActions();}
window.wardCancelInventorySelection=clearSelection;
window.wardSelectInventory=function(index){
 if(!usable())return;const slot=S.inv[index];if(!slot)return;
 const first=selectionIndex();
 if(combineArmed&&first>=0){if(first===index){combineArmed=false;return syncCarryActions();}return wardCombineInventory(first,index);}
 selected={slot,room:S.room};combineArmed=false;syncCarryActions();
};
window.wardBeginInventoryCombine=function(){
 if(!usable()||selectionIndex()<0)return;
 combineArmed=true;syncCarryActions();
};
window.wardUseSelectedInventory=function(){
 if(!usable())return;const index=selectionIndex();if(index<0)return;
 clearSelection();useInventorySlot(index);
 // Legacy upgrade/medical helpers can open the large inventory; direct actions return to the room.
 if(usable()&&document.querySelector('#m .inv-scroll'))$('m').innerHTML='';
};
window.wardCombineInventory=function(ai,bi){
 if(!usable()||!Number.isInteger(ai)||!Number.isInteger(bi)||ai===bi)return false;
 const a=S.inv[ai],b=S.inv[bi],action=pairAction(a,b);
 if(!action){WW.think('Those items do not fit together. Nothing has been used.');return false;}
 clearSelection();
 if(action.kind==='lighter'){wardCombineLighter();return true;}
 if(action.kind==='battery'){useBat(action.battery.n,false);return true;}
 if(action.kind==='reload'){S.eq=action.weapon.n;reload();return true;}
 if(action.kind==='upgrade'){S.eq=action.weapon.n;upgrade();if(usable()&&document.querySelector('#m .inv-scroll'))$('m').innerHTML='';return true;}
 const recipe=action.recipe,previous=S.inv.slice(),counts=previous.map(slot=>slot.c),inFight=!!(cm&&alive(S.room));
 for(const slot of [a,b]){slot.c--;if(!slot.c)S.inv.splice(S.inv.indexOf(slot),1);}
 if(!add(recipe.out,recipe.count)){previous.forEach((slot,i)=>slot.c=counts[i]);S.inv=previous;render();WW.think('There is no room for the finished item. I need a free carry slot.','space');return false;}
 if(recipe.out==='Developed Photograph'){S.f.photo=1;S.th2=S.th2||[];if(!S.docs.includes('Cold Storage Inventory'))S.th2.push('The photograph reveals a hidden route into Cold Storage. The image was taken before I arrived.');lg('Developed photograph: a hidden latch in the Records Annex responds to the image.');}
 else lg('Combined '+a.n+' and '+b.n+' into '+recipe.out+'.');
 soundEffect('combine');render();
 if(inFight){foe('You combine items while the threat closes in.');return true;}
 WW.think(recipe.out==='Reinforced Battery'?'The wire holds the cell contacts firmly. This reinforced battery gives the flashlight a longer charge.':'I put the '+recipe.out.toLowerCase()+' in my pack.');
 return true;
};
function syncCarryActions(){
 const host=$('inventorySlots');if(!host||!S)return;
 let index=selectionIndex();if(!usable()||index<0){selected=null;combineArmed=false;index=-1;}
 let panel=$('inventoryCarryActions');
 if(!panel){panel=document.createElement('section');panel.id='inventoryCarryActions';panel.className='inventory-carry-actions';panel.setAttribute('aria-live','polite');panel.setAttribute('aria-label','Selected item actions');document.body.append(panel);}
 for(const [i,cell]of [...host.querySelectorAll('.inventory-cell.filled')].entries()){
  const slot=S.inv[i];cell.dataset.inventoryIndex=String(i);cell.onclick=()=>wardSelectInventory(i);cell.setAttribute('aria-label',(combineArmed?'Combine with ':'Select ')+slot.n+(slot.c>1?' × '+slot.c:''));cell.setAttribute('aria-pressed',String(i===index));cell.classList.toggle('inventory-selected',i===index);cell.classList.toggle('combine-compatible',combineArmed&&!!pairAction(selected?.slot,slot));cell.title=combineArmed?'Combine with '+slot.n:'Select '+slot.n;
  const quantity=document.createElement('span');quantity.className='inventory-quantity-badge';quantity.setAttribute('aria-hidden','true');
  const ammo=Object.values(W).some(w=>w.ammo===slot.n),weapon=W[slot.n];
  quantity.textContent=weapon?String(S.ld[slot.n]||0)+' / '+cnt(weapon.ammo):ammo?String(slot.c):slot.c>1?'×'+slot.c:'';
  quantity.title=weapon?'Loaded / reserve rounds':ammo?'Rounds in this stack':'Quantity';
  cell.querySelector('.inventory-quantity-badge')?.remove();cell.append(quantity);
  const meta=cell.querySelector('.inv-meta');if(meta)meta.textContent=weapon?(S.eq===slot.n?'Equipped':''):'';
 }
 panel.hidden=index<0;if(index<0){panel.innerHTML='';return;}
 const slot=S.inv[index],p=policy(slot.n),use=selectedUse(slot.n);
 const compatible=S.inv.some(other=>!!pairAction(slot,other));
 panel.innerHTML='<div class="carry-selection-heading"><strong>'+e(slot.n)+(slot.c>1?' × '+slot.c:'')+'</strong><button type="button" class="carry-selection-close" onclick="wardCancelInventorySelection()" aria-label="Cancel item selection">×</button></div>'+(combineArmed?'<p>Select a highlighted item in your pack.</p><button type="button" class="btn" onclick="wardCancelInventorySelection()">Cancel combine</button>':'<p>'+e(p.spent?'Spent · all matching tasks are complete.':desc(slot.n))+'</p><div class="carry-selection-buttons">'+(use?'<button type="button" class="btn" onclick="wardUseSelectedInventory()">'+e(use)+'</button>':'')+'<button type="button" class="btn" '+(!compatible?'disabled title="No compatible ingredient is carried"':'')+' onclick="wardBeginInventoryCombine()">Combine</button><button type="button" class="btn" onclick="wardInspectInventory('+index+')">Inspect</button>'+(p.allowed?'<button type="button" class="btn" onclick="wardRequestDiscard('+index+')">Discard</button>':'')+'</div>');
 positionCarryActions();
}
function positionCarryActions(){
 const panel=$('inventoryCarryActions'),index=selectionIndex();if(!panel||panel.hidden||index<0)return;
 const cell=document.querySelector('[data-inventory-index="'+index+'"]');if(!cell)return;
 const r=cell.getBoundingClientRect(),width=Math.min(256,innerWidth-20);panel.style.width=width+'px';
 const height=panel.getBoundingClientRect().height,grid=$('inventorySlots').getBoundingClientRect();
 const narrow=innerWidth<=650;
 let left=narrow?grid.left:grid.left-width-12,top=narrow?grid.top-height-10:r.top;
 if(left<10)left=r.right+12;
 if(left+width>innerWidth-10)left=innerWidth-width-10;
 panel.style.left=Math.max(10,left)+'px';panel.style.top=Math.max(10,Math.min(innerHeight-height-10,top))+'px';
}
window.addEventListener('resize',positionCarryActions);
document.addEventListener('scroll',positionCarryActions,true);
document.addEventListener('click',event=>{if(!selected||event.target.closest?.('#inventoryCarryActions,#inventorySlots,#m'))return;clearSelection();},true);
const baseCarry=renderUnifiedInventory;renderUnifiedInventory=function(){const result=baseCarry();syncCarryActions();return result;};
WW.inventoryDirect={pairAction,selection:()=>({index:selectionIndex(),combining:combineArmed}),sync:syncCarryActions};
function manageButton(){const heading=document.querySelector('.unified-inventory-panel .panel-heading');if(!heading||heading.querySelector('.inventory-manage-button'))return;const button=document.createElement('button');button.type='button';button.className='btn inventory-manage-button';button.textContent='Manage';button.setAttribute('aria-label','Manage carried items');button.onclick=()=>invModal();heading.append(button);}
const autoSpent=new Set([...accessItems,'Power Fuse','Photographic Negative','Developing Fluid','Developed Photograph']);
function discardSpent(){
 if(!usable()||S.m>1)return [];
 const discarded=S.inv.filter(slot=>autoSpent.has(slot.n)&&policy(slot.n).spent);
 if(!discarded.length)return [];
 S.inv=S.inv.filter(slot=>!discarded.includes(slot));
 S.discardedItems=S.discardedItems||[];
 for(const slot of discarded){S.discardedItems.push({n:slot.n,c:slot.c,room:S.room,time:S.t,automatic:true});lg('No further use: '+slot.n+' removed from pack.');}
 S.discardedItems=S.discardedItems.slice(-100);
 if(selected&&discarded.includes(selected.slot)){selected=null;combineArmed=false;}
 return discarded;
}
const baseRender=render;render=function(){discardSpent();const result=baseRender();manageButton();return result;};manageButton();

// Practical observations belong in the existing thought card. The room and its targets stay available.
WW.think=function(text,requirement=null){if(!S)return;S.contextThought={room:S.room,text:String(text||''),requirement};renderSceneThought();};
const baseThought=renderSceneThought;
function thoughtResolved(thought){
 const requirement=thought.requirement;
 if(thought.room!==S.room)return true;
 if(!requirement)return false;
 if(requirement.startsWith('item:'))return has(requirement.slice(5));
 if(requirement.startsWith('flag:'))return !!S.f[requirement.slice(5)];
 switch(requirement){
  case 'light':return lit();
  case 'charge':return S.bat>0;
  case 'recover':return !S.f.flashlightDropped;
  case 'torch':return has('Flashlight');
  case 'power':return !!(S.f.power&&!S.f.powerOut);
  case 'concealed':return !S.f.hidingRoom;
  case 'fuel':return WW.fuel()>0;
  case 'warm':return WW.isWarm();
  case 'dry':return !S.f.wet&&!S.f.shivering;
  case 'space':return S.inv.length<carryLimit();
  case 'equip':return !!(W[S.eq]&&has(S.eq));
  case 'terminal':return R[S.room].o.some(o=>o[4].act==='save');
  case 'cache':return !!R[S.room].safe;
  case 'elevator':return WardChapter.requirements().length===0;
  default:return false;
 }
}
renderSceneThought=function(){
 baseThought();if(!S)return;const thought=S.contextThought;if(!thought)return;
 if(thoughtResolved(thought)){delete S.contextThought;return;}
 const node=$('sceneThoughtText');if(node)node.textContent=thought.text;$('sceneThought')?.classList.remove('hid');
};
function lightHint(value){const text=String(value||'');
 if(/keep the flashlight off while concealed/i.test(text))return 'concealed';
 if(/(?:need|require|switch|turn).*(?:flashlight|working lights).*examine|(?:not enough light|too dark|in the darkness).*(?:inspect|search|examine)|need the flashlight to examine/i.test(text))return 'light';
 if(/flashlight (?:fades|dies)|(?:no charge|find a battery|need a battery)/i.test(text))return 'charge';
 if(/flashlight (?:lies|is still) (?:under|on)|retrieve it before I can switch/i.test(text))return 'recover';
 if(/(?:bring|retrieve|need to find|needs).*(?:flashlight)|flashlight is in storage/i.test(text))return !has('Flashlight')?'torch':/generator power/i.test(text)?'power':null;
 return null;
}
function practicalHint(value){
 if(!S)return null;const text=String(value||''),light=lightHint(text);if(light)return light;
 const locked=text.match(/^Locked\. It needs: (.+)\.$/);if(locked)return 'item:'+canonicalItem(locked[1]);
 if(/^(?:Inventory full|Not enough inventory space|No room for the combined item)/i.test(text))return 'space';
 if(/^The (?:electronic lock has no power|charging cradle needs generator power|battery charger needs generator power|generator must be running|lift is still without power)/i.test(text))return 'power';
 if(/^A light-sensitive latch needs a developed photograph/i.test(text))return 'flag:photo';
 if(/^The lock is sealed\./i.test(text))return 'practical';
 if(/^The lighter is empty\./i.test(text))return 'fuel';
 if(/^This room is not warm enough\./i.test(text))return 'warm';
 if(/^The fuse fits, but the broken regulator/i.test(text))return 'flag:maintenancePrepared';
 if(/^The (?:containment elevator|elevator interlock|containment transfer is not authorized)/i.test(text)||/^Containment elevator locked/i.test(text))return 'elevator';
 if(/^The console needs power,/i.test(text))return 'flag:finalSecurityClearance';
 if(/^The (?:shotgun case is locked behind an electronic authorization|elevator terminal requires a Monolith executive authorization)/i.test(text))return 'flag:photoPuzzleSolved';
 if(/^The key hangs beyond the flooded working platform/i.test(text))return 'flag:drained';
 if(/^Find (?:a Continuity Terminal|a Terminal|a terminal) before saving/i.test(text))return 'terminal';
 if(/^No storage box in this room/i.test(text))return 'cache';
 if(/^You need to equip a firearm first/i.test(text))return 'equip';
 if(/^I need clean dressings/i.test(text))return 'item:Trauma Dressing';
 // Match actual item names only in short prerequisite advice, never in a story paragraph.
 if(text.length<280&&/\bneed(?:s)?\b|\brequire(?:s)?\b/i.test(text)){
  const name=Object.keys(ITEM_ART).sort((a,b)=>b.length-a.length).find(n=>text.toLowerCase().includes(n.toLowerCase())&&!has(n));
  if(name)return 'item:'+name;
 }
 if(/^(?:I need (?:the|a|an) |One substantial wooden plank would secure|The dynamo needs to cool before|The cradle’s two spare cells are exhausted)/i.test(text))return 'practical';
 return null;
}
const baseInteraction=interaction;interaction=function(value){const requirement=practicalHint(value);if(requirement){WW.think(value,requirement);return;}if(S?.contextThought&&(!S.contextThought.requirement||S.contextThought.requirement==='practical')){delete S.contextThought;renderSceneThought();}return baseInteraction(value);};
const baseToast=toast;toast=function(value){const requirement=practicalHint(value);if(requirement){WW.think(value,requirement);return;}return baseToast(value);};
const baseMessage=msg;msg=function(value,good){const requirement=good?null:practicalHint(value);if(requirement){S.msg=null;WW.think(value,requirement);return;}return baseMessage(value,good);};
WW.inventoryDiscard={policy,unfinishedUse,discardSpent};
const baseAdd=add;add=function(name,count=1,inventory=S?.inv,limit=null){
 const carried=inventory===S?.inv,had=carried?cnt('Wire Spool'):0,result=baseAdd(name,count,inventory,limit);
 if(result&&carried&&canonicalItem(name)==='Wire Spool'&&!had&&!S.f.wireCombineExplained){
  const run=S;S.f.wireCombineExplained=1;queueMicrotask(()=>{if(S===run&&usable()&&has('Wire Spool'))WW.think('This wire can reinforce a flashlight battery. Select it in my pack, choose Combine, then select a battery.');});
 }
 return result;
};
const carryStyle=document.createElement('style');carryStyle.textContent='.inventory-carry-actions{position:fixed;box-sizing:border-box;max-width:calc(100vw - 20px);margin:0;padding:11px;border:1px solid #716c61;border-radius:4px;background:#141313fa;color:#e2dcd2;font:12px/1.45 Roboto,Arial,sans-serif;z-index:130;box-shadow:0 8px 28px #000b;overflow:visible}.inventory-carry-actions[hidden]{display:none!important}.carry-selection-heading{display:flex;align-items:flex-start;gap:8px}.carry-selection-heading strong{font-weight:400;font-size:13px;overflow-wrap:anywhere;flex:1;min-width:0}.carry-selection-close{border:0;background:transparent;color:#bdb5a7;cursor:pointer;font-size:20px;line-height:1;padding:0 2px}.inventory-carry-actions p{margin:7px 0;color:#c0b9ac;overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.carry-selection-buttons{display:grid;grid-template-columns:1fr 1fr;gap:5px}.inventory-carry-actions .btn{min-height:31px!important;padding:5px 8px!important;font-size:11px!important;letter-spacing:0!important;margin:0!important}.inventory-carry-actions .btn:disabled{opacity:.4;cursor:default}.ward-playing .right-rail .inventory-cell.inventory-selected{border-color:#d6ba81!important;box-shadow:inset 0 0 0 1px #d6ba81!important;background:#a995651a!important}.ward-playing .right-rail .inventory-cell.combine-compatible{border-color:#c6b58b!important;background:#bca27422!important}.ward-playing .right-rail .inventory-cell.combine-compatible:after{content:"+";position:absolute;right:4px;top:1px;color:#dfcfaa;font-size:16px}.inventory-carry-actions .item-art{display:none}.inventory-quantity-badge{position:absolute;right:4px;bottom:3px;border-radius:2px;background:#111e;padding:1px 4px;font:600 12px/1.25 Roboto,Arial,sans-serif;color:#f1e7d3;pointer-events:none}.inventory-quantity-badge:empty{display:none}.ward-playing .right-rail .inventory-cell .inv-meta{right:auto!important;left:4px!important;font-size:9px!important;bottom:3px!important}.ward-playing .right-rail .inventory-cell:has(.inventory-quantity-badge:not(:empty)) .inv-meta{bottom:20px!important}@media(max-width:650px){.inventory-carry-actions p{font-size:11px}.inventory-quantity-badge{font-size:10px;padding:1px 3px;right:2px;bottom:2px}}';document.head.append(carryStyle);
const style=document.createElement('style');style.textContent='.inventory-discard-actions{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin:20px 0;padding:16px 0;border-top:1px solid var(--ln,#444);border-bottom:1px solid var(--ln,#444)}.inventory-discard-note{flex:1 1 200px;margin:0;line-height:1.5}.inventory-protected{font-size:12px;opacity:.7}.inventory-spent-label{color:var(--mu,#aaa)}.inventory-manage-button{margin-left:auto;padding:4px 8px!important;font-size:11px!important;min-height:26px}.unified-inventory-panel .panel-heading:has(.inventory-manage-button){display:flex;align-items:center;gap:8px}';document.head.append(style);
})();
