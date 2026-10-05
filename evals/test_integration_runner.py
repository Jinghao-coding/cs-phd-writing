import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_integration as runner


class HarnessChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.run=Path(self.tmp.name)/'run'
    def test_prepare_separates_answers_and_preserves_baseline(self):
        m=runner.prepare(self.run,'I1','current')
        self.assertTrue(m['project_sha256'])
        self.assertFalse((self.run/'skill/evals').exists())
        self.assertFalse((self.run/'skill/scripts/run_integration.py').exists())
        self.assertFalse((self.run/'skill/examples').exists())
        self.assertEqual(runner.hashes(self.run/'baseline'),runner.hashes(self.run/'project'))
        with self.assertRaises(ValueError):runner.prepare(self.run,'I1','current')
    def test_review_detects_any_write_and_records_patch(self):
        runner.prepare(self.run,'I2','none')
        p=self.run/'project/abstract.tex';p.write_text(p.read_text().replace('80','72'))
        checks=runner.collect(self.run,'test-double','unit test')
        self.assertEqual(checks['out_of_scope'],['abstract.tex'])
        self.assertIn('-本文',(self.run/'output.patch').read_text())
        self.assertTrue(checks['baseline_intact'])
    def test_no_skill_variant_and_unchanged_collection(self):
        runner.prepare(self.run,'I3','none')
        self.assertFalse((self.run/'skill').exists())
        self.assertNotIn('使用提供的技能',(self.run/'task.md').read_text())
        c=runner.collect(self.run,'test-double','unit test')
        self.assertEqual(c['changed_files'],[])
        self.assertEqual(c['negative_text_changed'],0)
    def test_baseline_tampering_detected(self):
        runner.prepare(self.run,'I1','none')
        (self.run/'baseline/abstract.tex').write_text('changed')
        self.assertFalse(runner.collect(self.run,'test-double','unit test')['baseline_intact'])
    def test_deleted_author_text_and_added_file(self):
        runner.prepare(self.run,'I4','none')
        p=self.run/'project/chapters/reclaim.tex';p.write_text(p.read_text().replace('读者退出临界区后递减引用计数。',''))
        (self.run/'project/extra.txt').write_text('extra')
        c=runner.collect(self.run,'test-double','unit test')
        self.assertEqual(c['negative_text_changed'],1)
        self.assertEqual(c['out_of_scope'],['extra.txt'])

if __name__=='__main__':unittest.main()
