#!/usr/bin/env python3
"""Check local site links, source preservation, math conversion, and scope."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote,urlsplit
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]


def luminance(h):
    rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    linear=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
    return sum(x*w for x,w in zip(linear,[.2126,.7152,.0722]))

def contrast(a,b):
    la,lb=sorted([luminance(a),luminance(b)])
    return (lb+.05)/(la+.05)

def check(site):
    site=site.resolve();baseline=json.loads((ROOT/'website/scientific_baseline.json').read_text());build=json.loads((site/'BUILD.json').read_text())
    docs={p:BeautifulSoup(p.read_text(),'html.parser') for p in site.rglob('*.html')}
    ids={p:{x['id'] for x in s.find_all(id=True)} for p,s in docs.items()}
    errors=[];links=0;math=0
    for p,soup in docs.items():
        if len(soup.find_all('h1'))!=1:errors.append(f'{p.relative_to(site)}: expected one h1')
        if not soup.find('main',id='main'): errors.append(f'{p}: main landmark missing')
        if soup.select('span.math:not(:has(math))'):errors.append(f'{p}: unconverted math')
        math+=len(soup.find_all('math'))
        for tag in soup.find_all(['a','img','script','link']):
            attr='src' if tag.name in ['img','script'] else 'href'
            if not tag.has_attr(attr):continue
            url=tag[attr];parts=urlsplit(url)
            if parts.scheme or parts.netloc:
                if tag.name!='a':errors.append(f'{p}: external runtime asset {url}')
                continue
            target=(p.parent/unquote(parts.path)).resolve() if parts.path else p
            if not target.is_relative_to(site): errors.append(f'{p.relative_to(site)}: escaping {url}');continue
            if target.is_dir():target=target/'index.html'
            if not target.is_file():errors.append(f'{p.relative_to(site)}: missing {url}');continue
            if parts.fragment and target in ids and unquote(parts.fragment) not in ids[target]:errors.append(f'{p.relative_to(site)}: missing anchor {url}')
            if tag.name=='img' and not tag.get('alt','').strip():errors.append(f'{p}: missing alt')
            links+=1
    for row in baseline['files']:
        for original in [ROOT/baseline.get('source_overrides', {}).get(row['path'], row['path']),site/'downloads'/row['path']]:
            if hashlib.sha256(original.read_bytes()).hexdigest()!=row['sha256']:errors.append('source changed: '+row['path'])
    if any(p.suffix.lower() in ['.ttf','.otf','.woff','.woff2'] for p in site.rglob('*')):errors.append('Standalone font file included')
    body=json.loads((ROOT/'website/palette.json').read_text())['colors']
    pairs={f'{fg}/paper':contrast(body[fg],body['paper']) for fg in ['ink','muted','iris','leaf','terracotta']}
    pairs.update({f'{fg}/white':contrast(body[fg],body['white']) for fg in ['ink','muted','iris','leaf','terracotta']})
    dark={'ink':'#EDF0E8','muted':'#BEC9BF','iris':'#B7C3F2','leaf':'#A6D0C1','focus':'#DDA487'}
    pairs.update({f'dark-{fg}/{bg}':contrast(color,surface) for fg,color in dark.items() for bg,surface in [('paper','#172321'),('surface','#1C2B28')]})
    if min(pairs.values())<4.5:errors.append('Insufficient tested text-token contrast')
    sections=build['extracted_sections']
    if len([r for r in sections if r['section'].startswith('M')])!=9:errors.append('Missing main question')
    if len(sections)!=17:errors.append('Missing appendix group')
    dialogue=(ROOT/'docs/DIALOGUE_REPORT.md').read_text()
    for row in sections:
        pattern=(r'^## '+row['section']+r'\. .+?$')
        start=re.search(pattern,dialogue,re.M)
        if not start:errors.append('Source section missing');continue
        tail=dialogue[start.end():]
        end=re.search(r'^#{1,2} ',tail,re.M)
        piece=dialogue[start.start():start.end()+end.start()].rstrip() if end else dialogue[start.start():].rstrip()
        if hashlib.sha256(piece.encode()).hexdigest()!=row['sha256']:errors.append('Extracted source section mismatch: '+row['section'])
    result={'passed':not errors,'html_pages':len(docs),'checked_local_links':links,'native_math_expressions':math,'preserved_baseline_files':len(baseline['files']),'source_sections_preserved':len(sections),'source_appendix_questions':len(re.findall(r'^### [A-H]\d+\.',dialogue,re.M)),'contrast_ratios_tested':pairs,'external_runtime_assets':0,'font_files_included':False,'full_accessibility_audit':False,'errors':errors}
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--site',type=Path,required=True);ap.add_argument('--report',type=Path)
    a=ap.parse_args();r=check(a.site);text=json.dumps(r,indent=2)+'\n'
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(text)
    print(text)
    raise SystemExit(0 if r['passed'] else 1)
