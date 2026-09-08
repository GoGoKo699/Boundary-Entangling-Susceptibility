#!/usr/bin/env python3
"""Evaluate the accepted plotting code with a color-only, in-memory preview.

No accepted file is overwritten. The baseline and preview artist geometry,
text, data arrays, error-bar segments, and image normalizations must agree.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from cycler import cycler

ROOT = Path(__file__).resolve().parents[2]
PLOTS = ROOT / 'scripts/figures'
sys.path.insert(0, str(PLOTS))
import export_formats


def clean(v):
    if isinstance(v, np.ndarray): return clean(v.tolist())
    if isinstance(v, (list, tuple)): return [clean(x) for x in v]
    if isinstance(v, dict): return {k: clean(x) for k, x in v.items()}
    if isinstance(v, np.generic): return v.item()
    return v


def geometry(fig):
    """Record properties whose change would exceed a palette-only revision."""
    fig.canvas.draw()
    result={'size':fig.get_size_inches().tolist(),'axes':[],
            'figure_text':[(x.get_text(),x.get_position(),x.get_fontsize()) for x in fig.texts]}
    for ax in fig.axes:
        entry={'bbox':ax.get_position().bounds,'xlim':ax.get_xlim(),'ylim':ax.get_ylim(),
               'xticks':ax.get_xticks(),'yticks':ax.get_yticks(),
               'xlabel':ax.get_xlabel(),'ylabel':ax.get_ylabel(),'title':ax.get_title(),
               'text':[(x.get_text(),x.get_position(),x.get_fontsize()) for x in ax.texts],
               'lines':[(x.get_xdata(),x.get_ydata(),x.get_marker(),x.get_markersize(),x.get_linestyle(),x.get_linewidth()) for x in ax.lines],
               'collections':[(x.get_offsets(),[p.vertices for p in x.get_paths()]) for x in ax.collections],
               'images':[(np.asarray(x.get_array()),x.norm.vmin,x.norm.vmax,x.get_extent()) for x in ax.images],
               'patches':[(p.get_path().vertices,p.get_transform().get_matrix()) for p in ax.patches]}
        result['axes'].append(entry)
    return clean(result)


def text_contrast(foreground, background):
    def luminance(color):
        components=to_rgb(color)
        return sum(w*(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4)
                   for w,x in zip([.2126,.7152,.0722],components))
    lo,hi=sorted([luminance(foreground),luminance(background)])
    return (hi+.05)/(lo+.05)


def readable_matrix_labels(fig, ink):
    """Change label colors only; retain text, positions, sizes, and matrix scales."""
    checks=[]
    for ax in fig.axes:
        for image in ax.images:
            data=np.asarray(image.get_array())
            if data.ndim!=2:continue
            for label in ax.texts:
                x,y=label.get_position();j,i=int(np.floor(x+.5)),int(np.floor(y+.5))
                if not(0<=i<data.shape[0] and 0<=j<data.shape[1]):continue
                background=to_hex(image.cmap(image.norm(data[i,j])))
                old=to_hex(label.get_color())
                chosen=max([ink,'#FFFFFF'],key=lambda foreground:text_contrast(foreground,background))
                if text_contrast(chosen,background)<4.5:chosen='#000000'
                label.set_color(chosen)
                checks.append({'text':label.get_text(),'cell':[i,j],'background':background,
                               'old_text_color':old,'text_color':chosen,'contrast':text_contrast(chosen,background)})
    if checks and min(x['contrast'] for x in checks)<4.5:
        raise AssertionError('Matrix label contrast below the preview target')
    return checks


class Recolor(ast.NodeTransformer):
    def __init__(self, mapping): self.mapping=mapping; self.changed=[]
    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value.lower() in self.mapping:
            new=self.mapping[node.value.lower()]
            self.changed.append({'line':node.lineno,'old':node.value,'new':new})
            return ast.copy_location(ast.Constant(value=new),node)
        return node


def build(output: Path):
    output=output.resolve()
    if output.is_relative_to(ROOT): raise ValueError('Preview output must be outside the scientific repository')
    output.mkdir(parents=True,exist_ok=False)
    palette=json.loads((ROOT/'website/palette.json').read_text())
    manifest=json.loads((ROOT/'website/figures.json').read_text())
    csv=ROOT/'data/processed/core_figures'
    commands=[('make_figure_01_frozen.py',['--csv',str(csv/'figure_01_panel_b.csv'),'--pdf','figure_01_panel_b.pdf','--png','figure_01_panel_b.png']),
              ('make_figure_02.py',['--csv',str(csv/'figure_02_boundary_codes.csv'),'--outdir','.']),
              ('make_figure_03.py',['--csv',str(csv/'figure_03_size_scaling.csv'),'--pdf','figure_03_size_scaling.pdf','--png','figure_03_size_scaling.png']),
              ('make_figure_04.py',['--distance-csv',str(csv/'figure_04_distance_decay.csv'),'--contrast-csv',str(csv/'figure_04_conditioning_contrast.csv'),
                '--distance-pdf','figure_04_distance_decay.pdf','--distance-png','figure_04_distance_decay.png',
                '--contrast-pdf','figure_04_conditioning_contrast.pdf','--contrast-png','figure_04_conditioning_contrast.png'])]
    original_save=export_formats.save_formats
    before={}; after={}; substitutions={}; matrix_labels={}
    old_argv=sys.argv[:]
    try:
        for style in ['baseline','irises']:
            for filename,args in commands:
                mpl.rcdefaults()
                if style=='irises':
                    mpl.rcParams['axes.prop_cycle']=cycler(color=[palette['colors']['iris'],palette['colors']['leaf'],palette['colors']['terracotta']])
                def save(fig,pdf,png):
                    name=Path(pdf).stem
                    if style=='irises':matrix_labels[name]=readable_matrix_labels(fig,palette['colors']['ink'])
                    (before if style=='baseline' else after)[name]=geometry(fig)
                    if style=='irises':original_save(fig,output/Path(pdf).name,output/Path(png).name)
                export_formats.save_formats=save
                raw=(PLOTS/filename).read_text()
                tree=ast.parse(raw)
                if style=='irises':
                    recolor=Recolor(palette['figure_mapping']); tree=recolor.visit(tree); ast.fix_missing_locations(tree)
                    substitutions[filename]=recolor.changed
                sys.argv=[str(PLOTS/filename)]+args
                exec(compile(tree,str(PLOTS/filename),'exec'),{'__name__':'__main__','__file__':str(PLOTS/filename)})
                plt.close('all')
    finally:
        sys.argv=old_argv; export_formats.save_formats=original_save; plt.close('all')
    expected={p for f in manifest for p in f['panels']}
    if set(before)!=expected or set(after)!=expected: raise AssertionError('Missing panel')
    if before!=after: raise AssertionError('Non-color artist property changed')
    result={'passed':True,'panels':len(expected),'new_statistics':False,'accepted_files_overwritten':False,
            'check':'Exact equality of recorded baseline/preview artist geometry, text, data, intervals and normalizations',
            'substitutions':substitutions,'matrix_label_color_checks':matrix_labels,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(csv.glob('*.csv'))},
            'exports':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.is_file()}}
    (output/'palette_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();r=build(a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['exports','substitutions','input_sha256']},indent=2))
