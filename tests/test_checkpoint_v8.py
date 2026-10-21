"""Legacy checkpoint loaders migrate old clearance and preserve actual v8 records."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[];errors=[]
versions=['last-ward-ch1-survival-review-5','last-ward-ch1-chapter-review-6','last-ward-ch1-chapter-review-7']
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);q=b.new_page(viewport={'width':1600,'height':1000},service_workers='block');q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8010');q.get_by_role('button',name='BEGIN INVESTIGATION').click();q.evaluate('nextIntro();nextIntro();nextIntro()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
 q.evaluate('''window.legacyCheckpoint=structuredClone(S);const s=window.legacyCheckpoint;s.hp=44;s.san=100;s.room='observation';s.roomView='front';s.roomViewRoom=s.room;s.prev='generator';s.sceneFocus=null;s.hallCombat=null;s.inv=[{n:'Flashlight',c:1},{n:'Handgun Ammo',c:9}];s.f={...s.f,power:1,photoPuzzleSolved:1,plexiIncidentSeen:1,researcherLastRoomSeen:1,doctorWallSeen:1,finalSecurityClearance:1,elevatorFusesInstalled:1,liftSeen:1,pursuerStarted:1,pursuerEscapes:2,falseEncounterSeen:1,visualEpisodes:2,chapter1Complete:0,dead:false};delete s.balanceVersion;for(const k of ['puzzleRevision','drained','transferBusReady','legacyPursuitProof'])delete s.f[k];s.enemyActors.forEach(a=>a.hp=0);s.en=Object.fromEntries(Object.keys(R).map(r=>[r,0]));s.vis=Object.fromEntries(Object.keys(R).map(r=>[r,1]));s.pursuer.active=false;''')
 for version in versions:
  for loader,key in [('wardLoadFinale','lw_ch1_finale_checkpoint'),('loadCheckpoint','lw_ch1_cinematic_glass_checkpoint')]:
   q.evaluate('''([version,key])=>{const s=structuredClone(window.legacyCheckpoint);s.buildId=version;localStorage.setItem(key,JSON.stringify(s));}''',[version,key])
   q.evaluate(loader+'()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
   got=q.evaluate('({build:S.buildId,expected:WardChapter.BUILD,drained:!!S.f.drained,transfer:!!S.f.transferBusReady,proof:!!S.f.legacyPursuitProof,revision:S.f.puzzleRevision,ammo:cnt("Handgun Ammo"),dead:S.enemyActors.filter(a=>a.hp<=0).length,actors:S.enemyActors.length})')
   assert got['build']==got['expected'] and got['drained'] and got['transfer'] and got['proof'] and got['revision']==8,(loader,version,got)
   assert got['ammo']==9 and got['dead']==got['actors'],(loader,version,got)
   checks.append(loader+' preserves '+version+' earned sump/supply/pursuit clearance, ammunition and cleared enemies')
 # A v8 record already has mechanical progress and pursuit evidence. Save the
 # fixture through the real Terminal before checking both checkpoint loaders;
 # unlike pre-v8 compatibility cases, it must not receive inferred clearance.
 q.evaluate('''S=structuredClone(window.legacyCheckpoint);S.buildId='last-ward-ch1-chapter-review-8';S.balanceVersion=8;S.room='lobby';S.roomView='front';S.roomViewRoom='lobby';S.f.puzzleRevision=8;S.f.drained=1;S.f.transferBusReady=1;S.f.pursuerStaggers=2;S.ob.wnc='done';S.inv.push({n:'Floppy Disk',c:1});render();saveGame()''')
 q.get_by_role('button',name='Save record',exact=True).click()
 q.evaluate('window.v8Record=JSON.parse(localStorage.getItem(K))')
 assert q.evaluate('window.v8Record.buildId==="last-ward-ch1-chapter-review-8"&&window.v8Record.saves===1&&!window.v8Record.inv.some(x=>x.n==="Floppy Disk")')
 for earned in [True,False]:
  for loader,key in [('wardLoadFinale','lw_ch1_finale_checkpoint'),('loadCheckpoint','lw_ch1_cinematic_glass_checkpoint')]:
   q.evaluate('''([key,earned])=>{const s=structuredClone(window.v8Record);s.room='observation';s.roomViewRoom=s.room;if(!earned){delete s.f.drained;delete s.f.transferBusReady;delete s.f.pursuerStaggers;delete s.ob.wnc;}localStorage.setItem(key,JSON.stringify(s));}''',[key,earned])
   q.evaluate(loader+'()');q.wait_for_function('WardWinter.roomViewRenderer()?.loaded')
   got=q.evaluate('({build:S.buildId,expected:WardChapter.BUILD,drained:!!S.f.drained,transfer:!!S.f.transferBusReady,proof:!!S.f.legacyPursuitProof,revision:S.f.puzzleRevision,staggers:S.f.pursuerStaggers||0,ammo:cnt("Handgun Ammo"),saves:S.saves,dead:S.enemyActors.filter(a=>a.hp<=0).length,actors:S.enemyActors.length})')
   assert got['build']==got['expected'] and got['revision']==8 and not got['proof'],(loader,earned,got)
   assert got['drained']==earned and got['transfer']==earned and got['staggers']==(2 if earned else 0),(loader,earned,got)
   assert got['ammo']==9 and got['saves']==1 and got['dead']==got['actors'],(loader,earned,got)
   checks.append(loader+' preserves a Terminal-saved v8 '+('completed mechanical clearance and two earned staggers' if earned else 'unfinished mechanical clearance without compatibility grants')+', ammunition and cleared enemies')
 assert not errors,errors;b.close()
(ROOT/'tests/results/checkpoint_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+v for v in checks))
