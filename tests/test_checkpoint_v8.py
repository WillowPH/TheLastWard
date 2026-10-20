"""Actual legacy checkpoint loaders retain earned late-run mechanical clearance."""
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
 assert not errors,errors;b.close()
(ROOT/'tests/results/checkpoint_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+v for v in checks))
