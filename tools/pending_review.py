#!/usr/bin/env python3
"""List only the recent seven days, or compact explicitly closed stale candidates.

Closed originals are retrievable from a verified immutable Git commit. Only
candidate JSON files are removed; unresolved candidates and shared reports stay.
"""
import argparse
import calendar
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

DAY=re.compile(r'^\d{4}-\d{2}-\d{2}$')
SHA=re.compile(r'^[0-9a-f]{40}$')
def digest(data):return hashlib.sha256(data).hexdigest()
def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temp.replace(path)
def recent_dates(root,today):
    cutoff=today-timedelta(days=6)
    return sorted(p.name for p in (root/'pending-review').iterdir() if p.is_dir() and DAY.fullmatch(p.name) and cutoff<=date.fromisoformat(p.name)<=today)
def candidates(root):
    # Full scan is reserved for cleanup or explicit maintenance, never daily list.
    for folder in sorted((root/'pending-review').iterdir()):
        if not folder.is_dir() or not DAY.fullmatch(folder.name):continue
        for f in sorted(folder.rglob('candidate-*.json')):
            if f.is_symlink():raise ValueError('Candidate symlink is not allowed')
            record=json.loads(f.read_text());yield f,record
def final_decision(root,record):
    d=record.get('archive_decision')
    if not isinstance(d,dict) or d.get('decision') not in ('merged','rejected'):return None
    if not d.get('human_reference') or not d.get('decided_at'):return None
    try:date.fromisoformat(d['decided_at'][:10])
    except (TypeError,ValueError):return None
    if d['decision']=='merged':
        target=(root/d.get('target_path','')).resolve()
        if not target.is_relative_to((root/'skills').resolve()) or not target.is_file() or d.get('release_verified') is not True or not SHA.fullmatch(d.get('release_commit','')):return None
    return d
def build_plan(root,today):
    cutoff=today-timedelta(days=6);eligible=[];retained=[]
    for f,r in candidates(root):
        relative=f.relative_to(root).as_posix();source_day=date.fromisoformat(f.relative_to(root/'pending-review').parts[0]);d=final_decision(root,r)
        item={'id':r.get('id',r.get('candidate_id',f.stem)),'source_path':relative,'sha256':digest(f.read_bytes()),'status':r.get('status','unknown')}
        if d and source_day<cutoff and date.fromisoformat(d['decided_at'][:10])<cutoff:
            item['decision']=d;eligible.append(item)
        else:
            item['reason']='unresolved_or_no_verified_final_decision' if not d else 'within_recent_seven_days';retained.append(item)
    return {'date':today.isoformat(),'recent_start':cutoff.isoformat(),'recent_dates':recent_dates(root,today),'eligible':eligible,'retained':retained}
def compact(root,today,source_commit,manual=False,apply=False):
    root=Path(root).resolve()
    if not manual and today.day!=calendar.monthrange(today.year,today.month)[1]:raise ValueError('Compaction requires month end or explicit manual trigger')
    plan=build_plan(root,today)
    if not apply:return plan
    if not SHA.fullmatch(source_commit or ''):raise ValueError('An immutable source commit is required')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if head!=source_commit:raise ValueError('Source commit is not the fixed local HEAD')
    index_path=root/'pending-review/archive/index.json';index=json.loads(index_path.read_text()) if index_path.exists() else {'schema':1,'items':[]}
    for item in plan['eligible']:
        data=(root/item['source_path']).read_bytes()
        old=subprocess.check_output(['git','show',source_commit+':'+item['source_path']],cwd=root)
        if digest(data)!=item['sha256'] or data!=old:raise ValueError('Candidate changed since snapshot; stop cleanup')
        d=item['decision']
        if d['decision']=='merged':
            subprocess.check_call(['git','cat-file','-e',d['release_commit']+':'+d['target_path']],cwd=root)
    known={x['source_path'] for x in index['items']}
    for item in plan['eligible']:
        if item['source_path'] not in known:
            index['items'].append(item|{'source_commit':source_commit,'archived_on':today.isoformat(),'summary':'pending-review/archive/archive-summary-'+today.strftime('%Y-%m')+'.md'})
    month=today.strftime('%Y-%m');summary=root/'pending-review/archive'/('archive-summary-'+month+'.md')
    text=f'# 暂存候选归档简报 {month}\n\n最近清理日：{today.isoformat()}。固定备份提交：{source_commit}。\n\n'
    items=[x for x in index['items'] if x['archived_on'].startswith(month)]
    text+=f'本月累计归档 {len(items)} 个已核实终态且超过近7天窗口的候选；本次 {len(plan["eligible"])} 个。未决候选及共用报告未删除。\n\n'
    for x in items:
        d=x['decision'];url='https://github.com/liuzikailzk/Ai-skill-/blob/'+x['source_commit']+'/'+x['source_path']
        text+=f'- {x["id"]}：{d["decision"]}；决定依据：{d["human_reference"]}；[原件]({url})；SHA-256：{x["sha256"]}。\n'
    if not items:text+='暂无可核实的已合并/已拒绝过期候选，未进行候选删除。\n'
    summary.parent.mkdir(parents=True,exist_ok=True);summary.write_text(text)
    dump(index_path,index)  # Archive pointers land before any candidate is removed.
    for item in plan['eligible']:
        if digest((root/item['source_path']).read_bytes())!=item['sha256']:raise ValueError('Concurrent candidate change; stop deletion')
    for item in plan['eligible']:(root/item['source_path']).unlink()
    dump(root/'pending-review/active-index.json',{'schema':1,'updated_on':today.isoformat(),'recent_start':plan['recent_start'],'items':plan['retained'],'note':'Metadata only. Daily list does not open old candidate bodies; old unresolved entries remain pending.'})
    dump(root/'pending-review/last-cleanup.json',{'date':today.isoformat(),'source_commit':source_commit,'manual':manual,'archived_count':len(plan['eligible']),'retained_count':len(plan['retained']),'summary':summary.relative_to(root).as_posix()})
    return plan|{'applied':True,'archived_count':len(plan['eligible'])}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['list','compact']);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--date',type=date.fromisoformat,default=datetime.now(ZoneInfo('Asia/Shanghai')).date());p.add_argument('--source-commit');p.add_argument('--manual',action='store_true');p.add_argument('--apply',action='store_true');a=p.parse_args();root=a.root.resolve()
    if a.command=='list':result={'date':a.date.isoformat(),'recent_dates':recent_dates(root,a.date),'older_bodies_read':0,'active_index':'pending-review/active-index.json'}
    else:result=compact(root,a.date,a.source_commit,a.manual,a.apply)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
