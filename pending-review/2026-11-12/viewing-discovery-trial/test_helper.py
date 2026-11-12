import json,socket,subprocess,sys,time,platform,importlib.metadata
from pathlib import Path
def port_open():
 try:
  with socket.create_connection(('127.0.0.1',8765),timeout=.3):return True
 except OSError:return False
assert not port_open(),'Port is in use; do not stop unrelated service'
results=[]
for label,command,port,expected in [('successful_command',['python3','probe_server.py','0'],8765,0),('failed_command',['python3','probe_server.py','7'],8765,7),('startup_timeout',['python3','probe_server.py','0'],8766,1)]:
 args=['python3','with_server.py','--server','exec python3 fixture_server.py','--port',str(port),'--timeout','2','--',*command]
 r=subprocess.run(args,text=True,capture_output=True,timeout=12)
 Path('helper-'+label+'.log').write_text(r.stdout+r.stderr)
 closed=not port_open()
 results.append({'case':label,'command':args,'expected_exit':expected,'actual_exit':r.returncode,'port_closed_after':closed,'pass':r.returncode==expected and closed})
 assert results[-1]['pass'],results[-1]
data={'scope':'with_server.py lifecycle only; no browser/UI assertions executed','python':platform.python_version(),'playwright':importlib.metadata.version('playwright'),'results':results,'ui_test_status':'blocked_by_environment_browser_socket_permission','browser_attempts':[{'mode':'default bundled chromium','result':'executable missing'},{'mode':'existing /usr/bin/chromium','result':'socket() failed: Operation not permitted; stopped without bypass'}]}
Path('webapp-test-results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(data,ensure_ascii=False,indent=2))
