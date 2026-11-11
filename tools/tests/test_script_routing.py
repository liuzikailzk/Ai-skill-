import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from script_workspace import extract_source, validate_analysis
from route_production import route

class ScriptRouting(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        p=Path(self.tmp.name)/'script.txt'
        p.write_text('人物资料\n第1集\n1-1 夜 内 客厅\n出场人物：甲、乙\n甲放下武器。\n甲看清伤口，扶住乙。\n甲说不用担心，手却发抖。\n1-2日 外 院子\n两人离开。\n')
        self.source=extract_source(p);scene=self.source['scenes'][0]
        def beat(i,ref,labels,primary):
            base={f:['unknown'] for f in ('event','relationship','emotion','function','change')};base.update(labels)
            return dict(id='beat'+str(i),source_refs=[ref],goal='保留原文行动',trigger='原文事件',outcome='原文结果',facts=[ref],interpretation='局部表达判断',entry_state={},exit_state={},uncertainties=[],labels=base,primary=primary)
        self.analysis={'source_sha256':self.source['source_sha256'],'extraction_sha256':self.source['extraction_sha256'],'analysis_revision':'fixture-v1','scenes':[dict(id=scene['id'],review_status='reviewed',reviewed_source_refs=scene['source_refs'],summary='从动作终止转为关心，保留表里不一',nonbeat_refs=scene['source_refs'][:2],beats=[beat(1,'P0005',{'event':['action'],'change':['action']},'event:action'),beat(2,'P0006',{'event':['rescue'],'emotion':['concern'],'change':['emotion']},'change:emotion'),beat(3,'P0007',{'event':['conversation'],'emotion':['ambivalence'],'change':['none']},'emotion:ambivalence')]) ]}
    def test_source_exact_coverage_and_missing_header_space(self):
        self.assertEqual(len(self.source['scenes']),2)
        self.assertEqual(self.source['scenes'][1]['id'],'1-2')
        self.assertEqual(self.source['coverage']['assigned_exactly_once'],9)
    def test_mutated_extracted_source_invalidates_analysis(self):
        self.source['paragraphs'][4]['text']='甲重新举起武器。'
        with self.assertRaisesRegex(ValueError,'Extracted source content changed'):validate_analysis(self.source,self.analysis)
    def test_annotations_preserve_local_changes(self):
        self.assertEqual(validate_analysis(self.source,self.analysis)['beats'],3)
        r=route(self.source,self.analysis,'1-1')
        self.assertEqual(r['beats'][0]['methods'][0]['id'],'action')
        self.assertEqual(r['beats'][1]['methods'][0]['id'],'action-performance')
        self.assertNotIn('film-emotion',r['read_plan_ids'])
        self.assertIn('script-analysis',r['read_plan_ids'])
        self.assertNotIn('film-model',r['read_plan_ids'])
        self.assertTrue(all(len(b['methods'])<=2 for b in r['beats']))
    def test_reassuring_reveal_does_not_force_suspense(self):
        b=self.analysis['scenes'][0]['beats'][2]
        b['labels']['function']=['reveal'];b['labels']['emotion']=['relief'];b['primary']='function:reveal'
        result=route(self.source,self.analysis,'1-1')['beats'][2]
        self.assertEqual(result['methods'][0]['id'],'film-information')
        self.assertFalse({'film-suspense','action-reveal'} & {x['id'] for x in result['methods']})
    def test_playful_contact_does_not_become_combat(self):
        b=self.analysis['scenes'][0]['beats'][2];b['labels']['event']=['physical_action'];b['labels']['function']=['comic_relief'];b['primary']='function:comic_relief'
        methods=route(self.source,self.analysis,'1-1')['beats'][2]['methods']
        self.assertEqual([x['id'] for x in methods],['film-comedy','film-continuity'])
    def test_source_revision_mismatch_stops(self):
        self.analysis['source_sha256']='wrong'
        with self.assertRaisesRegex(ValueError,'different source'):validate_analysis(self.source,self.analysis)
    def test_unreviewed_scene_stops(self):
        self.analysis['scenes'][0]['review_status']='unreviewed'
        with self.assertRaises(ValueError):validate_analysis(self.source,self.analysis)
    def test_incomplete_whole_script_cannot_claim_complete(self):
        with self.assertRaisesRegex(ValueError,'incomplete'):validate_analysis(self.source,self.analysis,require_complete=True)
    def test_missing_narrative_cannot_hide_as_nonbeat(self):
        s=self.analysis['scenes'][0];s['beats']=s['beats'][:-1];s['nonbeat_refs'].append('P0007')
        with self.assertRaisesRegex(ValueError,'Narrative'):validate_analysis(self.source,self.analysis)
    def test_out_of_scene_reference_stops(self):
        self.analysis['scenes'][0]['beats'][0]['source_refs']=['P0009']
        with self.assertRaisesRegex(ValueError,'out-of-scope'):validate_analysis(self.source,self.analysis)
    def test_reordered_beats_stops(self):
        self.analysis['scenes'][0]['beats'].reverse()
        with self.assertRaisesRegex(ValueError,'out-of-order'):validate_analysis(self.source,self.analysis)
    def test_fabricated_quote_stops(self):
        self.analysis['scenes'][0]['beats'][0]['quotes']=[{'ref':'P0005','text':'虚构对白'}]
        with self.assertRaisesRegex(ValueError,'Quote differs'):validate_analysis(self.source,self.analysis)
    def test_unknown_label_stops(self):
        self.analysis['scenes'][0]['beats'][0]['labels']['emotion']=['invented']
        with self.assertRaisesRegex(ValueError,'Unknown labels'):validate_analysis(self.source,self.analysis)
    def test_partial_analysis_does_not_route_unseen_scene(self):
        with self.assertRaisesRegex(ValueError,'not reviewed'):route(self.source,self.analysis,'1-2')
    def test_annotation_edit_changes_project_binding(self):
        a=route(self.source,self.analysis,'1-1');self.analysis['scenes'][0]['summary']='修正的解释'
        b=route(self.source,self.analysis,'1-1');self.assertNotEqual(a['project_revision'],b['project_revision'])
    def test_no_annotations_is_not_a_pass(self):
        self.analysis['scenes']=[]
        with self.assertRaisesRegex(ValueError,'No reviewed'):validate_analysis(self.source,self.analysis)
    def test_null_semantic_fields_do_not_pass_schema(self):
        self.analysis['scenes'][0]['beats'][0]['goal']=None
        with self.assertRaisesRegex(ValueError,'Nonempty text'):validate_analysis(self.source,self.analysis)
    def test_accepted_case_cannot_be_a_routed_method(self):
        from query_knowledge import load_catalog, validate_taxonomy
        taxonomy=json.loads((ROOT/'knowledge/taxonomy.json').read_text())
        taxonomy['method_routes']['event:action']=['case-stepback-continuous']
        with self.assertRaisesRegex(ValueError,'eligible direct method'):validate_taxonomy(taxonomy,load_catalog())
    def test_refreshed_extraction_still_requires_new_analysis(self):
        from script_workspace import extraction_digest
        self.source['paragraphs'][4]['text']='另一个动作'
        self.source['extraction_sha256']=extraction_digest(self.source)
        with self.assertRaisesRegex(ValueError,'different extraction'):validate_analysis(self.source,self.analysis)

if __name__=='__main__':unittest.main()
