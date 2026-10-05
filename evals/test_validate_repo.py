"""Mutation tests: broken repository metadata must actually fail validation."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import validate_repo as v


class RepoChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in v.REQUIRED:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('')
        for name in ('SKILL.md','README.md','README.en.md','CHANGELOG.md','evals/cases.md','evals/acceptance.md'):
            (self.root/name).write_text((ROOT/name).read_text())
    def test_bad_relative_link_and_anchor(self):
        (self.root/'check.md').write_text('# Title\n[bad](missing.md)\n[anchor](#absent)\n')
        errors=v.link_errors(self.root)
        self.assertTrue(any('missing.md' in e for e in errors))
        self.assertTrue(any('#absent' in e for e in errors))
    def test_code_external_images_and_duplicate_headings(self):
        (self.root/'image.png').write_bytes(b'example')
        (self.root/'check.md').write_text('# Title\n# Title\n[a](#title-1)\n![img](image.png)\n[web](https://example.org/a#x)\n`[code](missing)`\n  ```md\n[code](missing)\n  ```\n<a id="custom"></a>\n[a](#custom)\n')
        self.assertFalse([e for e in v.link_errors(self.root) if e.startswith('check.md:')])
    def test_case_missing_duplicate_and_gap(self):
        path=self.root/'evals/acceptance.md'
        path.write_text(path.read_text().replace('| C1 |','| C2 |',1))
        self.assertTrue(any('correspondence' in e for e in v.case_errors(self.root)))
        self.assertTrue(any('duplicate' in e for e in v.case_errors(self.root)))
        path=self.root/'evals/cases.md';path.write_text(path.read_text().replace('## C2：','## C99：'))
        self.assertTrue(any('noncontinuous' in e for e in v.case_errors(self.root)))
    def test_current_version_conflict_history_unchanged(self):
        self.assertFalse(v.version_errors(self.root))
        p=self.root/'README.md';p.write_text(p.read_text().replace('主分支 v0.6.0','主分支 v9.9.9'))
        self.assertTrue(any('conflict' in e for e in v.version_errors(self.root)))
    def test_missing_distribution_file(self):
        (self.root/'LICENSE').unlink()
        self.assertIn('missing required file: LICENSE',v.validate(self.root))
    def test_integration_correspondence(self):
        (self.root/'evals/integration/expected/scope.json').write_text('{"I1": []}')
        self.assertTrue(any('correspondence' in e for e in v.integration_errors(self.root)))
    def test_inline_code_heading_anchor(self):
        (self.root/'check.md').write_text('# Use `term`\n[link](#use-term)\n')
        self.assertFalse([e for e in v.link_errors(self.root) if e.startswith('check.md:')])
    def test_metadata_missing(self):
        (self.root/'SKILL.md').write_text('# No metadata')
        self.assertTrue(v.version_errors(self.root))


if __name__=='__main__':unittest.main()
