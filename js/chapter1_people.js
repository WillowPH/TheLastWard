/* Named staff, one-time story consequences and evidence consistency. */
(function(){
'use strict';
R.security.o.push(['clara','Clara Whitmore','◉','The surviving security operator keeps her voice low.',{act:'clara'}]);
R.stafflounge.o.push(['shaw','Nurse Evelyn Shaw','◉','A nurse watches the corridor from beside the kitchenette.',{act:'shaw'}]);
R.pharmacy.o.push(['judith','Nurse Judith Price','◉','An infected nurse folds an empty medicine wrapper. She is not attacking.',{act:'judith'}]);
R.surgery.o.push(['kessler','Dr. Adrian Kessler','◉','The doctor remains by the tiled wall.',{act:'kessler'}]);
DOCS['Incident Report 09-17']='SECURITY — OFFICER THOMAS REED\n\nThe exterior chains were fitted on Graham Strickland’s written orders. We were told the ambulance evacuation was cancelled while staff were still waiting at the doors. The hold order carries Richard Halbrook’s authorization.\n\nA recovery subject was transferred through Laundry. Its escort instruction says SUBJECT X. The recording contains heavy steps and no conversation.';
DOCS['Rourke’s final annotation']='DR. EDMUND ROURKE — LULLABY\n\nLenora Blackwell called the continuity trial a preservation of experience. She stopped describing the people who would have to live with it. Bela is a witness, not a judge.\n\nThe transfer console will accept the archive drive once the executive portraits identify the authorized signatories. If the operator wakes, do not tell him what to remember. Show him what was recorded.';
DOCS['Furnace Log']=`MARTIN HELLER — BOILER SERVICE

A heatproof tool compartment beside the firebox contains the last precision insert. The main generator failure was not a fuel shortage. The relay bypass was left disabled on Strickland’s order.

We could have kept the ward lights on.`;
DOCS['Autopsy Report 4']=`DR. NATHANIEL GRAVES — MORTUARY OBSERVATION

The subject retained a reflex response after the recorded time of death. The chart was relabelled twice. Drawer 12 contains a transfer slip, not an identification.

Graves requested that the original admission dates be removed.`;
DOCS['Chaplain Letter']=`I refused Blackwell’s request to bless the continuity trial. I can still leave clean dressings for whoever reaches this room.

The locked reliquary holds emergency aid. The archive memorial register records the dedication date needed to open the chapel.`;
DOCS['Staff Lounge Note']=`MISSING — NURSE MARIAN VALE

Last seen at the staff residence after the evacuation hold. Her name was removed from the shift roster. If you find her silver locket, leave it with Evelyn Shaw.

Someone added: the mortuary register was checked. She was never admitted there.`;
const originalDocumentText=docText;
docText=function(title){let text=originalDocumentText(title);if(title==='Resident Diary')text+='\n\nMarian Vale left her locket here before a security escort took her toward the service lift. She was alive. The public roster was changed before the alarm.';return text;};
const baseCheckpoint=loadCheckpoint;
loadCheckpoint=function(){baseCheckpoint();if(S){configureWorld(S.seed,true);placeTelephones(S.seed);S.f.hidingRoom=null;S.sceneFocus=null;render()}};
const basePursuitCheckpoint=loadFirstFloorCheckpoint;
loadFirstFloorCheckpoint=function(){basePursuitCheckpoint();if(S){placeTelephones(S.seed);S.f.hidingRoom=null;S.sceneFocus=null;render()}};
const inheritedAct=act;
act=function(id){if(id==='clara'){if(S.f.claraGone)return interaction('The operator has left. Her headset hangs over the chair.');S.f.claraSpoken=1;S.ob.clara='read';modal('Clara Whitmore · Security','<p>“Clara. Night security. I tried to release the outside doors. Strickland revoked the local overrides.”</p><p>She glances at your blank wristband. “I saw someone wearing that band on the cameras before the outage. I can’t prove it was you.”</p><p>“The evacuation plan is on the desk. Use it. If power returns, I’ll try the internal line.”</p><button class="btn p" onclick="closeModal()">Leave her to the monitors</button>');return renderScene()}
 if(id==='shaw'){S.ob.shaw='read';if(S.f.shawSpoken)return interaction('Shaw keeps listening at the service door. “I can help the people here. You need to find out who is still controlling the locks.”');S.f.shawSpoken=1;S.th2.push('Evelyn Shaw believes Daniel Mercer may still be lucid enough to help.');modal('Nurse Evelyn Shaw','<p>“I’m Evelyn Shaw. Don’t point that at me.” She waits until your hands lower.</p><p>“Daniel Mercer is still conscious in treatment. Some of them can still understand us. Don’t assume you know which.”</p><p>She looks toward the ceiling. “Kessler kept taking orders from Graves after the ward closed. The researchers knew something was wrong long before the sirens.”</p><button class="btn p" onclick="closeModal()">Let her stay here</button>');return renderScene()}
 if(id==='judith'){S.f.judithVisits=(S.f.judithVisits||0)+1;S.ob.judith='read';const lines=['“Price. Judith Price. Eight o’clock medication. I still have to finish.”','“One tablet for the patient. One name for the record. They changed the names.”','“Eight... eight... patient is the name is the...”'];interaction(lines[Math.min(2,S.f.judithVisits-1)]+' The nurse folds the wrapper again. She does not advance.');if(!S.f.judithSanity){S.f.judithSanity=1;S.san=Math.max(0,S.san-3)}return render()}
 if(id==='kessler'){if(!S.f.doctorWallSeen)return doctorAtWall();return interaction('Kessler has stopped striking the tiles. The words “You were awake the first time” still hang in the room.');}
 const result=inheritedAct(id);if(!S.f.missingNurseSolved&&['Mortuary Transfer Slip','Resident Diary','Staff Lounge Note'].every(t=>S.docs.includes(t))){S.f.missingNurseSolved=1;S.san=Math.min(100,S.san+5);S.th2.push('Marian Vale was alive when security escorted her to the service elevator. The missing-person record was altered before the alarm.');lg('Reconstructed the missing nurse’s transfer from three records.');}return result;
};
researcherLastRoom=function(){if(S.f.researcherLastRoomSeen)return false;S.f.researcherLastRoomSeen=1;S.f.researchers=1;S.f.researcherAftermathSeen=1;S.san=Math.max(0,S.san-10);S.docs.push('Final Research Entry','Rourke’s final annotation');S.th2.push('Rourke left evidence that LULLABY continued after the staff were ordered to remain inside.');lg('Recovered Dr. Edmund Rourke’s final evidence.');render();modal('Dr. Edmund Rourke’s last room','<p>The researcher is motionless at his desk, one hand still resting on a notebook. A field recorder has run to the end of its tape.</p><p>His last pages name Lenora Blackwell and Project LULLABY. A second annotation describes the transfer authorization console.</p><p class="c1-thought">He left the evidence where someone could find it. Was he expecting me?</p><button class="btn p" onclick="doc(\'Rourke’s final annotation\')">Read the annotation</button><button class="btn" onclick="closeModal()">Step away</button>');return true;};
const previousArrival=chapterArrival;
chapterArrival=function(from,to){if(S.f.power&&S.f.claraSpoken&&!S.f.claraGone&&to==='security'){S.f.claraGone=1;S.th2.push('Clara left Security after the power returned. Her last note points toward the first-floor observation console.');interaction('Clara’s chair is empty. A note reads: “The camera archive is upstairs, through Maintenance. Do not take the outside line.”');}return previousArrival(from,to)};
doc=function(title){const corporate=/Directive|Consent|Transcript|Report|Patient File|Specimen|Power Control|Authorization|Transfer Slip|Safety Notice/.test(title),path='assets/identity/monolith.svg',logo=window.WardEmbeddedAssets?.[path]||path;modal(htmlSafe(title),'<div class="paper">'+(corporate?'<header class="monolith-letterhead"><img src="'+logo+'" alt="Monolith emblem"><div><strong>MONOLITH PHARMACEUTICALS</strong><small>Preserving Life. Securing Peace.</small></div></header>':'')+htmlSafe(docText(title))+'</div>')};
const inheritedInventorySlot=useInventorySlot;
useInventorySlot=function(index){const slot=S.inv[index];if(!slot)return;const name=slot.n;if(W[name]||HEALS[name]||name==='Flashlight'||['Battery','Reinforced Battery','Stabilizer Part'].includes(name)||Object.values(W).some(w=>w.ammo===name))return inheritedInventorySlot(index);const marks={'Cabinet Key':'RECEPTION · CABINET SERVICE','Staff Access Card':'MONOLITH · NIGHT STAFF · INTERNAL ACCESS','Maintenance Key':'M. HELLER · SERVICE ARCHIVE','Maintenance Tools':'INSULATED CONTACT TOOLS · M. HELLER','Encrypted Drive':'OBSERVATION ARCHIVE · TRANSFER CONTROL','Tunnel Key':'BOILER ACCESS','Crank Handle':'SERVICE WINCH'};modal(htmlSafe(name),'<div class="c1-item-examine">'+itemIconMarkup(name)+'<p>'+htmlSafe(desc(name))+'</p>'+(marks[name]?'<p class="c1-thought">'+htmlSafe(marks[name])+'</p>':'')+'</div><button class="btn" onclick="invModal()">Organize / combine inventory</button>')};
const originalRender=render;
render=function(){originalRender();if(!S)return;const light=$('lightBtn');if(light)light.textContent=!has('Flashlight')?'FLASHLIGHT NOT FOUND':(S.lightOn?'TURN FLASHLIGHT OFF':'TURN FLASHLIGHT ON')+' · '+S.bat;const condition=$('conditionLabel');if(condition){condition.textContent=S.hp>75?'FINE':S.hp>25?'CAUTION':'DANGER';condition.className=S.hp>75?'fine':S.hp>25?'caution':'danger';}const objective=$('obj');if(objective)objective.textContent=S.f.chapter1Complete?'Chapter 1 complete. Export your transfer record.':S.f.chapter1Revelation?'The service elevator is ready. Choose when to descend.':S.f.finalSecurityClearance?'Break contact with Subject X and reach the service elevator.':S.f.power?'Follow the powered records and containment systems.':'Investigate Blackridge and restore emergency power.';};
})();
