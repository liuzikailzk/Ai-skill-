#!/usr/bin/env python3
"""Read-only checks for recorded audit gates; never proves source truth or votes for the user."""
import argparse, json
from datetime import datetime, date
from pathlib import Path

def present(value):
    return value is not None and value != '' and value != [] and value != {}

def evaluate(item, ledger, as_of):
    errors=[]; evidence=[]; repro=[]; release=[]
    target=item.get('proposed_version')
    searches=item.get('searches',[])
    if sorted(x.get('slot',0) for x in searches)!=[1,2,3]: evidence.append('three_sequential_search_records_required')
    elif any(x.get('result_status')!='completed' or not all(present(x.get(k)) for k in ['query','time','scope','summary']) for x in searches): evidence.append('search_result_or_metadata_missing')
    else:
        times=[datetime.fromisoformat(x['time']) for x in sorted(searches,key=lambda x:x['slot'])]
        if times!=sorted(times): evidence.append('searches_not_sequential')
        reverse=next(x for x in searches if x['slot']==3)
        if not any(w in reverse['query'].lower() for w in ['失效','踩坑','bug','不兼容','替代','deprecated']): evidence.append('countersearch_terms_missing')
    sources={s['id']:s for s in item.get('sources',[])}
    qualifying=[]
    for pair in item.get('independence',[]):
        a=sources.get(pair.get('first'),{}); b=sources.get(pair.get('second'),{})
        if (a.get('tier') in ['S','A'] and b.get('tier') in ['A','B'] and a.get('first_party') is True
            and a.get('id')!=b.get('id') and a.get('url')!=b.get('url') and pair.get('verdict')=='independent'
            and present(pair.get('reason')) and a.get('identity_verified') and b.get('identity_verified')):
            qualifying.append(pair)
    if not qualifying: evidence.append('primary_SA_plus_independent_AB_required')
    for s in sources.values():
        if not all(present(s.get(k)) for k in ['url','title','author','retrieved_at']): evidence.append('source_metadata_missing:'+s['id'])
    claims=item.get('evidence_matrix',[])
    if not claims: evidence.append('claim_matrix_missing')
    for c in claims:
        ids=c.get('supports',[])
        if not present(c.get('claim')) or not any(p['first'] in ids and p['second'] in ids for p in qualifying): evidence.append('core_claim_lacks_independent_support')
    conflict=item.get('unresolved_conflict',False) or item.get('fatal_counterevidence',False)
    if conflict:evidence.append('unresolved_conflict')
    if item.get('rejected',False) or item.get('compliance_block',False):evidence.append('proposal_rejected_or_compliance_block')
    r=item.get('reproduction',{})
    for k in ['environment','steps','parameters','seed_availability','expected','actual','failure_conditions']:
        if not present(r.get(k)):repro.append('reproduction_missing:'+k)
    if not r.get('passed'):repro.append('reproduction_not_passed')
    if not isinstance(r.get('actual'),dict) or not present(r.get('actual',{}).get('artifact')):repro.append('actual_artifact_missing')
    currency=item.get('currency',{})
    if not present(currency.get('last_verified')):release.append('last_verified_missing')
    expiry=currency.get('expires_on')
    if expiry and date.fromisoformat(expiry)<as_of:release.append('expired')
    if currency.get('kind')=='theory' and currency.get('current_version_applicable') is not True:release.append('theory_current_applicability_missing')
    if currency.get('kind') in ['volatile','generation'] and not expiry:release.append('expiry_missing')
    overlap=item.get('overlap',{})
    dims=overlap.get('dimensions',[])
    if len(dims)!=4:release.append('four_dimension_overlap_required')
    else:
        values=[]
        for dim in dims:
            n=dim.get('denominator',0); pts=dim.get('points',[])
            if not n or len(pts)>n or any(v not in [0,0.5,1] for v in pts) or not dim.get('comparisons'):release.append('overlap_item_scoring_invalid');continue
            values.append(sum(pts)/n)
        if len(values)==4:
            percent=sum(values)*25
            if abs(percent-overlap.get('percent',-1))>0.01:release.append('overlap_percent_mismatch')
            if percent>=70 and (item.get('proposal_action')!='iteration' or not item.get('existing_skill')):release.append('overlap_70_requires_iteration')
    answers=item.get('adversarial_review',[])
    if len(answers)!=7 or not all(present(a) for a in answers):release.append('seven_adversarial_answers_required')
    vote=item.get('human_vote',{})
    vote_pass=bool(vote.get('approved') and not vote.get('revoked') and target and vote.get('version')==target
                   and all(present(vote.get(k)) for k in ['user_quote','time','review_id']))
    if not vote_pass:release.append('human_vote_missing_revoked_or_wrong_version')
    elif datetime.fromisoformat(vote['time']).astimezone(__import__('zoneinfo').ZoneInfo('Asia/Shanghai')).weekday()!=4:release.append('friday_human_review_required')
    regression=item.get('regression',{})
    if not all(present(regression.get(k)) for k in ['fixed_task','environment','old_run','new_run','comparison','rollback_target']) or regression.get('passed') is not True:release.append('fixed_old_new_regression_required')
    if not item.get('version_comparison'):release.append('version_comparison_missing')
    if ledger is None:release.append('global_ledger_unavailable')
    else:
        if any(date.fromisoformat(f['ends_on'])>=as_of and date.fromisoformat(f['starts_on'])<=as_of for f in ledger.get('freezes',[])):release.append('admission_frozen')
    if item.get('release',{}).get('verified') is not True or not item.get('release',{}).get('verification_evidence'):release.append('release_save_not_verified')
    if conflict:status='conflicted'
    elif 'expired' in release:status='deprecated' if item.get('status')=='active' else 'candidate'
    elif item.get('status') in ['deprecated','rolled_back']:status=item['status']
    elif evidence or repro:status='candidate'
    elif release:status='observing'
    else:status='active'
    return {'id':item.get('id'),'evidence_vote':not evidence,'reproduction_vote':not repro,'human_vote':vote_pass,
            'maximum_permitted_status':status,'may_publish':status=='active' and not(evidence or repro or release),'gaps':evidence+repro+release,
            'scope':'Recorded-field validation only; no independent verification of source truth, actual artifacts, or user identity.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('record');ap.add_argument('--ledger');ap.add_argument('--date',default=date.today().isoformat());a=ap.parse_args()
    record=json.loads(Path(a.record).read_text());ledger=json.loads(Path(a.ledger).read_text()) if a.ledger else None
    print(json.dumps(evaluate(record,ledger,date.fromisoformat(a.date)),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
