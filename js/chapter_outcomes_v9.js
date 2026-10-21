/* One-time decisions leave different, saved people and practical consequences. */
(function(){
'use strict';
const WW=WardWinter,e=htmlSafe;
const living=()=>!!(S&&S.hp>0&&!S.f.dead&&!S.f.chapter1Complete&&!WW.isPaused?.());
const patientTitle='Daniel Mercer — bedside record';
const kesslerTitle='Kessler — theatre observation';
const dangerCost=values=>S.m<1?values[0]:S.m>1?values[2]:values[1];
function thought(text){(S.th2||(S.th2=[])).push(text);WW.think?.(text);}
function record(title,lines){
 if(!S.docs.includes(title))S.docs.push(title);
 DOCS[title]=lines.join('\n\n');
}
function patientRecord(){
 const history=S.f.patientHistory||[];
 record(patientTitle,['DANIEL MERCER / ISOLATION TREATMENT',...history]);
}
function rememberPatient(line){
 const history=S.f.patientHistory||(S.f.patientHistory=[]);
 if(!history.includes(line))history.push(line);
 patientRecord();
}
function normalize(){
 if(!S)return;
 const choice=S.f.beggingPatientChoice;
 if(!S.f.patientOutcomeVersion){
  // Earlier decisions keep their established condition. An earlier abandoned
  // patient receives a fresh warning interval, never an instant load penalty.
  S.f.patientOutcome=choice==='killed'?'dead':choice==='helped'?'stabilized':choice==='left'?'untreated':null;
  if(choice==='left')S.f.patientDeterioratesAt=S.t+18;
  S.f.patientOutcomeVersion=9;
 }
 if(choice==='killed'){S.f.patientOutcome='dead';S.ob.beggingPatient='done';}
 if(choice==='helped'){S.f.patientOutcome='stabilized';S.ob.beggingPatient='done';}
 if(S.f.patientHistory?.length)patientRecord();
 if(S.f.kesslerRecord)record(kesslerTitle,S.f.kesslerRecord);
}
WW.patientDescription=()=>{
 const state=S.f.patientOutcome;
 if(S.f.beggingPatientChoice==='killed')return 'A sheet covers Daniel Mercer on the bed. The monitor is silent. His death and the decision that led to it are permanent.';
 if(state==='stabilized')return 'Clean dressings cover Mercer’s wounds. His breathing has settled, and his eyes follow the door. The restraints remain secure; the treatment has bought him time, not cured the infection.';
 if(state==='contained')return 'Mercer is no longer lucid. The repaired wrist restraint keeps his infected body on the bed, away from the door. He will not follow me into the corridor.';
 if(state==='transformed')return 'Dark veins spread across Mercer’s face. He strains against one remaining wrist restraint; the other strap hangs broken. He cannot leave the bed, but reaching him is dangerous.';
 if(state==='untreated')return 'Mercer remains untreated and conscious. His breaths come in short bursts, and the right wrist restraint is beginning to fray. I can still bring a clean dressing before he deteriorates.';
 return 'Daniel Mercer lies restrained on the bed, conscious and frightened. Dark veins reach above his collar, and the monitor races when he pulls against the straps.';
};
WW.patientRoomAsset=(room,view='front')=>{
 if(!S||room!=='isoward'||view!=='front'||S.f.beggingPatientChoice==='killed')return null;
 return {stabilized:'assets/room_views/isoward_stabilized.webp',transformed:'assets/room_views/isoward_transformed.webp',contained:'assets/room_views/isoward_contained.webp'}[S.f.patientOutcome]||null;
};
WW.kesslerDescription=()=>{
 if(!S.f.doctorWallSeen)return 'A figure in a stained coat faces the tiled wall beside the operating table. Slow impacts cut through the emergency hum.';
 const contact=S.f.kesslerResponse;
 return 'Kessler has collapsed against the damaged tiles. Dark veins spread above his collar; his jaw works in involuntary spasms.'+(contact==='speak'?' His brief answer is preserved in my theatre observation.':contact==='approach'?' I stepped inside his reach and paid for it.':contact==='leave'?' I heard the final impacts from the doorway.':' I watched the infection take his balance.')+' The laundry door is the way back.';
};
function patientModal(){
 const returning=S.f.beggingPatientChoice==='left';
 modal(returning?'Daniel Mercer · still lucid':'Daniel Mercer · the restrained patient',
  '<p>'+e(returning?'He recognizes me. The untreated wounds and the fraying strap are worse, but he can still answer.':'He follows my hand with his eyes. Dark veins spread from his collar, but he is still lucid. “Please. I can feel it changing me.”')+'</p>'+
  '<p>A clean Trauma Dressing may steady him long enough to remain lucid. It cannot cure the infection. Leaving him untreated may change what I find on a later visit.</p>'+
  '<div class="choice-actions"><button class="btn p" onclick="choosePatientFate(\'helped\')">Try to treat him</button><button class="btn" onclick="choosePatientFate(\'left\')">Leave him alive</button><button class="btn" onclick="choosePatientFate(\'killed\')">End his suffering</button></div>');
}
function deterioration(){
 if(!living()||S.room!=='isoward'||S.f.beggingPatientChoice!=='left'||S.f.patientOutcome!=='untreated'||S.t<(S.f.patientDeterioratesAt||Infinity))return false;
 S.f.patientOutcome='transformed';S.f.patientDeteriorationSeen=1;S.san=Math.max(0,S.san-6);
 rememberPatient('I returned after leaving him untreated. Daniel no longer recognized me. His right restraint had snapped; his left wrist still held him on the bed.');
 thought('Daniel has turned. He is still tethered to the bed. I can keep my distance; I do not have to put my hands near him.');
 render();afterPatient(true);return true;
}
function afterPatient(first=false){
 const secured=S.f.patientOutcome==='contained',handled=!!S.f.patientAftermathHandled;
 modal('Daniel Mercer · the broken restraint',
  '<p>'+e(first?'The bed frame rattles. Daniel lunges until the last wrist strap catches. His clouded eyes no longer track my face.':'Daniel remains infected and tethered to the bed. He cannot follow me out of this room.')+'</p>'+
  '<p>'+e(secured?'The repaired restraint holds. I will not risk reaching in again.':'I can stay beyond his reach. Securing the loose strap means putting my arm close to his teeth and risking injury.')+'</p>'+
  (!handled&&!secured?'<button class="btn" onclick="wardPatientAftermath(\'secure\')">Secure the loose restraint · risk injury</button>':'')+
  '<button class="btn" onclick="choosePatientFate(\'killed\')">End his suffering</button><button class="btn p" onclick="wardPatientAftermath(\'retreat\')">Keep my distance</button>');
}
beggingPatient=function(){
 if(!living()||S.room!=='isoward')return;
 normalize();if(deterioration())return;
 if(S.f.beggingPatientChoice==='killed')return interaction(WW.patientDescription());
 if(S.f.patientOutcome==='stabilized')return interaction(WW.patientDescription());
 if(['transformed','contained'].includes(S.f.patientOutcome))return afterPatient();
 patientModal();
};
choosePatientFate=function(choice){
 if(!living()||S.room!=='isoward'||!['helped','left','killed'].includes(choice))return;
 normalize();if(S.f.beggingPatientChoice==='killed'||S.f.patientOutcome==='stabilized')return;
 if(deterioration())return;
 const transformed=['transformed','contained'].includes(S.f.patientOutcome);
 if(choice==='killed'){
  const loaded=W[S.eq]&&has(S.eq)&&(S.ld[S.eq]||0)>0;
  if(!has('Utility Knife')&&!loaded)return modal('The patient is still alive','<p>I need the utility knife or a loaded firearm. No choice has been committed.</p><button class="btn" onclick="beggingPatient()">Return to the patient</button>');
  modal('End his suffering?',
   '<p>'+e(transformed?'Daniel has turned, but ending his life is still irreversible. I will cover him with the sheet.':'Daniel is still conscious. This ends his life permanently; clean dressings are the other way I can try to help.')+'</p>'+
   '<p>A firearm spends one loaded round and may draw nearby infected. The utility knife is quiet, but I must get close.</p>'+
   (has('Utility Knife')?'<button class="btn" onclick="wardConfirmPatient(\'knife\')">Use utility knife</button>':'')+
   (loaded?'<button class="btn" onclick="wardConfirmPatient(\'firearm\')">Use loaded firearm</button>':'')+
   '<button class="btn" onclick="beggingPatient()">Do not do this</button>');return;
 }
 if(transformed)return afterPatient();
 if(choice==='helped'){
  if(!has('Trauma Dressing'))return modal('Treatment supplies needed','<p>I need one Trauma Dressing. Daniel remains alive; no treatment or final decision has been committed.</p><button class="btn" onclick="beggingPatient()">Return to the patient</button>');
  rem('Trauma Dressing',1);S.f.beggingPatientChoice='helped';S.f.patientOutcome='stabilized';S.ob.beggingPatient='done';S.san=Math.max(0,S.san-5);
  rememberPatient('I cleaned his wounds, applied a Trauma Dressing and secured both restraints. Daniel remained lucid. The dressing bought time; it did not cure him.');
  rememberPatient('Daniel warned me that the corridor purge handle opens three exterior windows, and that spare patrol equipment was left behind the ward entry rather than on the bedside shelves.');
  thought('Daniel is still here because I stopped to help. His warning about the three windows may spare me another mistake.');
  advanceTime(2);$('m').innerHTML='';S.sceneFocus=null;render();
  return modal('Daniel Mercer · stabilized','<p>His breathing settles while I bind the wounds and fasten the straps. The clouding in his eyes eases. He can still recognize me.</p><p>“The purge handle opens all three windows. Don’t leave them open in this cold. Patrol stores... behind the ward entry.”</p><p>I have used one Trauma Dressing. He is steadier and still lucid. The infection has not been cured.</p><button class="btn p" onclick="closeModal()">Step away</button>');
 }
 if(S.f.beggingPatientChoice!=='left'){
  S.f.beggingPatientChoice='left';S.f.patientWasLeft=1;S.f.patientOutcome='untreated';S.f.patientDeterioratesAt=S.t+18;S.san=Math.max(0,S.san-7);
  rememberPatient('I left Daniel alive and untreated. The right wrist restraint was fraying. I could still return with a Trauma Dressing while he remained lucid.');
  thought('I left Daniel breathing. If I mean to help him, I should return soon with a clean dressing.');
 }
 S.ob.beggingPatient='pending';$('m').innerHTML='';S.sceneFocus=null;render();
 return modal('Daniel Mercer · left alive','<p>I leave him conscious behind the treatment-room door. The damaged restraint keeps scraping the bed rail.</p><p>I can return with a Trauma Dressing before he deteriorates. Leaving him alive does not mean leaving him unchanged.</p><button class="btn p" onclick="closeModal()">Step away</button>');
};
wardConfirmPatient=function(method){
 if(!living()||S.room!=='isoward'||S.f.beggingPatientChoice==='killed'||S.f.patientOutcome==='stabilized'||!['knife','firearm'].includes(method))return;
 if(method==='knife'&&!has('Utility Knife')||method==='firearm'&&(!W[S.eq]||!has(S.eq)||!(S.ld[S.eq]>0)))return;
 const changed=['transformed','contained'].includes(S.f.patientOutcome);
 S.f.beggingPatientChoice='killed';S.f.patientOutcome='dead';S.f.patientMethod=method;S.ob.beggingPatient='done';S.san=Math.max(0,S.san-(changed?12:17));
 rememberPatient((changed?'After the infection took his lucidity, I ended Daniel’s life':'I ended Daniel’s life while he could still understand me')+(method==='knife'?' with the utility knife.':' with one firearm round.')+' I covered him with the bed sheet. This cannot be undone.');
 thought(changed?'I could not bring Daniel back after leaving him. I ended what was left and covered his face.':'I ended Daniel Mercer’s suffering and covered him. I will never know whether the treatment might have bought him more time.');
 if(method==='firearm'){S.ld[S.eq]--;soundEffect('shot');noise();}else soundEffect('knife');
 advanceTime(2);$('m').innerHTML='';S.sceneFocus=null;render();
 modal('Daniel Mercer','<p>The monitor is silent. I draw the bed sheet over him; his face and body remain covered.</p><p>This decision cannot be undone. '+(method==='firearm'?'The shot has carried beyond the room.':'No gunshot has warned the adjoining rooms.')+'</p><button class="btn p" onclick="closeModal()">Step away</button>');
};
window.wardPatientAftermath=function(choice){
 if(!living()||S.room!=='isoward'||S.f.beggingPatientChoice!=='left'||!['transformed','contained'].includes(S.f.patientOutcome)||!['secure','retreat'].includes(choice))return;
 if(choice==='secure'){
  if(S.f.patientAftermathHandled)return;
  S.f.patientAftermathHandled=1;S.f.patientOutcome='contained';const cost=dangerCost([6,9,12]);S.hp=Math.max(0,S.hp-cost);S.f.patientRestraintInjury=cost;
  rememberPatient('I secured Daniel’s broken restraint. Reaching inside his grasp cost me '+cost+' health. The repaired strap keeps him away from the doorway; he cannot follow me.');
  soundEffect('hit');if(S.hp<=0)return die();advanceTime(2);
  $('m').innerHTML='';S.sceneFocus=null;render();return modal('The restraint holds','<p>His nails catch my forearm as I fasten the strap. I pull free and retreat beyond the bed.</p><p>I lost '+cost+' health. He remains infected, but the repaired strap holds. I will not have to reach in again.</p><button class="btn p" onclick="closeModal()">Step away</button>');
 }
 if(!S.f.patientAftermathHandled){S.f.patientAftermathHandled=1;rememberPatient('I kept beyond his reach and left the infected Daniel tethered to the bed. I took no physical injury.');}
 $('m').innerHTML='';S.sceneFocus=null;render();
};
doctorAtWall=function(){
 if(!living()||S.room!=='surgery'||S.f.doctorWallSeen)return false;
 S.f.doctorWallEncounterStarted=1;render();
 modal('Dr. Adrian Kessler · the tiled wall',
  '<div class="doctor-wall-scene"><img class="doctor-evidence-image" src="assets/room_views/surgery_front.webp" alt="Kessler strikes the tiled wall; dark veins show above his stained collar"><p>The doctor strikes his head against the tiles. Dark veins run above his collar. His jaw twitches between impacts; this is an infection taking control of him.</p><p>Calling to him may reach what is left of his awareness. Approaching puts me within reach of his hands. Watching means seeing the deterioration happen.</p></div><button class="btn" onclick="wardFinishKessler(\'speak\')">Call his name</button><button class="btn" onclick="wardFinishKessler(\'approach\')">Approach carefully · risk injury</button><button class="btn" onclick="wardFinishKessler(\'inspect\')">Watch from the doorway</button><button class="btn" onclick="wardFinishKessler(\'leave\')">Back away</button>');
 document.querySelector('#m .mh button')?.remove();WardSound.play('impact',{volume:.4});return true;
};
wardFinishKessler=function(choice){
 if(!living()||S.room!=='surgery'||S.f.doctorWallSeen||!['speak','approach','inspect','leave'].includes(choice))return;
 const response={
  speak:{sanity:14,condition:'lucid',line:'His eyes briefly find mine. “You were awake the first time.” The recognition breaks into a wet cough. A spasm takes his legs, and he collapses against the tiles, one hand still clawing at the wall.',thought:'For a moment Kessler recognized me. Then the infection took his voice.'},
  approach:{sanity:12,condition:'seizing',line:'Kessler turns before I can touch his shoulder. His hand rakes my arm. I recoil as a convulsion folds him against the wall; dark veins tighten along his neck.',thought:'I reached for Kessler as if he were still an ordinary patient. His grip was far too strong.'},
  inspect:{sanity:16,condition:'seizing',line:'I keep watching. The impacts lose their rhythm. Dark veins spread along his jaw; his teeth work against an empty mouth. His legs finally buckle, but the twitching does not stop.',thought:'I watched the infection take Kessler. He did not simply sit down; his body stopped obeying him.'},
  leave:{sanity:8,condition:'unresponsive',line:'I back out of reach. Two final impacts come from the alcove, then a scraping collapse. From the doorway I can still see his jaw working and the dark veins above his collar.',thought:'I backed away before Kessler turned toward me. The impacts stopped; the infection did not.'}
 }[choice];
 S.f.doctorWallSeen=1;S.f.kesslerResponse=choice;S.f.kesslerCondition=response.condition;S.ob.kessler='read';S.san=Math.max(0,S.san-response.sanity);
 let injury='';if(choice==='approach'){const cost=dangerCost([4,6,8]);S.hp=Math.max(0,S.hp-cost);S.f.kesslerInjury=cost;injury=' His grasp cost me '+cost+' health.';soundEffect('hit');}
 S.f.kesslerRecord=['DR. ADRIAN KESSLER / THEATRE OBSERVATION',response.line+injury,'I chose to '+({speak:'call his name',approach:'approach him',inspect:'watch from the doorway',leave:'back away'}[choice])+'. The encounter is over; his infected aftermath remains in the theatre.'];
 record(kesslerTitle,S.f.kesslerRecord);thought(response.thought);lg('Kessler: '+choice+'. His infected aftermath remains.');
 if(S.hp<=0)return die();$('m').innerHTML='';S.sceneFocus=null;render();
 modal('The theatre falls quiet','<p>'+e(response.line+injury)+'</p><p>The infection is still visible. This encounter will not repeat.</p><button class="btn p" onclick="closeModal()">Step back</button>');
};
finishWallDoctor=function(){return wardFinishKessler('leave');};
const arrive=chapterArrival;
chapterArrival=function(from,to){
 const result=arrive(from,to);normalize();
 if(result||!living()||to!=='isoward'||$('m').children.length)return result;
 return deterioration()||result;
};
const configure=configureWorld;
configureWorld=function(...args){const result=configure(...args);normalize();return result;};
const stress=WW.incidentStress;
WW.incidentStress=()=>stress()+(S?.f.patientDeteriorationSeen?6:0);
WW.patientOutcomes={normalize,deterioration,patientTitle,kesslerTitle};
})();
