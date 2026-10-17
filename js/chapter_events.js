/* Persistent interaction beats layered over the base chapter engine. */
const PHONE_BEATS=[
 {title:'An unanswered line',text:'The receiver lifts from its cradle. The bell dies. Nothing follows—not a dial tone, not breathing, not even static. Three knocks come from the wall behind the booth.',thought:'Who could ring a telephone with no wires?'},
 {title:'The accusation',text:'A voice with a cracked, tired edge says: “Murderer.” Before you can ask who is speaking, the line goes dead. A faint click repeats in an adjoining room.',thought:'That voice knows something about me. I need to know what.'},
 {title:'The wrong voice',text:'An old tape hiss. A woman says “Bela is not the question.” A voice that sounds exactly like yours replies, “Then why did you keep asking?” The line disconnects.',thought:'That cannot be me. Unless someone recorded me before I woke up.'}
];
// A call happens once at one physical telephone; later calls ring at different seed-chosen phones.
// The seed is generated and saved silently; story beats themselves do not change.
const PHONE_LOCATIONS_2=['stafflounge','laundry','pharmacy'];
const PHONE_LOCATIONS_3=['residence','records','observation'];
function phoneRoomsForSeed(seed){return ['lobby',PHONE_LOCATIONS_2[hashSeed(seed+'::phone-two')%PHONE_LOCATIONS_2.length],PHONE_LOCATIONS_3[hashSeed(seed+'::phone-three')%PHONE_LOCATIONS_3.length]]}
function placeTelephones(seed){
 for(const r of Object.values(R))r.o=r.o.filter(o=>!String(o[0]).startsWith('phone_stage_')&&!String(o[0]).startsWith('phone_decoy_'));
 S.phoneRooms=phoneRoomsForSeed(seed);
 S.phoneRooms.slice(1).forEach((r,i)=>{
  const id='phone_stage_'+(i+2);
  R[r].o.push([id,'Wall telephone','☎','A hard-wired hospital telephone. Its numbered plate has been removed.',{act:'payphone'}]);
 });
 // Additional silent phones do not all ring; their locations rotate between runs.
 const decoyLocations=['security','residence','chapel','records','isoward','b2gallery'];
 const shuffled=decoyLocations.map((r,i)=>[r,hashSeed(seed+'::dead-phone-'+r)]).sort((a,b)=>a[1]-b[1]);
 shuffled.slice(0,3).forEach(([r],i)=>{if(!S.phoneRooms.includes(r))R[r].o.push(['phone_decoy_'+i,'Disconnected telephone','☎','The handset is dusty and the cable ends beneath the wall plate.',{act:'payphone'}])});
}
function phoneMilestone(){return S.f.plexiIncidentSeen&&S.f.photoPuzzleSolved?3:S.f.power?2:1}
function phoneTarget(){return (S.phoneRooms||phoneRoomsForSeed(S.seed))[S.f.phoneStep||0]}
function maybeRingRoomPhone(room){return ringPayphone(room)}
function ringPayphone(room=S.room){if(!S||!S.f?.introComplete)return false;const step=S.f.phoneStep||0;
 if(step>=3||S.f.phoneRinging||step>=phoneMilestone()||room!==phoneTarget())return false;
 S.f.phoneRinging=true;S.f.ringingPhoneRoom=room;
 const title=step===0?'The reception payphone begins ringing.':'A different telephone begins ringing nearby.';
 lg(title);interaction('A real bell rings somewhere in '+R[room].n+'.');soundEffect('phone');render();return true;
}
function answerPayphone(id){const step=S.f.phoneStep||0,room=S.room,target=phoneTarget();
 const idExpected=step===0?'payphone':'phone_stage_'+(step+1);
 if(step>=3||room!==target||id!==idExpected||!S.f.phoneRinging){return interaction('The line is dead. It will not ring.');}
 const beat=PHONE_BEATS[step],variant=hashSeed(S.seed+'::phone-variation-'+step)%3;
 S.f.phoneRinging=false;S.f.ringingPhoneRoom=null;S.f.phoneStep=step+1;
 S.f['answeredPhone_'+room]=1;S.ob[id]='read';
 const additions=['A distant set of footsteps falls out of rhythm.','Water trickles down the disconnected line.','A cabinet latch clicks in the room behind you.'];
 const extra=additions[variant];S.th2=S.th2||[];S.th2.push('Telephone: '+beat.thought);
 interaction(beat.text+' '+extra);lg('The telephone in '+R[room].n+' fell silent.');soundEffect('click');advanceTime(1);render();
 modal(beat.title,`<div class="unique-event"><p>${beat.text}</p><p>${extra}</p><p class="unique-thought">${beat.thought}</p><p class="micro">This telephone will not ring again.</p></div><button class="btn p" onclick="closeModal()">Hang up</button>`);
}
function beggingPatient(){const choice=S.f.beggingPatientChoice;
 if(choice){return interaction(choice==='helped'?'His breathing is steadier. Whether he survives, you cannot know.':choice==='killed'?'The treatment room is quiet. You cannot take the choice back.':'He has fallen quiet, but you can still hear the monitor ticking behind the door.');}
 modal('The patient in isolation',`<div class="unique-event"><p>A conscious patient struggles weakly against the hospital restraints. His eyes follow you.</p><p>“Please. I can feel it changing me. Don't let me become one of them.”</p><p class="unique-thought">He's not a monster. Not yet. What am I supposed to do?</p></div><div class="choice-actions"><button class="btn p" onclick="choosePatientFate('helped')">Try to treat him</button><button class="btn" onclick="choosePatientFate('left')">Leave him alive</button><button class="btn" onclick="choosePatientFate('killed')">End his suffering</button></div>`);
}
function choosePatientFate(choice){if(S.f.beggingPatientChoice)return;if(choice==='helped'&&!has('Trauma Dressing'))return interaction('I need clean dressings to attempt any treatment.');if(choice==='killed'&&!W[S.eq])return interaction('I have nothing that could end this quickly. I cannot make that promise.');if(choice==='killed'&&(S.ld[S.eq]||0)<=0)return interaction('The weapon is empty. The patient watches me, terrified.');
 S.f.beggingPatientChoice=choice;S.ob.beggingPatient='read';const consequences={helped:['You secure the restraints, treat the wounds and leave an emergency note. His breathing slows.','I tried. Whatever this is, at least I tried.',-5],left:['You leave him conscious behind the door. His voice follows you down the corridor.','I left a living man there. I still hear him.',-7],killed:['You raise the weapon. A single shot ends the plea. The echo stays with you long after the sound is gone.','I chose for him. What if he could have recovered?',-17]};const [line,thought,cost]=consequences[choice];if(choice==='helped')rem('Trauma Dressing',1);if(choice==='killed'){S.ld[S.eq]--;soundEffect('shot');noise()}
 S.san=Math.max(0,S.san+cost);S.th2=S.th2||[];S.th2.push(thought);lg('Isolation patient: '+choice+'.');$('m').innerHTML='';render();modal('The isolation room',`<div class="unique-event"><p>${sceneDetail(line,choice==='killed'?'The room becomes silent. You cannot undo the decision.':line)}</p><p class="unique-thought">${thought}</p></div><button class="btn p" onclick="closeModal()">Leave</button>`);
}
function plexiIncident(){if(S.f.plexiIncidentSeen)return interaction('The shattered viewing chamber is empty. The emergency door has been sealed since the incident.');S.f.plexiIncidentSeen=1;S.ob.plexiScene='read';S.san=Math.max(0,S.san-18);S.th2=S.th2||[];S.th2.push('I watched a scientist die behind reinforced glass. The creature was real.');
 lg('Witnessed the containment incident. The observation area is permanently damaged.');render();modal('Behind the plexiglass',`<div class="unique-event"><div class="plexi-vignette" role="img" aria-label="A shadowy creature approaches a containment scientist behind reinforced glass"><span class="plexi-figure"></span><span class="plexi-creature"></span><span class="plexi-glass"></span></div><p>A scientist staggers to the glass and begs you to release the latch. Behind him a dark, jointed figure rises from beneath the examination bench.</p><p>${sceneDetail('The figure seizes him and tears through his protective suit. Blood spatters across the plexiglass as he vanishes beneath its limbs.','The emergency lamps go out as something lunges. The scientist’s scream ends in a heavy impact. When the lights return, the glass is smeared and the room is empty.')}</p><p class="unique-thought">He saw me. He thought I could save him.</p></div><button class="btn p" onclick="closeModal()">Back away</button>`);
}
function speakResearcher(){if(S.f.researcherSpoken)return interaction("The researcher's intercom has gone dead. His security badge is still on the desk.");S.f.researcherSpoken=1;S.ob.b2NPC='read';S.th2.push('A surviving researcher said Bela was the proof, not the person responsible.');render();modal('Surviving staff',`<div class="unique-event"><p>The researcher keeps a hand on the emergency switch. He asks whether you are “the first version.” You say you don't understand.</p><p>“Of course you don't. You didn't remember last time either. Bela was never running the experiment. She was evidence that it worked.”</p><p>He flees when a containment alarm sounds, leaving his badge on the counter.</p></div><button class="btn p" onclick="closeModal()">Keep moving</button>`)}
function useDeconPanel(){if(S.f.decon){return interaction('The decontamination lock has disengaged. The inner doors stand open.')}if(!S.docs.includes('B2 Containment Shift Report'))return interaction('The interlock warns that the chamber must be checked against the containment incident report.');S.f.decon=1;S.ob.deconSwitch='done';lg('Decontamination lock reset using the incident report.');interaction('The interlock runs its safety test. Three amber lights become white; a door releases with a hiss.');render()}
function hearRadio(){const key='radio_'+S.room;if(S.f[key])return interaction('Only steady static remains. Whatever was transmitted has passed.');S.f[key]=1;const possibilities=['“If this message reaches the wards, do not answer the second knock.”','“All personnel. The patient is awake. The patient does not know it.”','“Bela has asked us to shut down continuity. Request denied.”'];const line=possibilities[hashSeed(S.seed+'::'+S.room)%possibilities.length];interaction('The radio crackles: '+line+' Then the carrier dies.');S.th2.push('Radio transmission: '+line);lg('A brief radio transmission came through.');S.san=Math.max(0,S.san-2);render();}
function triggerServiceTrap(){if(S.f.trapUsed)return interaction('The overhead hoist has collapsed. The lever does nothing.');const p=initPursuer();if(!p.active)return interaction('The suspended load could delay something very large, but pulling it now would waste the trap.');if(!['laundry','ward','eastcorridor'].includes(p.room))return interaction('The pursuer is too far from the hoist. I need to wait until it comes closer.');S.f.trapUsed=1;S.ob.traplever='done';p.cooldown=Math.max(8,p.cooldown||0);p.noise=0;p.room='ward';lg('Released the laundry hoist, staggering Subject X.');interaction('The lever snaps. The suspended machinery crashes across the service passage. Heavy footsteps stop beneath the debris—then begin again, slower.');soundEffect('impact');render();}
function reinforceWindow(){if(S.f.windowBarricaded)return interaction('The window is reinforced. No infected can climb through this opening.');if(!has('Wooden Plank'))return interaction('The glass is cracked and vulnerable. One sturdy plank would secure it.');rem('Wooden Plank',1);S.f.windowBarricaded=1;S.ob.windowBoard='done';lg('Boarded up the cracked east-wing window.');interaction('You secure the plank over the broken glass. The corridor feels a little less exposed.');soundEffect('door');render();}

function inspectLiftControls(){if(S.f.liftDescended)return inspectLiftControlsLegacy();if(!S.f.power)return interaction('The lift is still without power.');if(!S.f.photoPuzzleSolved)return interaction('The elevator terminal requires a Monolith executive authorization. Perhaps the powered Security portraits contain the missing identity.');if(!S.f.pursuerStarted||!(S.f.pursuerEscapes>0))return interaction('The containment elevator remains shuttered while Subject X is active in the service passages. I must survive its pursuit and get clearance before descending.');if(!S.f.chapter1Revelation){
 S.f.chapter1Revelation=1;S.docs.push('Lift Security Transcript');S.th2=S.th2||[];S.th2.push('Blackridge recorded me participating in LULLABY before I woke here. The footage shows me working the procedure controls.');lg('Chapter 1 revelation: a security recording confirms your involvement in LULLABY.');render();
 modal('Chapter 1 — The record',`<div class="unique-event"><p>Before the elevator opens, an old monitor activates. On its screen, you stand at an operating console. The recording is dated days before your admission.</p><p>The man on the recording has your hands, your voice, your bloodstained wristband. He authorizes a LULLABY trial.</p><p>There is no mistaking him. <b>You worked on Project LULLABY.</b> But the recording cannot tell you whether you chose it, were forced, or are even the original man.</p><p class="unique-thought">I wasn't just a patient. What did I help them do?</p></div><button class="btn p" onclick="finishChapterOneReveal()">Face the elevator</button>`);const x=$('m').querySelector('.mh button');if(x)x.remove();return;
 }inspectLiftControlsLegacy()}
function finishChapterOneReveal(){$('m').innerHTML='';inspectLiftControlsLegacy()}
DOCS['Lift Security Transcript']='SECURITY VIDEO — ELEVATOR TRANSFER\n\nA male operator with the protagonist’s appearance and voice orders a LULLABY procedure to begin. The patient field is blank; the witness name is BELA / J-09.\n\nThe date predates his documented admission to Blackridge. This proves participation, not why he participated.';
function mirroredHallucination(){if(S.f.mirrorHallucination){return interaction('The reflection is ordinary now. The voice you heard has not returned.')}S.f.mirrorHallucination=1;S.ob.vaultFigure='read';modal('A figure at the mirror',`<div class="unique-event"><p>A human outline stands in the glass where your reflection should be. Its shadow points in the wrong direction, and you cannot hear it breathe.</p><p class="unique-thought">If this is real, it is waiting for me. If it isn't, what does that make me?</p></div><button class="btn" onclick="decideHallucination(false)">Wait and observe</button><button class="btn p" onclick="decideHallucination(true)">Fire at the figure</button>`);}
function decideHallucination(shoot){if(shoot){const w=W[S.eq];if(!w||!has(S.eq)||(S.ld[S.eq]||0)<=0)return interaction('My hand reaches for a weapon I cannot fire. The figure is already fading.');S.ld[S.eq]--;soundEffect('shot');noise();S.san=Math.max(0,S.san-4);lg('Fired at a hallucination. Lost one round.');}else{S.san=Math.min(100,S.san+3);lg('Waited and recognized a hallucination from its mismatched shadow.');}$('m').innerHTML='';interaction(shoot?'The bullet shatters empty glass. There was never anyone there.':'The figure fades. Its shadow never touched the wall.');render()}
function belaScreen(){if(S.f.belaScreenSeen)return interaction('The footage has ended. Bela was never the one conducting the procedure.');S.f.belaScreenSeen=1;S.ob.atriumScreen='read';S.th2=S.th2||[];S.th2.push('Bela was not my judge. She witnessed the experiment and became its evidence.');interaction('The monitor shows Bela restrained inside the trial chamber as the operator gives orders. The operator has your face.');lg('An alternate recording clarified Bela’s role as a witness and subject.');render();}

// One-time, optional 1990s photographic arrangement puzzle; recorded in the same save flags.
function portraitOrder(){
 const names=['Dr. Kessler','Dr. Rourke','Dr. Blackwell'];
 const scores=names.map(n=>({n,h:hashSeed(S.seed+'::portrait-'+n)})).sort((a,b)=>a.h-b.h);
 return scores.map(v=>v.n);
}
function portraitPuzzle(){
 if(S.f.photoPuzzleSolved)return interaction('The photographs are now in order. A Monolith executive directive is filed in Files.');
 if(!S.f.power)return interaction('The portraits sit behind dark glass. The reading lamp needs generator power before the appointment dates can be seen.');
 const order=portraitOrder(),dates=['1991','1994','1998'];
 const labels=['Dr. Kessler','Dr. Rourke','Dr. Blackwell'].map(n=>({name:n,year:dates[order.indexOf(n)]}));
 const html=labels.map(({name,year})=>`<button class="btn" onclick="portraitChoice('${name}')">${name}<small style="display:block">Appointed ${year}</small></button>`).join('');
 modal('The shift photographs',`<div class="unique-event"><p>Three portraits hang beneath the hospital crest, with the dates exposed by the restored backlight.</p><p>A note on the frame reads: <b>File each appointment from earliest to latest.</b></p><p class="micro">Select the photographs in order. ${S.f.portraitProgress||0} / 3 placed.</p><div class="choice-actions">${html}</div><button class="btn" onclick="closeModal()">Leave them</button></div>`);
}
function portraitChoice(name){const order=portraitOrder(),i=S.f.portraitProgress||0;
 if(name!==order[i]){S.f.portraitProgress=0;interaction('The backing clips resist. The photograph order was wrong.');portraitPuzzle();return}
 S.f.portraitProgress=i+1;
 if(S.f.portraitProgress<3){portraitPuzzle();return}
 S.f.photoPuzzleSolved=1;S.ob.staffPortraits='read';if(!S.docs.includes('Monolith Executive Directive'))S.docs.push('Monolith Executive Directive');
 S.th2=S.th2||[];S.th2.push('Monolith Pharmaceuticals secretly funded LULLABY and ordered Blackridge to conceal the experiments. Bela was listed as company property.');
 lg('The photographs release a hidden company directive.');render();modal('Behind the portraits',`<div class="unique-event"><p>The final photograph clicks into place. A folded executive directive slips from behind the frame. Its letterhead is MONOLITH PHARMACEUTICALS.</p><p>You read it and file the document automatically.</p><p class="unique-thought">A company signed off on all of this. The hospital wasn't the only thing hiding the truth.</p></div><button class="btn p" onclick="closeModal()">Keep the file</button>`);
}
function inspectKennel(){if(S.f.kennelSeen)return interaction('The shattered cages remain open. You keep your distance from the glass.');
 S.f.kennelSeen=1;S.ob.kennelGlass='read';S.san=Math.max(0,(S.san||100)-8);
 const variants=['A sharp bark comes from an empty pen. Then every light in the kennel row dims.','Something growls from behind the ventilation grille. The cages are empty when the sound stops.'];
 const line=variants[hashSeed(S.seed+'::kennel')%variants.length];
 S.th2=S.th2||[];S.th2.push('Monolith tested LULLABY on animals as well as patients. Something escaped the kennels.');
 interaction(line);lg('The kennel encounter will not repeat.');render();modal('The experimental kennels',`<div class="unique-event"><p>${line}</p><p>The identification collars bear the same company emblem as the research files.</p><p class="unique-thought">They experimented on animals down here. What happened to them?</p><p class="micro">Composure shaken.</p></div><button class="btn p" onclick="closeModal()">Leave the glass</button>`);
}
