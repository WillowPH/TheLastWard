/* The Last Ward — approved screenshot and Chapter 1 interaction polish.
   This file does not create a second UI. It reinforces the existing single cinematic stage. */
(function(){
'use strict';
// Visible scene response to previously established narrative state. Does not add permanent HUD meters.
const baseThought=renderSceneThought;
renderSceneThought=function(){baseThought();if(!S)return;
 const p=$('sceneThoughtText');if(!p)return;
 const room=S.room, f=S.f||{};
 if(room==='isoward'&&f.beggingPatientChoice){
  p.textContent=f.beggingPatientChoice==='killed'?'I chose for him. This room will never be quiet again.':f.beggingPatientChoice==='helped'?'I tried to help. That has to mean something.':'I left him breathing. I do not know what I would find if I went back.';
 }else if(room==='surgery'&&f.doctorWallSeen){
  p.textContent='The tiles are silent. I can still hear the impacts.';
 }else if(room==='generator'&&f.power){
  p.textContent='Power. Finally. What else did I wake up when I turned it on?';
 }else if(room==='observation'&&f.plexiIncidentSeen){
  p.textContent='He thought I could save him. He was wrong.';
 }
};
// Provide a concise visual information language inside the screenshot-approved survival sidebar.
const originalRender=render;
render=function(){originalRender();if(!S)return;
 const v=$('mentalLabel');if(v)v.title='Sanity affects perception, hallucinations and some story events.';
 const brand=document.querySelector('.ward-brand small');if(brand)brand.textContent='CHAPTER 1 · BLACKRIDGE MEDICAL COMPLEX · 1998';
 const h=$('conditionHint');if(h&&S.hp<=75)h.textContent=S.hp<=25?'Severe limp · escape difficult':S.hp<=50?'Limping · strained breathing':'Slight limp · movement slowed';
 const light=$('lightBtn');if(light)light.textContent=S.lightOn?'TURN FLASHLIGHT OFF · '+S.bat:'TURN FLASHLIGHT ON · '+S.bat;
};
// Portability: make explicit save files available for offline website or locally downloaded edition.
// This exports the last saved Continuity Terminal record, not a free quick-save.
window.wardExportRecord=function(){
 const saved=read(K)||read(KB);if(!saved){interaction('There is no saved Continuity Terminal record to export.');return;}
 const json=JSON.stringify({game:'The Last Ward',format:1,record:saved});const url=URL.createObjectURL(new Blob([json],{type:'application/json'}));
 const a=document.createElement('a');a.href=url;a.download='the-last-ward-record.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),3500);
};
window.wardImportRecord=function(input){const file=input.files?.[0];if(!file)return;
 if(file.size>1_000_000){interaction('This file is too large to be a normal save record.');return;}
 const reader=new FileReader();reader.onload=()=>{try{
  const json=JSON.parse(String(reader.result));if(json.game!=='The Last Ward'||json.format!==1||!valid(json.record))throw Error('Invalid save file');
  if(!confirm('Replace the latest Continuity Terminal save with this imported record?'))return;
  localStorage.setItem(K,JSON.stringify(json.record));loadGame();
 }catch(e){interaction('The imported file is not a valid The Last Ward save. No existing record was changed.');}}
 reader.readAsText(file);
};
const formerSaveMenu=saveMenu;
saveMenu=function(){formerSaveMenu();const content=document.querySelector('#m .mb');if(!content)return;
 content.insertAdjacentHTML('beforeend',`<div class="record-backup"><strong>Portable save record</strong><p class="micro">Export your latest saved Continuity Terminal record for offline play or another browser. Importing replaces that record.</p><button class="btn" onclick="wardExportRecord()">Export saved record</button><label class="btn backup-import">Import saved record<input type="file" accept=".json,application/json" onchange="wardImportRecord(this)" hidden></label></div>`);
};
// Show a consistent accessibility cue for covered, clicked, and locked scene parts.
const stage=document.getElementById('interactiveScene');
if(stage)stage.addEventListener('keydown',e=>{if(e.key==='Escape'&&S?.sceneFocus){wardCloseFocus();e.preventDefault()}});
})();
