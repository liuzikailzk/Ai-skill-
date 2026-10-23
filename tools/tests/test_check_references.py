import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location('check_references',Path(__file__).resolve().parents[1]/'check_references.py')
MODULE=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MODULE)

class ReferenceChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.source=Path('skills/script-video-shot-director/references/a.md')
        (self.root/self.source).parent.mkdir(parents=True)
    def put(self,path):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('x')
    def resolve(self,path,kind='markdown_link',line='',code=False):
        return MODULE.resolve(self.root,self.source,path,kind,line,code)
    def test_explicit_link_does_not_fallback_to_package_root(self):
        self.put('skills/script-video-shot-director/references/b.md')
        self.assertEqual(self.resolve('references/b.md')['status'],'missing')
    def test_relative_parent(self):
        self.put('skills/script-video-shot-director/SKILL.md')
        self.assertEqual(self.resolve('../SKILL.md')['status'],'exists')
    def test_percent_decoding_and_fragment(self):
        self.put('skills/script-video-shot-director/references/a b.md')
        self.assertEqual(self.resolve('a%20b.md#section')['status'],'exists')
    def test_external(self):
        self.assertEqual(self.resolve('https://example.invalid/a.md')['status'],'external')
    def test_bare_package_path(self):
        self.put('skills/script-video-shot-director/references/b.md')
        self.assertEqual(self.resolve('references/b.md','bare_path')['resolution'],'package_relative')
    def test_missing_explicit_example_cannot_be_excluded(self):
        self.assertEqual(self.resolve('example.md')['status'],'missing')
    def test_parameterized_path(self):
        self.assertEqual(self.resolve('history/<修订号>/before.json','bare_path')['status'],'template')
    def test_missing_loading_instruction_is_not_output(self):
        self.assertEqual(self.resolve('lost.md','bare_path','必须读取 lost.md')['status'],'missing')
    def test_multiple_targets_not_silently_picked(self):
        self.put('skills/script-video-shot-director/references/x/data.json')
        self.put('skills/script-video-shot-director/references/y/data.json')
        self.assertEqual(self.resolve('data.json','bare_path')['status'],'ambiguous')
    def test_history_missing_stays_visible(self):
        source=Path('skills/script-video-shot-director/references/learning-log.md')
        self.assertEqual(MODULE.resolve(self.root,source,'lost.md','bare_path','原快照 lost.md',False)['status'],'historical_artifact_unavailable')
    def test_graph_indirect_cycle(self):
        result=MODULE.strongly_connected({'a':{'b'},'b':{'c'},'c':{'a','d'},'d':set()})
        self.assertEqual(result,[['a','b','c']])
    def test_acyclic_shared_dependency(self):
        self.assertEqual(MODULE.strongly_connected({'a':{'c'},'b':{'c'},'c':set()}),[])
    def test_self_cycle(self):
        self.assertEqual(MODULE.strongly_connected({'a':{'a'}}),[['a']])
    def test_reference_definition_and_use(self):
        found=MODULE.extract('[文档][rule]\n[rule]: b.md\n')
        self.assertEqual([f[2] for f in found],['markdown_reference','markdown_definition'])
    def test_link_label_is_not_counted_as_an_extra_reference(self):
        found=MODULE.extract('[b.md](b.md)；见 c.md；https://example.invalid/d.md')
        self.assertEqual([f[1] for f in found],['b.md','c.md'])
    def test_template_command_argument(self):
        found=MODULE.extract('`python scripts/run.py <record.json>`')
        self.assertIn('<record.json>',[f[1] for f in found])
    def test_canonical_ledger(self):
        self.put('skills/script-video-shot-director/references/audit/global-state.json')
        source=Path('skills/manga-reasoning-storyboard/references/learning-policy.md')
        result=MODULE.resolve(self.root,source,'global-state.json','bare_path','三套共用一本global-state.json',False)
        self.assertEqual(result['status'],'exists')
    def test_case_sensitive(self):
        self.put('skills/script-video-shot-director/references/B.md')
        self.assertEqual(self.resolve('b.md')['status'],'missing')
    def test_unicode_filename_and_template(self):
        found=MODULE.extract('见 `中文文件.md` 和 references/cases/YYYY-MM-DD-案例名.md')
        self.assertEqual([x[1] for x in found],['中文文件.md','references/cases/YYYY-MM-DD-案例名.md'])
    def test_chinese_conjunction_does_not_merge_two_filenames(self):
        found=MODULE.extract('history/X/before.json及manifest.json；见 references/a.json与references/b.md')
        self.assertEqual([x[1] for x in found],['history/X/before.json','manifest.json','references/a.json','references/b.md'])

if __name__=='__main__':unittest.main()
