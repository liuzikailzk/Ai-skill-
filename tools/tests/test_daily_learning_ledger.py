import copy
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('daily',Path(__file__).resolve().parents[1]/'daily_learning_ledger.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class DailyLedgerTests(unittest.TestCase):
 def setUp(self): self.d=m.initialize('2026-11-13','AUDIT-20261113-01',{})
 def test_three_plus_one_and_failed_counts(self):
  for i in range(1,4):
   m.reserve(self.d,self.d['run_id'],'techniques',str(i));m.finish(self.d,self.d['run_id'],'techniques',i,'failed')
  with self.assertRaises(ValueError):m.reserve(self.d,self.d['run_id'],'techniques','four')
  m.reserve(self.d,self.d['run_id'],'news','news');m.finish(self.d,self.d['run_id'],'news',1,'completed')
  with self.assertRaises(ValueError):m.reserve(self.d,self.d['run_id'],'news','second')
 def test_unknown_reservation_no_retry(self):
  m.reserve(self.d,self.d['run_id'],'techniques','a')
  for q in ['a','b']:
   with self.assertRaises(ValueError):m.reserve(self.d,self.d['run_id'],'techniques',q)
 def test_owner_and_closed(self):
  with self.assertRaises(ValueError):m.reserve(self.d,'different','news','a')
  self.d['status']='partial_closed'
  with self.assertRaises(ValueError):m.reserve(self.d,self.d['run_id'],'news','a')
 def test_no_private_or_extra_fields(self):
  self.d['user_feedback']='private'
  with self.assertRaises(ValueError):m.validate(self.d)
 def test_legacy_prevents_reset(self):
  for key in ['days','news_days']:
   with self.assertRaises(ValueError):m.initialize('2026-11-13','R',{key:{'2026-11-13':{'consumed':1}}})
 def test_result_idempotence_and_no_rewrite(self):
  m.reserve(self.d,self.d['run_id'],'news','a');m.finish(self.d,self.d['run_id'],'news',1,'failed');m.finish(self.d,self.d['run_id'],'news',1,'failed')
  with self.assertRaises(ValueError):m.finish(self.d,self.d['run_id'],'news',1,'completed')
 def test_only_hash_no_query_content(self):
  m.reserve(self.d,self.d['run_id'],'news','test public query');self.assertNotIn('test public query',str(self.d));self.assertEqual(len(self.d['news'][0]['query_sha256']),64)

 def test_uncertain_conservatively_blocks_more_queries(self):
  m.reserve(self.d,self.d['run_id'],'techniques','a');m.finish(self.d,self.d['run_id'],'techniques',1,'uncertain')
  with self.assertRaises(ValueError):m.reserve(self.d,self.d['run_id'],'techniques','b')
  self.d['status']='partial_closed';m.validate(self.d)
