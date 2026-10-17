/* Authored pilot-room geometry, in percentages of the uncropped 4:3 art plane.
   One fixture may hold related objects; no collision search or generic placement. */
(function(){
'use strict';
const fixture=(id,label,rect,ids,important=false)=>({id,label,rect,ids,important});
const rooms={
 lobby:{offscreen:['records','surgery'],doors:{security:[34.5,38,10,26],eastcorridor:[72.5,37.5,18,24]},fixtures:[
 fixture('reception','Reception desk',[69,54,16,8],['desk'],true),fixture('intercom','Intercom panel',[43,34,3,8],['int']),fixture('locker','Staff locker',[95,35,8,22],['lock','coat']),fixture('phone','Payphone',[50,35,4,10],['payphone'],true),fixture('cache','Field cache',[88,77,20,18],['box']),fixture('terminal','Continuity Terminal',[96,53,7,12],['term'],true),fixture('window','Rain-streaked entrance windows',[15,33,18,25],['win','sealedExit'])]},
 security:{doors:{lobby:[9,40,14,51],eastcorridor:[95,38,9,45]},fixtures:[
 fixture('monitors','Monitor wall',[39,35,24,21],['cam','rep2']),fixture('report','Incident report',[55,58,12,6],['rep']),fixture('drawer','Security desk drawer',[46,69,12,12],['drw'],true),fixture('roster','Duty roster',[57,31,10,15],['ros']),fixture('coffee','Cold coffee',[65,56,5,6],['cof']),fixture('cabinet','Equipment cabinet',[81,37,12,29],['rev','reva']),fixture('map','Floor plan rack',[68,38,9,12],['mapboard'],true),fixture('portraits','Staff portraits',[44,13,18,14],['staffPortraits']),fixture('journal','Night attendant journal',[72,63,15,6],['attendantDiary1']),fixture('phone','Disconnected telephone',[84.5,56,11,7],['@phone']),fixture('cache','Supply cache',[76,76,12,8],['@loot'])]},
 eastcorridor:{doors:{lobby:[9,48,12,67],ward:[49,44,9,23],security:[96,48,8,67]},fixtures:[
 fixture('light','Emergency lighting',[50,11,7,14],['fixture']),fixture('trolley','Broken trolley',[72,62,22,20],['trolley']),fixture('directory','Old wall directory',[23,32,7,25],['directory']),fixture('radio','Portable staff radio',[25,52,8,5],['radioHall'],true),fixture('window','Cracked ward window',[77,35,15,28],['windowBoard']),fixture('exit','Bolted fire exit',[34,44,5,36],['emergencyExit']),fixture('valve','Damaged sprinkler valve',[62,32,4,7],['staffSprinkler'])]},
 ward:{doors:{eastcorridor:[6,43,9,62],room12:[22,40,8,46],archive:[50,41,9,13],laundry:[60,42,4,20],pharmacy:[71,42,5,32],surgery:[84,43,10,49],isoward:[97,43,6,66]},fixtures:[
 fixture('names','Patient name boards',[33,33,6,17],['nb']),fixture('gurney','Overturned gurney',[37,63,21,14],['gur'],true),fixture('keypad','Pharmacy entry panel',[77,39,3,6],['kp'],true),fixture('trail','Drag marks',[77,78,12,7],['drg']),fixture('lockbox','Night nurse’s equipment box',[54,74,10,8],['nightPistol'],true),fixture('ammo','Ammunition envelope',[63,78,6,4],['pistolRounds']),fixture('journal','Night attendant journal',[32,83,10,6],['nightJournal']),fixture('cache','Supply cache',[88,84,8,7],['@loot'])]},
 room12:{doors:{ward:[7,36,12,48],residence:[96,36,8,52],children:[81,36,9,48]},fixtures:[
 fixture('file','Patient file',[35,57,7,12],['file'],true),fixture('restraints','Cut restraints',[48,53,13,8],['rs']),fixture('drawer','Bedside drawer',[69,57,8,8],['drw12'],true),fixture('cabinet','Medical cabinet',[65,28,15,21],['cab'],true),fixture('shelves','Supply shelves',[49,29,13,20],['shf','shf2']),fixture('tray','Instrument tray',[20,69,24,11],['tray12']),fixture('nailer','Broken pneumatic nailer',[13,61,20,6],['nailgun','nails'])]}
};
function matches(id,ids){return ids.includes(id)||(ids.includes('@phone')&&id.startsWith('phone_'))||(ids.includes('@loot')&&id.startsWith('seedloot_'));}
function groups(room){const conf=rooms[room];if(!conf)return null;const visible=availableRoomObjects(),used=new Set();const out=conf.fixtures.map(f=>{const objects=visible.filter(o=>matches(o[0],f.ids));objects.forEach(o=>used.add(o[0]));return {...f,kind:'desk',objects};}).filter(f=>f.objects.length);
 const missing=visible.filter(o=>!used.has(o[0]));if(missing.length)console.error('Unmapped room objects',room,missing.map(o=>o[0]));return out;}
window.WardRoomLayers={rooms,groups,revision:1};
})();
