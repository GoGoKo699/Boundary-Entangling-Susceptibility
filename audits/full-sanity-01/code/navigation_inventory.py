#!/usr/bin/env python3
"""Read-only baseline link/source inventory; fragment check approximates GitHub slugs."""
from pathlib import Path
import ast, csv, html, json, re, subprocess, sys, unicodedata
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'audits/full-sanity-01/results'


def headings(path):
    seen={};result=set()
    for text in path.read_text().splitlines():
        match=re.match(r'^#{1,6}\s+(.*)',text)
        if not match:continue
        title=match.group(1).strip().rstrip('#').strip()
        title=re.sub('<[^>]+>','',title)
        title=''.join(c for c in title.lower() if c in '-_ ' or unicodedata.category(c)[0] in 'LN')
        slug=title.replace(' ','-')
        count=seen.get(slug,0);seen[slug]=count+1
        result.add(slug+(f'-{count}' if count else ''))
    return result


def main():
    paths=[ROOT/s for s in subprocess.check_output(['git','ls-tree','-r','--name-only','00009cf7cc02104e4c776863b3ea551bd38e00f4'],cwd=ROOT,text=True).splitlines()]
    links=[];imports=[];fragments=[]
    local_names={p.stem for p in paths if p.suffix=='.py'}
    for path in paths:
        if path.suffix=='.md':
            content=path.read_text()
            patterns=[r'!?\[[^\]]*\]\(([^)]+)\)',r'<(?:img|source)\b[^>]*\bsrc=[\"\']([^\"\']+)[\"\']']
            for pattern in patterns:
                for match in re.finditer(pattern,content,flags=re.I):
                    target=html.unescape(match.group(1).strip())
                    if target.startswith(('http://','https://','mailto:','data:')):continue
                    target=re.split(r'\s+[\"\']',target,maxsplit=1)[0].strip('<>')
                    p,_,frag=target.partition('#')
                    p=unquote(p.split('?',1)[0])
                    dest=(ROOT/p.lstrip('/')) if p.startswith('/') else ((path.parent/p) if p else path)
                    status='exists' if dest.exists() else 'missing'
                    if frag and status=='exists' and dest.suffix=='.md':
                        status='fragment_exists' if unquote(frag) in headings(dest) else 'fragment_review'
                        if status=='fragment_review':fragments.append([str(path.relative_to(ROOT)),target])
                    links.append(dict(source=str(path.relative_to(ROOT)),line=content[:match.start()].count('\n')+1,target=target,status=status))
        if path.suffix=='.py':
            tree=ast.parse(path.read_text())
            for node in ast.walk(tree):
                names=[]
                if isinstance(node,ast.Import):names=[x.name for x in node.names]
                elif isinstance(node,ast.ImportFrom):names=[node.module] if node.module else []
                for name in names:
                    root=name.split('.')[0]
                    local=path.parent/(root+'.py')
                    status='stdlib' if root in sys.stdlib_module_names or root=='__future__' else ('local' if local.exists() or root in local_names or root=='boundary_susceptibility' else 'dependency')
                    imports.append(dict(source=str(path.relative_to(ROOT)),line=node.lineno,module=name,status=status))
    OUT.mkdir(parents=True,exist_ok=True)
    for name,rows in [('navigation_links.csv',links),('navigation_imports.csv',imports)]:
        with (OUT/name).open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    report=dict(baseline='00009cf7cc02104e4c776863b3ea551bd38e00f4',
                tracked_files=len(paths),markdown_files=sum(p.suffix=='.md' for p in paths),
                python_files=sum(p.suffix=='.py' for p in paths),local_links=len(links),
                missing_links=[r for r in links if r['status']=='missing'],fragment_review=fragments,
                dependencies=sorted(set(r['module'].split('.')[0] for r in imports if r['status']=='dependency')),
                manuscript_tex=[str(p.relative_to(ROOT)) for p in paths if p.suffix=='.tex'],
                editable_schematic_formats=[str(p.relative_to(ROOT)) for p in paths if p.suffix.lower() in ['.drawio','.vsdx','.fig','.ai','.pptx','.odp']],
                limitation='Local existence, AST imports and approximate GitHub heading slugs only; external URLs and live GitHub math rendering not tested here.')
    (OUT/'navigation_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
