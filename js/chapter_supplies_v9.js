/* Deliberate finite reserves. Difficulty changes supply packages, never geometry. */
(function(){
'use strict';
const WW=WardWinter;
const plans={
 story:{cells:['earlyBattery','drw12','childNightCell','courierCell'],disks:{securityRecordDisks:2,gur:1,pharmacyBattery:1,generatorRecordDisks:2,residenceRecordDisks:1,finalRibbon:1},medical:['clinicDressing','childrenDressing','isolationFirstAid']},
 normal:{cells:['earlyBattery','drw12','courierCell'],disks:{securityRecordDisks:1,gur:1,pharmacyBattery:1,generatorRecordDisks:1,residenceRecordDisks:1,finalRibbon:1},medical:['clinicDressing']},
 nightmare:{cells:['earlyBattery','drw12'],disks:{securityRecordDisks:1,gur:1,pharmacyBattery:0,generatorRecordDisks:1,residenceRecordDisks:0,finalRibbon:1},medical:[]}
};
const cellIds=['earlyBattery','drw12','linenBattery','childNightCell','courierCell'];
const extraMedical=['clinicDressing','childrenDressing','isolationFirstAid'];
const diskLocations={securityRecordDisks:'the cloakroom return counter behind reception',gur:'the Patient Wing medicine cupboard behind the entry door',pharmacyBattery:'the Pharmacy returns box behind the clerk’s desk',generatorRecordDisks:'the maintenance bench behind the generator',residenceRecordDisks:'the rear desk in Staff Residence',finalRibbon:'the final elevator Terminal'};
const mode=()=>S.m<1?'story':S.m>1?'nightmare':'normal';
function remove(id){
 for(const r of Object.values(R))r.o=r.o.filter(o=>o[0]!==id);
 for(const scene of Object.values(WardScenes))for(const f of scene.fixtures){f.ids=f.ids.filter(v=>v!==id);f.collectibles=(f.collectibles||[]).filter(v=>v.id!==id);}
}
function apply(){
 if(!S)return;
 const plan=plans[mode()];
 for(const id of cellIds)if(!plan.cells.includes(id))remove(id);
 for(const id of extraMedical)if(!plan.medical.includes(id))remove(id);
 for(const [id,count]of Object.entries(plan.disks)){
  const o=WW.find(id);if(!o)continue;
  if(!count){remove(id);continue;}
  o[4].give=[['Floppy Disk',count]];
  o[3]=(count===1?'One sealed blank disk remains.':'Two sealed blank disks remain.')+' Each records one save at a Terminal; the disk is used only if the save succeeds.';
 }
 const purge=WW.find('purgeSupplies');
 if(purge){purge[4].give=purge[4].give.filter(([name])=>name!=='Battery');purge[3]='The released linen-return compartment holds one sealed patrol ammunition sleeve. Close the windows before opening it.';}
 // Seeded ammunition sleeves remain as before. Cells, medical aid and save
 // disks are guaranteed authored reserves rather than an extra random jackpot.
 for(const o of Object.values(R).flatMap(r=>r.o))if(/^seedloot_/.test(o[0])&&!(o[4].give||[]).some(([name])=>/Ammo|Shells|Rounds/.test(name)))remove(o[0]);
 const charger=WW.find('charger');if(charger)charger[3]='The rear maintenance charging cradle contains one 65% reserve cell. Once used, only its slow emergency hand dynamo remains available.';
 S.supplyVersion=9;
}
const configure=configureWorld;
configureWorld=function(...args){const result=configure.apply(this,args);apply();return result;};

const chargerStatus=WW.chargerStatus;
WW.chargerStatus=function(id){
 if(id==='charger'&&S&&(S.f.generatorChargeUses||0)>=1)return {available:false,label:'Battery charger · empty',reason:'The cradle’s reserve cell has been used. Find a spare cell or use the emergency hand dynamo only when nearly empty.'};
 return chargerStatus(id);
};
rechargeAtGenerator=function(){
 if(!WW.canAct?.()||WW.isPaused?.())return false;
 if(S.room!=='generator')return WW.think?.('The charging cradle is on the rear generator maintenance bench.');
 const status=WW.chargerStatus('charger');if(!status.available)return interaction(status.reason);
 S.f.generatorChargeUses=(S.f.generatorChargeUses||0)+1;
 S.bat=Math.min(100,S.bat+65);advanceTime(2);soundEffect('relay');
 interaction('The cradle’s single reserve cell restores 65% flashlight charge. Its supply is now empty. The hand dynamo remains an emergency fallback.');
 render();return true;
};
const save=saveGame;
saveGame=function(...args){
 if(WW.canAct?.()&&!has('Floppy Disk')&&R[S.room].o.some(o=>o[4].act==='save')){
  const next=Object.keys(diskLocations).find(id=>WW.find(id)&&S.ob[id]!=='done');
  const stored=(S.box||[]).some(slot=>slot.n==='Floppy Disk'&&slot.c>0);
  WW.think?.(stored?'I have blank Floppy Disks in storage. I can retrieve one at a Storage box before using this Terminal.':next?'This Terminal needs a blank Floppy Disk. There may still be unused disks on '+diskLocations[next]+'.':'I need a blank Floppy Disk to save here. Check the supplies I left in rooms or in a Storage box.','item:Floppy Disk');
  return;
 }
 return save.apply(this,args);
};
function summary(){
 const totals={};
 for(const o of Object.values(R).flatMap(r=>r.o))for(const [name,count]of o[4].give||[])totals[name]=(totals[name]||0)+count;
 return {mode:mode(),cells:totals.Battery||0,disks:totals['Floppy Disk']||0,dressings:totals['Trauma Dressing']||0,medkits:totals['Field Medkit']||0,healing:(totals['Trauma Dressing']||0)*HEALS['Trauma Dressing']+(totals['Field Medkit']||0)*HEALS['Field Medkit'],cradleCharges:1};
}
WW.supplies9={plans,mode,summary};
})();
