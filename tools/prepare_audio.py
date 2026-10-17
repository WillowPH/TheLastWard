"""Transcode selected CC0 recordings and create two foley derivatives.
Source checkout: https://github.com/lavenderdotpet/CC0-Public-Domain-Sounds
No synthesized waveforms or electronic replacement tones are used.
"""
from pathlib import Path
import subprocess,json,hashlib,sys,shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/ward-cc0')
OUT=ROOT/'audio/chapter1';OUT.mkdir(parents=True,exist_ok=True)
files={
'door_open':'100-CC0-SFX/door_open.ogg','door_close':'100-CC0-SFX/door_close_02.ogg',
'step_tile_1':'100-cc0-sfx-2/sfx100v2_footstep_01.ogg','step_tile_2':'100-cc0-sfx-2/sfx100v2_footstep_02.ogg',
'step_wet':'100-cc0-sfx-2/sfx100v2_footstep_wet_02.ogg','step_wood':'100-cc0-sfx-2/sfx100v2_footstep_wood_02.ogg',
'subject_step_1':'warfork-cc0/sounds/world/ft_step_met1.ogg','subject_step_2':'warfork-cc0/sounds/world/ft_step_met2.ogg',
'infected_step':'100-cc0-sfx-2/sfx100v2_footstep_02.ogg','breathing':'80-CC0-creature-SFX/breath.ogg',
'rain':'30-cc0-sfx-loops/rain.ogg','water':'30-cc0-sfx-loops/water_flowing.ogg',
'machine':'100-cc0-sfx-2/sfx100v2_loop_machine_02.ogg','room_hum':'100-cc0-sfx-2/sfx100v2_loop_machine_01.ogg',
'generator_start':'100-CC0-SFX/machine_01.ogg','elevator':'100-CC0-SFX/machine_03.ogg',
'gunshot':'warfork-cc0/sounds/weapons/machinegun_fire.ogg','reload':'warfork-cc0/sounds/weapons/weapon_switch.ogg',
'metal':'100-CC0-SFX/metal_02.ogg','relay':'100-CC0-SFX/key_open_01.ogg','mechanism':'100-CC0-SFX/machine_02.ogg',
'impact':'100-CC0-SFX/hit_03.ogg','glass':'100-CC0-SFX/glass_02.ogg','cloth':'100-CC0-wood-metal-SFX/cloth_01.ogg',
'switch':'100-CC0-SFX/key_open_02.ogg','phone_ring':'100-CC0-SFX/bell_03.ogg'}
# Only select a real cloth recording if supplied by this library.
if not (SOURCE/files['cloth']).exists():files['cloth']='100-CC0-SFX/dishes_01.ogg'
manifest=[]
for name,relative in files.items():
 source=SOURCE/relative
 if not source.exists():raise FileNotFoundError(source)
 filters='alimiter=limit=0.9'
 if name.startswith('subject_step'):filters='asetrate=44100*0.72,aresample=44100,lowpass=f=2800,bass=g=5,alimiter=limit=0.85'
 if name=='infected_step':filters='asetrate=44100*0.84,aresample=44100,alimiter=limit=0.8'
 # Mechanical bell foley in a telephone cadence. This is sampled metal, not a sine ringtone.
 if name=='phone_ring':filters='atrim=duration=0.22,afade=t=out:st=0.12:d=0.1,apad=whole_dur=0.28,aloop=loop=9:size=12348,atrim=duration=2.7,alimiter=limit=0.8'
 target=OUT/(name+'.ogg')
 subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-i',str(source),'-af',filters,'-ar','44100','-ac','1','-c:a','libvorbis','-q:a','4',str(target)],check=True)
 manifest.append({'name':name,'source':relative,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'license':'CC0-1.0','processing':filters})
(ROOT/'audio/SOURCES.json').write_text(json.dumps({'repository':'https://github.com/lavenderdotpet/CC0-Public-Domain-Sounds','commit':subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip(),'recordings':manifest},indent=2)+'\n')
shutil.copy2(SOURCE/'LICENSE',ROOT/'audio/CC0-LICENSE.txt')
print('Prepared',len(manifest),'bundled recorded effects/loops')
