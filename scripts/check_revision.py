#!/usr/bin/env python3
"""Read-only revision diagnostics. Findings are candidates, not semantic verdicts."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

MACRO = re.compile(r'\\(?:[A-Za-z]*cite[A-Za-z]*|label|ref|eqref|autoref|cref|Cref|pageref)\*?(?![A-Za-z])')
MATH = re.compile(r'\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$|\\\[.*?\\\]|\\\(.*?\\\)', re.S)
FENCE = re.compile(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)',re.M|re.S)
NUMBER = re.compile(r'(?<![A-Za-z0-9_])[-+−]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?%?')


def balanced(text, pos, opening, closing):
    depth = 0
    for i in range(pos, len(text)):
        if text[i] == '\\':
            continue
        # An odd run of preceding backslashes escapes a delimiter.
        j = i - 1
        while j >= 0 and text[j] == '\\':
            j -= 1
        if (i - 1 - j) % 2:
            continue
        if text[i] == opening:
            depth += 1
        elif text[i] == closing:
            depth -= 1
            if depth == 0:
                return i + 1
    return None


def protected(text):
    spans = [(m.start(), m.end(), 'code', m.group()) for m in FENCE.finditer(text)]
    for m in MATH.finditer(text):
        if not any(a <= m.start() < b for a,b,_,_ in spans):
            spans.append((m.start(),m.end(),'math',m.group()))
    for m in MACRO.finditer(text):
        if any(a <= m.start() < b for a,b,_,_ in spans):
            continue
        pos = m.end()
        while pos < len(text):
            while pos < len(text) and text[pos].isspace():
                pos += 1
            if pos >= len(text) or text[pos] not in '[{':
                break
            end = balanced(text,pos,text[pos],']' if text[pos]=='[' else '}')
            if end is None:
                break
            pos = end
        spans.append((m.start(),pos,'reference',text[m.start():pos].rstrip()))
    return Counter((kind,value) for _,_,kind,value in spans)


def changes(before, after):
    return {'removed': list((before-after).elements()), 'added':list((after-before).elements())}


def load_glossary(path):
    data = json.loads(Path(path).read_text())
    if not isinstance(data,dict) or not isinstance(data.get('terms'),list):
        raise ValueError('glossary must contain a terms list')
    if not isinstance(data.get('allow',[]),list) or any(not isinstance(x,str) or not x for x in data.get('allow',[])):
        raise ValueError('allow must contain nonempty strings')
    for term in data['terms']:
        if not isinstance(term,dict) or not isinstance(term.get('preferred'),str) or not term['preferred']:
            raise ValueError('each term needs a nonempty preferred string')
        if not isinstance(term.get('variants'),list) or any(not isinstance(x,str) or not x for x in term['variants']):
            raise ValueError('variants must contain nonempty strings')
    return data


def analyze(before, after, glossary=None):
    findings=[]
    if glossary:
        for line_no,line in enumerate(after.splitlines(),1):
            masked=line
            for allowed in sorted(glossary.get('allow',[]),key=len,reverse=True):
                masked=masked.replace(allowed,' ' * len(allowed))
            for term in glossary['terms']:
                for variant in term['variants']:
                    for m in re.finditer(re.escape(variant),masked):
                        findings.append({'line':line_no,'column':m.start()+1,'found':variant,'preferred':term['preferred'],'reason':term.get('reason','check project definition')})
    return {'protected_changes':changes(protected(before),protected(after)),
            'number_changes':changes(Counter(NUMBER.findall(before)),Counter(NUMBER.findall(after))),
            'terminology_candidates':findings,
            'interpretation':'Review candidates in context; counts do not verify scope, order, causality or scientific meaning.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before',type=Path)
    parser.add_argument('after',type=Path)
    parser.add_argument('--glossary',type=Path)
    args=parser.parse_args()
    try:
        result=analyze(args.before.read_text(),args.after.read_text(),load_glossary(args.glossary) if args.glossary else None)
    except (OSError,ValueError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    sys.exit(main())
