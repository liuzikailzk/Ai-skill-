from pathlib import Path
from datetime import date,timedelta
import copy,json,sys,tempfile,hashlib,unittest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import plan_learning as p

class CurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.c=p.load_curriculum()
    def test_completed_today_not_reassigned(self):self.assertFalse(p.plan('2026-10-26',self.c)['active'])
    def test_first_run_is_style(self):
        r=p.plan('2026-10-27',self.c);self.assertEqual((r['week'],r['course_id']),('A','style'))
    def test_alternating_subjects(self):
        for day,course in [('2026-10-29','motion'),('2026-11-05','performance'),('2026-10-31','assets'),('2026-11-07','workflow')]:
            self.assertEqual(p.plan(day,self.c)['course_id'],course)
    def test_core_classes_repeat(self):
        for day,course in [('2026-11-02','prompt'),('2026-11-09','prompt'),('2026-11-03','style'),('2026-11-10','style')]:self.assertEqual(p.plan(day,self.c)['course_id'],course)
    def test_pilot_covers_all_subjects(self):
        days=[p.plan(date(2026,10,27)+timedelta(days=i),self.c) for i in range(14)]
        self.assertEqual({x['course_id'] for x in days},set(self.c['courses']))
        self.assertTrue(days[-1]['pilot_review_due'])
    def test_review_and_backup_preserved(self):
        self.assertTrue(p.plan('2026-10-30',self.c)['friday_review_due'])
        self.assertTrue(p.plan('2026-10-31',self.c)['saturday_backup_due'])
    def test_bad_anchor_rejected(self):
        c=copy.deepcopy(self.c);c['cycle_anchor_monday']='2026-10-27'
        with self.assertRaises(ValueError):p.plan('2026-10-28',c)
    def test_actual_pending_coverage(self):self.assertEqual(p.check_index()['result'],'PASS')
    def test_missing_candidate_cannot_pass_closeout(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'knowledge').mkdir();(r/'pending-review').mkdir()
            (r/'knowledge/catalog.json').write_text(json.dumps({'entries':[]}))
            (r/'pending-review/active-index.json').write_text(json.dumps({'items':[{'id':'x','status':'candidate','source_path':'pending-review/x.json'}]}))
            self.assertEqual(p.check_index(r)['issues'][0]['reason'],'missing_catalog_entry')
    def test_mismatched_hash_and_scope_detected(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'knowledge').mkdir();(r/'pending-review').mkdir();(r/'pending-review/x.json').write_text('{}')
            item={'id':'x','status':'candidate','source_path':'pending-review/x.json','sha256':'wrong'}
            (r/'knowledge/catalog.json').write_text(json.dumps({'entries':[{'path':item['source_path'],'status':'active','sha256':'wrong','modes':['production']}]}))
            (r/'pending-review/active-index.json').write_text(json.dumps({'items':[item]}))
            reasons={x['reason'] for x in p.check_index(r)['issues']};self.assertEqual(reasons,{'stale_metadata_hash','status_mismatch','pending_scope_violation'})
if __name__=='__main__':unittest.main()
