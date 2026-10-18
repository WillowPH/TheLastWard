/* Carry management and practical thoughts. Progression items stay protected until their last use. */
(function(){
'use strict';
const WW=WardWinter,e=htmlSafe;
const accessItems=new Set(['Cabinet Key','Staff Access Card','Archive Key','Boiler Key','Bolt Cutters','Crank Handle','Maintenance Tools','Encrypted Drive']);
const resources=new Set(['Battery','Reinforced Battery','Ink Ribbon','Antiseptic','Wire Spool','Stabilizer Part','Wooden Plank']);
const keepsakes=new Set(['Silver Locket','Executive Photograph','Continuity Reel','Emergency Record Spool','Chapel Seal','Morgue Seal','Lab Seal','Boiler Seal']);
let pending=null,serial=0;
const usable=()=>!!(S&&S.hp>0&&!S.f.chapter1Complete&&!WW.orbit?.busy);
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
 return protect('Keep this equipment. It may still be needed. Use a field cache to store it safely.');
}
function actions(index){const slot=S.inv[index];if(!slot)return '';const p=policy(slot.n);return '<div class="inventory-discard-actions"><p class="inventory-discard-note">'+(p.spent?'<b>Spent item</b> · ':'')+e(p.reason)+'</p>'+(p.allowed?'<button type="button" class="btn" onclick="wardRequestDiscard('+index+')">Discard'+(slot.c>1?' stack':'')+'</button>':'<span class="inventory-protected" aria-label="Protected item">Keep</span>')+'</div>';}
window.wardInspectInventory=function(index){
 if(!usable())return;pending=null;const slot=S.inv[index];if(!slot)return;
 const n=slot.n,p=policy(n),uses=W[n]?'Equip':HEALS[n]?'Use':n==='Flashlight'?'Toggle flashlight':['Battery','Reinforced Battery'].includes(n)?'Recharge':Object.values(W).some(w=>w.ammo===n)?'Load compatible weapon':n==='Stabilizer Part'?'Upgrade equipped weapon':null;
 modal(e(n),'<div class="c1-item-examine">'+itemIconMarkup(n)+'<p>'+e(desc(n))+'</p>'+(slot.c>1?'<p>Quantity · '+slot.c+'</p>':'')+(n==='Lighter'?'<p>Fuel · '+WW.fuel()+' / 6 ignitions</p>':'')+'</div>'+(uses?'<button class="btn p" onclick="wardUseManagedItem('+index+')">'+e(uses)+'</button>':'')+(has('Lighter')&&has('Lighter Fluid')&&['Lighter','Lighter Fluid'].includes(n)?'<button class="btn p" onclick="wardCombineLighter();closeModal()">Combine lighter + fluid</button>':'')+actions(index)+'<button class="btn" onclick="invModal()">All carried items</button>');
};
window.wardUseManagedItem=function(index){if(!usable()||!S.inv[index])return;$('m').innerHTML='';useInventorySlot(index);};
window.wardRequestDiscard=function(index){
 if(!usable())return;const slot=S.inv[index];if(!slot)return;const p=policy(slot.n);
 if(!p.allowed){WW.think(p.reason);return;}
 pending={slot,index,room:S.room,token:++serial};
 modal('Discard '+e(slot.n)+'?', '<div class="c1-item-examine">'+itemIconMarkup(slot.n)+'<p>'+e(slot.n)+(slot.c>1?' × '+slot.c:'')+'</p></div><p>'+e(p.spent?'This item has no remaining use. Discard it to free one carry slot?':'Discard this whole stack to free one carry slot? You may want to store it in a field cache instead.')+'</p><p><b>This is permanent. It cannot be picked up again.</b></p><button class="btn" onclick="wardInspectInventory('+index+')">Keep item</button><button class="btn p" onclick="wardConfirmDiscard('+pending.token+')">Discard permanently</button>');
 pending.modal=document.querySelector('#m .md');
};
window.wardConfirmDiscard=function(token){
 const request=pending;pending=null;
 if(!usable()||!request||request.token!==token||request.modal!==document.querySelector('#m .md')||request.room!==S.room||S.inv[request.index]!==request.slot||!policy(request.slot.n).allowed)return;
 const slot=request.slot;S.inv.splice(request.index,1);S.discardedItems=S.discardedItems||[];S.discardedItems.push({n:slot.n,c:slot.c,room:S.room,time:S.t});S.discardedItems=S.discardedItems.slice(-100);
 lg('Discarded '+slot.n+(slot.c>1?' ×'+slot.c:'')+'.');soundEffect('pickup');$('m').innerHTML='';render();WW.think('I leave '+(slot.c>1?'the remaining ':'the ')+slot.n.toLowerCase()+' behind. There is space in my pack now.');invModal();
};
const baseInventory=invModal;
invModal=function(category='all'){
 pending=null;const result=baseInventory(category);if(!S)return result;
 const rows=S.inv.map((slot,index)=>({slot,index})).filter(({slot})=>category==='all'||itemCategory(slot.n)===category);
 document.querySelectorAll('#m .inventory-item-row').forEach((row,i)=>{const entry=rows[i];if(!entry)return;const controls=row.lastElementChild;const detail=document.createElement('button');detail.type='button';detail.className='btn';detail.textContent='Inspect / manage';detail.onclick=()=>wardInspectInventory(entry.index);controls.append(detail);const p=policy(entry.slot.n);if(p.spent){const label=document.createElement('small');label.className='inventory-spent-label';label.textContent='Spent · safe to discard';row.querySelector('.inventory-menu-copy').append(document.createElement('br'),label);}});
 return result;
};
const baseSlot=useInventorySlot;
useInventorySlot=function(index){const slot=S?.inv[index],result=baseSlot(index);if(!slot)return result;const body=document.querySelector('#m .mb');if(body&&document.querySelector('#m .c1-item-examine')&&!body.querySelector('.inventory-discard-actions'))body.insertAdjacentHTML('beforeend',actions(index));return result;};
function manageButton(){const heading=document.querySelector('.unified-inventory-panel .panel-heading');if(!heading||heading.querySelector('.inventory-manage-button'))return;const button=document.createElement('button');button.type='button';button.className='btn inventory-manage-button';button.textContent='Manage';button.setAttribute('aria-label','Manage carried items');button.onclick=()=>invModal();heading.append(button);}
const baseRender=render;render=function(){const result=baseRender();manageButton();return result;};manageButton();

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
 if(/^The (?:electronic lock has no power|charging cradle needs generator power|lift is still without power)/i.test(text))return 'power';
 if(/^A light-sensitive latch needs a developed photograph/i.test(text))return 'flag:photo';
 if(/^The lock is sealed\./i.test(text))return 'practical';
 if(/^The lighter is empty\./i.test(text))return 'fuel';
 if(/^This room is not warm enough\./i.test(text))return 'warm';
 if(/^The fuse fits, but the broken regulator/i.test(text))return 'flag:maintenancePrepared';
 if(/^The (?:containment elevator|elevator interlock|containment transfer is not authorized)/i.test(text)||/^Containment elevator locked/i.test(text))return 'elevator';
 if(/^The console needs power,/i.test(text))return 'flag:finalSecurityClearance';
 if(/^The (?:shotgun case is locked behind an electronic authorization|elevator terminal requires a Monolith executive authorization)/i.test(text))return 'flag:photoPuzzleSolved';
 if(/^The key hangs beyond the flooded working platform/i.test(text))return 'flag:drained';
 if(/^Find a Continuity Terminal before saving/i.test(text))return 'terminal';
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
WW.inventoryDiscard={policy,unfinishedUse};
const style=document.createElement('style');style.textContent='.inventory-discard-actions{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin:20px 0;padding:16px 0;border-top:1px solid var(--ln,#444);border-bottom:1px solid var(--ln,#444)}.inventory-discard-note{flex:1 1 200px;margin:0;line-height:1.5}.inventory-protected{font-size:12px;opacity:.7}.inventory-spent-label{color:var(--mu,#aaa)}.inventory-manage-button{margin-left:auto;padding:4px 8px!important;font-size:11px!important;min-height:26px}.unified-inventory-panel .panel-heading:has(.inventory-manage-button){display:flex;align-items:center;gap:8px}';document.head.append(style);
})();
