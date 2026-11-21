import hashlib, json, subprocess, shutil
from pathlib import Path

root=Path(__file__).resolve().parent
def run(args):
    p=subprocess.run(args,cwd=root,capture_output=True,text=True)
    return {'args':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
create=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','testsrc2=size=160x96:rate=24:duration=2','-an','-c:v','libx264','-preset','veryfast','-crf','18','-g','48','-bf','2','fixture.mp4']
setup=run(create)
assert setup['returncode']==0,setup
probe=run(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,key_frame','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_frames,start_time,duration','-of','json','fixture.mp4'])
metadata=json.loads(probe['stdout'])
cases=[]
for name,opts in [('first',[]),('time125',['--time','00:00:01.250']),('index30',['--index','30']),('past_end',['--time','00:01:39']),('past_index',['--index','999'])]:
    out=root/(name+'.png')
    assert not out.exists(),'Use a fresh trial directory'
    result=run(['bash','frame.sh','fixture.mp4',*opts,'--out',out.name])
    result.update(name=name,exists=out.exists(),bytes=out.stat().st_size if out.exists() else 0,sha256=digest(out))
    cases.append(result)
stale=root/'stale.png';shutil.copyfile(root/'first.png',stale);before=digest(stale)
result=run(['bash','frame.sh','fixture.mp4','--time','00:01:39','--out','stale.png'])
result.update(name='past_end_existing_file',exists=stale.exists(),sha256=digest(stale),before_sha256=before,unchanged=digest(stale)==before)
cases.append(result)
reference=run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','fixture.mp4','-vf','select=eq(n\\,30)','-frames:v','1','reference30.png'])
assert reference['returncode']==0,reference
def pixels(p):
    data=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-f','rawvideo','-pix_fmt','rgb24','-'])
    return hashlib.sha256(data).hexdigest()
comparisons={name:pixels(root/(name+'.png')) for name in ['time125','index30','reference30']}
result={'fixture':'synthetic calibration, not a film or production deliverable','setup':setup,'source_sha256':digest(root/'fixture.mp4'),'script_sha256':digest(root/'frame.sh'),'metadata':metadata,'cases':cases,'reference_command':reference,'decoded_rgb_hashes':comparisons,'same_target_pixels':len(set(comparisons.values()))==1,'ffmpeg':run(['ffmpeg','-version'])['stdout'].splitlines()[0],'ffprobe':run(['ffprobe','-version'])['stdout'].splitlines()[0]}
(root/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'frames':len(metadata['frames']),'cases':[{k:c[k] for k in ['name','returncode','exists'] } for c in cases],'same_target_pixels':result['same_target_pixels'],'stale_unchanged':cases[-1]['unchanged']},ensure_ascii=False))
