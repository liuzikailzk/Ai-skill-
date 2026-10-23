import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import date

TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_reference_reads import plan
from pending_review import build_plan,compact,recent_dates

class RuntimeCleanup(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        (self.root/'pending-review').mkdir();(self.root/'skills/test').mkdir(parents=True)
    def put(self,path,text=''):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);return p
    def candidate(self,day='2026-10-01',decision=None,status='candidate'):
        obj={'id':'C1','status':status}
        if decision:obj['archive_decision']=decision
        return self.put('pending-review/'+day+'/candidate-c1.json',json.dumps(obj))
    def decision(self,kind='rejected',day='2026-10-02'):
        return {'decision':kind,'decided_at':day,'human_reference':'explicit user decision in source record'}
    def git(self):
        subprocess.check_call(['git','init','-q'],cwd=self.root)
        subprocess.check_call(['git','add','.'],cwd=self.root)
        subprocess.check_call(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','【V1.2.0】fixture'],cwd=self.root)
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root,text=True).strip()
    def test_depth_one_does_not_read_c(self):
        self.put('a.md','[B](b.md)');self.put('b.md','[C](c.md)');self.put('c.md','[A](a.md)')
        result=plan(self.root,['a.md']);self.assertEqual([(x['path'],x['depth']) for x in result['planned_reads']],[('a.md',0),('b.md',1)])
    def test_self_and_duplicate_paths(self):
        self.put('a.md','[Self](a.md) [B](b.md) [B2](./b.md)');self.put('b.md')
        result=plan(self.root,['a.md','./a.md']);self.assertEqual(len(result['planned_reads']),2);self.assertEqual(len(result['skipped']),1)
    def test_dependency_cannot_reset_root_in_same_task(self):
        self.put('a.md');self.put('b.md')
        with self.assertRaises(ValueError):plan(self.root,['b.md'],{'seed_roots':['a.md'],'read_paths':[]})
    def test_read_set_deduplicates(self):
        self.put('a.md','[B](b.md)');self.put('b.md')
        result=plan(self.root,['a.md'],{'seed_roots':['a.md'],'read_paths':['a.md','b.md']});self.assertEqual(result['planned_reads'],[])
    def test_recent_seven_calendar_days(self):
        for d in ['2026-10-16','2026-10-17','2026-10-23','2026-10-24']:(self.root/'pending-review'/d).mkdir()
        self.assertEqual(recent_dates(self.root,date(2026,10,23)),['2026-10-17','2026-10-23'])
    def test_unresolved_is_never_archived_by_age(self):
        self.candidate();self.assertEqual(build_plan(self.root,date(2026,10,23))['eligible'],[])
    def test_status_active_alone_is_not_merge_proof(self):
        self.candidate(status='active');self.assertEqual(build_plan(self.root,date(2026,10,23))['eligible'],[])
    def test_new_final_decision_stays_recent(self):
        self.candidate(decision=self.decision(day='2026-10-22'));self.assertEqual(build_plan(self.root,date(2026,10,23))['eligible'],[])
    def test_rejected_needs_human_reference(self):
        d=self.decision();d['human_reference']='';self.candidate(decision=d)
        self.assertEqual(build_plan(self.root,date(2026,10,23))['eligible'],[])
    def test_merged_needs_real_target_and_readback(self):
        self.candidate(decision=self.decision('merged'));self.assertEqual(build_plan(self.root,date(2026,10,23))['eligible'],[])
    def test_manual_or_month_end_only(self):
        with self.assertRaises(ValueError):compact(self.root,date(2026,10,23),None)
    def test_apply_preserves_unresolved_and_is_idempotent(self):
        f=self.candidate(decision=self.decision());keep=self.put('pending-review/2026-10-02/candidate-wait.json','{"id":"WAIT","status":"candidate"}')
        report=self.put('pending-review/2026-10-01/audit-report.md','shared evidence')
        head=self.git();result=compact(self.root,date(2026,10,23),head,manual=True,apply=True)
        self.assertEqual(result['archived_count'],1);self.assertFalse(f.exists());self.assertTrue(keep.exists());self.assertTrue(report.exists())
        index=json.loads((self.root/'pending-review/archive/index.json').read_text());self.assertEqual(index['items'][0]['source_commit'],head)
        self.assertEqual(compact(self.root,date(2026,10,23),head,manual=True,apply=True)['archived_count'],0)
    def test_modified_snapshot_is_not_deleted(self):
        f=self.candidate(decision=self.decision());head=self.git();x=json.loads(f.read_text());x['changed']=True;f.write_text(json.dumps(x))
        with self.assertRaises(ValueError):compact(self.root,date(2026,10,23),head,manual=True,apply=True)
        self.assertTrue(f.exists())

if __name__=='__main__':unittest.main()
