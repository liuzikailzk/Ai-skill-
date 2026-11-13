#!/usr/bin/env python3
"""Prepare minimal daily records; remote publication/readback is a separate required step."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LIMITS = {'techniques': 3, 'news': 1}
PURPOSES = ['candidate', 'cross_validation', 'counterevidence']

def validate(d):
    if set(d) != {'schema','date','run_id','status','techniques','news'}: raise ValueError('Unexpected fields')
    if d['schema'] != 1 or date.fromisoformat(d['date']).isoformat() != d['date']: raise ValueError('Invalid schema/date')
    if not re.fullmatch(r'[A-Za-z0-9-]{1,64}',d['run_id']): raise ValueError('Invalid run_id')
    if d['status'] not in ['in_progress','completed','partial_closed']: raise ValueError('Invalid status')
    for kind,limit in LIMITS.items():
        if not isinstance(d[kind],list) or len(d[kind])>limit: raise ValueError('Quota exceeded')
        for n,q in enumerate(d[kind],1):
            if set(q) != {'slot','purpose','query_sha256','status'}: raise ValueError('Unexpected query fields')
            if q['slot'] != n or q['purpose'] != (PURPOSES[n-1] if kind=='techniques' else 'news'): raise ValueError('Invalid slot/purpose')
            if not re.fullmatch('[0-9a-f]{64}',q['query_sha256']): raise ValueError('Invalid query digest')
            if q['status'] not in ['reserved','completed','failed','uncertain']: raise ValueError('Invalid query status')
            if n<len(d[kind]) and q['status']=='reserved': raise ValueError('Earlier query unresolved')
    return d

def initialize(day,run_id,legacy):
    if day in legacy.get('days',{}) or day in legacy.get('news_days',{}): raise ValueError('Existing legacy date: reconcile; never reset quota')
    current=legacy.get('current_run')
    if isinstance(current,dict) and current.get('date')==day: raise ValueError('Legacy run in progress')
    return validate(dict(schema=1,date=day,run_id=run_id,status='in_progress',techniques=[],news=[]))

def reserve(d,run_id,kind,query):
    validate(d)
    if run_id!=d['run_id'] or d['status']!='in_progress': raise ValueError('Not owned or closed')
    if not query.strip(): raise ValueError('Empty query')
    rows=d[kind];digest=hashlib.sha256(query.encode()).hexdigest()
    if any(q['query_sha256']==digest for q in rows): raise ValueError('Already reserved/attempted; do not resend')
    if len(rows)>=LIMITS[kind] or any(q['status'] in ['reserved','uncertain'] for q in rows): raise ValueError('Quota exhausted or unresolved slot')
    n=len(rows)+1;rows.append(dict(slot=n,purpose=PURPOSES[n-1] if kind=='techniques' else 'news',query_sha256=digest,status='reserved'))
    return validate(d)

def finish(d,run_id,kind,slot,result):
    validate(d)
    if run_id!=d['run_id'] or d['status']!='in_progress': raise ValueError('Not owned or closed')
    if result not in ['completed','failed','uncertain'] or not 1<=slot<=len(d[kind]): raise ValueError('Invalid completion')
    q=d[kind][slot-1]
    if q['status'] not in ['reserved',result]: raise ValueError('Cannot rewrite prior result')
    q['status']=result
    return validate(d)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['status','init','reserve','finish','close']);p.add_argument('--date',required=True);p.add_argument('--run-id',required=True);p.add_argument('--kind',choices=LIMITS);p.add_argument('--query');p.add_argument('--slot',type=int);p.add_argument('--result',choices=['completed','failed','uncertain','partial_closed']);a=p.parse_args()
    if date.fromisoformat(a.date).isoformat()!=a.date: raise ValueError('Noncanonical date')
    path=ROOT/'registry/learning-days'/f'{a.date}.json'
    if a.action=='init':
        if path.exists(): raise ValueError('Daily record exists; use status')
        legacy=json.loads((ROOT/'skills/script-video-shot-director/references/audit/global-state.json').read_text())
        d=initialize(a.date,a.run_id,legacy)
    else:
        d=validate(json.loads(path.read_text()))
        if d['date']!=a.date: raise ValueError('Filename and record date mismatch')
        if a.action=='reserve':
            if a.kind is None or a.query is None: p.error('reserve requires --kind and --query')
            reserve(d,a.run_id,a.kind,a.query)
        elif a.action=='finish':
            if a.kind is None or a.slot is None or a.result not in ['completed','failed','uncertain']: p.error('finish requires --kind --slot --result completed|failed|uncertain')
            finish(d,a.run_id,a.kind,a.slot,a.result)
        elif a.action=='close':
            if d['run_id']!=a.run_id: raise ValueError('Not owned')
            if any(q['status']=='reserved' for k in LIMITS for q in d[k]): raise ValueError('Unresolved queries cannot close')
            if a.result not in ['completed','partial_closed']: p.error('close requires --result completed|partial_closed')
            if d['status']!='in_progress' and d['status']!=a.result: raise ValueError('Cannot change closed result')
            d['status']=a.result
    validate(d)
    if a.action!='status':
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'record':d,'remote_publication_verified':False},ensure_ascii=False))
if __name__=='__main__': main()
