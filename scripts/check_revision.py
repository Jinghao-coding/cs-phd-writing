#!/usr/bin/env python3
"""Read-only lexical revision diagnostics; candidates are not semantic verdicts."""
import argparse
from collections import Counter
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys

MACRO = re.compile(r'\\(?:[A-Za-z]*cite[A-Za-z]*|label|ref|eqref|autoref|cref|Cref|pageref)\*?(?![A-Za-z])')
MATH = re.compile(r'\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$|\\\[.*?\\\]|\\\(.*?\\\)', re.S)
# Global numeric counts retain the v0.6 interface. Local objects include markers/units.
NUMBER = re.compile(r'(?<![A-Za-z0-9_])[-+−]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?%?')
UNIT = re.compile(r'(?:\\%|%|[ \t]*(?:ns|us|µs|μs|ms|s|min|h|Hz|kHz|MHz|GHz|B|KB|MB|GB|TB|KiB|MiB|GiB|bit|bits|bytes|W|J|mJ|m|cm|mm)(?:/s)?(?![A-Za-z]))')


def escaped(text, pos):
    j = pos - 1
    while j >= 0 and text[j] == '\\':
        j -= 1
    return (pos - 1 - j) % 2 == 1


def balanced(text, pos, opening, closing):
    depth = 0
    for i in range(pos, len(text)):
        if escaped(text, i):
            continue
        if text[i] == opening:
            depth += 1
        elif text[i] == closing:
            depth -= 1
            if depth == 0:
                return i + 1
    return None


def code_regions(text):
    """CommonMark-style fences indented 0–3 spaces; an open fence reaches EOF."""
    spans, start, delimiter, offset = [], None, '', 0
    for line in text.splitlines(keepends=True):
        if start is None:
            m = re.match(r' {0,3}(`{3,}|~{3,})([^\r\n]*)', line)
            if m and not (m[1][0] == '`' and '`' in m[2]):
                start, delimiter = offset, m[1]
        elif re.fullmatch(r' {0,3}' + re.escape(delimiter[0]) +
                          '{' + str(len(delimiter)) + r',}[ \t]*(?:\r?\n)?', line):
            spans.append((start, offset + len(line), 'code'))
            start = None
        offset += len(line)
    if start is not None:
        spans.append((start, len(text), 'code'))
    return spans


def overlaps(start, end, spans):
    return any(start < b and a < end for a, b, *_ in spans)


def location(text, start, end):
    def point(pos):
        return {'line': text.count('\n', 0, pos) + 1,
                'column': pos - text.rfind('\n', 0, pos)}
    return {'start': start, 'end': end, **point(start), 'end_position': point(end)}


def extract(text):
    spans = code_regions(text)
    warnings = []
    for m in MATH.finditer(text):
        if not escaped(text, m.start()) and not overlaps(m.start(), m.end(), spans):
            spans.append((m.start(), m.end(), 'math'))
    for m in MACRO.finditer(text):
        if escaped(text, m.start()) or overlaps(m.start(), m.end(), spans):
            continue
        pos, last = m.end(), m.end()
        while pos < len(text):
            while pos < len(text) and text[pos].isspace():
                pos += 1
            if pos >= len(text) or text[pos] not in '[{':
                break
            end = balanced(text, pos, text[pos], ']' if text[pos] == '[' else '}')
            if end is None:
                warnings.append({'kind': 'unclosed_macro_argument', **location(text, m.start(), pos)})
                break
            pos = last = end
        spans.append((m.start(), last, 'reference'))
    for m in NUMBER.finditer(text):
        if overlaps(m.start(), m.end(), spans):
            continue
        end = m.end()
        unit = UNIT.match(text, end) if not m[0].endswith('%') else None
        if unit:
            end = unit.end()
        spans.append((m.start(), end, 'number'))
    spans.sort()
    objects = []
    for start, end, kind in spans:
        # Clauses localize association; full paragraphs retain neighboring evidence.
        left = max([text.rfind(c, 0, start) for c in '\n。！？；，'] + [-1]) + 1
        right = min([p for c in '\n。！？；，' if (p := text.find(c, end)) >= 0] + [len(text)])
        pleft = text.rfind('\n\n', 0, start) + 2
        if pleft == 1:
            pleft = 0
        pright = text.find('\n\n', end)
        if pright < 0:
            pright = len(text)
        obj = {'kind': kind, 'text': text[start:end], **location(text, start, end),
               'context': text[left:right], 'context_start': left,
               'paragraph': text[pleft:pright], 'paragraph_start': pleft}
        # Internal key: replace all extracted objects in this clause, preserving roles.
        skeleton, cursor = [], left
        for a, b, k in spans:
            if left <= a and b <= right:
                skeleton.extend((text[cursor:a], '{' + k + '}'))
                cursor = b
        skeleton.append(text[cursor:right])
        obj['_slot'] = ''.join(skeleton)
        objects.append(obj)
    return objects, warnings


def protected(text):
    return Counter((o['kind'], o['text']) for o in extract(text)[0] if o['kind'] != 'number')


def changes(before, after):
    return {'removed': list((before - after).elements()), 'added': list((after - before).elements())}


def public(obj):
    return {k: v for k, v in obj.items() if not k.startswith('_')}


def local_changes(before, after, old, new):
    remaining_old, remaining_new = list(range(len(old))), list(range(len(new)))
    candidates = []
    opcodes = SequenceMatcher(None, before, after, autojunk=False).get_opcodes()
    hunks = [{'before': location(before, a, b), 'after': location(after, c, d)}
             for tag, a, b, c, d in opcodes if tag != 'equal']

    def pair(i, j, kind, basis):
        a, b = old[i], new[j]
        if kind:
            candidates.append({'candidate_type': kind, 'object_type': a['kind'],
                               'before': public(a), 'after': public(b), 'match_basis': basis,
                               'uncertainty': 'Lexical match only; verify association and meaning in context.'})
        remaining_old.remove(i)
        remaining_new.remove(j)

    # Stable occurrences, including duplicates and intact relocated paragraphs.
    for i in remaining_old[:]:
        matches = [j for j in remaining_new if (old[i]['kind'], old[i]['text'], old[i]['context']) ==
                   (new[j]['kind'], new[j]['text'], new[j]['context'])]
        if matches:
            pair(i, matches[0], None, 'identical_text_and_context')
    # A unique lexical role within a clause can expose same-multiset swaps.
    for i in remaining_old[:]:
        key = (old[i]['kind'], old[i]['_slot'])
        matches = [j for j in remaining_new if (new[j]['kind'], new[j]['_slot']) == key]
        peers = [k for k in remaining_old if (old[k]['kind'], old[k]['_slot']) == key]
        if len(matches) == len(peers) == 1:
            j = matches[0]
            kind = 'local_replacement'
            if old[i]['kind'] == 'number':
                av, bv = NUMBER.match(old[i]['text']), NUMBER.match(new[j]['text'])
                if av and bv and av[0].rstrip('%') == bv[0].rstrip('%'):
                    kind = 'unit_or_marker_changed'
            pair(i, j, kind, 'unique_clause_slot')
    for i in remaining_old[:]:
        matches = [j for j in remaining_new if (old[i]['kind'], old[i]['text']) ==
                   (new[j]['kind'], new[j]['text'])]
        peers = [k for k in remaining_old if (old[k]['kind'], old[k]['text']) ==
                 (old[i]['kind'], old[i]['text'])]
        if len(matches) == len(peers) == 1:
            pair(i, matches[0], 'context_or_position_changed', 'unique_identical_object')
    # Avoid guessing which repeated occurrence corresponds to which new object.
    for indices, objects, side in ((remaining_old, old, 'before'), (remaining_new, new, 'after')):
        for i in indices:
            candidates.append({'candidate_type': 'unmatched_' + ('old' if side == 'before' else 'new'),
                               'object_type': objects[i]['kind'], side: public(objects[i]),
                               'match_basis': 'unresolved',
                               'uncertainty': 'May be added, removed, moved or edited; no reliable pairing.'})
    return candidates, hunks


def load_glossary(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('terms'), list):
        raise ValueError('glossary must contain a terms list')
    if not isinstance(data.get('allow', []), list) or any(not isinstance(x, str) or not x for x in data.get('allow', [])):
        raise ValueError('allow must contain nonempty strings')
    for term in data['terms']:
        if not isinstance(term, dict) or not isinstance(term.get('preferred'), str) or not term['preferred']:
            raise ValueError('each term needs a nonempty preferred string')
        if not isinstance(term.get('variants'), list) or any(not isinstance(x, str) or not x for x in term['variants']):
            raise ValueError('variants must contain nonempty strings')
    return data


def analyze(before, after, glossary=None):
    old, old_warnings = extract(before)
    new, new_warnings = extract(after)
    candidates, hunks = local_changes(before, after, old, new)
    findings = []
    if glossary:
        masked = list(after)
        for start, end, _ in code_regions(after):
            masked[start:end] = ['\n' if c == '\n' else ' ' for c in after[start:end]]
        masked = ''.join(masked)
        for allowed in sorted(glossary.get('allow', []), key=len, reverse=True):
            masked = masked.replace(allowed, ''.join('\n' if c == '\n' else ' ' for c in allowed))
        for term in glossary['terms']:
            for variant in term['variants']:
                for m in re.finditer(re.escape(variant), masked):
                    findings.append({**location(after, m.start(), m.end()), 'found': variant,
                                     'preferred': term['preferred'], 'reason': term.get('reason', 'check project definition')})
    counts = lambda objs: Counter((o['kind'], o['text']) for o in objs if o['kind'] != 'number')
    return {'protected_changes': changes(counts(old), counts(new)),
            'number_changes': changes(Counter(NUMBER.findall(before)), Counter(NUMBER.findall(after))),
            'terminology_candidates': findings, 'schema_version': 2,
            'local_candidates': candidates, 'diff_hunks': hunks,
            'objects': {'before': [public(o) for o in old], 'after': [public(o) for o in new]},
            'coverage_warnings': {'before': old_warnings, 'after': new_warnings},
            'position_convention': 'Unicode code points; 0-based half-open offsets; 1-based lines/columns; newline-normalized CLI input.',
            'interpretation': 'Lexical candidates only. Counts and local matches do not verify scientific meaning. Intact clause moves may be silent; inspect diff_hunks.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--glossary', type=Path)
    args = parser.parse_args()
    try:
        result = analyze(args.before.read_text(encoding='utf-8'), args.after.read_text(encoding='utf-8'),
                         load_glossary(args.glossary) if args.glossary else None)
    except (OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
