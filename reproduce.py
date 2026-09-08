#!/usr/bin/env python3
"""Rebuild the six approved panels; validate all 18 PDF/PNG/SVG outputs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
STEMS = ['figure_01_panel_b','figure_02_response_matrix','figure_02_redistribution_matrix',
         'figure_03_size_scaling','figure_04_distance_decay','figure_04_conditioning_contrast']

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core-figures', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/'reproduced_figures')
    args = parser.parse_args()
    if not args.core_figures:
        parser.error('select --core-figures')
    # A fresh staging directory prevents stale files from making an incomplete run pass.
    # Existing user directories are never recursively deleted.
    with tempfile.TemporaryDirectory(prefix='boundary-figures-') as temporary:
        out=Path(temporary)
        data=ROOT/'data/processed/core_figures'
        scripts=ROOT/'scripts/figures'
        commands=[
            ['make_figure_01_frozen.py','--csv',data/'figure_01_panel_b.csv','--pdf',out/(STEMS[0]+'.pdf'),'--png',out/(STEMS[0]+'.png')],
            ['make_figure_02.py','--csv',data/'figure_02_boundary_codes.csv','--outdir',out],
            ['make_figure_03.py','--csv',data/'figure_03_size_scaling.csv','--pdf',out/(STEMS[3]+'.pdf'),'--png',out/(STEMS[3]+'.png')],
            ['make_figure_04.py','--distance-csv',data/'figure_04_distance_decay.csv','--contrast-csv',data/'figure_04_conditioning_contrast.csv',
             '--distance-pdf',out/(STEMS[4]+'.pdf'),'--distance-png',out/(STEMS[4]+'.png'),
             '--contrast-pdf',out/(STEMS[5]+'.pdf'),'--contrast-png',out/(STEMS[5]+'.png')],
        ]
        for name,*rest in commands:
            subprocess.run([sys.executable,str(scripts/name),*map(str,rest)],check=True)
        expected={stem+suffix for stem in STEMS for suffix in ['.pdf','.png','.svg']}
        if {p.name for p in out.iterdir()} != expected:
            raise RuntimeError('The staging output set is not exactly six PDF/PNG/SVG triples')
        for name in sorted(expected):
            path=out/name
            content=path.read_bytes()
            if len(content)<500:raise RuntimeError(f'Unexpectedly small figure: {name}')
            if path.suffix=='.pdf' and not content.startswith(b'%PDF-'):raise RuntimeError(name)
            if path.suffix=='.png' and not content.startswith(b'\x89PNG\r\n\x1a\n'):raise RuntimeError(name)
            if path.suffix=='.svg':ET.fromstring(content)
        args.output.mkdir(parents=True,exist_ok=True)
        for name in sorted(expected):shutil.copy2(out/name,args.output/name)
        (args.output/'EXPORT_STATUS.json').write_text(json.dumps({'figure_files':18,'complete':True,
            'baseline':'approved 2026-09-08: Irises colors only; adopted Figure 1 intervals and no-fit Figure 4 unchanged',
            'interpretation':'observed distance means and original intervals; no fitted decay law'},indent=2)+'\n')
    print(f'Validated 18 figure files in {args.output}')

if __name__=='__main__':main()
