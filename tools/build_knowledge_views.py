#!/usr/bin/env python3
"""Generate browsable inventory and compact task views from authoritative metadata."""
import argparse
import json
from pathlib import Path
import subprocess
from query_knowledge import ROOT, MODES, SKILLS, eligible

def generate(root=ROOT):
    root=Path(root);c=json.loads((root/'knowledge/catalog.json').read_text());outputs={}
    for mode in MODES:
        for skill in (list(SKILLS) if mode in ('production','analysis') else [None]):
            name=mode+('-'+skill if skill else '')
            lines=['# '+name+' 短目录','', '只作定位，不替代正文。先按任务资格与适用条件筛选，候选与案例不自动成为制作规则。','', '| ID | 用途 | 定位 |','|---|---|---|']
            for e in c['entries']:
                if eligible(e,mode,[skill] if skill else None):
                    loc=e['path']+(' → '+e['section'] if e.get('section') else '')
                    lines.append('| '+e['id']+' | '+e['status']+'；'+e['summary'].replace('|','／')+' | '+loc+' |')
            outputs['knowledge/views/'+name+'.md']='\n'.join(lines)+'\n'
    paths=set(subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines())
    paths.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=root,text=True).splitlines())
    paths.update(outputs);paths.update(['registry/library-inventory.json','knowledge/library-map.md'])
    records=[]
    for path in sorted(paths):
        if any(part in ('__pycache__','.cache') for part in Path(path).parts) or path.endswith('.pyc'):continue
        if not (root/path).exists() and path not in outputs and path not in ('registry/library-inventory.json','knowledge/library-map.md'): continue
        group='history' if any(x in Path(path).parts for x in ('history','archive','failure-history')) else 'pending' if path.startswith('pending-review/') else 'runtime' if path.startswith(('skills/','knowledge/')) else 'tools' if path.startswith('tools/') else 'registry' if path.startswith('registry/') else 'repository'
        records.append({'path':path,'group':group})
    outputs['registry/library-inventory.json']=json.dumps({'schema':1,'scope':'Browsable paths, not a list of executable rules','entries':records},ensure_ascii=False,indent=2)+'\n'
    lines=['# 知识图书馆导航','', '正文只有一份权威来源。分类与短目录是可重建视图；全库可见不等于全库可执行。','', '## 按任务检索','']
    for path in outputs:
        if path.startswith('knowledge/views/'):lines.append('- ['+Path(path).stem+'](views/'+Path(path).name+')')
    lines += ['', '## 内容所在位置','', '- skills：三套入口与媒介专用正文。','- knowledge/shared：公共规则。','- knowledge/catalog.json：带状态和精确定位的运行目录。','- pending-review：候选、来源与审计证据，按状态使用。','- history 与各级 archive：历史追溯，不执行旧指令。','- registry：版本、恢复与清单。','- tools：确定性检索、读取与检查工具。','', '完整路径清单见 [library-inventory.json](../registry/library-inventory.json)。新增正文后更新元数据，再运行 tools/build_knowledge_views.py；不要手工维护第二份知识。']
    outputs['knowledge/library-map.md']='\n'.join(lines)+'\n'
    return outputs

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    outputs=generate()
    for path,text in outputs.items():
        target=ROOT/path
        if a.check:
            if not target.is_file() or target.read_text()!=text:raise SystemExit('Stale generated view: '+path)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    print(json.dumps({'result':'PASS','generated_files':len(outputs),'check_only':a.check}))
if __name__=='__main__':main()
