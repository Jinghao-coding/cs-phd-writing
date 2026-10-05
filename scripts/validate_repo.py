#!/usr/bin/env python3
"""Offline repository checks. Run from any directory; Python standard library only."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from check_revision import code_regions

REQUIRED = ['SKILL.md', 'README.md', 'README.en.md', 'CHANGELOG.md', 'LICENSE',
            'NOTICE.md', 'agents/openai.yaml', 'references/revision-workflow.md',
            'references/language-tools.md', 'assets/project-template/project-instructions.snippet.md',
            'assets/project-template/docs/thesis-writing-profile.md',
            'assets/project-template/docs/paper-to-thesis-map.md',
            'assets/project-template/docs/university-writing-spec.md',
            'assets/project-template/docs/reference-thesis-notes.md',
            'evals/cases.md', 'evals/acceptance.md', 'evals/test_revision_check.py',
            'evals/test_validate_repo.py', 'scripts/check_revision.py', 'scripts/validate_repo.py',
            '.github/workflows/validate.yml', 'scripts/run_integration.py',
            'evals/integration/expected/scope.json', 'evals/integration/expected/rubric.md',
            'evals/integration/project/main.tex', 'evals/integration/project/main-full.tex',
            'evals/integration/project/chapters/background.tex', 'evals/integration/project/chapters/reclaim.tex',
            'evals/integration/project/shared/notation.tex', 'evals/integration/project/algorithms/reclaim.tex',
            'evals/integration/project/tables/results.tex', 'evals/integration/project/archive/reclaim-v1.tex',
            'evals/integration/project/AGENTS.md']


def prose(text, inline=True):
    chars = list(text)
    for a, b, _ in code_regions(text):
        chars[a:b] = ['\n' if c == '\n' else ' ' for c in text[a:b]]
    result = ''.join(chars)
    return re.sub(r'(`+)(.*?)\1', '' if inline else r'\2', result)


def anchors(text):
    text = prose(text, inline=False)
    result = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    counts = Counter()
    for heading in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', text, re.M):
        heading = re.sub(r'<[^>]+>', '', heading)
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        n = counts[slug]
        counts[slug] += 1
        result.add(slug + ('-' + str(n) if n else ''))
    return result


def link_errors(root):
    errors = []
    for file in sorted(root.rglob('*.md')):
        if '.git' in file.parts:
            continue
        text = prose(file.read_text(encoding='utf-8'))
        targets = re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\)', text)
        targets += re.findall(r'^ {0,3}\[[^\]\n]+\]:\s*(<[^>]+>|\S+)', text, re.M)
        for raw in targets:
            url = urlsplit(raw.strip('<>'))
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            target = (file.parent / path).resolve() if path else file.resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f'{file.relative_to(root)}: link escapes package: {raw}')
                continue
            if not target.exists():
                errors.append(f'{file.relative_to(root)}: missing link: {raw}')
            elif url.fragment and target.suffix.lower() == '.md':
                if unquote(url.fragment) not in anchors(target.read_text(encoding='utf-8')):
                    errors.append(f'{file.relative_to(root)}: missing anchor: {raw}')
    return errors


def version_errors(root):
    errors = []
    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    front = re.match(r'\A---\n(.*?)\n---\n', skill, re.S)
    if not front:
        return ['SKILL.md: missing YAML frontmatter']
    for key in ('name', 'description'):
        if not re.search(r'^' + key + r':\s*\S+', front[1], re.M):
            errors.append(f'SKILL.md: missing {key}')
    name = re.search(r'^name:\s*["\']?([^\n"\']+)', front[1], re.M)
    if name and name[1].strip() != 'cs-phd-writing':
        errors.append('SKILL.md: unexpected skill name')
    versions = re.findall(r'^  version:\s*["\']?(\d+\.\d+\.\d+)["\']?\s*$', front[1], re.M)
    if len(versions) != 1:
        return errors + ['SKILL.md: expected one metadata.version']
    version = versions[0]
    for filename in ('README.md', 'README.en.md'):
        text = (root / filename).read_text(encoding='utf-8')
        declarations = re.findall(r'(?:主分支|[Mm]ain branch)\s+v(\d+\.\d+\.\d+)', text)
        if declarations != [version]:
            errors.append(f'{filename}: current version conflict: {declarations}, expected {version}')
    # History remains historical. Only check that the declared version has an entry.
    changelog = (root / 'CHANGELOG.md').read_text(encoding='utf-8')
    if not re.search(r'^## ' + re.escape(version) + r'\b', changelog, re.M):
        errors.append(f'CHANGELOG.md: no entry for {version}')
    return errors


def case_errors(root):
    cases = re.findall(r'^## C(\d+)[：:]', (root/'evals/cases.md').read_text(encoding='utf-8'), re.M)
    acceptance = re.findall(r'^\| C(\d+) \|', (root/'evals/acceptance.md').read_text(encoding='utf-8'), re.M)
    errors = []
    for name, values in [('cases', cases), ('acceptance', acceptance)]:
        repeated = [v for v, n in Counter(values).items() if n > 1]
        if repeated:
            errors.append(f'{name}: duplicate case IDs: {repeated}')
    if set(cases) != set(acceptance):
        errors.append(f'case correspondence missing: cases-only={sorted(set(cases)-set(acceptance))}, acceptance-only={sorted(set(acceptance)-set(cases))}')
    nums = {int(c) for c in cases}
    if not nums or nums != set(range(1, max(nums)+1)):
        errors.append('cases: missing/noncontinuous case IDs')
    return errors


def integration_errors(root):
    config = root/'evals/integration/expected/scope.json'
    if not config.exists():
        return []  # Required-file check reports it.
    try:
        scopes = json.loads(config.read_text(encoding='utf-8'))
        if not isinstance(scopes, dict) or not scopes:
            raise ValueError('scope must be a nonempty object')
        tasks = {p.stem for p in (root/'evals/integration/tasks').glob('I*.md')}
        rubric = (root/'evals/integration/expected/rubric.md').read_text(encoding='utf-8')
        expected = set(re.findall(r'^\| (I\d+) \|', rubric, re.M))
        errors = []
        if set(scopes) != tasks or tasks != expected:
            errors.append('integration task/scope/rubric correspondence missing')
        for task, files in scopes.items():
            if not isinstance(files, list) or any(not isinstance(p, str) for p in files):
                errors.append(f'{task}: invalid scope')
                continue
            for p in files:
                if not (root/'evals/integration/project'/p).is_file():
                    errors.append(f'{task}: scope file missing: {p}')
        return errors
    except (OSError, ValueError) as exc:
        return ['integration configuration: ' + str(exc)]


def validate(root):
    errors = [f'missing required file: {p}' for p in REQUIRED if not (root/p).is_file()]
    errors.extend(link_errors(root))
    errors.extend(integration_errors(root))
    if all((root/p).is_file() for p in ('SKILL.md', 'README.md', 'README.en.md', 'CHANGELOG.md')):
        errors.extend(version_errors(root))
    if all((root/p).is_file() for p in ('evals/cases.md', 'evals/acceptance.md')):
        errors.extend(case_errors(root))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--skip-tests', action='store_true', help='Only structural checks, useful while editing')
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    tests = None
    if not args.skip_tests:
        proc = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'evals', '-p', 'test_*.py'],
                              cwd=args.root, text=True, capture_output=True)
        tests = {'exit_code': proc.returncode, 'output': proc.stdout + proc.stderr}
        if proc.returncode:
            errors.append('Python regression tests failed')
    print(json.dumps({'errors': errors, 'tests': tests}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
