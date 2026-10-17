/* Illustrated room scenes. Every doorway comes from D, the same source used by travel and the map.
   The scene's distinctive physical objects are placed in fixed coordinates, not rendered as a list. */
const SCENE_CONFIG={
 lobby:{style:'reception',sites:[['Reception desk','desk','desk','int'],['Staff locker','locker','lock','coat'],['Payphone','phone','payphone','win'],['Field cache','crate','box'],['Continuity Terminal','screen','term']]},
 security:{style:'security',sites:[['Monitor wall','screen','cam','rep2'],['Security desk','desk','rep','drw','ros','cof'],['Equipment cabinet','locker','rev','reva'],['Floor plan rack','paper','mapboard'],['Staff portraits','paper','staffPortraits']]},
 eastcorridor:{style:'corridor',sites:[['Emergency lighting','lamp','fixture'],['Broken trolley','cart','trolley'],['Old wall directory','paper','directory','radioHall','windowBoard']]},
 ward:{style:'ward',sites:[['Patient name boards','paper','nb'],['Nurses station','desk','gur','drg'],['Pharmacy entry panel','screen','kp']]},
 room12:{style:'patient',sites:[['Patient bed','bed','file','rs','drw12'],['Medical cabinets','locker','cab','shf','shf2'],['Instrument tray','cart','tray12','nailgun','nails']]},
 archive:{style:'records',sites:[['Archive shelves','books','memo','tin','fus'],['Gun cabinet','locker','gun'],['Memorial plaque','screen','cat','flr'],['Discreet drawer','desk','hid','eastMap']]},
 generator:{style:'power',sites:[['Generator controls','machine','pan','log'],['Maintenance tools','cart','stb','bt2','charger'],['Continuity station','screen','term2','box2'],['Abandoned equipment','locker','smg','smga']]},
 observation:{style:'glass',sites:[['Observation window','glass','glasssound'],['Records terminal','screen','tr','con','dr']]},
 core:{style:'core',sites:[['LULLABY console','screen','fin']]},
 pharmacy:{style:'pharmacy',sites:[['Dispensing counter','desk','rib','am'],['Medicine fridge','locker','med','shelf5'],['Storage shelves','books','shelf2','shelf3','shelf4'],['Maintenance shelf','cart','bat','bol']]},
 chapel:{style:'chapel',sites:[['Reliquary','altar','rel'],['Chaplains desk','desk','let'],['Storage cabinet','locker','box3']]},
 morgue:{style:'morgue',sites:[['Cold drawer no.12','locker','dw'],['Autopsy records','paper','aut'],['Supply trolley','cart','sh','flare','flarea']]},
 lab:{style:'lab',sites:[['Centrifuge','machine','cen'],['Research desk','desk','ln'],['Armory safe','locker','sf','sfmag','sfram','sfmed'],['Weapon rack','rack','rif','rifam']]},
 sealgate:{style:'gate',sites:[['Seal mechanism','machine','gt']]},
 residence:{style:'residence',sites:[['Nightstand and diary','desk','dia'],['Breaker board','screen','brk'],['Field terminal','screen','term4']]},
 tunnel:{style:'tunnel',sites:[['Winch assembly','machine','wnc'],['Chained lock','locker','tk'],['Flood mark','paper','dvn','uv']]},
 boiler:{style:'boiler',sites:[['Old furnace','machine','fur','fl'],['Pressure pipes','pipe','pip'],['Tool compartment','locker','mag']]},
 laundry:{style:'laundry',sites:[['Laundry machines','machine','lau','lauant'],['Service chute','pipe','chute'],['Equipment bench','desk','pouch','tag','serviceMap'],['Overhead hoist','machine','traplever'],['Hide behind linens','locker','laundryhide']]},
 children:{style:'children',sites:[['Children’s drawings','paper','draw'],['Toy chest','crate','toy','neg']]},
 records:{style:'records',sites:[['Ledger table','desk','ledger','cab2','lasttape'],['Sealed partition','gate','wall']]},
 surgery:{style:'surgery',sites:[['Operating table','bed','opnote'],['Surgical instruments','cart','tray','mask']]},
 isolation:{style:'isolation',sites:[['Observation mirror','glass','mirror'],['Isolation charts','paper','isolog'],['Medicine shelf','locker','medcab','medgauze']]},
 specimen:{style:'lab',sites:[['Specimen registry','desk','specdoc'],['Sample rack','rack','dev','wire']]},
 powercontrol:{style:'power',sites:[['Relay controls','machine','relays','pwrmemo'],['Service shelf','cart','parts2']]},
 stafflounge:{style:'lounge',sites:[['Staff noticeboard','paper','loungeNote'],['Kitchenette','desk','coffee','sink'],['Utility locker','locker','harness']]},
 lift:{style:'elevator',sites:[['Freight controls','screen','liftpanel','liftlog'],['Mirror','glass','liftmirror']]},
 sublevel:{style:'sublevel',sites:[['Continuity station','screen','lowerterminal','lowerbox','lowerribbon'],['Admissions desk','desk','admissions'],['Security shutter','gate','lowerdoor']]},
 containment:{style:'containment',sites:[['Observation bay','glass','lowerglass'],['Access panel','screen','lowerrecord'],['Ceiling speaker','lamp','lowervoice']]},
 coldstore:{style:'cold',sites:[['Frozen evidence','locker','coldlog','reel','cacheammo','cachemed']]},
 memoryvault:{style:'records',sites:[['Archival docket','paper','vaultDocket'],['Chronology keypad','screen','memDoor'],['Film reels','rack','vaultReel'],['Mirror','glass','vaultFigure']]},
 mirrorward:{style:'patient',sites:[['Calibration note','paper','echoFile'],['Alignment panel','screen','echoConsole'],['Patient glass','glass','echoWard']]},
 continuityatrium:{style:'containment',sites:[['Final witness file','paper','atriumRecord'],['Field terminal','screen','atriumTerminal'],['Storage locker','locker','atriumCache'],['Observation screen','glass','atriumScreen']]},
 isoward:{style:'patient',sites:[['Patient restraints','bed','beggingPatient'],['Treatment trolley','cart','patientTherapy'],['Observation clipboard','paper','patientFile']]},
 b2gallery:{style:'glass',sites:[['Plexiglass enclosure','glass','plexiScene'],['Emergency console','screen','plexiReport'],['Security locker','locker','b2Hide']]},
 b2decon:{style:'lab',sites:[['Decontamination controls','machine','deconSwitch'],['Records cabinet','books','deconFile'],['Researcher intercom','screen','b2NPC']]},
 b2sleep:{style:'residence',sites:[['Bunk and belongings','bed','bunkFile'],['Locker','locker','b2Rations'],['Portable radio','screen','b2Radio']]},
 b2kennels:{style:'kennels',sites:[['Observation pen','glass','kennelGlass'],['Veterinary ledger','paper','kennelLedger'],['Wash station','cart','kennelSink'],['Containment locks','gate','kennelDoors']]}
};
const SCENE_SITE_POS=[[27,70],[65,69],[47,43],[80,84],[14,84]];
// Hotspot locations are associated with the actual furniture and vary by room identity.
const SCENE_ROOM_POS={
 lobby:[[30,72],[68,73],[48,43],[84,86],[76,43]],
 security:[[31,35],[40,78],[77,71],[61,45]],
 eastcorridor:[[47,24],[35,72],[73,56]],
 ward:[[55,43],[31,76],[80,69]],
 room12:[[35,70],[75,63],[53,80]],
 laundry:[[29,66],[75,47],[44,80],[82,25],[15,47]],
 generator:[[43,53],[25,79],[77,46]],
 pharmacy:[[35,80],[76,52],[26,40],[79,83]],
 lift:[[49,55],[74,40]],
 isoward:[[35,73],[70,70],[75,40]],
 b2gallery:[[55,37],[27,79],[77,72]],
 memoryvault:[[28,65],[70,76],[29,33],[76,38]],
 mirrorward:[[26,45],[50,72],[78,48]],
 continuityatrium:[[27,51],[54,78],[80,75],[75,36]]
};
const SCENE_STYLE_POS={
 security:[[33,35],[42,78],[76,72],[62,47],[85,78]],
 corridor:[[45,26],[38,76],[72,60],[80,82]],
 patient:[[32,71],[75,65],[53,44],[78,81]],
 records:[[25,48],[69,56],[47,38],[72,82]],
 pharmacy:[[33,77],[77,52],[25,42],[78,82]],
 power:[[48,52],[26,76],[74,42],[83,78]],
 glass:[[54,45],[25,74],[78,72]],
 lab:[[45,45],[29,77],[73,63],[78,38]],
 morgue:[[28,68],[50,44],[76,72]],
 residence:[[28,77],[65,49],[82,72]],
 laundry:[[32,64],[74,41],[42,80],[80,27],[17,52]],
 sublevel:[[53,46],[29,79],[78,66]],
 containment:[[51,47],[27,71],[79,42]]
};
// Door and prop hotspots share one collision-aware coordinate system. Coordinates are % of 800×330.
const SCENE_DOOR_POS=[[8,30],[91,30],[49,24],[8,71],[91,71],[31,22],[71,22],[49,70]];
function sceneLayout(doors,groups,room){
 const n=doors.length,doorPlaces=[],itemPlaces=[];
 const byCount={1:[49],2:[10,90],3:[9,50,91],4:[8,34,66,92],5:[7,28,50,72,93],6:[7,24,41,59,76,93],7:[7,22,36,50,64,78,93]};
 const xs=byCount[n]||Array.from({length:n},(_,i)=>8+i*84/Math.max(1,n-1));
 xs.forEach((x,i)=>doorPlaces.push([x,26+(i%2===0?0:2)]));
 const hash=hashSeed(room+'::furniture');
 const locations=[[27,80],[70,81],[49,69],[15,73],[84,74],[35,65],[65,63],[49,87],[19,87],[80,87],[36,56],[65,55]];
 for(let i=0;i<groups.length;i++){
  const preferred=[groups[i].x,groups[i].y],choices=[preferred,...locations.slice(hash%locations.length),...locations.slice(0,hash%locations.length)];
  const collision=(pt,other,dx,dy)=>Math.abs(pt[0]-other[0])<dx&&Math.abs(pt[1]-other[1])<dy;
  let chosen=choices.find(pt=>!doorPlaces.some(d=>collision(pt,d,17,44))&&!itemPlaces.some(q=>collision(pt,q,14,23)));
  if(!chosen)chosen=choices.find(pt=>!doorPlaces.some(d=>collision(pt,d,12,34))&&!itemPlaces.some(q=>collision(pt,q,10,16)));
  itemPlaces.push((chosen||preferred).slice());
 }
 return {doorPlaces,itemPlaces};
}
// A different structural silhouette and period-appropriate signage for every room, even when rooms share a furniture category.
function roomSignature(room){
 const name=(R[room]?.n||room).toUpperCase(),h=hashSeed(room+'::scene'),kind=(SCENE_CONFIG[room]?.style||'corridor');
 const title=htmlSafe(name.length>24?name.slice(0,24):name);
 const marks=Array.from({length:3},(_,i)=>{const x=65+((h>>((i*7)%23))%650),y=30+((h>>((i*5+3)%21))%175);return `<path d="M${x} ${y}l${(i%2?19:-13)} 13 l7 -17" stroke="#9a857f" opacity=".16" stroke-width="1.6" fill="none"/>`}).join('');
 const adorn={security:'<path d="M50 176H742" stroke="#73818b" stroke-width="5" stroke-dasharray="8 13"/>',patient:'<path d="M90 159H708" stroke="#8a6972" stroke-width="3" opacity=".65"/>',corridor:'<path d="M395 12v178" stroke="#858b8f" stroke-width="4" stroke-dasharray="17 29" opacity=".38"/>',power:'<path d="M40 120H755" stroke="#9e7e60" stroke-width="7" stroke-dasharray="22 12" opacity=".35"/>',lab:'<circle cx="674" cy="110" r="48" fill="none" stroke="#728a91" opacity=".37" stroke-width="4"/>',kennels:'<path d="M0 140H800" stroke="#8a827c" stroke-width="4" opacity=".35"/>',glass:'<path d="M64 165L720 70" stroke="#8ba0a5" opacity=".3" stroke-width="5"/>',pharmacy:'<path d="M72 145H735" stroke="#a59b88" stroke-width="3" stroke-dasharray="30 8" opacity=".4"/>'}[kind]||'';
 return `<svg class="room-signature" viewBox="0 0 800 330" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${adorn}${marks}<g opacity=".85"><rect x="280" y="13" width="240" height="32" rx="2" fill="#26242a" stroke="#7a7071" stroke-width="1.4"/><text x="400" y="34" font-family="Roboto,Arial" text-anchor="middle" font-size="15" fill="#e4d7cf" letter-spacing="1">${title}</text></g></svg>`;
}

const SCENE_COLOR={kennels:'#827b76',reception:'#9b6e64',security:'#768b9c',corridor:'#828999',ward:'#8f8691',patient:'#8995a3',records:'#978576',power:'#ad845f',glass:'#788f9d',core:'#ad6378',pharmacy:'#8e9991',chapel:'#9c8b86',morgue:'#7d9aa5',lab:'#829aa8',gate:'#a26c78',residence:'#9d8c7b',tunnel:'#657a87',boiler:'#b28565',laundry:'#918a86',children:'#938b9b',surgery:'#9b8287',isolation:'#778f9d',lounge:'#9a8f7a',elevator:'#8e96a0',sublevel:'#7da0ad',containment:'#8aa7a9',cold:'#8caabc'};
function htmlSafe(s){return String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;')}
function sceneArchitecture(style){
 const s=SCENE_COLOR[style]||'#8a8490';let elements='';
 const furniture=(x,y,w,h,shade='#333a41')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${shade}" stroke="#78818a" stroke-width="1.3"/><path d="M${x+7} ${y+10} H${x+w-7}" stroke="${s}" opacity=".5"/>`;
 switch(style){
 case 'kennels':elements=Array.from({length:5},(_,i)=>`<rect x="${52+i*140}" y="63" width="117" height="160" fill="#192025" stroke="#727e84" stroke-width="4"/><path d="M${62+i*140} 65V223M${86+i*140} 65V223M${110+i*140} 65V223M${135+i*140} 65V223" stroke="#535962" stroke-width="3"/>`).join('')+furniture(230,257,335,49,'#4c4243');break;
 case 'reception':elements=furniture(118,203,280,68,'#434448')+furniture(450,126,82,157,'#484b51')+`<rect x="585" y="78" width="100" height="118" fill="#1c252d" stroke="#85919a" stroke-width="4"/><path d="M635 78V196M585 134H685" stroke="#46555c"/><text x="249" y="228" text-anchor="middle" font-size="16" fill="#c4afa6">RECEPTION</text>`;break;
 case 'security':elements=Array.from({length:5},(_,i)=>`<rect x="${84+i*121}" y="55" width="104" height="88" rx="4" fill="#101d27" stroke="#596977" stroke-width="4"/><path d="M${90+i*121} 110 l33 -17 20 11 24 -35" stroke="#5d8083" opacity=".5" fill="none"/>`).join('')+furniture(180,218,395,60);break;
 case 'corridor':elements=`<path d="M235 0 L560 0 L730 330 L70 330Z" fill="#293036" stroke="#5f6068" stroke-width="3"/><path d="M356 0 L443 0 L480 180 L318 180Z" fill="#101519" stroke="#555d66" stroke-width="3"/><path d="M0 90H238M562 90H800M0 164H175M625 164H800" stroke="#888b94" stroke-width="4" opacity=".35"/>`;break;
 case 'patient':case 'isolation':case 'surgery':elements=furniture(173,177,308,105,'#4a5358')+`<rect x="191" y="185" width="85" height="32" rx="6" fill="#8d9090"/><rect x="178" y="226" width="294" height="46" fill="#676e70"/><path d="M180 219H472" stroke="#b5b1ae" stroke-width="2"/>`+furniture(565,142,87,164);break;
 case 'pharmacy':case 'records':case 'cold':elements=Array.from({length:5},(_,i)=>furniture(74+i*129,54,108,175,i%2?'#343d45':'#3f4144')).join('')+furniture(170,248,439,52);break;
 case 'power':case 'boiler':elements=furniture(186,101,385,167,'#48454b')+Array.from({length:5},(_,i)=>`<circle cx="${230+i*70}" cy="150" r="16" fill="#232a2e" stroke="#9f9c8d" stroke-width="3"/>`).join('')+`<path d="M0 100H184 M572 110H800" stroke="${s}" stroke-width="9" opacity=".35"/>`;break;
 case 'glass':case 'containment':case 'lab':case 'sublevel':case 'core':elements=`<rect x="115" y="31" width="570" height="217" rx="5" fill="#18282d" stroke="#74838d" stroke-width="8"/><path d="M305 31V248M494 31V248M115 137H685" stroke="#65747e" stroke-width="6"/><path d="M150 45 L272 224 M340 43 L454 227" stroke="#708792" stroke-width="1" opacity=".35"/>`+furniture(344,221,127,58);break;
 case 'morgue':elements=Array.from({length:4},(_,i)=>furniture(114+i*143,92,126,139,'#4a555f')).join('')+Array.from({length:4},(_,i)=>`<path d="M${126+i*143} 130H${224+i*143} M${126+i*143} 188H${224+i*143}" stroke="#abb5b8" opacity=".5"/>`).join('');break;
 case 'elevator':case 'gate':elements=`<rect x="200" y="17" width="400" height="253" fill="#222930" stroke="#9d9ea4" stroke-width="9"/><path d="M400 17 V270" stroke="#a5a5a9" stroke-width="7"/>`+furniture(625,114,49,125);break;
 case 'chapel':elements=`<path d="M390 22V179 M345 68H435" stroke="#8c7780" stroke-width="13"/>`+furniture(250,219,305,57,'#4c3a3d');break;
 case 'children':elements=furniture(184,210,384,61)+`<path d="M179 106 Q205 84 232 108 T288 108 T344 108 T400 108" fill="none" stroke="#997f8a" stroke-width="3"/>` ;break;
 case 'tunnel':elements=`<path d="M75 160 Q390 -240 725 160L725 299H75Z" fill="#1c252f" stroke="#68737c" stroke-width="8"/><path d="M80 284 Q390 244 720 290" stroke="#4b647c" stroke-width="14"/>`;break;
 case 'laundry':elements=Array.from({length:4},(_,i)=>`<rect x="${120+i*151}" y="111" width="126" height="152" rx="5" fill="#444b50" stroke="#77818a" stroke-width="4"/><circle cx="${183+i*151}" cy="191" r="44" fill="#20292d" stroke="#879098" stroke-width="6"/>`).join('');break;
 default:elements=furniture(147,202,360,76)+furniture(560,92,92,166);
 }
 return `<svg class="scene-paint" viewBox="0 0 800 330" preserveAspectRatio="xMidYMid slice" role="presentation" aria-hidden="true"><defs><linearGradient id="wallGrad" x1="0" y1="0" x2=".2" y2="1"><stop stop-color="#34353b"/><stop offset="1" stop-color="#171b22"/></linearGradient><linearGradient id="floorGrad" x1="0" y1="0" x2=".2" y2="1"><stop stop-color="#2a282e"/><stop offset="1" stop-color="#131318"/></linearGradient></defs><rect width="800" height="330" fill="url(#wallGrad)"/><path d="M0 251H800V330H0Z" fill="url(#floorGrad)"/><path d="M0 251H800 M0 0V251 M800 0V251" stroke="${s}" stroke-width="3" opacity=".55"/><path d="M0 298H800 M0 319H800 M220 251L130 330 M400 251V330 M580 251L670 330" stroke="#4d4850" opacity=".42" fill="none"/>${elements}<path d="M0 20H800" stroke="${s}" stroke-width="4" opacity=".25"/><rect width="800" height="330" fill="#07080e" opacity=".23"/><path d="M15 12L215 120" stroke="#8c93a0" opacity=".07" stroke-width="60"/></svg>`;
}
function drawDoor(x,y,locked,entry=false){const X=x*8,Y=y*3.3;return `<g transform="translate(${X-40} ${Y-67})"><rect x="0" y="0" width="80" height="139" rx="3" fill="#10131a" stroke="${entry?'#bbaaa0':locked?'#ad555d':'#8b8990'}" stroke-width="${entry?5:4}"/><rect x="8" y="7" width="64" height="125" rx="2" fill="#25262d" stroke="#4f525e" stroke-width="2"/><path d="M14 13H66M12 127H68" stroke="#8c8b91" opacity=".7"/><rect x="21" y="27" width="36" height="25" fill="#101b22" stroke="#636e75" stroke-width="2"/><circle cx="63" cy="86" r="3.5" fill="#d1b7a0"/>${entry?'<path d="M4 138H76" stroke="#efc59e" stroke-width="4" opacity=".7"/>':''}${locked?'<path d="M34 82h16v16H34zm3 0v-7a5 5 0 0 1 10 0v7" stroke="#d9a4a0" fill="none" stroke-width="3"/>':''}</g>`}
function drawProp(kind,x,y){const X=x*8,Y=y*3.3;let path='';switch(kind){
 case 'desk':path='<path d="M-49 4h98v26h-98z" fill="#5c4b48" stroke="#b6a9a0" stroke-width="2"/><path d="M-40 30v22m80-22v22" stroke="#74737c" stroke-width="7"/>';break;
 case 'locker':path='<rect x="-26" y="-67" width="52" height="102" fill="#434955" stroke="#b1acaa" stroke-width="3"/><path d="M0 -67V35M-15 -29h7m23 0h-7" stroke="#9a979b" stroke-width="2"/>';break;
 case 'phone':path='<rect x="-19" y="-49" width="38" height="61" rx="3" fill="#353b44" stroke="#b3a89a" stroke-width="3"/><path d="M-12 -40 Q0 -51 12 -40L7 -31Q0 -36 -7 -31Z" fill="#b9ada0"/><circle cy="-11" r="9" fill="#1b242c" stroke="#8a909a"/>';break;
 case 'screen':path='<rect x="-44" y="-61" width="88" height="67" fill="#131d29" stroke="#8e939a" stroke-width="4"/><path d="M-36 -30l16 -6 15 8 17 -13 17 6" fill="none" stroke="#658e93" opacity=".6"/><path d="M0 6v20m-35 0h70" stroke="#7c8188" stroke-width="4"/>';break;
 case 'paper':path='<rect x="-22" y="-36" width="46" height="57" transform="rotate(-7)" fill="#b3aaa0" stroke="#ddd1c0" stroke-width="2"/><path d="M-14 -23h27m-27 10h27m-27 10h18" stroke="#605a5e" opacity=".8"/>';break;
 case 'bed':path='<rect x="-52" y="-31" width="104" height="62" rx="4" fill="#666c72" stroke="#b6b6b7" stroke-width="4"/><rect x="-44" y="-21" width="29" height="18" rx="4" fill="#a8a4a4"/><path d="M-46 25h90" stroke="#d1c7bd"/>';break;
 case 'cart':path='<rect x="-41" y="-32" width="82" height="54" fill="#494f55" stroke="#a2a5aa" stroke-width="3"/><path d="M-33 -12h66M-35 22v20m70-20v20" stroke="#8e969a" stroke-width="3"/><circle cx="-32" cy="44" r="6" fill="#191d23"/><circle cx="32" cy="44" r="6" fill="#191d23"/>';break;
 case 'machine':path='<rect x="-51" y="-56" width="102" height="92" fill="#45474d" stroke="#9b989b" stroke-width="4"/><circle cx="-19" cy="-25" r="10" fill="#252630" stroke="#a8a4a6"/><circle cx="18" cy="-25" r="10" fill="#252630" stroke="#a8a4a6"/><path d="M-36 10h72" stroke="#8f7373" stroke-width="5"/>';break;
 case 'books':case 'rack':path='<rect x="-48" y="-57" width="96" height="100" fill="#34343a" stroke="#87828a" stroke-width="3"/><path d="M-48 -22h96M-48 12h96" stroke="#ada5a6" stroke-width="4"/>'+Array.from({length:6},(_,i)=>`<rect x="${-38+i*13}" y="-50" width="8" height="25" fill="${i%2?'#655960':'#8e7772'}"/>`).join('');break;
 case 'glass':path='<rect x="-56" y="-73" width="112" height="113" fill="#1b3035" opacity=".84" stroke="#b3a7a9" stroke-width="5"/><path d="M0 -73v113M-56 -17h112" stroke="#8098a2" stroke-width="4"/><path d="M-30 -53l20 13" stroke="#b5b8b7" opacity=".3"/>';break;
 case 'pipe':path='<path d="M-44 -70v115h88V-30" fill="none" stroke="#8c878a" stroke-width="18"/><path d="M-44 -15h88" stroke="#4c535b" stroke-width="8"/>';break;
 case 'crate':path='<rect x="-37" y="-32" width="74" height="69" fill="#554c47" stroke="#9f9083" stroke-width="3"/><path d="M-35 -30l70 65M35 -30l-70 65" stroke="#736c66" stroke-width="6"/>';break;
 case 'altar':path='<rect x="-55" y="-25" width="110" height="55" fill="#51424a" stroke="#c0a5a1" stroke-width="4"/><path d="M0 -75v50M-22 -57h44" stroke="#d3b5aa" stroke-width="9"/>';break;
 case 'lamp':path='<path d="M0 -78v38" stroke="#b4b0ae" stroke-width="6"/><path d="M-35 -44h70l-13 21h-44Z" fill="#878087" stroke="#b4b0ae" stroke-width="3"/>';break;
 case 'gate':path='<rect x="-56" y="-76" width="112" height="126" fill="#171c24" stroke="#96939c" stroke-width="8"/><path d="M-40 -70v114M-20 -70v114M0 -70v114M20 -70v114M40 -70v114" stroke="#676871" stroke-width="5"/>';break;
 }return `<g transform="translate(${X} ${Y})">${path}</g>`}
function roomConnections(){return Object.keys(D).filter(k=>D[k].a===S.room||D[k].b===S.room).map(k=>({id:k,door:D[k],to:D[k].a===S.room?D[k].b:D[k].a}));}
function siteGroups(){const conf=SCENE_CONFIG[S.room]||{style:'corridor',sites:[]};const objects=availableRoomObjects();const seen=new Set();const positions=SCENE_ROOM_POS[S.room]||SCENE_STYLE_POS[conf.style]||SCENE_SITE_POS;const groups=(conf.sites||[]).map((s,i)=>{const list=objects.filter(o=>s.slice(2).includes(o[0]));list.forEach(o=>seen.add(o[0]));return {id:`site_${i}`,label:s[0],kind:s[1],objects:list,x:(positions[i]||SCENE_SITE_POS[i]||[50,65])[0],y:(positions[i]||SCENE_SITE_POS[i]||[50,65])[1]}}).filter(g=>g.objects.length);const missed=objects.filter(o=>!seen.has(o[0]));
 const phoneObjects=missed.filter(o=>String(o[0]).startsWith('phone_'));
 if(phoneObjects.length){phoneObjects.forEach(o=>seen.add(o[0]));groups.push({id:'telephone',label:'Wall telephone',kind:'phone',objects:phoneObjects,x:78,y:47})}
 const remaining=missed.filter(o=>!seen.has(o[0]));if(remaining.length){let g=groups.find(x=>x.kind==='desk')||groups[0];if(g)g.objects.push(...remaining);else groups.push({id:'site_0',label:'Nearby furnishings',kind:'desk',objects:remaining,x:44,y:65})}return groups;}
function sceneDoorLabel(to,door){const knownRoom=S.vis[to]||S.mapParts>0&&mappedRoom(to);const name=knownRoom?R[to].n:(to==='security'?'SECURITY — destination unknown':to==='ward'?'East wing corridor':to==='eastcorridor'?'Unlit corridor':to==='lift'?'Service elevator':'Unmarked passage');const open=doorOpen(door.id);return (open?'':'Locked · ')+name+(open?'':' · '+(door.door.need||'Access restricted'))}
function sceneDoorTravel(to){go(to)}
function sceneTooltip(text){const el=document.getElementById('sceneTooltip');if(el){el.textContent=text;el.classList.add('visible')}}
function sceneTooltipClear(){const el=document.getElementById('sceneTooltip');if(el){el.textContent='';el.classList.remove('visible')}}
function renderScene(){const host=$('interactiveScene');if(!host||!S)return;const conf=SCENE_CONFIG[S.room]||{style:'corridor'};const doors=roomConnections(),groups=siteGroups();if(S.sceneFocusRoom!==S.room){S.sceneFocus=null;S.sceneFocusRoom=S.room}
 const dark=!!R[S.room].dark&&!lit(),layout=sceneLayout(doors,groups,S.room);
 const sceneArt=sceneArchitecture(conf.style)+roomSignature(S.room);let doorArt='',doorButtons='';
 doors.forEach((d,i)=>{const pos=layout.doorPlaces[i],open=doorOpen(d.id),entry=S.prev===d.to&&S.prev!==S.room,tip=sceneDoorLabel(d.to,d);doorArt+=drawDoor(...pos,!open,entry);doorButtons+=`<button class="hotspot door-hotspot ${open?'':'is-locked'} ${entry?'entry-door':''}" style="left:${pos[0]}%;top:${pos[1]}%" data-tip="${htmlSafe(tip)}" aria-label="${htmlSafe(tip)}" onmouseenter="sceneTooltip(this.dataset.tip)" onmouseleave="sceneTooltipClear()" onfocus="sceneTooltip(this.dataset.tip)" onblur="sceneTooltipClear()" onclick="sceneDoorTravel('${d.to}')"><span class="door-label">${open?'DOOR':'LOCKED'}</span></button>`});
 let propArt='',propButtons='';groups.forEach((g,i)=>{const pos=layout.itemPlaces[i];propArt+=drawProp(g.kind,...pos);const active=S.sceneFocus===g.id;propButtons+=`<button class="hotspot prop-hotspot ${active?'is-active':''}" style="left:${pos[0]}%;top:${pos[1]}%" data-tip="${htmlSafe(g.label)}" aria-label="Examine ${htmlSafe(g.label)}" onmouseenter="sceneTooltip(this.dataset.tip)" onmouseleave="sceneTooltipClear()" onfocus="sceneTooltip(this.dataset.tip)" onblur="sceneTooltipClear()" onclick="sceneInspect('${g.id}')"><span class="hotspot-dot" aria-hidden="true">⌕</span></button>`});
 host.innerHTML=`<div class="scene-image">${sceneArt}<svg class="scene-overdraw" viewBox="0 0 800 330" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${propArt}${doorArt}</svg><div class="scene-haze"></div>${doorButtons}${propButtons}<div class="scene-darkness ${dark?'deep-dark':''}" aria-hidden="true"></div><div id="sceneTooltip" class="scene-tooltip" role="status" aria-live="off"></div></div><div class="scene-bottom-caption">${R[S.room].dark&&!lit()?'Dark room · Switch on the flashlight to investigate':`${doors.length} passage${doors.length===1?'':'s'} · ${groups.length} places to examine`}</div>`;renderSceneDrawer();}
function sceneInspect(id){if(!S)return;if(R[S.room].dark&&!lit()){interaction('In the darkness I can only make out the furniture. I need the flashlight or working lights to examine its contents.');return;}S.sceneFocus=S.sceneFocus===id?null:id;S.f['sceneSeen_'+S.room+'_'+id]=1;renderScene();}
function sceneAction(id){act(id);if(S)renderScene()}
function renderSceneDrawer(){const host=$('sceneDrawer');if(!host||!S)return;const group=siteGroups().find(g=>g.id===S.sceneFocus);if(!group){host.classList.add('hid');host.innerHTML='';return;}host.classList.remove('hid');host.innerHTML=`<div class="drawer-header"><b>${htmlSafe(group.label)}</b><button class="btn" onclick="sceneInspect('${group.id}')">Close ×</button></div><div class="drawer-content">${group.objects.map(o=>{const [id,name,,description,sp]=o,st=S.ob[id],isDone=st==='done'||st==='read';const verb=isDone?'Done':sp.doc?'Read file':sp.give?'Take':sp.expand?'Equip':sp.act==='map'?'Examine map':sp.act==='payphone'?(S.f.phoneRinging&&S.room===S.f.ringingPhoneRoom?'Answer call':'Check line'):sp.act==='trap'?'Pull lever':sp.act==='hide'?'Hide':sp.act==='barricade'?'Board window':sp.act==='npc'?'Talk':sp.look?'Examine':'Use / inspect';return `<div class="drawer-item ${isDone?'done':''}"><div class="drawer-copy"><b>${htmlSafe(name)}</b><small>${htmlSafe(description)}</small>${isDone?'<small class="marked">✓ Recorded / resolved</small>':''}</div><button class="btn ${isDone?'':'p'}" ${isDone?'disabled':''} onclick="sceneAction('${id}')">${verb}</button></div>`}).join('')}</div>`;}
function hideInRoom(){if(!HIDING_AREAS.has(S.room))return interaction('There is nowhere safe to hide here.');if(!S.pursuer?.active)return interaction('You crouch behind the furniture. For now the corridor is quiet.');S.f.hidingRoom=S.room;S.f.hidingUntil=(S.t||0)+5;interaction('You slip into cover and hold your breath. The pursuer may pass if it did not see you enter.');S.pursuer.cooldown=Math.max(2,S.pursuer.cooldown||0);render()}

// Interior monologue is a separate text channel. Rerenders (flashlight, shots) never reroll it.
const ROOM_THOUGHT_LINES={
 lobby:['I woke here. Someone must know who I am.','That humming is still there. I cannot find which machine is making it.','I keep looking at the front doors like I am allowed to leave.'],
 security:['Did someone watch me before I woke up?','If there were cameras, there must be recordings.','The screens feel more like witnesses than equipment.'],
 eastcorridor:['Do not waste the light. Keep moving.','Something is beyond that darkness. I can hear it breathe.','I keep thinking I have walked this corridor before.'],
 ward:['These names are supposed to mean something to me.','Not everyone here is gone. I need to remember that.'],
 generator:['One machine controls so much of the building. Why?','Power means lights. It might also mean opening things that should stay closed.'],
 lift:['I can still turn back. But the answer is underneath me.','Why do my hands already know these controls?'],
 b2kennels:['They experimented on animals as well.','I can hear claws on concrete, but the cages are empty.']
};
function renderSceneThought(){if(!S)return;const host=$('sceneThought'),txt=$('sceneThoughtText');if(!host||!txt)return;
 const f=S.f||(S.f={});
 if(f.thoughtForRoom!==S.room){
  const lines=ROOM_THOUGHT_LINES[S.room]||[
   'I need to find out what happened here. The records might be lying.',
   'This place feels familiar. That scares me more than the noises.',
   'Stay calm. Look for something real. Anything.'
  ];
  f.thoughtVisits=f.thoughtVisits||{};const index=f.thoughtVisits[S.room]||0;
  f.thoughtForRoom=S.room;f.thoughtShown=lines[(hashSeed(S.seed+'::thought-'+S.room)+index)%lines.length];f.thoughtVisits[S.room]=index+1;
 }
 txt.textContent=f.thoughtShown||'';host.classList.toggle('hid',!f.thoughtShown);
}
