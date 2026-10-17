"""Authored against the final 27 new backgrounds. No runtime placement fallback."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
rooms={}
def room(id,doors,fixtures,threat=(55,85,42)):
 fs=[]
 for entry in fixtures:
  key,label,rect,ids,*opts=entry
  f={'id':key,'label':label,'rect':rect,'ids':ids.split()}
  if opts:f.update(opts[0])
  fs.append(f)
 rooms[id]={'doors':doors,'fixtures':fs,'threat':threat}
room('lobby',{'ls':[42,35,11,33],'lw':[74,32,16,28]},[
 ('dynamo','Reception emergency dynamo',[67,74,5,6],'emergencyDynamo',{'layer':'dynamo'}),('desk','Reception desk',[86,68,15,6],'desk',{'drawer':True}),('locker','Staff locker',[91,34,6,26],'lock'),('coat','Coat hook',[97,36,5,23],'coat'),('terminal','Continuity Terminal',[85,51,6,9],'term'),('box','Field cache',[75,60,9,9],'box'),('intercom','Intercom panel',[63.5,33,3,6],'int'),('phone','Public payphone',[57,31,4,11],'payphone'),('window','Rain-streaked window',[24,25,13,24],'win'),('entrance','Chained main entrance',[11,43,9,17],'sealedExit')])
room('security',{'ls':[7,37,11,57],'es':[95,37,8,60]},[
 ('clara','Clara Whitmore',[85,39,8,16],'clara',{'actor':'operator_clara','actorRect':[84,66,32,64]}),('report','Incident report',[51,57,14,6],'rep'),('cabinet','Equipment cabinet',[26,33,16,34],'rev reva'),('drawer','Desk drawer',[29,73,12,13],'drw',{'drawer':True}),('roster','Duty roster',[75,23,9,13],'ros'),('monitors','Camera monitors',[51,30,23,18],'cam rep2'),('coffee','Cold coffee',[46,52,4,4],'cof'),('map','Folded floor plan',[75,58,20,6],'mapboard'),('portraits','Staff portraits',[54,13,20,10],'staffPortraits'),('diary','Night attendant journal',[39,52,8,4],'attendantDiary1'),('phone','Desk telephone',[69,50,8,8],'@phone'),('cache','Supply pouch',[88,58,5,4],'@supply',{'layer':'pouch'})])
room('eastcorridor',{'lw':[11,46,15,65],'ew':[52,47,8,21],'es':[95,46,8,68]},[
 ('light','Ceiling light',[50.5,13,4,10],'fixture'),('trolley','Broken trolley',[74,64,18,17],'trolley'),('directory','East wing directory',[28,30,7,28],'directory'),('radio','Portable staff radio',[30,52,6,5],'radioHall'),('window','Cracked ward window',[77,35,12,27],'windowBoard'),('exit','Bolted fire exit',[36,42,3,29],'emergencyExit'),('valve','Damaged sprinkler valve',[64,11,5,7],'staffSprinkler')])
room('ward',{'ew':[9,36,14,43],'northPassage':[91,35,12,26]},[
 ('gurney','Overturned gurney',[90,64,18,19],'gur'),('names','Patient name boards',[33,25,12,16],'nb'),('lockbox','Night nurse equipment box',[48,39,8,6],'nightPistol'),('ammo','Ammunition envelope',[44,43,4,2],'pistolRounds',{'layer':'paper'}),('journal','Night attendant journal',[39,39,6,3],'nightJournal')])
room('wardnorth',{'wr':[7,51,7,48],'wi':[25,47,10,36],'northPassage':[77,47,10,36],'servicePassage':[93,51,7,48]},[
 ('notice','Patient transfer notice',[63,39,4,8],'northBoard'),('trolley','Linen trolley',[39,60,13,16],'northTrolley')])
room('wardservice',{'wa':[9,37,11,48],'wp':[24,39,5,31],'wl':[75,37,5,29],'servicePassage':[90,38,8,45]},[
 ('map','Ward service map',[51,27,8,12],'crossDiagram'),('cupboard','Staff supply alcove',[65,37,7,23],'crossCabinet'),('cover','Supply recess',[65,68,16,22],'crossHide'),('keypad','Pharmacy keypad',[20,31,2.5,7],'kp'),('trail','Drag marks',[34,76,10,6],'serviceTrail')])
room('room12',{'wr':[4,30,7,45],'rr':[75,30,10,30],'rc12':[96,30,7,45]},[
 ('file','Patient file',[68,59,6,12],'file'),('cabinet','Medical cabinet',[56,28.5,9,15],'cab'),('shelf','Supply shelves',[54,39,6,5],'shf shf2'),('restraints','Cut restraints',[48,55,7,12],'rs'),('drawer','Bedside drawer',[31,50,11,7],'drw12',{'drawer':True}),('tray','Instrument tray',[14,65,18,9],'tray12')])
room('isoward',{'wi':[13,34,17,55]},[
 ('patient','Daniel Mercer',[66,43,27,22],'beggingPatient'),('trolley','Treatment trolley',[35,49,15,25],'patientTherapy'),('chart','Isolation admission chart',[71,17,8,17],'patientFile'),('phone','Disconnected telephone',[58,27,4,7],'@phone',{'layer':'phone'})])
room('archive',{'wa':[8,26,8,38],'ag':[22,26,7,23],'ac':[77,26,7,23],'ar':[92,26,8,38]},[
 ('memo','Research memo',[61,54,12,5],'memo'),('cabinet','Long-gun cabinet',[68,30,10,18],'gun tin'),('fuse','Equipment shelf',[66,42,6,4],'fus'),('plaque','Memorial plaque lock',[50,19,7,14],'cat'),('drawer','Hidden index drawer',[36,69,9,8],'hid',{'drawer':True}),('folder','Patient folder',[70.5,58.5,7,4],'flr'),('survey','Restricted wing survey',[33,50,10,5],'eastMap')])
room('pharmacy',{'wp':[9,37,13,66]},[
 ('judith','Nurse Judith Price',[71,78,8,25],'judith',{'actor':'infected_nurse'}),('fridge','Medical fridge',[79,38,14,39],'med shelf5'),('ribbon','Clerk desk',[43,44,10,4],'rib'),('cutters','Maintenance rack',[93,65,5,27],'bol'),('drawer','Dispensing drawer',[54,53,15,8],'am shelf3',{'drawer':True}),('battery','Torch rack',[59,42,7,5],'bat'),('shelves','Upper shelf',[42,21,21,12],'shelf2'),('returns','Returns basket',[52,42,7,5],'shelf4'),('tools','Maintenance tool roll',[64,48,5,3],'maintenanceKit',{'layer':'pouch'}),('phone','Wall telephone',[66,28,4,9],'@phone',{'layer':'phone'}),('cache','Supply pouch',[35,45,4,4],'@supply',{'layer':'pouch'})])
room('laundry',{'lr':[5,32,8,40],'wl':[94,33,9,39]},[
 ('cart','Laundry cart',[42,53,15,20],'lau'),('antiseptic','Antiseptic pouch',[50,70,5,4],'lauant',{'layer':'pouch'}),('chute','Laundry chute',[76,42,8,13],'chute'),('pouch','Field equipment pouch',[13,63,8,6],'pouch'),('map','Service wing floor plan',[82,23,7,12],'tag serviceMap'),('plank','Dry wooden plank',[14,51,5,18],'sparePlank'),('locker','Supply locker hiding place',[61,41,12,32],'laundryhide'),('lever','Overhead hoist release',[26,32,5,13],'traplever'),('journal','Loose journal page',[13,73,7,4],'attendantDiary2',{'layer':'paper'}),('phone','Wall telephone',[85,33,3,7],'@phone'),('cache','Supply pouch',[65,68,6,4],'@supply',{'layer':'pouch'})])
room('generator',{'liftEntry':[23,35,7,23],'ag':[36,35,7,23],'go':[70,31,6,12],'gm':[85,35,6,22]},[
 ('log','Maintenance log',[6,69,11,7],'log'),('panel','Generator fuse panel',[7,37,10,21],'pan'),('terminal','Continuity Terminal',[95,44,7,10],'term2',{'layer':'terminal'}),('box','Field cache',[3,56,5,11],'box2'),('cradle','Charging cradle',[14,58,8,7],'charger'),('parts','Parts locker',[95,61,7,10],'stb'),('tools','Tool cabinet',[22,85,8,10],'bt2'),('regulator','Regulator housing',[46,54,8,15],'regulator'),('dynamo','Emergency hand charger',[22,67,4,6],'handCharge',{'layer':'dynamo'})])
room('powercontrol',{'spc':[9,45,12,48],'oi':[94,46,11,41]},[
 ('memo','Power control memo',[48,40,3,8],'pwrmemo'),('relays','Relay rack',[62,37,18,21],'relays'),('parts','Spare parts tray',[47,52,10,5],'parts2'),('clearance','Containment authorization console',[60,66,9,10],'clearance',{'layer':'terminal'})])
room('boiler',{'mb':[9,46,11,46]},[
 ('log','Furnace log',[88,54,12,10],'fl'),('furnace','Furnace hatch',[50,49,10,14],'fur'),('pipes','Pipe rack',[31,39,13,31],'pip'),('tin','Tool tin',[31,64,7,7],'mag')])
room('tunnel',{'mt':[13,24,10,42]},[
 ('note','Diver note',[13,74,17,14],'dvn'),('winch','Winch mechanism',[64,74,19,25],'wnc'),('key','Chained key',[87,30,3,10],'tk'),('writing','Faint wall writing',[29,24,5,12],'uv')])
room('morgue',{'mt':[42,31,9,29],'mb':[62,34,11,37],'gm':[86,35,11,38]},[
 ('report','Autopsy report',[27,66,24,13],'aut'),('drawer','Mortuary drawer',[23,31,18,13],'dw'),('cart','Supply cart',[96,64,7,22],'sh')])
room('chapel',{'ac':[8,37,10,39]},[
 ('letter','Chaplain letter',[80,41,9,6],'let'),('reliquary','Reliquary',[55,37,5,10],'rel'),('chest','Field cache',[94,56,11,12],'box3'),('phone','Disconnected telephone',[30,47,4,8],'@phone',{'layer':'phone'})])
room('children',{'rc12':[11,38,14,62]},[
 ('drawing','Children’s drawing',[32,30,9,15],'draw'),('negative','Photographic negative',[46,66,14,8],'neg'),('rabbit','Wind-up rabbit',[85,79,12,22],'toy')])
room('residence',{'rr':[7,31,11,49],'rl':[97,34,6,56]},[
 ('diary','Resident diary',[71,47,7,4],'dia'),('breaker','Breaker panel',[24,23,8,16],'brk'),('terminal','Continuity Terminal',[29,39,8,10],'term4'),('phone','Wall telephone',[34,59,5,8],'@phone',{'layer':'phone'})])
room('stafflounge',{'rl':[9,39,13,65]},[
 ('shaw','Nurse Evelyn Shaw',[78,79,8,27],'shaw',{'actor':'nurse_shaw'}),('note','Staff lounge note',[34,26,9,20],'loungeNote'),('thermos','Thermos and supplies',[59,56,10,12],'coffee'),('harness','Utility harness',[94,33,8,25],'harness'),('sink','Utility sink',[85,38,8,6],'sink'),('phone','Wall telephone',[24,27,3,8],'@phone'),('cache','Supply pouch',[63,68,8,6],'@supply',{'layer':'pouch'})])
room('records',{'ar':[50,34,12,40],'rc':[94,32,9,44]},[
 ('ledger','Memorial ledger',[20,78,17,12],'ledger'),('cabinet','Carbon cabinet',[29,41,14,28],'cab2'),('wall','Sealed service hatch',[75,28,6,8],'wall'),('tape','Field recorder',[59,48,6,5],'lasttape'),('journal','Rourke’s final journal',[73,48,9,5],'finalJournal attendantDiary3'),('phone','Wall telephone',[61,32,4,8],'@phone',{'layer':'phone'})])
room('surgery',{'lr':[4,30,6,43]},[
 ('kessler','Dr. Adrian Kessler',[28,43,8,21],'kessler',{'after':{'flag':'doctorWallSeen','rect':[26,51,10,5]}}),('notes','Operating theatre notes',[20,25,8,9],'opnote'),('tray','Instrument tray',[88,51,12,9],'tray'),('mask','Anaesthesia mask',[75,39,6,12],'mask'),('shotgun','Security shotgun case',[59,34,18,8],'lateShotgun shotShells'),('exit','Bolted theatre exit',[97,29,6,41],'surgeryExit')])
room('observation',{'go':[8,33,12,45],'os':[95,35,9,47]},[
 ('transcript','Transcript 4B',[37,42,6,3],'tr'),('consent','Original consent',[25,26,5,12],'con'),('console','Archive console',[27,38,6,10],'dr'),('glass','Restricted scratched glass',[82,29,7,23],'glasssound'),('notice','Viewing safety notice',[35,37,3,5],'glassNotice'),('phone','Desk telephone',[47,45,5,6],'@phone',{'layer':'phone'})])
room('specimen',{'os':[6,35,10,48],'spc':[95,38,9,53]},[
 ('register','Specimen register',[39,50,11,5],'specdoc'),('fluid','Developing fluid',[50,45,4,10],'dev'),('wire','Wire spool',[70,52,5,7],'wire')])
room('isolation',{'oi':[10,36,13,54]},[
 ('log','Isolation log',[24,32,3,10],'isolog'),('cabinet','Medical cabinet',[95,30,9,25],'medcab medgauze'),('mirror','Covered mirror',[81,42,10,40],'mirror')])
room('coldstore',{'rc':[12,44,16,71]},[
 ('log','Cold storage inventory',[32,32,5,12],'coldlog'),('reel','Continuity reel',[61,55,15,8],'reel'),('medkit','Field medkit',[30,60,6,6],'cachemed')])
room('lift',{'liftEntry':[9,48,14,78]},[
 ('controls','Elevator controls',[79,37,4,24],'liftpanel'),('manifest','Lift service manifest',[91,33,6,18],'liftlog'),('mirror','Elevator mirror',[30,34,7,24],'liftmirror'),('terminal','Final Continuity Terminal',[90,70,8,10],'finalTerminal',{'layer':'terminal'}),('ribbon','Emergency record spool',[81,74,5,4],'finalRibbon'),('cache','Transfer field cache',[91,82,12,9],'finalBox')])
# Loose collectible artwork is separate from each base room and uses authored positions.
loose={
 'lobby':{'desk':[('desk','key',[86,68,4,3])]},
 'security':{'drawer':[('drw','keycard',[29,73,5,4])],'map':[('mapboard','floor_map',[75,58,18,6])]},
 'ward':{'gurney':[('gur','ink_ribbon',[90,64,6,4])],'lockbox':[('nightPistol','handgun',[48,40.3,6.8,2.6])],'ammo':[('pistolRounds','handgun_ammo',[44,43,4,2])]},
 'room12':{'cabinet':[('cab','key',[56,28.5,3,4])],'shelf':[('shf2','dressing',[54,39,5,4])],'drawer':[('drw12','battery',[31,50,5,4])]}
}
for room_id,fixtures in loose.items():
 for fixture in rooms[room_id]['fixtures']:
  if fixture['id'] in fixtures:
   fixture.pop('layer',None)
   fixture['collectibles']=[{'id':id,'asset':'assets/items/'+name+'.png','rect':rect} for id,name,rect in fixtures[fixture['id']]]
for f in rooms['security']['fixtures']:
 if f['id']=='clara':f['actorHit']='46% 2%,59% 3%,64% 8%,63% 17%,70% 23%,73% 50%,72% 57%,70% 65%,72% 91%,75% 99%,60% 99%,55% 71%,51% 61%,48% 76%,45% 92%,47% 96%,32% 96%,30% 92%,36% 72%,37% 61%,29% 54%,30% 32%,35% 22%,43% 18%,42% 10%'
 if f['id']=='cabinet':f['ids']=['rev']
(ROOT/'data/chapter1_scenes.json').write_text(json.dumps(rooms,indent=2,ensure_ascii=False)+'\n')
(ROOT/'js/scene_manifest.js').write_text('/* Generated from the explicitly authored data/chapter1_scenes.json. */\nwindow.WardScenes='+json.dumps(rooms,ensure_ascii=False,separators=(',',':'))+';\n')
print('Authored scenes:',len(rooms))
