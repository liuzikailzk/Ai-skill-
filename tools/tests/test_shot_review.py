import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from query_knowledge import load_catalog, query
from shot_review import CHECKS, evaluate, shot_plan, template


def completed_sheet(plan, revision, selected):
    sheet = template(plan, revision, selected)
    for check in plan['checks']:
        for phase in ('preflight', 'review'):
            evidence = check.get('inputs', ['input']) if phase == 'preflight' else check['media']
            sheet['checks'][check['id']][phase] = {
                'status': 'passed', 'version': revision if phase == 'preflight' else selected,
                'evidence': {key: 'fixture record / 00:02-00:04' for key in evidence},
                'observation': 'synthetic regression observation',
            }
    return sheet


class ShotChecks(unittest.TestCase):
    def test_identifiers_cover_both_numbered_case_tables(self):
        rules = json.loads((ROOT / CHECKS).read_text(encoding='utf-8'))
        recorded = set()
        for prefix, path in rules['sources'].items():
            body = (ROOT / path).read_text(encoding='utf-8')
            recorded.update(re.findall(r'^\| (?:WF01-R03-)?(' + prefix + r'\d+) ·', body, re.M))
        indexed = {code for row in rules['checks'] for code in row['cases']}
        self.assertTrue({'F24', 'Q57'} <= recorded)
        self.assertEqual(indexed, recorded)

    def test_production_lookup_without_project_name(self):
        catalog = load_catalog()
        r = query(catalog, '新故事，三人扶车对话', 'production', ['assets', 'film'])
        checks = {item['id']: item for item in r['shot_review']['checks']}
        self.assertTrue({'blocking', 'dialogue', 'voice', 'action'} <= checks.keys())
        self.assertNotIn('animal', checks)
        self.assertIn('Q34', checks['blocking']['cases'])
        self.assertIn('F11', checks['dialogue']['cases'])
        self.assertNotIn('shot_review', query(catalog, '三人扶车对话', 'analysis', ['film']))
        self.assertNotIn('shot_review', query(catalog, '三人扶车对话', 'production', ['manga']))
        self.assertNotIn('shot_review', query(catalog, '人物海报', 'production', ['assets']))
        self.assertEqual([c['id'] for c in shot_plan('空山静景')['checks']], ['coverage'])
        tags = query(catalog, '空山静景', 'production', ['film'], risk_tags=['dialogue'])
        self.assertTrue({'dialogue', 'voice'} <= {c['id'] for c in tags['shot_review']['checks']})
        with self.assertRaises(ValueError):
            shot_plan('风景', ['unknown'])

    def test_empty_sheet_and_missing_audio_block(self):
        plan = shot_plan('甲对乙说话')
        sheet = template(plan, 'shotA@2', 'take1')
        self.assertFalse(evaluate(plan, sheet, 'preflight', 'shotA@2')['allow'])
        sheet = completed_sheet(plan, 'shotA@2', 'take1')
        del sheet['checks']['voice']['review']['evidence']['audio']
        sheet['checks']['voice']['review']['evidence']['transcript'] = 'ASR matched'
        self.assertTrue(evaluate(plan, sheet, 'preflight', 'shotA@2')['allow'])
        result = evaluate(plan, sheet, 'review', 'shotA@2', 'take1')
        self.assertEqual(result['pending'], ['voice/review'])
        self.assertFalse(result['allow'])

    def test_rejection_regression_and_stale_receipts(self):
        plan = shot_plan('补拍三人对话')
        sheet = completed_sheet(plan, 'shotA@2', 'take1')
        self.assertTrue(evaluate(plan, sheet, 'review', 'shotA@2', 'take1')['allow'])
        self.assertFalse(evaluate(plan, sheet, 'review', 'shotA@3', 'take1')['allow'])
        self.assertFalse(evaluate(plan, sheet, 'review', 'shotA@2', 'take2')['allow'])
        self.assertFalse(evaluate(shot_plan('改成四人对话'), sheet, 'review', 'shotA@2', 'take1')['allow'])
        sheet['selected_version'] = 'take2'
        self.assertFalse(evaluate(plan, sheet, 'review', 'shotA@2', 'take2')['allow'])
        sheet['selected_version'] = 'take1'
        sheet['user_decision'] = 'rejected'
        self.assertEqual(evaluate(plan, sheet, 'review', 'shotA@2', 'take1')['status'], 'failed')
        sheet['user_decision'] = 'accepted'
        sheet['checks']['blocking']['review']['status'] = 'failed'
        self.assertEqual(evaluate(plan, sheet, 'review', 'shotA@2', 'take1')['failed'], ['blocking/review'])

    def test_continuation_requires_matching_passed_upstream_and_binding(self):
        first = shot_plan('空旷的马场')
        upstream = evaluate(first, completed_sheet(first, 'E2-S6@1', 'T3-C2'),
                            'review', 'E2-S6@1', 'T3-C2')
        plan = shot_plan('下马后接下一镜')
        ids = {item['id'] for item in plan['checks']}
        self.assertTrue({'reference', 'action', 'animal', 'cut'} <= ids)
        sheet = completed_sheet(plan, 'E2-S7@1', 'T1-C1')
        sheet['upstream'] = {key: upstream[key] for key in ('input_revision', 'selected_version', 'plan_id')}
        def check(up):
            return evaluate(plan, sheet, 'preflight', 'E2-S7@1', upstream=up)
        self.assertTrue(check(upstream)['allow'])
        self.assertEqual(check(None)['status'], 'pending')
        self.assertEqual(check(dict(upstream, status='failed', allow=False))['status'], 'failed')
        self.assertFalse(check(dict(upstream, selected_version='T3-C1'))['allow'])
        self.assertFalse(check(dict(upstream, phase='preflight'))['allow'])
        sheet['checks']['reference']['preflight']['evidence'].pop('binding')
        self.assertFalse(check(upstream)['allow'])
