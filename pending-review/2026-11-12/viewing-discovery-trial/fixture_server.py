from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse
import json,time

PAGE='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>资格材料交互试验页</title>
<style>body{font:18px system-ui;background:#f2f5f9;padding:40px;color:#182537}main{max-width:760px;margin:auto;background:white;border-radius:18px;padding:36px}small{color:#6b7480}label{display:block;margin:22px 0}section{padding:18px;background:#f2f5ff;border-radius:10px}button{padding:12px 30px;background:#3659c7;color:white;border:0;border-radius:8px}#result{margin-top:24px}</style>
<main><small>本地模拟 · 非真实业务系统 · 不含真实考生数据</small><h1>资格材料交互试验页</h1><div id="app">正在加载表单…</div></main>
<script>
const q=new URLSearchParams(location.search);
fetch('/form').then(r=>r.text()).then(html=>{
 document.querySelector('#app').innerHTML=html;
 const checkbox=document.querySelector('#qualification'), material=document.querySelector('#material'), section=document.querySelector('#materials');
 checkbox.addEventListener('change',()=>{section.hidden=!checkbox.checked;if(q.get('bug')==='1'){if(checkbox.checked)material.required=true;}else material.required=checkbox.checked;document.querySelector('#result').textContent='';});
 document.querySelector('#next').addEventListener('click',()=>{document.querySelector('#result').textContent=document.querySelector('form').checkValidity()?'可进入下一步':'请补充材料';});
});
if(q.get('poll')==='1')setInterval(()=>fetch('/poll'),200);
</script></html>'''
FORM='''<form novalidate><label><input type="checkbox" id="qualification">专项资格</label><section id="materials" hidden><label for="material">资格材料</label><input type="file" id="material"></section><button type="button" id="next">下一步</button><div id="result" role="status" aria-live="polite"></div></form>'''
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/form':time.sleep(.15);body=FORM
  elif path=='/poll':body='{}'
  else:body=PAGE
  data=body.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def log_message(self,*args):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
