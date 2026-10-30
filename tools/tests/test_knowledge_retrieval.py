import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import query_knowledge as q

class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.catalog=q.load_catalog()
    def result(self,s,mode='lookup',skills=None,**kw):return q.query(self.catalog,s,mode,skills,**kw)
    def test_fight_retrieves_accepted_case_with_limits(self):
        r=self.result('做有打击感的古装连续攻防','production',['film'])
        self.assertEqual(r['matches'][0]['id'],'case-stepback-continuous')
        self.assertIn('不证明',r['matches'][0]['summary'])
        self.assertIn('film-model',{x['id'] for x in r['required_rules']})
        self.assertIn('film-motion',{x['id'] for x in r['required_rules']})
    def test_historical_case_not_filtered_by_seven_days(self):
        r=self.result('这个月17号的退一步')
        self.assertIn('case-stepback-final',{x['id'] for x in r['matches']})
        self.assertIn('case-stepback-continuous',{x['id'] for x in r['matches']})
    def test_light_failure_is_warning_not_positive(self):
        r=self.result('灯都灭了地面还亮')
        hits=[x for x in r['matches'] if x['status']=='failure_case']
        self.assertTrue(hits)
        self.assertTrue(all('禁止作为正面' in x['summary'] for x in hits))
    def test_static_assets_dont_load_video_or_governance(self):
        r=self.result('人物服装角色卡','production',['assets'])
        paths=[x['path'] for x in r['required_rules']+r['matches']]
        self.assertFalse(any('model-capability' in p or 'credit-policy' in p or 'global-state' in p for p in paths))
        self.assertEqual(r['entry_roots'],['skills/script-visual-assets/SKILL.md'])
    def test_manga_understanding_is_not_video_generation(self):
        r=self.result('这页漫画气泡谁在说话','analysis',['manga'])
        self.assertIn('panels',{x['id'] for x in r['matches']})
        self.assertNotIn('manga-action',{x['id'] for x in r['matches']})
        self.assertFalse(any('model' in x['id'] for x in r['required_rules']))
        self.assertEqual(r['skills'],['manga'])
    def test_dynamic_manga_adds_film_entry(self):
        r=self.result('漫画动态分镜','production',['manga'])
        self.assertEqual(set(r['skills']),{'manga','film'})
    def test_pending_is_never_in_production_even_if_mislabeled(self):
        catalog=copy.deepcopy(self.catalog)
        e=next(e for e in catalog['entries'] if e['status']=='candidate')
        e['modes'].append('production')
        r=q.query(catalog,e['id'],'production',['film'])
        self.assertNotIn(e['id'],[x['id'] for x in r['matches']])
        r=q.query(catalog,e['id'],'learning')
        self.assertIn(e['id'],[x['id'] for x in r['matches']])
    def test_search_opens_no_result_bodies(self):
        with patch.object(Path,'read_text',side_effect=AssertionError('body read')):
            r=self.result('打斗')
        self.assertEqual(r['bodies_read_by_search'],0)
    def test_unknown_query_reports_gap(self):
        r=self.result('买菜的土豆多少钱')
        self.assertEqual(r['matches'],[])
        self.assertIn('不能据此断言不存在',r['fallback'])
    def test_stale_index_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'knowledge').mkdir();(p/'file.md').write_text('modified')
            c=copy.deepcopy(self.catalog);c['entries']=[dict(id='e',title='e',path='file.md',tags=['e'],summary='e',status='existing_rule',modes=['lookup'],skills=['film'],sha256='0'*64)]
            (p/'knowledge/catalog.json').write_text(json.dumps(c))
            with self.assertRaisesRegex(AssertionError,'stale index'):q.validate(p)
    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):q.safe_path(ROOT,'../secret')
    def test_complete_catalog_hashes_and_direct_depth(self):
        self.assertEqual(q.validate()['result'],'PASS')
    def test_skill_selection_required(self):
        with self.assertRaises(ValueError):self.result('提示词','production')
    def test_dynamic_asset_gate_optional_but_required_when_selected(self):
        r=self.result('首帧人物','production',['assets'],dynamic_images=True)
        self.assertIn('assets-motion',{x['id'] for x in r['required_rules']})
    def test_shared_rules_read_once_for_dynamic_manga(self):
        r=self.result('漫画动态分镜','production',['manga'])
        paths=[x['path'] for x in r['required_rules']]
        self.assertEqual(len(paths),len(set(paths)))
        self.assertEqual(paths.count('knowledge/shared/model-capability-gate.md'),1)
        self.assertEqual(paths.count('knowledge/shared/input-and-style.md'),1)
        self.assertIn('skills/manga-reasoning-storyboard/references/production-core.md',paths)
        self.assertIn('skills/script-video-shot-director/references/production-core.md',paths)
    def test_legacy_ids_resolve_to_canonical_rule(self):
        a=self.result('film-model','lookup')['matches'][0]
        b=self.result('manga-model','lookup')['matches'][0]
        self.assertEqual(a['path'],b['path'])
        self.assertEqual(a['path'],'knowledge/shared/model-capability-gate.md')
    def test_static_poster_keeps_asset_scope(self):
        r=self.result('宣传海报封面','production',['assets'])
        paths=[x['path'] for x in r['required_rules']]
        self.assertEqual(r['skills'],['assets'])
        self.assertIn('skills/script-visual-assets/references/style-preproduction-policy.md',paths)
        self.assertFalse(any('motion-readiness' in p or 'model-capability' in p for p in paths))

if __name__=='__main__':unittest.main()
