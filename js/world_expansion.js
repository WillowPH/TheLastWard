/* World expansion: first-floor corridors, map discovery, grounded encounters, Chapter 2 access. */
R.eastcorridor={n:'East Corridor',short:'East Hall',ch:1,x:110,y:290,dark:1,d:'The corridor slopes gently toward the patient wing. Only the emergency EXIT stencil is visible without a light. Someone has dragged a trolley across the tiles; fresh scraping marks end beneath a broken ceiling fixture.',o:[
 ['fixture','Ceiling light','◉','The bulb hums but never settles into a steady glow.',{look:1,th:'The power is out here. I need the flashlight to see the side alcoves.'}],
 ['trolley','Broken trolley','▤','Beneath the dust, a nameplate has been ripped loose.',{look:1,th:'Every wheel is locked. Something pushed this against the far wall.'}],
 ['directory','East wing directory','▥','A damaged board shows the Wards and Pharmacy ahead.',{look:1,th:'I read the corridor names and still cannot remember walking through them.'}],
 ['radioHall','Portable staff radio','◖','The receiver emits faint static between bursts of silence.',{act:'radio'}]
 ]};
D.lw.b='eastcorridor';D.ew={a:'eastcorridor',b:'ward',need:'Staff Access Card'};
D.es={a:'eastcorridor',b:'security',flag:'power'}; // Later powered staff shortcut
R.security.o.push(['mapboard','Folded first-floor plan','▤','An evacuation plan is clipped inside the security cabinet. It can be copied into your map, without taking a carry slot.',{act:'map',mapPart:1}]);
R.laundry.o.push(['serviceMap','Service wing floor plan','▤','A maintenance route diagram is pinned beside the laundry hoist.',{act:'map',mapPart:2}]);
R.archive.o.push(['eastMap','Restricted wing survey','▤','A partially erased architectural survey includes sealed operating corridors.',{act:'map',mapPart:3}]);
// Stage firearms so that the starting exploration and first dark corridor are not trivialized.
const securityGun=R.security.o.find(o=>o[0]==='rev');securityGun[1]='Empty sidearm case';securityGun[3]='A service weapon was signed out to the night nurse. The log lists the Patient Wing.';securityGun[4]={look:1,th:'The pistol is gone. Whoever took it went toward the wards.'};
const securityAmmo=R.security.o.find(o=>o[0]==='reva');securityAmmo[4]={look:1,th:'The ammunition sleeve has been emptied. It is stamped NIGHT SHIFT.'};
R.ward.o.push(['nightPistol','Night nurse’s locked equipment box','▣','A handwritten tag says that the cabinet key belongs at Reception. Its contents might help you survive.',{need:'Cabinet Key',give:[['Handgun',1]]}],['pistolRounds','One paper ammo envelope','▤','Six handgun cartridges wrapped in an old patient receipt.',{give:[['Handgun Ammo',6]]}]);
// Extra optional supplies can be concealed, but never keys or critical progression objects.
for(const [room,id] of [['room12','drw12'],['pharmacy','am'],['coldstore','cacheammo']]){const o=R[room]?.o.find(x=>x[0]===id);if(o)o[4].hidden=1;}
// Help keep loot meaningful: remove uneconomic old weapon cache props already in legacy records.
const obsolete=['smg','smga','rif','rifam','flare','flarea','nailgun','nails'];for(const k in R)R[k].o=R[k].o.filter(o=>!obsolete.includes(o[0]));
// Make rescue/moral decisions a first-floor thread. The event is non-repeatable and persisted.
R.isoward={n:'Isolation Treatment Room',short:'Treatment',ch:1,x:198,y:287,d:'Through a narrow glass slot, a conscious patient pleads with someone who is no longer here. Old restraints bind his wrists. A pressure monitor has no power, and the medicine trolley has been dragged out of reach.',o:[
 ['beggingPatient','The restrained patient','◉','He is lucid enough to ask for help, and terrified of what he is becoming.',{act:'npc'}],
 ['patientTherapy','Treatment trolley','✚','A closed cabinet bears the emergency treatment protocol.',{look:1,th:'There is enough equipment to attempt basic care, but no clean sedative.'}],
 ['patientFile','Isolation admission chart','▤','The chart describes a reversible infection stage, but its conclusion has been crossed out.',{doc:'Isolation Patient Chart'}]
]};D.wi={a:'ward',b:'isoward'};
DOCS['Isolation Patient Chart']='ISOLATION OBSERVATION — PATIENT 14\n\nPatient remains lucid. Agitation and pain increasing. Stage II conversion may be reversible with sedation and monitored treatment. Isolation should be maintained. Do not assume every infected patient is beyond help.\n\nLast notation: “We ran out of treatment supplies before we ran out of patients.”';
// First chapter ends with a meaningful revelation before the service lift opens to Chapter 2.
R.b2gallery={n:'Plexiglass Research Gallery',short:'Gallery',ch:2,x:190,y:67,d:'A row of reinforced plexiglass doors separates the observation gallery from containment cells. One console remains active. The emergency lighting washes the floor with a weak violet pulse.',o:[
 ['plexiScene','The observation chamber','◈','A scientist pounds on a reinforced pane while a large shape moves behind him.',{act:'plexi'}],
 ['plexiReport','Containment shift report','▤','A clipboard lies beneath the viewing slot.',{doc:'B2 Containment Shift Report'}],
 ['b2Hide','Narrow equipment alcove','▣','There is space to crouch out of sight between the storage cases.',{act:'hide'}]
]};
R.b2decon={n:'Decontamination Lab',short:'Decon Lab',ch:2,x:260,y:65,d:'Steel wash stations line a medical examination chamber. Here the equipment is clean and the staff labels are new. A surviving researcher waits near a powered intercom with an anxious look.',o:[
 ['deconSwitch','Decontamination console','▥','A three-switch isolation sequence is printed beneath the glass.',{act:'decon'}],
 ['deconFile','Sublevel personnel register','▤','An updated staff register includes names missing from public hospital records.',{doc:'Sublevel Personnel Register'}],
 ['b2NPC','Surviving researcher','◉','The researcher keeps checking the door, trying to decide whether to trust you.',{act:'researchNpc'}]
]};
R.b2sleep={n:'Research Staff Dormitory',short:'Dormitory',ch:2,x:320,y:65,d:'Four narrow bunks and an overturned chair. A portable radio whispers through static. Someone has scratched an apology into the paintwork above a bed.',o:[
 ['bunkFile','A frightened note','▤','A note folded under the lower bunk.',{doc:'Dormitory Apology'}],
 ['b2Rations','Staff locker','▣','A food parcel and a small medical kit remain.',{give:[['Trauma Dressing',1]]}],
 ['b2Radio','Portable radio','◖','A compact receiver sits beside an unplugged clock.',{act:'radio'}]
]};
D.b2g={a:'containment',b:'b2gallery'};D.b2d={a:'b2gallery',b:'b2decon',flag:'decon'};D.b2s={a:'b2decon',b:'b2sleep'};
DOCS['B2 Containment Shift Report']='B2 CONTAINMENT SHIFT — INCIDENT 12\n\nDo not open the plexiglass doors while the subjects are agitated. The cells have no ordinary emergency release. A staff scientist reports hearing footsteps in an empty chamber.\n\nDr. Malcolm Webb requests all recordings be preserved, not destroyed.';
DOCS['Sublevel Personnel Register']='RESTRICTED STAFF ROSTER\n\nChief of Continuity: Dr. Blackwell. Research witness: J-09 / Bela. Escort field: SUBJECT X. Security intake signatures were removed using chemical bleaching.\n\nRemark: the same man has signed the shift register on dates before his recorded admission.';
DOCS['Dormitory Apology']='I heard the machine speak in my daughter’s voice. That was the point I understood we had made something wrong.\n\nWe kept saying the reconstruction was a patient. Nobody wanted to say who had been reconstructed. I cannot stay here.';
// This is an additive chapter assignment, not a replacement for the existing saved room graph.
for(const k of ['sublevel','containment','observation','lab','specimen','powercontrol','coldstore','isolation','sealgate'])if(R[k])R[k].ch=2;
R.core.ch=3;
// Bela is a LULLABY witness/subject, not a mandatory 34-HP boss.
// The finale is resolved through evidence and the player's choice, not an ammo softlock.
delete E.core;
// Keep key progression rooms from becoming hidden random-loot opportunities.
for(const k in R)for(const o of R[k].o){const sp=o[4];if(sp.need||sp.flag||sp.code||sp.seq||sp.doc||sp.expand||sp.need3||sp.act==='map')sp.hidden=0;}
// A limited, visible barricade resource; not a progression key and never required.
R.eastcorridor.o.push(['windowBoard','Cracked ward window','▤','The glass is fractured and an infected silhouette passes outside at night.',{act:'barricade'}]);
R.laundry.o.push(['sparePlank','Dry wooden plank','▰','One usable plank rests beneath a broken laundry pallet.',{give:[['Wooden Plank',1]]}],['laundryhide','Supply locker hiding place','▣','A narrow steel locker stands just beyond the row of washers.',{act:'hide'}],['traplever','Overhead hoist release','⬇','The rusty emergency lever would drop a heavy machine across the service passage.',{act:'trap'}]);
ICON['Wooden Plank']='▰';STK['Wooden Plank']=2;
// Only spawns if the exposed window is left unboarded past the pursuer milestone.
E.eastcorridor={n:'Window-breach infected',hp:7,dmg:[3,6]};

// Patient names are a clue, never an impossible remembered identity.
const nameBoard=R.ward.o.find(o=>o[0]==='nb');nameBoard[3]='A cracked ward board lists M. CALLAHAN, A. HART, B. KELLER and three names erased with solvent. One surname makes your hand hesitate.';nameBoard[4]={look:1,th:'Callahan. That name feels familiar, but I cannot tell whether it belongs to me or someone I knew.',sn:4};
// Chapter 3: a separate memory reconstruction wing with its own documents and two locks.
R.memoryvault={n:'Continuity Memory Vault',short:'Memory Vault',ch:3,x:70,y:260,d:'The last wing does not resemble the hospital. Cabinets hold sealed film reels, labelled by what their owners no longer remember. A medical camera stands pointed at a chair bolted to the floor.',o:[
 ['vaultDocket','Memory vault docket','▤','A record of a numbered dedication date used by the old hospital.',{doc:'Memory Vault Docket'}],
 ['memDoor','Chronology keypad','▥','Four numbers. The adjacent docket links it to a date the original staff were told to remember.',{code:'0000',flag:'memoryLock'}],
 ['vaultReel','Damaged memory reel','◈','The speaker repeats a man saying he cannot bear another reconstruction.',{look:1,th:'I know this voice. It sounds like me pleading with someone to stop.'}],
 ['vaultFigure','Something in the mirror','◉','An impossibly still figure waits where the glass ought to reflect your face.',{act:'hallucination'}]
]};
R.mirrorward={n:'Reconstruction Ward',short:'Reconstruction',ch:3,x:170,y:260,d:'Beds have been placed in a perfect circle around a central light. Their monitors show identical heartbeats at different times. A childlike voice hums behind the wall, then stops abruptly.',o:[
 ['echoFile','Continuity calibration note','▤','A maintenance note describes the order of the three signal colours.',{doc:'Continuity Calibration Note'}],
 ['echoConsole','Echo alignment panel','▥','Three coloured buttons must be pressed in the order recorded by maintenance.',{seq:'RGB',flag:'memoryStable'}],
 ['echoWard','Patient observation mirror','◈','A figure blinks a second after you do.',{look:1,th:'I can see the other beds. All of them have my wristband number.'}]
]};
R.continuityatrium={n:'Continuity Atrium',short:'Atrium',ch:3,x:260,y:260,safe:1,d:'A final observation corridor leads toward the core chamber. Beyond the glass, recordings of the protagonist and Bela play out of sequence. Nothing in the archive proves which recording came first.',o:[
 ['atriumRecord','The final witness transcript','▤','A typed exchange between the first operator and the witness.',{doc:'Final Witness Transcript'}],
 ['atriumTerminal','Continuity Terminal','▤','An old field terminal stands ready beside the sealed door.',{act:'save'}],
 ['atriumCache','Supply locker','▣','A shared storage box has been moved into the final corridor.',{act:'box'}],
 ['atriumScreen','Bela on the monitor','◈','A recording plays with the sound turned down. It resembles the same moment from another point of view.',{act:'belaScreen'}]
]};
D.sc.b='memoryvault';D.mv={a:'memoryvault',b:'mirrorward',flag:'memoryLock'};D.va={a:'mirrorward',b:'continuityatrium',flag:'memoryStable'};D.acore={a:'continuityatrium',b:'core'};
DOCS['Memory Vault Docket']='CONTINUITY ARCHIVES\n\nUse the date from the Memorial Ledger, in the same day-month order, to unlock the memory vault chronology cabinet. An archived copy of the ledger is filed in the Records Annex.\n\nEvery reconstruction is assigned a death date and a date of admission. Neither necessarily identifies the original.';
DOCS['Continuity Calibration Note']='SIGNAL CALIBRATION\n\nAfter the generator incident, the alignment console was reset in the colour order used by the first-floor emergency breaker panel. The order is printed in the Staff Residence diary.\n\nThe vault will not open until all three indicators are stable.';
DOCS['Final Witness Transcript']='BELA / J-09 — WITNESS STATEMENT\n\nI am not the person choosing for him. They taught me to recognize the voice they kept rebuilding.\n\nThe operator insisted that the experiment continue after the first failure. I never learned whether that insistence was his own choice or another recording.\n\nIf he reaches me, let him see what was kept. Then let him decide what to do with it.';

// Chapter 1 optional picture puzzle: powered examination lamp exposes dates on three staff portraits.
// This introduces the corporate antagonist while creating a purposeful return to Security after the generator.
R.security.o.push(['staffPortraits','Three staff portraits','▧','Three faded photographs have appointment dates beneath their frames. The backlight works only once the generator is restored.',{act:'portrait'}]);
DOCS['Monolith Executive Directive']='MONOLITH PHARMACEUTICALS — EXECUTIVE DIRECTIVE 77\n\nThe Blackridge program is to remain outside ordinary hospital oversight. All continuity data, including Bela/J-09 and SUBJECT X, shall remain company property until the next successful reconstruction.\n\nNo survivor, witness, or member of the medical staff is authorized to release this information. The public hospital board will be told there was a maintenance failure.\n\nSigned: MONOLITH EXECUTIVE OFFICE';
// Chapter 2 optional animal experimentation wing. Environmental horror, not another loot dump.
R.b2kennels={n:'Experimental Kennels',short:'Kennels',ch:2,x:317,y:135,dark:1,d:'Behind the observation glass, narrow animal enclosures form two banks. Veterinary restraints and shredded identification collars lie beneath a sink. A metallic scratching comes from an empty cage; no animal is visible.',o:[
 ['kennelGlass','Glass-fronted pen','◈','There are deep scratches on the inside of the pane. One enclosure looks recently occupied.',{act:'kennel'}],
 ['kennelLedger','Veterinary intake ledger','▤','A clinical form lists dogs delivered to Blackridge under the Monolith logo.',{doc:'Animal Trial Register'}],
 ['kennelSink','Veterinary wash station','▣','Surgical wash basins and a hanging restraint. Something struck the glass hard enough to crack the frame.',{look:1,th:'They experimented on animals down here, too. How far did these tests go?'}],
 ['kennelDoors','Containment cage locks','▥','Three cage doors have been forced open from within. A steel security latch keeps the hallway sealed.',{look:1,th:'Whatever was in here escaped. I need to keep listening before I go further.'}]
]};
D.b2k={a:'b2gallery',b:'b2kennels'};
DOCS['Animal Trial Register']='MONOLITH PHARMACEUTICALS — VETERINARY DIVISION\n\nSubject group K-01 through K-09. Species: canine. Objective: observe response to memory imprinting and conditioned voice commands.\n\nTrial 6: animals react to recorded commands that were never played during training. Trial 7: pen interior damaged. Staff told to discontinue night feeding.\n\nTransfer warning: Do not attempt to recover escaped test subjects without containment personnel.';

// Chapter 1 progression: the regulator needs a maintenance kit, not just a fuse.
R.generator.o.push(['regulator','Burned-out generator regulator','⚙','The contacts must be realigned with a proper maintenance tool before installing the fuse.',{act:'regulator'}]);
// Early archives hold the essential fuse but NOT an early shotgun.
const earlyShot=R.archive.o.find(o=>o[0]==='gun');if(earlyShot){earlyShot[1]='Empty long-gun cabinet';earlyShot[3]='A signed-out shotgun was sent to the restricted operating corridor.';earlyShot[4]={look:1,th:'Only its outline remains in the foam. The maintenance requisition mentions Surgery.'};}
const earlyShells=R.archive.o.find(o=>o[0]==='tin');if(earlyShells){earlyShells[3]='An empty ammunition tin.';earlyShells[4]={look:1,th:'The shells were removed for the restricted operating team.'};}
R.surgery.o.push(['lateShotgun','Security shotgun case','▣','A Monolith security shotgun is secured with the executive access latch. The case can be opened after power and the staff-photo archive are restored.',{act:'lateShotgun'}]);
// Physical containment and an explorable exit object, never an unexplained map edge.
R.lobby.o.push(['sealedExit','Main entrance — chained','▥','Thick chains run through the rain-streaked glass handles; mechanical bolts hold the emergency shutters.',{look:1,th:'The chains are outside the doors. Someone locked us inside on purpose. MONOLITH — Preserving Life. Securing Peace.'}]);
R.eastcorridor.o.push(['emergencyExit','Bolted fire exit','▥','Steel bolts and a containment shutter bar the stairwell.',{look:1,th:'The fire route is sealed from the other side. This lockdown was designed to keep people in as well as keep something out.'}]);
// No casual elevator shortcut: return after the first-floor story and pursuit.
D.liftEntry.flag='chapter1Ready';
// Move late-story observation and final research room upstairs without adding new underground content.
R.observation.ch=1;
R.records.o.push(['finalJournal','Researcher’s abandoned notebook','▤','The last entry is dated after the laboratory was evacuated.',{act:'finalJournal'}]);
R.eastcorridor.o.push(['staffSprinkler','Damaged sprinkler valve','▣','Water gathers around a snapped copper pressure line.',{act:'sprinkler'}]);
R.ward.o.push(['nightJournal','Night attendant journal','▤','Loose diary pages, some dated and others barely legible.',{doc:'Night Attendant Journal'}]);
DOCS['Night Attendant Journal']='SEPTEMBER 12, 1998\n\nThey reassigned me to the East Wing again. I promised Evelyn I would finish the shift and go home. The new patients cannot receive visitors, and security keeps asking which doors I have opened.\n\nSEPTEMBER 14, 1998\n\nMy hands ache. Kessler says it is exhaustion. I keep finding my own handwriting on notes I cannot remember writing. Someone spoke to me from inside the vents.\n\nSEPTEMBER 16\n\nShaw stopped speaking to me. I have forgotten the number to my own locker. It is written here somewhere. Need to stop hearing the tapping.\n\n17\n\ndoors breathe. no clock. they say my name.\n\nnot mine. not mine. not';
DOCS['Monolith Executive Directive']='MONOLITH PHARMACEUTICALS\nPreserving Life. Securing Peace.\n\nCONTAINMENT DIRECTIVE 09-17 — GRAHAM STRICKLAND\n\nExterior evacuation remains forbidden. Reinforcement shutters and exterior chain locks must not be disengaged, irrespective of surviving staff. The continuation of LULLABY is classified above facility-level emergency authority.\n\nAuthorized by CEO RICHARD HALBROOK.';

D.go.flag='power'; // The observation ward is reachable after generator repair, before the elevator descent.
