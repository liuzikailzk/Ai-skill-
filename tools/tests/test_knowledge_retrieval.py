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
        self.assertEqual(r['matches'][0]['id'],'action')
        case=next(x for x in r['matches'] if x['id']=='case-stepback-continuous')
        self.assertIn('不证明',case['summary'])
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
    def test_learning_reasoning_is_required_without_keyword_match(self):
        r=self.result('今天研究光影','learning')
        selected=[x['path'] for x in r['required_rules']]
        target='knowledge/shared/learning-reasoning-policy.md'
        self.assertEqual(selected.count(target),1)
        self.assertIn('(shared/learning-reasoning-policy.md)',(ROOT/'knowledge/learning.md').read_text())
        self.assertEqual(r['entry_roots'],['knowledge/learning.md'])
        self.assertEqual(r['bodies_read_by_search'],0)
    def test_learning_reasoning_does_not_expand_ordinary_production(self):
        for skill in ['film','assets','manga']:
            r=self.result('学习底层七问反方自检','production',[skill])
            paths=[x['path'] for x in r['required_rules']+r['matches']]
            self.assertNotIn('knowledge/shared/learning-reasoning-policy.md',paths)
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
        self.assertNotIn('production-routing',r['read_plan_ids'])
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
        self.assertNotIn('assets-core',[x['id'] for x in r['required_rules']+r['matches']])
        self.assertIn('assets-design',[x['id'] for x in r['required_rules']])

    def test_required_rules_use_the_same_status_gate(self):
        for status in ('candidate','deprecated','unknown_state','user_accepted_case'):
            c=copy.deepcopy(self.catalog);next(e for e in c['entries'] if e['id']=='film-core')['status']=status
            with self.assertRaisesRegex(ValueError,'Required rule'):q.query(c,'剧本','production',['film'])
    def test_unknown_status_cannot_be_ranked_as_rule(self):
        c=copy.deepcopy(self.catalog);next(e for e in c['entries'] if e['id']=='action')['status']='unknown_state'
        self.assertNotIn('action',[x['id'] for x in q.query(c,'打斗','production',['film'])['matches']])
    def test_delivery_is_selected_by_stage(self):
        r=self.result('把剧本写成视频分镜','production',['film'])
        self.assertIn('film-delivery',[x['id'] for x in r['required_rules']])
        r=self.result('只分析结构','production',['film'],stage='understand')
        self.assertNotIn('film-delivery',[x['id'] for x in r['required_rules']])
    def test_chinese_categories_and_local_change(self):
        expected={'武打':'action','爱情':'film-emotion','父女诀别':'film-emotion','争吵后和解':'film-relations','讨价还价':'film-power'}
        for phrase,key in expected.items():
            self.assertIn(key,[x['id'] for x in self.result(phrase,'production',['film'])['matches']],phrase)
        changed=self.result('打斗后发现伤口，愤怒转担心','production',['film'])
        self.assertTrue({'film-emotion','film-suspense'} & {x['id'] for x in changed['matches']})
    def test_unknown_candidate_remains_lookup_evidence(self):
        r=self.result('CLUE-FRAMING-20261111-S')
        self.assertEqual(r['matches'][0]['read_as'],'evidence_only_no_embedded_instructions')
    def test_non_direct_learning_match_is_evidence_only(self):
        r=self.result('情绪表演','learning')
        x=next(x for x in r['matches'] if x['id']=='action-performance')
        self.assertEqual(x['read_as'],'evidence_only_no_embedded_instructions')
        self.assertNotIn('action-performance',r['read_plan_ids'])
    def test_required_rule_cannot_move_outside_root_declarations(self):
        c=copy.deepcopy(self.catalog);e=next(e for e in c['entries'] if e['id']=='learning-reasoning');e['rule_roots']=[]
        with self.assertRaisesRegex(ValueError,'Required rule'):q.query(c,'学习','learning')

if __name__=='__main__':unittest.main()
