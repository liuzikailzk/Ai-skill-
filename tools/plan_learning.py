#!/usr/bin/env python3
"""Resolve the approved daily subject and check pending metadata coverage."""
import argparse
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from query_knowledge import safe_path

ROOT = Path(__file__).resolve().parents[1]

def load_curriculum(root=ROOT):
    return json.loads((Path(root)/'knowledge/curriculum.json').read_text())

def plan(day, config):
    if isinstance(day,str):day=date.fromisoformat(day)
    anchor=date.fromisoformat(config['cycle_anchor_monday'])
    if anchor.weekday()!=0:raise ValueError('Cycle anchor must be Monday')
    if day<date.fromisoformat(config['effective_from']):
        return {'date':day.isoformat(),'active':False,'reason':'课表尚未生效，不补跑已完成日期'}
    if config.get('trial_end') and day>date.fromisoformat(config['trial_end']):
        return {'date':day.isoformat(),'active':False,'reason':'本周试行已结束；不自动续期或补跑'}
    week=config['cycle_weeks'][((day-anchor).days//7)%len(config['cycle_weeks'])]
    course=config['weekly'][str(day.weekday())]
    if isinstance(course,dict):course=course[week]
    return {'date':day.isoformat(),'timezone':config['timezone'],'active':True,'week':week,
            'course_id':course,**config['courses'][course],
            'common_goal':config.get('common_standard',{}).get('goal'),
            'required_output_items':[x['name'] for x in config.get('common_standard',{}).get('deliverables',[])],
            'empty_result_rule':config.get('common_standard',{}).get('honest_empty_result'),
            'pilot_review_due':day==date.fromisoformat(config['pilot_review_on']),
            'saturday_backup_due':day.weekday()==5,'friday_review_due':day.weekday()==4,
            'execution_note':'仅确定当日科目；先查当日运行/预算，同日已完成不重跑。没有执行研究或生成。'}

def check_index(root=ROOT):
    root=Path(root);catalog=json.loads((root/'knowledge/catalog.json').read_text())
    active=json.loads((root/'pending-review/active-index.json').read_text())
    by_path={e['path']:e for e in catalog['entries']};issues=[];checked=0
    for item in active['items']:
        if item['status'] not in ('candidate','observing','conflicted'):continue
        checked+=1;path=item['source_path'];entry=by_path.get(path)
        if entry is None:
            issues.append({'id':item['id'],'reason':'missing_catalog_entry'});continue
        source=safe_path(root,path)
        if not source.is_file():
            issues.append({'id':item['id'],'reason':'missing_source'});continue
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        if digest!=entry.get('sha256') or digest!=item.get('sha256'):
            issues.append({'id':item['id'],'reason':'stale_metadata_hash'})
        if entry['status']!=item['status']:
            issues.append({'id':item['id'],'reason':'status_mismatch'})
        if not {'learning','lookup'}.issubset(entry['modes']) or {'production','analysis'}.intersection(entry['modes']):
            issues.append({'id':item['id'],'reason':'pending_scope_violation'})
    return {'result':'FAIL' if issues else 'PASS','pending_items_checked':checked,'issues':issues,
            'scope':'索引元数据完整性，不代表方法验证或人类票通过'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--date',help='Asia/Shanghai local date, YYYY-MM-DD')
    p.add_argument('--days',type=int,default=1)
    p.add_argument('--check-index',action='store_true')
    a=p.parse_args()
    if a.check_index:
        result=check_index()
    else:
        c=load_curriculum();day=date.fromisoformat(a.date) if a.date else datetime.now(ZoneInfo(c['timezone'])).date()
        if not 1<=a.days<=31:p.error('--days must be 1..31')
        result=plan(day,c) if a.days==1 else [plan(day+timedelta(days=i),c) for i in range(a.days)]
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if isinstance(result,dict) and result.get('result')=='FAIL':raise SystemExit(1)
if __name__=='__main__':main()
