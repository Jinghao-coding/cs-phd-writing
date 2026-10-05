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

class LocalChecks(unittest.TestCase):
    def local(self, a, b):
        return checker.analyze(a,b)['local_candidates']
    def test_number_association_swap(self):
        r=checker.analyze('A为18 ms，B为24 ms','A为24 ms，B为18 ms')
        self.assertEqual(r['number_changes'], {'added':[], 'removed':[]})
        self.assertEqual(len(r['local_candidates']),2)
        self.assertEqual(r['local_candidates'][0]['before']['context'],'A为18 ms')
    def test_reference_association_swap(self):
        r=checker.analyze(r'A采用方法甲\cite{a}。B采用方法乙\cite{b}。',r'A采用方法甲\cite{b}。B采用方法乙\cite{a}。')
        self.assertFalse(r['protected_changes']['removed'])
        self.assertEqual(len(r['local_candidates']),2)
    def test_units_and_markers(self):
        for a,b in [(r'25\%','25'),('25%','25'),('12 ms','12 s'),('12 MiB/s','12 MB/s')]:
            with self.subTest(a=a):
                self.assertEqual(self.local(a,b)[0]['candidate_type'],'unit_or_marker_changed')
    def test_indented_code_and_glossary(self):
        a='  ```py\nx=a # 吞吐量\n  ```\n正文吞吐量'
        g={'terms':[{'preferred':'吞吐率','variants':['吞吐量']}], 'allow':[]}
        r=checker.analyze(a,a.replace('x=a','x=b'),g)
        self.assertEqual(len(r['protected_changes']['removed']),1)
        self.assertEqual(len(r['terminology_candidates']),1)
        self.assertEqual(r['terminology_candidates'][0]['line'],4)
    def test_fence_boundaries(self):
        for text in ['   ~~~py\nx=a\n   ~~~~\n','```\nx=a\n','````\n```\nx=a\n````\n']:
            with self.subTest(text=text):
                self.assertEqual(len(checker.code_regions(text)),1)
                self.assertTrue(checker.analyze(text,text.replace('x=a','x=b'))['protected_changes']['removed'])
        self.assertFalse(checker.code_regions('    ```\nx=a\n    ```'))
    def test_unchanged_repeated_objects(self):
        a=r'A为12 ms，B为12 ms。\cite{k}和\cite{k}。'
        self.assertFalse(self.local(a,a))
        self.assertEqual(len(checker.analyze(a,a.replace('B为12 ms','B为13 ms'))['number_changes']['removed']),1)
    def test_intact_paragraph_reordering(self):
        a=r'A采用方法甲\cite{a}。'; b=r'B采用方法乙\cite{b}。'
        r=checker.analyze(a+'\n\n'+b,b+'\n\n'+a)
        self.assertFalse(r['protected_changes']['removed'])
        self.assertFalse(r['local_candidates'])
        self.assertTrue(r['diff_hunks'])
    def test_equivalent_rewrite_is_not_verdict(self):
        r=checker.analyze('24 ms降至18 ms','降低25%')
        self.assertTrue(r['local_candidates'])
        self.assertNotIn('passed',r)
        self.assertTrue(all('uncertainty' in c for c in r['local_candidates']))
    def test_prose_edit_preserves_objects(self):
        a=r'系统满足 $x\leq C$，见\cite{k}。等待时间为18 ms。'
        r=checker.analyze(a,a.replace('系统满足','该方法满足'))
        self.assertFalse(r['protected_changes']['removed'])
        self.assertFalse(r['number_changes']['removed'])
        self.assertTrue(all(c['candidate_type']=='context_or_position_changed' for c in r['local_candidates']))
    def test_positions_unicode_and_context(self):
        text='前文\nA为18 ms，B为24 ms'
        o=checker.extract(text)[0][0]
        self.assertEqual((o['start'],o['end'],o['line'],o['column']),(5,10,2,3))
        self.assertEqual(text[o['start']:o['end']],o['text'])
    def test_math_delimiters_and_escaped_text(self):
        for a in [r'$x$',r'$$x$$',r'\(x\)',r'\[x\]',r'\begin{equation*}x\end{equation*}']:
            with self.subTest(a=a):
                self.assertEqual(len(checker.analyze(a,a.replace('x','y'))['protected_changes']['removed']),1)
        self.assertFalse(checker.protected(r'价格\$5，文字\\cite{a}'))
        self.assertEqual(len(checker.protected(r'\cite[见\{注\}]{a,b}')),1)
    def test_unclosed_macro_warning(self):
        self.assertTrue(checker.analyze('',r'\cite{a')['coverage_warnings']['after'])
    def test_unmatched_repetitions_are_uncertain(self):
        r=self.local('12 ms与12 ms','13 s与14 s')
        self.assertTrue(r)
        self.assertTrue(all(c['match_basis']=='unresolved' for c in r))
    def test_bad_input_and_utf8(self):
        out=subprocess.run([sys.executable,str(SCRIPT),'/nonexistent/a','/nonexistent/b'],capture_output=True)
        self.assertEqual(out.returncode,2)

if __name__=='__main__':unittest.main()
