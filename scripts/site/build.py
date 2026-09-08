#!/usr/bin/env python3
"""Build an offline, source-derived project website without editing the study."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit, quote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / 'website'
REPO = 'https://github.com/GoGoKo699/Boundary-Entangling-Susceptibility'

@dataclass
class Page:
    output: str
    source: str
    title: str
    section: str
    text: str
    extracted: bool = False


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def relative(current: str, target: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(current) or '.')


def title_of(text: str, fallback: str) -> str:
    m=re.search(r'^#{1,6}\s+(.+)$', text, re.M)
    return m.group(1) if m else fallback


def build(output: Path, figures: Path | None = None) -> dict:
    output=output.resolve()
    if output.is_relative_to(ROOT): raise ValueError('Output must be outside the scientific repository')
    if output.exists(): raise FileExistsError('Use a new output directory; the builder does not remove existing files')
    baseline=json.loads((WEB/'scientific_baseline.json').read_text())
    originals={r['path']:r for r in baseline['files']}
    def source_path(path):
        return ROOT / baseline.get('source_overrides', {}).get(path, path)
    for path,r in originals.items():
        raw=source_path(path).read_bytes()
        if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']: raise ValueError(f'Frozen source changed: {path}')
    converter=subprocess.run(['pandoc','--version'],check=True,capture_output=True,text=True).stdout.splitlines()[0]
    output.mkdir(parents=True)
    pages=[]; routes={}; extracted=[]; math_normalizations=[]; figure_manifest=json.loads((WEB/'figures.json').read_text())
    palette=json.loads((WEB/'palette.json').read_text())
    for path in sorted(originals):
        p=Path(path)
        if p.suffix.lower()=='.md':
            text=source_path(path).read_text()
            dest='library/'+p.with_suffix('.html').as_posix()
            section='Reference'
            if path in ['docs/SCIENTIFIC_STORY.md','docs/DIALOGUE_REPORT.md','docs/DIALOGUE_QUESTION_MAP.md']: section='The story'
            elif path in ['docs/THEORY.md','docs/NOTATION.md','docs/NUMERICAL_METHODS.md','docs/CLAIM_EVIDENCE_MAP.md']: section='Theory & methods'
            elif path in ['docs/REPRODUCTION.md','docs/CODE_MAP.md','docs/REPRODUCIBILITY_LIMITS.md','docs/VALIDATION.md','docs/DATA_POLICY.md']: section='Reproduce'
            pages.append(Page(dest,path,title_of(text,p.stem),section,text));routes[path]=dest
    for name,title in [('index','Boundary entangling susceptibility'),('resources','Everything behind the result'),('design','Color and reading guide')]:
        source=f'website/content/{name}.md';dest='index.html' if name=='index' else f'{name}/index.html'
        text=(ROOT/source).read_text()
        if name=='design':
            swatches='<div class="swatches">'+''.join(f'<div class="swatch"><span style="background:{v}" aria-hidden="true"></span><strong>{k.capitalize()}</strong><code>{v}</code></div>' for k,v in palette['colors'].items())+'</div>'
            text=text.replace('<!-- PALETTE -->',swatches)
        pages.append(Page(dest,source,title,'Home' if name=='index' else 'Resources',text));routes[source]=dest
    dialogue=(ROOT/'docs/DIALOGUE_REPORT.md').read_text()
    for letter,pattern,stop,prefix in [('M',r'^## (M[1-9])\. (.+)$','# Part II.','read'),
                                      ('A',r'^## ([A-H])\. (.+)$','# Source register','appendix')]:
        matches=list(re.finditer(pattern,dialogue,re.M))
        for i,m in enumerate(matches):
            end=matches[i+1].start() if i+1<len(matches) else dialogue.index(stop,m.start())
            body=dialogue[m.start():end].rstrip()
            key=m.group(1).lower(); dest=f'{prefix}/{key}.html'
            extracted.append({'page':dest,'source':'docs/DIALOGUE_REPORT.md','section':m.group(1),'sha256':sha(body.encode()),'start_line':dialogue[:m.start()].count('\n')+1})
            pages.append(Page(dest,'docs/DIALOGUE_REPORT.md',m.group(1)+'. '+m.group(2), 'The story' if prefix=='read' else 'Appendix',body,True))
    gallery='# Four figures, three comparison designs\n\nEach figure has a different job. The cards below link the observation to its definition, data, code, and uncertainty. The accepted panels are shown here; a separate color-only preview explores the Irises palette.\n\n'
    for f in figure_manifest:
        gallery+=f'## Figure {f["id"]}. {f["title"]}\n\n**{f["question"]}**\n\n{f["interpretation"]}\n\n'
        gallery+='<div class="panel-row">'+''.join(f'<a href="../../figures/core/{p}.pdf"><img src="../../figures/core/{p}.png" alt="Accepted Figure {f["id"]}: {p.replace("_"," ")}"></a>' for p in f['panels'])+'</div>\n\n'
        gallery+=f'[Read the source question](site:read/{f["story"].lower()}.html) · [Methods and boundaries](../../docs/{f["method"]}) · [Plotting code](../../scripts/figures/{f["script"]})\n\n'
        gallery+='Data: '+', '.join(f'[{d}](../../data/processed/core_figures/{d})' for d in f['data'])+'.\n\n'
        for p in f['panels']:
            gallery+=f'**{p}**: [PDF](../../figures/core/{p}.pdf) · [PNG](../../figures/core/{p}.png) · [SVG](../../figures/core_svg/{p}.svg).\n\n'
    gallery+='The original combined layouts include externally maintained schematics. Only the six accepted Python panels are tracked here; no TeX or TikZ source is introduced by this site. The exact published-layout assembly must not be inferred from these component panels. See the [figure baseline](../../docs/FIGURE_BASELINE.md).\n'
    pages.append(Page('figures/index.html','website/content/figures.md','The four figures','Four figures',gallery))
    # Optional palette previews have separate paths and are never substituted for accepted figures.
    if figures:
        figures=figures.resolve(); validation=json.loads((figures/'palette_verification.json').read_text())
        if not validation['passed']: raise ValueError('Unverified color preview')
        for p in figures.iterdir():
            dest=output/'palette-preview'/p.name; dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        preview='# Irises palette: six-panel comparison\n\nThese are presentation candidates, not replacements for the accepted figures. Numeric arrays, interval endpoints, text, marker geometry, axis limits, and normalizations are checked against the original plotting code.\n\n'
        for f in figure_manifest:
            for p in f['panels']:
                preview+=f'## {p}\n\n<div class="comparison"><figure><img src="../../figures/core/{p}.png" alt="Accepted colors: {p}"><figcaption>Accepted colors</figcaption></figure><figure><img src="site:palette-preview/{p}.png" alt="Irises color proposal: {p}"><figcaption>Irises proposal, same data and layout</figcaption></figure></div>\n\n[Preview PDF](site:palette-preview/{p}.pdf) · [Preview SVG](site:palette-preview/{p}.svg)\n\n'
        preview+='[Palette and encoding rules](design.md) · [Color-only verification](site:palette-preview/palette_verification.json)\n'
        pages.append(Page('design/figures.html','website/content/preview.md','Review the figure palette','Resources',preview))
    for p in pages: routes.setdefault(p.source,p.output)
    # Keep downloadable source bytes and all needed scientific assets available offline.
    for path in originals:
        target=output/'downloads'/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source_path(path),target)
    for source in ['website/palette.json','website/figures.json','website/README.md','website/EDITORIAL_POLICY.md']:
        target=output/'downloads'/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,target)
    directories={'.'}
    for path in originals:
        parent=PurePosixPath(path).parent
        directories.update(str(p) for p in [parent,*parent.parents])
    def dir_dest(path):return 'browse/index.html' if path=='.' else f'browse/{path}/index.html'
    # Directory pages are generated only for the included baseline, not the container filesystem.
    for directory in sorted(directories):
        items=[]
        for child in sorted(directories):
            if child!='.' and str(PurePosixPath(child).parent)==directory:
                items.append(f'<tr><td><a href="site:{dir_dest(child)}">{html.escape(PurePosixPath(child).name)}/</a></td><td>Directory</td></tr>')
        for path,r in sorted(originals.items()):
            if str(PurePosixPath(path).parent)==directory:
                target=routes.get(path,'downloads/'+path)
                items.append(f'<tr><td><a href="site:{target}">{html.escape(PurePosixPath(path).name)}</a></td><td>{r["bytes"]:,} bytes</td></tr>')
        text=f'# Source files: {html.escape(directory)}\n\nThis index lists the included scientific baseline. The source downloads retain their original bytes.\n\n<table><thead><tr><th>File</th><th>Contents</th></tr></thead><tbody>'+''.join(items)+'</tbody></table>'
        pages.append(Page(dir_dest(directory),'website/content/browser.md',f'Source files: {directory}','Source files',text))
    top=[('Home','index.html'),('The story','read/m1.html'),('Four figures','figures/index.html'),('Theory & methods',routes['docs/THEORY.md']),('Reproduce',routes['docs/REPRODUCTION.md']),('Resources','resources/index.html')]
    preferred=['docs/SCIENTIFIC_STORY.md','docs/THEORY.md','docs/NOTATION.md','docs/NUMERICAL_METHODS.md','docs/CLAIM_EVIDENCE_MAP.md',
               'docs/REPRODUCTION.md','docs/CODE_MAP.md','docs/FIGURE1_UNCERTAINTY.md','docs/EVIDENCE_REASSESSMENT.md','docs/REPRODUCIBILITY_LIMITS.md','docs/RELATED_WORK.md']
    page_by_dest={p.output:p for p in pages}
    def link(current,target,label,cls=''):
        url=relative(current,target)
        return f'<a href="{html.escape(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+(' aria-current="page"' if current==target else '')+f'>{html.escape(label)}</a>'
    def rewrite(url, page):
        if url.startswith('site:'): return relative(page.output,url[5:])
        bits=urlsplit(url)
        if bits.scheme or bits.netloc or not bits.path: return url
        source=posixpath.normpath(posixpath.join(posixpath.dirname(page.source),unquote(bits.path)))
        if source=='..' or source.startswith('../') or source.startswith('/'): raise ValueError(f'Escaping source link: {url}')
        if source in routes: dest=routes[source]
        elif source in directories: dest=dir_dest(source)
        elif source in originals or (output/'downloads'/source).exists(): dest='downloads/'+source
        else: raise FileNotFoundError(f'{page.source}: link target {url} -> {source}')
        return quote(relative(page.output,dest),safe='/._-')+('?' + bits.query if bits.query else '')+('#'+bits.fragment if bits.fragment else '')
    def render(page):
        parsed=subprocess.run(['pandoc','--from=markdown+gfm_auto_identifiers+tex_math_single_backslash-implicit_figures-smart','--to=json'],input=page.text,text=True,capture_output=True,check=True)
        ast=json.loads(parsed.stdout)
        def math_fonts(node):
            if isinstance(node,list):
                for x in node: math_fonts(x)
            elif isinstance(node,dict):
                if node.get('t')=='Math':
                    # Pandoc's MathML writer rejects legacy TeX font declarations.
                    # Expand only brace-delimited roman text in Math nodes.
                    # The original Markdown and downloadable source are untouched.
                    original=node['c'][1]
                    converted=re.sub(r'\{\\rm\s+([^{}]+)\}',r'\\mathrm{\1}',original)
                    node['c'][1]=converted
                    if converted != original:
                        math_normalizations.append({'page':page.output,'before':original,'after':converted})
                else:
                    for x in node.values(): math_fonts(x)
        math_fonts(ast)
        proc=subprocess.run(['pandoc','--from=json','--to=html5','--mathml','--wrap=none'],input=json.dumps(ast),text=True,capture_output=True,check=True)
        if proc.stderr.strip(): raise RuntimeError(f'{page.source}: pandoc warning: {proc.stderr}')
        soup=BeautifulSoup(proc.stdout,'html.parser')
        headers=soup.find_all(re.compile('^h[1-6]$'))
        if headers:
            headers[0].name='h1'
            for tag in headers[1:]:
                if tag.name=='h1':tag.name='h2'
        for a in soup.find_all('a',href=True):
            a['href']=rewrite(a['href'],page)
            if a['href'].startswith(('https:','http:')):a['rel']='noreferrer noopener'
        for tag in soup.find_all(src=True):
            tag['src']=rewrite(tag['src'],page)
            if tag.name=='img':tag['loading']='lazy';tag['decoding']='async'
        for table in soup.find_all('table'):
            wrap=soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':'Scrollable data table'})
            table.wrap(wrap)
        for expression in soup.find_all('math'):
            block=expression.get('display')=='block'
            wrap=soup.new_tag('span',attrs={'class':'math-scroll' if block else 'math-inline'})
            if block:
                wrap['tabindex']='0';wrap['role']='region';wrap['aria-label']='Mathematical expression; scroll horizontally if needed'
            expression.wrap(wrap)
        for script in soup.find_all(['script','iframe']):script.decompose()
        for tag in soup.find_all(True):
            for attr in list(tag.attrs):
                if attr.lower().startswith('on'):del tag[attr]
        for code in soup.select('pre'):
            code['tabindex']='0'
        toc='<ol>'+''.join(f'<li>{link(page.output,page.output+"#"+h["id"],h.get_text(" ",strip=True))}</li>' for h in soup.find_all(['h2'],id=True))+'</ol>'
        # Plain source tags in the scientific dialogue point to their existing source register.
        if page.extracted:
            footer=BeautifulSoup('<p class="source-context">Source citations such as [S2] refer to the <a>complete source register</a>.</p>','html.parser')
            footer.a['href']=relative(page.output,routes['docs/DIALOGUE_REPORT.md'])+'#source-register-and-reproduction'
            soup.append(footer)
        return str(soup),toc,soup.get_text(' ',strip=True)
    search=[]; rendered=[]
    for page in pages:
        content,toc,plain=render(page)
        sidebar='<p class="nav-label">Read the argument</p>'+''.join(link(page.output,f'read/m{i}.html',f'{i:02}  '+page_by_dest[f'read/m{i}.html'].title.split('. ',1)[1]) for i in range(1,10))
        sidebar+='<details><summary>Appendix questions</summary>'+''.join(link(page.output,p.output,p.title) for p in pages if p.section=='Appendix')+'</details>'
        sidebar+='<p class="nav-label">Inspect & reproduce</p>'+''.join(link(page.output,routes[s],page_by_dest[routes[s]].title) for s in preferred if s!='docs/SCIENTIFIC_STORY.md')
        sidebar+=link(page.output,'browse/index.html','Source-file index')+link(page.output,'design/index.html','Color & reading guide')
        if figures:sidebar+=link(page.output,'design/figures.html','Review the Irises figures')
        previous_next=''
        if page.output.startswith('read/m'):
            i=int(re.search(r'm(\d)',page.output).group(1)); entries=[]
            if i>1:entries.append(link(page.output,f'read/m{i-1}.html','Previous question'))
            if i<9:entries.append(link(page.output,f'read/m{i+1}.html','Next question'))
            else:entries.append(link(page.output,'figures/index.html','Inspect the four figures'))
            previous_next='<nav class="step-nav" aria-label="Reading sequence">'+''.join(entries)+'</nav>'
        nav=''.join(link(page.output,d,t) for t,d in top)
        root=relative(page.output,'index.html').removesuffix('index.html')
        sourceinfo=''
        if page.source in originals:
            sourceinfo=f'<details class="source-info"><summary>Page source and scientific baseline</summary><p>{link(page.output,"downloads/"+page.source,page.source)} · <a href="{REPO}/blob/{baseline["commit"]}/{page.source}" rel="noreferrer">View this source on GitHub</a></p><p>Baseline <code>{baseline["commit"]}</code>. '+('Question extracted from the existing dialogue without rewriting its text.' if page.extracted else 'Rendered directly from the scientific source.')+'</p></details>'
        ribbon='<span class="preview-label">Private website preview</span>'
        doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><meta name="color-scheme" content="light dark"><title>{html.escape(page.title)} | Boundary entangling susceptibility</title><link rel="stylesheet" href="{relative(page.output,'assets/site.css')}"><script defer src="{relative(page.output,'assets/search-index.js')}"></script><script defer src="{relative(page.output,'assets/site.js')}"></script></head>
<body data-root="{root}" class="{'home' if page.output=='index.html' else 'reading'}"><a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner"><a class="brand" href="{relative(page.output,'index.html')}"><span>Boundary entangling</span><strong>susceptibility</strong></a><div class="header-tools">{ribbon}<button type="button" id="theme" aria-label="Switch reading theme">Dark</button><button type="button" id="menu" aria-controls="side-navigation" aria-expanded="false">Contents</button></div></div><nav class="top-nav" aria-label="Main">{nav}</nav></header>
<div class="layout"><aside class="sidebar" id="side-navigation" aria-label="Project contents"><form role="search" id="search-form"><label for="search">Search the project</label><input id="search" type="search" autocomplete="off" placeholder="purity, bootstrap, near cut…"><div id="search-status" role="status" aria-live="polite"></div><div id="search-results"></div></form><nav>{sidebar}</nav></aside>
<main id="main"><div class="kicker">{html.escape(page.section)}</div><article>{content}</article>{previous_next}{sourceinfo}<footer class="page-footer">Boundary-Entangling-Susceptibility · Scientific sources preserved · {link(page.output,'resources/index.html','Sources, scope & reuse')}</footer></main><aside class="on-page" aria-label="On this page"><strong>On this page</strong>{toc}</aside></div>
</body></html>'''
        target=output/page.output;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc)
        rendered.append({'path':page.output,'source':page.source,'source_text_sha256':sha(page.text.encode()),'mathml_count':content.count('<math')})
        if page.section!='Source files':search.append({'title':page.title,'url':page.output,'section':page.section,'text':plain})
    (output/'assets').mkdir(exist_ok=True)
    for name in ['site.css','site.js']:shutil.copyfile(WEB/'assets'/name,output/'assets'/name)
    (output/'assets/search-index.js').write_text('window.BES_SEARCH='+json.dumps(search,ensure_ascii=False).replace('</','<\\/')+';\n')
    (output/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (output/'.nojekyll').touch()
    report={'status':'repository-build preview; not deployed','scientific_commit':baseline['commit'],'scientific_tree':baseline['tree'],'source_files_preserved':len(originals),'pages':len(pages),'converter':converter,'mathml_count':sum(r['mathml_count'] for r in rendered),'new_scientific_analysis':False,'extracted_sections':extracted,'source_pages':rendered,'runtime_external_assets':0,'palette_preview':bool(figures),'render_only_math_normalizations':math_normalizations}
    (output/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--figures',type=Path)
    a=parser.parse_args();r=build(a.output,a.figures);print(json.dumps({k:v for k,v in r.items() if k not in ['source_pages','extracted_sections']},indent=2))
