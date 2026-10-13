import unittest,copy
from datetime import date
from audit_gate import evaluate

def valid():
    return {'id':'fixture','proposed_version':'1.1.0','proposal_action':'iteration','existing_skill':'fixture-skill','status':'observing',
    'searches':[{'slot':n,'query':'material bug' if n==3 else 'material','time':f'2026-10-16T09:0{n}:00+08:00','scope':'official and independent','summary':'fixture','result_status':'completed'} for n in [1,2,3]],
    'sources':[{'id':n,'tier':t,'first_party':n=='a','identity_verified':True,'url':'https://example.invalid/'+n,'title':n,'author':n,'retrieved_at':'2026-10-16T09:00:00+08:00'} for n,t in [('a','S'),('b','A')]],
    'independence':[{'first':'a','second':'b','verdict':'independent','reason':'fictional test teams differ'}],
    'evidence_matrix':[{'claim':'fixture claim','supports':['a','b'],'confidence':'high'}],
    'reproduction':{'environment':{'model':'fictional-test'},'steps':['fixture'],'parameters':{'prompt':'fixture'},'seed_availability':'not exposed','expected':'fixture','actual':{'artifact':'test fixture, not real generation'},'failure_conditions':['fixture'],'passed':True},
    'currency':{'kind':'generation','last_verified':'2026-10-16','expires_on':'2027-04-16'},
    'overlap':{'percent':75,'dimensions':[{'denominator':2,'points':[1,0.5],'comparisons':['same','partial']} for _ in range(4)]},
    'adversarial_review':['fixture answer']*7,'human_vote':{'approved':True,'revoked':False,'version':'1.1.0','user_quote':'fictional test only','time':'2026-10-16T15:00:00+08:00','review_id':'fixture'},
    'regression':{'fixed_task':'fixture','environment':'same','old_run':'fixture-old','new_run':'fixture-new','comparison':'fixture','rollback_target':'1.0.0','passed':True},
    'version_comparison':[{'old':'1.0.0','new':'1.1.0'}],'release':{'verified':True,'verification_evidence':'fictional fixture only'}}
class GateTests(unittest.TestCase):
    def check(self,x,ledger=None):return evaluate(x,{'freezes':[]} if ledger is None else ledger,date(2026,10,16))
    def test_complete_fixture(self):self.assertTrue(self.check(valid())['may_publish'])
    def test_no_actual(self):
        x=valid();x['reproduction']['actual']=None;self.assertEqual(self.check(x)['maximum_permitted_status'],'candidate')
    def test_no_human(self):
        x=valid();x['human_vote']={};self.assertEqual(self.check(x)['maximum_permitted_status'],'observing')
    def test_duplicate_or_partial_source(self):
        for change in ['partial','duplicate']:
            x=valid()
            if change=='partial':x['independence'][0]['verdict']='partially_independent'
            else:x['sources'][1]['url']=x['sources'][0]['url']
            self.assertFalse(self.check(x)['evidence_vote'])
    def test_conflict_even_with_human(self):
        x=valid();x['unresolved_conflict']=True;self.assertEqual(self.check(x)['maximum_permitted_status'],'conflicted')
    def test_overlap(self):
        x=valid();x['proposal_action']='new_skill';self.assertIn('overlap_70_requires_iteration',self.check(x)['gaps'])
    def test_freeze(self):self.assertFalse(self.check(valid(),{'freezes':[{'starts_on':'2026-10-15','ends_on':'2026-10-20'}]})['may_publish'])
    def test_revoked(self):
        x=valid();x['human_vote']['revoked']=True;self.assertFalse(self.check(x)['may_publish'])
    def test_expiry(self):
        x=valid();x['currency']['expires_on']='2026-10-01';self.assertFalse(self.check(x)['may_publish'])
    def test_counterquery(self):
        x=valid();x['searches'][2]['query']='material';self.assertFalse(self.check(x)['evidence_vote'])
    def test_saved_failure(self):
        x=valid();x['release']['verified']=False;self.assertFalse(self.check(x)['may_publish'])
    def test_wrong_version(self):
        x=valid();x['human_vote']['version']='1.0.0';self.assertFalse(self.check(x)['may_publish'])
    def test_archived_never_automatic_publish(self):
        for state in ['deprecated','rolled_back']:
            x=valid();x['status']=state;self.assertFalse(self.check(x)['may_publish'])
    def test_active_expired_deprecated(self):
        x=valid();x['status']='active';x['currency']['expires_on']='2026-10-01';self.assertEqual(self.check(x)['maximum_permitted_status'],'deprecated')
if __name__=='__main__':unittest.main()
