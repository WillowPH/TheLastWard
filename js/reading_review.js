/* One record at a time: readable pages, labelled evidence and local feedback. */
(function(){'use strict';
const WW=WardWinter,e=htmlSafe;let record=null,filePage=0,fileTab='leads',fileQuery='',fromFiles=false;
WW.isReadingRecord=()=>!!document.querySelector('#m .record-reader,#m .winter-object-modal,#m .winter-portrait-grid');
// Documents and open mechanisms stop encounter clocks as well as the turn
// clock. Rebase saved real deadlines once when reading ends; do not charge the
// same time again when the player uses the separate game Pause over a reader.
let clockState=null,readingStarted=null;
function shiftReadingDeadlines(object,delta){if(!object||typeof object!=='object'||!delta)return;for(const [key,value]of Object.entries(object)){if(value&&typeof value==='object')shiftReadingDeadlines(value,delta);else if(typeof value==='number'&&value>1e12&&/deadline|Real$|UntilReal$/i.test(key))object[key]=value+delta;}}
WW.readingClock=function(){
 const now=Date.now();
 if(clockState!==S){clockState=S;readingStarted=null;}
 if(WW.isPaused?.()){
  if(readingStarted!==null)shiftReadingDeadlines(S,now-readingStarted);
  readingStarted=null;return {paused:true,now};
 }
 const reading=!!(WW.isSurvivalPaused?.()||WW.isReadingRecord());
 if(reading){if(readingStarted===null)readingStarted=now;return {paused:true,now:readingStarted};}
 if(readingStarted!==null){shiftReadingDeadlines(S,now-readingStarted);readingStarted=null;}
 return {paused:false,now};
};
new MutationObserver(()=>WW.readingClock()).observe($('m'),{childList:true,subtree:true});
document.addEventListener('ward:pause',()=>WW.readingClock());
document.addEventListener('ward:resume',()=>WW.readingClock());
WW.sceneWarning=function(text){const host=$('interactiveScene');if(!host)return;let banner=host.querySelector('.scene-warning-banner');if(!banner){banner=document.createElement('p');banner.className='scene-warning-banner';banner.setAttribute('role','status');host.append(banner);}banner.textContent=text;clearTimeout(WW.warningTimer);WW.warningTimer=setTimeout(()=>banner.remove(),4500);};
function rows(text,width,font){const ctx=document.createElement('canvas').getContext('2d');ctx.font=font;const out=[];for(const paragraph of text.split('\n')){let row='';for(const word of paragraph.split(/\s+/).filter(Boolean)){const next=row?row+' '+word:word;if(row&&ctx.measureText(next).width>width){out.push(row);row=word;}else row=next;}out.push(row);}return out;}
function paginate(){const paper=document.querySelector('.record-reader .winter-paper-text');if(!paper||!record)return;
 paper.style.removeProperty('font-size');paper.style.removeProperty('line-height');
 function layout(){const style=getComputedStyle(paper),line=parseFloat(style.lineHeight)||26,limit=Math.max(1,Math.floor(paper.clientHeight/line)),all=rows(record.text,Math.max(20,paper.clientWidth-6),style.font),pages=[];for(let i=0;i<all.length;){let count=Math.min(limit,all.length-i);paper.textContent=all.slice(i,i+count).join('\n');while(count>1&&paper.scrollHeight>paper.clientHeight){count--;paper.textContent=all.slice(i,i+count).join('\n');}pages.push(paper.textContent);i+=count;}return pages.length?pages:[''];}
 let pages=layout();const original=getComputedStyle(paper),fontSize=parseFloat(original.fontSize),lineHeight=parseFloat(original.lineHeight);
 // Avoid a separate sheet containing only a trailing phrase. A small adjustment
 // is allowed only when the whole record still fits at a readable type size.
 if(pages.length===2&&pages[1].trim().split(/\s+/).length<=18){let fitted=false;for(const [ratio,leading]of [[.94,.9],[.9,.8],[.86,.78]]){const size=fontSize*ratio;if(size<(paper.closest('.handwritten')?20:15))break;paper.style.setProperty('font-size',size+'px','important');paper.style.setProperty('line-height',Math.max(size*1.08,lineHeight*leading)+'px','important');const candidate=layout();if(candidate.length===1){pages=candidate;fitted=true;break;}}if(!fitted){paper.style.removeProperty('font-size');paper.style.removeProperty('line-height');}}
 record.pages=pages;record.page=Math.min(record.page,record.pages.length-1);paint();}

function paint(){if(!record)return;const root=document.querySelector('.record-reader');if(!root)return;root.querySelector('.winter-paper-text').textContent=record.pages[record.page]||'';root.querySelector('.record-page-number').textContent='Page '+(record.page+1)+' of '+record.pages.length;root.querySelector('[data-page="-1"]').disabled=record.page===0;root.querySelector('[data-page="1"]').disabled=record.page>=record.pages.length-1;}
WW.readRecord=function(title,text,options={}){record={title,text:String(text||''),page:0,pages:[''],typed:!!options.transcript};const hand=/note|diary|journal|letter|annotation|postcard|photograph|handover/i.test(title)&&!options.journal;
 modal(e(title),'<section class="record-reader" data-record="'+e(title)+'"><div class="winter-document-tools"><button class="btn" onclick="WardWinter.toggleTranscription()">'+(hand?'Readable transcription':'Paper view')+'</button><span>'+(options.journal?'Personal journal':hand?'Handwritten record · 1998':'Blackridge archive copy · 1998')+'</span></div><article class="winter-document '+(hand?'handwritten':'typed')+' damage-'+hashSeed(title)%3+'"><div class="winter-paper-text"></div><span class="winter-paper-stain" aria-hidden="true"></span></article><footer class="record-pages"><button class="btn" data-page="-1" onclick="WardWinter.recordPage(-1)" aria-label="Previous document page">‹</button><span class="record-page-number" aria-live="polite"></span><button class="btn" data-page="1" onclick="WardWinter.recordPage(1)" aria-label="Next document page">›</button>'+(fromFiles?'<button class="btn record-return" onclick="evidenceModal()">Return to Files</button>':'<button class="btn record-return" onclick="closeModal()">Return to room</button>')+'</footer></section>');
 document.querySelector('#m .md').classList.add('winter-document-modal','record-modal');const paper=document.querySelector('.record-reader');new ResizeObserver(paginate).observe(paper);paginate();};
document.fonts?.addEventListener('loadingdone',paginate);
WW.recordPage=delta=>{if(record){record.page=Math.max(0,Math.min(record.pages.length-1,record.page+delta));paint();}};
WW.toggleTranscription=()=>{const paper=document.querySelector('.record-reader .winter-document');if(paper){paper.classList.toggle('transcription-view');paginate();}};
WW.reader=()=>record;
doc=function(title){WW.readRecord(title,docText(title));};
// Current work is grouped by the problem it helps solve. Only documents
// actually collected in this run can contribute a clue or a Read link.
function goals(){return [
 {id:'generator',label:'Generator',task:'Restore the hospital generator.',done:!!S.f.power,show:true,titles:['Maintenance Log']},
 {id:'pharmacy',label:'Pharmacy lock',task:'Identify the pharmacy access sequence.',done:!!S.f.pharm,show:!!S.vis.wardservice||S.docs.includes('Duty Roster'),titles:['Duty Roster']},
 {id:'breaker',label:'Electrical panel',task:'Release the service crank from its breaker cupboard.',done:S.ob.brk==='done',show:!!S.f.power||!!S.vis.residence,titles:['Resident Diary','Continuity Calibration Note']},
 {id:'pit',label:'Lift-pit drainage',task:'Drain the shared sump before using the service lift.',done:!!S.f.drained,show:!!S.vis.tunnel||S.docs.includes('Heller’s winter maintenance note'),titles:['Diver Note','Heller’s winter maintenance note']},
 {id:'supply',label:'Transfer supply',task:'Isolate a safe supply for the elevator safeguards.',done:!!S.f.transferBusReady,show:!!S.vis.powercontrol||S.docs.includes('Power Control Memo')||!!S.f.power,titles:['Power Control Memo','Rourke’s final annotation']},
 {id:'interlock',label:'Elevator interlock',task:'Recover the four plugs and test their contact order.',done:!!S.f.elevatorFusesInstalled,show:S.docs.includes('Heller’s winter maintenance note')||!!S.vis.archive||WW.fuses.some(name=>has(name)),titles:['Archive component transfer','Heller’s winter maintenance note']},
 {id:'memorial',label:'Archive memorial',task:'Investigate the archive dedication lock.',done:!!S.f.chapel,show:!!S.vis.archive||S.docs.includes('Memorial Ledger'),titles:['Memorial Ledger']},
 {id:'clearance',label:'Transfer clearance',task:'Verify the executive record and archive transfer authorization.',done:!!S.f.finalSecurityClearance,show:!!S.f.photoPuzzleSolved||!!S.f.researcherLastRoomSeen||!!S.vis.observation,titles:['Monolith Executive Directive','Rourke’s final annotation','Containment Transfer Authorization']},
 {id:'pursuer',label:'Containment pursuit',task:'Create a safe opening past the containment pursuer.',done:!!WW.balance8?.strategy?.(),show:!!S.f.pursuerStarted,titles:S.docs.filter(title=>/hoist|pursuer|heavy boots|subject x/i.test(String(docText(title))))},
 {id:'preparation',label:'Supplies & optional equipment',task:'Review where the night staff left ammunition and restricted equipment.',done:!!S.f.chapter1Complete,show:S.docs.includes('Security ammunition issue log'),titles:['Security ammunition issue log']}
 ].map(g=>({...g,show:g.show||g.titles.some(title=>S.docs.includes(title))}));}
function excerpt(title){const parts=String(docText(title)).split(/\n\s*\n/).map(v=>v.trim()).filter(Boolean),body=parts.find((v,i)=>i>0&&/[a-z]/.test(v))||parts.at(-1)||'';const text=body.replace(/\s+/g,' ');return text.length>180?text.slice(0,177).replace(/\s+\S*$/,'')+'…':text;}
function storyTopic(title){if(/telephone|transmission/i.test(title))return 'Telephone & transmissions';if(/Mimi|Nursing|Shaw|Judith|attendant|journal|diary|Kessler|portrait/i.test(title))return 'Staff & personal records';if(/LULLABY|Rourke|Consent|Research|Testimony|Executive|Transfer Authorization/i.test(title))return 'LULLABY evidence';return 'Hospital records';}
WW.fileCatalogue=function(){const list=goals();return [...new Set(S.docs)].filter(title=>typeof title==='string').map(title=>{const related=list.filter(g=>g.titles.includes(title)),room=Object.entries(R).find(([,r])=>r.o?.some(o=>o[4].doc===title))?.[0],service=/Maintenance Log|winter maintenance|component transfer|Diver Note|Power Control Memo|Duty Roster|Memorial Ledger|Calibration|ammunition issue/i.test(title);return {title,topic:related[0]?.label||storyTopic(title),room,lead:related.some(g=>g.show&&!g.done),goals:related.map(g=>g.id),story:!service||/Rourke|Executive/i.test(title),excerpt:excerpt(title)};}).sort((a,b)=>Number(b.lead)-Number(a.lead)||a.topic.localeCompare(b.topic)||a.title.localeCompare(b.title));};
const goalRooms={generator:['generator'],pharmacy:['wardservice','pharmacy'],breaker:['residence'],pit:['tunnel'],supply:['powercontrol'],interlock:['powercontrol','archive','records','pharmacy'],memorial:['archive'],clearance:['powercontrol','observation'],preparation:['security']};
WW.fileGoals=()=>{const catalogue=WW.fileCatalogue();return goals().filter(g=>g.show&&!g.done).map(g=>({...g,clues:catalogue.filter(v=>v.goals.includes(g.id))})).sort((a,b)=>Number((goalRooms[b.id]||[]).includes(S.room))-Number((goalRooms[a.id]||[]).includes(S.room)));};
function recordEntry(v,compact=false){return '<article class="file-entry '+(compact?'file-clue':'')+'"><div><strong>'+e(v.title)+'</strong><small>'+e(v.topic)+(v.room?' · '+e(R[v.room].n):'')+'</small><p class="file-clue-excerpt">'+e(v.excerpt)+'</p></div><button class="btn" data-file="'+e(v.title)+'" aria-label="Read '+e(v.title)+'">Read</button></article>';}
function fileList(){const root=$('recordFileList');if(!root)return;const all=WW.fileCatalogue();let items,perPage,draw;
 if(fileTab==='leads'){
  items=WW.fileGoals().filter(g=>!fileQuery||(g.label+' '+g.task+' '+g.clues.map(v=>v.title+' '+v.excerpt).join(' ')).toLowerCase().includes(fileQuery));perPage=innerWidth>1100&&innerHeight>=850?2:1;
  draw=g=>'<section class="file-objective" data-file-objective="'+g.id+'"><header><h3>'+e(g.label)+'</h3><span>'+g.clues.length+' collected '+(g.clues.length===1?'clue':'clues')+'</span></header><p class="file-objective-task">'+e(g.task)+'</p>'+(g.clues.length?g.clues.slice(0,2).map(v=>recordEntry(v,true)).join(''):'<p class="file-no-clue">No relevant record has been collected yet. Notes read in the rooms will be linked here.</p>')+(g.clues.length>2?'<p class="file-more-clues">Other collected evidence: '+g.clues.slice(2).map(v=>'<button class="btn" data-file="'+e(v.title)+'">'+e(v.title)+'</button>').join(' ')+'</p>':'')+'</section>';
 }else{
  items=all.filter(v=>(fileTab!=='story'||v.story)&&(!fileQuery||(v.title+' '+v.topic+' '+v.excerpt).toLowerCase().includes(fileQuery)));perPage=innerWidth<=700||innerHeight<850?2:4;draw=v=>recordEntry(v);
 }
 const pages=Math.max(1,Math.ceil(items.length/perPage));filePage=Math.min(filePage,pages-1);root.dataset.mode=fileTab;root.innerHTML=items.slice(filePage*perPage,filePage*perPage+perPage).map(draw).join('')||'<p class="file-no-clue">'+(fileTab==='leads'?'No unfinished objective matches this search. All records retains the evidence from completed work.':'No collected records match this section.')+'</p>';for(const b of root.querySelectorAll('[data-file]'))b.onclick=()=>{if(!S.docs.includes(b.dataset.file))return;fromFiles=true;doc(b.dataset.file);};$('filePageNumber').textContent=(filePage+1)+' / '+pages;$('filePrevious').disabled=filePage===0;$('fileNext').disabled=filePage>=pages-1;
}
WW.fileTab=function(tab){fileTab=['leads','all','story'].includes(tab)?tab:'leads';filePage=0;fileQuery='';evidenceModal();};
WW.fileSearch=function(query){fileQuery=query.toLowerCase();filePage=0;fileList();};
WW.filePage=function(delta){filePage=Math.max(0,filePage+delta);fileList();};
window.addEventListener('resize',()=>{if(document.querySelector('#m .file-browser'))fileList();});
evidenceModal=function(){fromFiles=false;modal('Files','<section class="file-browser"><p>Progression links collected evidence to unfinished work. Story keeps personal and hospital records. Completed clues remain in All records.</p><nav class="inv-tabs">'+[['leads','Progression'],['story','Story'],['all','All records']].map(([id,label])=>'<button class="btn '+(fileTab===id?'active':'')+'" onclick="WardWinter.fileTab(\''+id+'\')">'+label+'</button>').join('')+'</nav><label class="file-search">Find a record<input type="search" value="'+e(fileQuery)+'" oninput="WardWinter.fileSearch(this.value)" placeholder="Title, objective or clue"></label><div id="recordFileList"></div><footer class="record-pages"><button class="btn" id="filePrevious" onclick="WardWinter.filePage(-1)" aria-label="Previous Files page">‹</button><span id="filePageNumber"></span><button class="btn" id="fileNext" onclick="WardWinter.filePage(1)" aria-label="Next Files page">›</button></footer></section>');document.querySelector('#m .md').classList.add('file-modal');fileList();};
const closeBase=closeModal;closeModal=function(){fromFiles=false;return closeBase();};
// Link only evidence the player has already collected; the lock retains its own
// physical clue and the record never fills in the answer for the player.
WW.readPuzzleRecord=function(id,title,kind){if(WW.canAct&&!WW.canAct()||!S.docs.includes(title))return;fromFiles=false;doc(title);const footer=document.querySelector('.record-pages'),button=document.createElement('button');button.className='btn';button.textContent='Return to puzzle';button.onclick=()=>kind==='sequence'?seqModal(id):codeModal(id);footer.querySelector('.record-return')?.replaceWith(button);};
function related(id,kind){const titles=id==='kp'?['Duty Roster']:id==='cat'||id==='memDoor'?['Memorial Ledger','Opening day photograph']:id==='sf'?['Maintenance Log']:id==='brk'?['Resident Diary','Continuity Calibration Note']:[];const body=document.querySelector('#m .mb');for(const title of titles.filter(t=>S.docs.includes(t))){const button=document.createElement('button');button.className='btn related-record';button.textContent='Read '+title;button.onclick=()=>WW.readPuzzleRecord(id,title,kind);body?.append(button);}}
const codeBase=codeModal;codeModal=function(id){if(WW.canAct&&!WW.canAct())return;const result=codeBase(id);related(id,'code');return result;};
const sequenceBase=seqModal;seqModal=function(id,value=''){if(WW.canAct&&!WW.canAct())return;const result=sequenceBase(id,value);related(id,'sequence');return result;};
journal=function(){fromFiles=false;const leads=WardChapter.requirements().map(v=>'• '+v).join('\n'),history=(S.thoughtHistory||[]).slice(-12).map(v=>R[v.room].n+'\n'+v.text),thoughts=[...(S.th2||[]),...history];WW.readRecord('Personal journal','UNFINISHED WORK\n\n'+(leads||'The elevator is ready.')+'\n\nRECENT THOUGHTS\n\n'+[...new Set(thoughts)].slice(-18).join('\n\n'),{journal:true});};
const statusBase=WW.updateStatus;WW.updateStatus=function(){const result=statusBase();if(!S)return result;const hint=$('conditionHint');let recover=$('recoverExposure');if(!recover&&hint){recover=document.createElement('button');recover.id='recoverExposure';recover.className='btn';recover.textContent='Dry off and warm up';recover.onclick=()=>wardWarmUp();hint.after(recover);}if(recover)recover.hidden=!(S.hp>0&&!S.f.dead&&WW.isWarm()&&(S.f.wet||S.f.shivering||S.f.coldExposure>0));return result;};
})();
