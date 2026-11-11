import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from read_knowledge import extract_sections, read_units
from knowledge_snapshot import validated_catalog
import query_knowledge as q

class ExactReads(unittest.TestCase):
    def test_section_keeps_boundaries_without_neighbor(self):
        text='# Rules\nIntro\n## Limits\nNo guessing\n## Chosen\nYes\n### Child\nMore\n## Other\nNo\n'
        result=extract_sections(text,['Chosen','Limits'])
        self.assertIn('No guessing',result);self.assertIn('More',result);self.assertNotIn('## Other',result)
    def test_ambiguous_and_missing_sections_fail(self):
        for title in ['A','Missing']:
            with self.assertRaises(ValueError):extract_sections('# Doc\n## A\nx\n## A\ny\n',[title])
    def test_real_read_receipt_and_reuse(self):
        result,state=read_units(ROOT,['film-emotion'],'production',['film'],project_revision='fixture1')
        self.assertIn('不得默认套用女频',result['reads'][0]['body'])
        self.assertNotIn('### 喜剧',result['reads'][0]['body'])
        again,_=read_units(ROOT,['film-emotion'],'production',['film'],state,'fixture1')
        self.assertEqual(again['reads'],[])
        with self.assertRaises(ValueError):read_units(ROOT,['film-emotion'],'production',['film'],state,'fixture2')
    def test_candidate_cannot_be_read_as_production(self):
        with self.assertRaises(ValueError):read_units(ROOT,['CLUE-FRAMING-20261111-S'],'production',['film'])
    def test_snapshot_invalidates_after_source_change(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'knowledge').mkdir();(root/'AGENTS.md').write_text('fixture');(root/'rule.md').write_text('old')
            cat={'entries':[{'path':'rule.md'}]};(root/'knowledge/catalog.json').write_text(json.dumps(cat))
            subprocess.run(['git','init','-q'],cwd=root,check=True);subprocess.run(['git','add','.'],cwd=root,check=True)
            subprocess.run(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],cwd=root,check=True)
            cache=root/'receipt.json'
            with patch.object(q,'validate',return_value={'result':'PASS'}) as check:
                _,a=validated_catalog(root,cache);_,b=validated_catalog(root,cache)
                self.assertFalse(a['validation_reused']);self.assertTrue(b['validation_reused']);self.assertEqual(check.call_count,1)
            (root/'rule.md').write_text('changed')
            with patch.object(q,'validate',side_effect=AssertionError('stale index')):
                with self.assertRaisesRegex(AssertionError,'stale index'):validated_catalog(root,cache)
            self.assertEqual(json.loads(cache.read_text())['signature']['files']['rule.md'][0],3)
    def test_changed_qualification_invalidates_reader_receipt(self):
        result,state=read_units(ROOT,['film-emotion'],'production',['film'],project_revision='test')
        c=copy.deepcopy(q.load_catalog());next(e for e in c['entries'] if e['id']=='film-emotion')['status']='candidate'
        with patch('read_knowledge.validated_catalog',return_value=(c,{'id':'changed'})):
            with self.assertRaises(ValueError):read_units(ROOT,['film-emotion'],'production',['film'],state,'test')
    def test_reuse_requires_task_binding(self):
        _,state=read_units(ROOT,['film-emotion'],'production',['film'])
        with self.assertRaisesRegex(ValueError,'explicit project'):read_units(ROOT,['film-emotion'],'production',['film'],state)
    def test_entry_change_invalidates_body_receipts(self):
        result,state=read_units(ROOT,['film-emotion'],'production',['film'],project_revision='test')
        self.assertTrue(result['entry_reads'])
        state['root_hashes']={'old-root':'old-hash'}
        result,_=read_units(ROOT,['film-emotion'],'production',['film'],state,'test')
        self.assertTrue(result['entry_reads']);self.assertTrue(result['reads'])

if __name__=='__main__':unittest.main()
