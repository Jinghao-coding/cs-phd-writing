#!/usr/bin/env python3
"""Prepare isolated, answer-free Agent tasks and collect immutable evidence; no model API."""
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

from check_revision import analyze

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'evals/integration'


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def prepare(destination, task, variant):
    if destination.exists():
        raise ValueError('destination must not exist; use a fresh run directory')
    if task not in {'I1', 'I2', 'I3', 'I4'}:
        raise ValueError('unknown task')
    destination.mkdir(parents=True)
    shutil.copytree(FIXTURE/'project', destination/'project')
    shutil.copyfile(FIXTURE/'tasks'/f'{task}.md', destination/'task.md')
    skill_files = {}
    if variant != 'none':
        source = ROOT if variant == 'current' else Path(variant).resolve()
        # Exclude evaluation answers and completed examples from the tested skill view.
        for name in ('SKILL.md', 'references', 'assets', 'scripts', 'agents', 'LICENSE', 'NOTICE.md'):
            src, dst = source/name, destination/'skill'/name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if name == 'scripts':
                dst.mkdir(exist_ok=True)
                shutil.copyfile(src/'check_revision.py', dst/'check_revision.py')
            elif src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__'))
            elif src.exists():
                shutil.copyfile(src, dst)
        skill_files = hashes(destination/'skill')
    else:
        task_path = destination/'task.md'
        task_path.write_text(task_path.read_text().replace('使用提供的技能', ''))
    # Baseline and run metadata are held by the harness, outside the Agent's project.
    shutil.copytree(destination/'project', destination/'baseline')
    meta = {'prepared_at': datetime.now(timezone.utc).isoformat(), 'task': task,
            'variant': variant, 'project_sha256': hashes(destination/'baseline'),
            'skill_sha256': skill_files, 'host': platform.platform(),
            'python': sys.version.split()[0], 'execution_status': 'not_run'}
    (destination/'manifest.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return meta


def collect(run, model, method, build=False):
    meta = json.loads((run/'manifest.json').read_text())
    before, after = hashes(run/'baseline'), hashes(run/'project')
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    allowed = json.loads((FIXTURE/'expected/scope.json').read_text())[meta['task']]
    diffs, candidates = [], {}
    for name in changed:
        a, b = run/'baseline'/name, run/'project'/name
        old = a.read_text(encoding='utf-8') if a.exists() else ''
        new = b.read_text(encoding='utf-8') if b.exists() else ''
        diffs.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True), 'before/'+name, 'after/'+name))
        candidates[name] = analyze(old, new)
    result = {'collected_at': datetime.now(timezone.utc).isoformat(), 'model': model,
              'method': method, 'changed_files': changed,
              'out_of_scope': sorted(set(changed)-set(allowed)),
              'baseline_intact': before == meta['project_sha256'],
              'skill_intact': not meta['skill_sha256'] or hashes(run/'skill') == meta['skill_sha256'],
              'negative_text_samples': 2,
              'negative_text_changed': sum(s not in (run/'project/chapters/reclaim.tex').read_text() for s in
                  ['读者退出临界区后递减引用计数。', '仅当对象已经退役且不再被读者引用时，回收器才释放对象空间。']),
              'semantic_assessment': 'requires separate reviewer; no total score',
              'build': {'status': 'not_run'}}
    if build:
        exe = shutil.which('xelatex')
        if exe:
            (run/'build').mkdir(exist_ok=True)
            for tex in (run/'project').rglob('*.tex'):
                (run/'build'/tex.relative_to(run/'project').parent).mkdir(parents=True, exist_ok=True)
            command = [exe, '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
                       '-output-directory='+str((run/'build').resolve()), 'main.tex']
            outputs = []
            for _ in range(2):
                proc = subprocess.run(command, cwd=run/'project', capture_output=True, text=True, timeout=120)
                outputs.append(proc.stdout + proc.stderr)
                if proc.returncode:
                    break
            (run/'build.log').write_text('\n'.join(outputs))
            result['build'] = {'command': command, 'status': 'completed', 'exit_code': proc.returncode}
        else:
            result['build'] = {'status': 'not_run', 'reason': 'xelatex unavailable'}
    (run/'output.patch').write_text(''.join(diffs))
    (run/'candidates.json').write_text(json.dumps(candidates, ensure_ascii=False, indent=2))
    (run/'checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='action', required=True)
    p = subs.add_parser('prepare');p.add_argument('destination', type=Path)
    p.add_argument('--task', choices=['I1','I2','I3','I4'], required=True)
    p.add_argument('--variant', default='current', help='current, none, or previous skill path')
    p = subs.add_parser('collect');p.add_argument('run', type=Path)
    p.add_argument('--model', required=True);p.add_argument('--method', required=True)
    p.add_argument('--build', action='store_true')
    args = parser.parse_args()
    try:
        result = prepare(args.destination, args.task, args.variant) if args.action == 'prepare' else collect(args.run, args.model, args.method, args.build)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, str(exc)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(result.get('out_of_scope')) or result.get('baseline_intact') is False or result.get('skill_intact') is False or bool(result.get('build',{}).get('exit_code',0)))


if __name__ == '__main__':
    sys.exit(main())
