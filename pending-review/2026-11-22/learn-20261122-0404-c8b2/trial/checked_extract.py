"""Isolated trial alternative, not an installed Skill or production workflow."""
import subprocess, sys, tempfile
from pathlib import Path

def main():
    if len(sys.argv)!=4:
        print('Usage: checked_extract.py INPUT TIME NEW_OUTPUT',file=sys.stderr); return 2
    source, timestamp, target = sys.argv[1:]
    out=Path(target)
    if not Path(source).is_file() or out.exists():
        print('Input missing or output already exists',file=sys.stderr); return 2
    with tempfile.TemporaryDirectory(prefix='frame-trial-') as folder:
        frame=Path(folder)/'frame.png'
        p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n','-abort_on','empty_output','-ss',timestamp,'-i',source,'-map','0:v:0','-frames:v','1',str(frame)])
        if p.returncode!=0: return p.returncode
        if not frame.exists() or frame.stat().st_size==0:
            print('No new image produced',file=sys.stderr); return 3
        verify=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(frame),'-frames:v','1','-f','null','-'])
        if verify.returncode!=0: return 4
        try:
            with out.open('xb') as dest: dest.write(frame.read_bytes())
        except FileExistsError:
            print('Output appeared during extraction',file=sys.stderr); return 2
    print(str(out)); return 0

if __name__=='__main__':sys.exit(main())
