"""Focused regression tests for read-only diagnostics; standard library only."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/check_revision.py'
spec=importlib.util.spec_from_file_location('checker',SCRIPT)
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class RevisionChecks(unittest.TestCase):
    def test_prose_only_edit(self):
        a=r'系统使用 $x_i\leq C$，见\eqref{eq:a}和\cite[p.~2]{a,b}。'
        r=checker.analyze(a,a.replace('系统使用','调度器遵循'))
        self.assertEqual(r['protected_changes'],{'removed':[],'added':[]})
    def test_math_and_citation_damage(self):
        r=checker.analyze(r'$x\leq C$ \cite[见{附录}]{a,b}',r'$x<C$ \cite[见{附录}]{a}')
        self.assertEqual(len(r['protected_changes']['removed']),2)
        self.assertEqual(len(r['protected_changes']['added']),2)
    def test_display_math(self):
        a=r'\begin{align}a&=b\\c&=d\end{align}'
        self.assertEqual(len(checker.analyze(a,a.replace('=d','=e'))['protected_changes']['removed']),1)
    def test_duplicate_reference_removed(self):
        self.assertEqual(len(checker.analyze(r'\ref{x} \ref{x}',r'\ref{x}')['protected_changes']['removed']),1)
    def test_numeric_equivalent_still_reviewed(self):
        self.assertTrue(checker.analyze('24 ms降至18 ms','降低25%')['number_changes']['added'])
    def test_glossary_exception_is_local(self):
        g={'terms':[{'preferred':'吞吐率','variants':['吞吐量']}],'allow':['历史接口吞吐量']}
        r=checker.analyze('','历史接口吞吐量与吞吐量',g)
        self.assertEqual(len(r['terminology_candidates']),1)
        self.assertEqual(r['terminology_candidates'][0]['column'],9)
    def test_fenced_code(self):
        self.assertEqual(len(checker.analyze('```py\nx=1\n```\n','```py\nx=2\n```\n')['protected_changes']['removed']),1)
    def test_condition_is_for_semantic_review(self):
        r=checker.analyze('仅当节点空闲时下发任务。','下发任务。')
        self.assertFalse(r['protected_changes']['removed'])
        self.assertNotIn('passed',r)
    def test_cli_read_only_and_bad_glossary(self):
        with tempfile.TemporaryDirectory() as d:
            a,b,g=[Path(d)/n for n in ('a.tex','b.tex','g.json')]
            a.write_text('18 ms');b.write_text('16 ms');g.write_text('{"terms":null}')
            out=subprocess.run([sys.executable,str(SCRIPT),str(a),str(b)],capture_output=True)
            self.assertEqual(out.returncode,0)
            self.assertEqual(a.read_text(),'18 ms');self.assertEqual(b.read_text(),'16 ms')
            bad=subprocess.run([sys.executable,str(SCRIPT),str(a),str(b),'--glossary',str(g)],capture_output=True)
            self.assertEqual(bad.returncode,2)

if __name__=='__main__':unittest.main()
