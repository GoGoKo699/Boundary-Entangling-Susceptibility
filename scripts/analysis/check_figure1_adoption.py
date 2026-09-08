#!/usr/bin/env python3
"""Check current Figure 1 provenance, protected inputs, and optional full replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
FIGURE3_SOURCE='scripts/figures/make_figure_03.py'
FIGURE3_OUTPUTS={
    'figures/core/figure_03_size_scaling.pdf',
    'figures/core/figure_03_size_scaling.png',
    'figures/core_svg/figure_03_size_scaling.svg',
}
FIGURE3_OLD_LABEL=r'$\beta_n=\partial\chi_{\rm rel}/\partial(p/0.02)$'
FIGURE3_NEW_LABEL=r'within-spectrum $\beta_n$ (per $\Delta p=0.02$)'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def check_tables(current, historical):
    required=['run','family','family_label','family_order','estimate','ci_low','ci_high','common_cells','response','p_low','p_high']
    if current.columns.tolist()!=required or historical.columns.tolist()!=required or len(current)!=10:
        raise ValueError('Wrong table schema or row count')
    fixed=[c for c in required if c not in ['ci_low','ci_high']]
    if not current[fixed].equals(historical[fixed]):
        raise ValueError('Only Figure 1 interval columns may change')
    values=current[['estimate','ci_low','ci_high']].astype(float)
    if not np.isfinite(values.to_numpy()).all() or not (values.ci_low<=values.estimate).all() or not (values.estimate<=values.ci_high).all():
        raise ValueError('Invalid interval')

def figure3_label_successors(root, palette):
    """Allow exactly one ylabel replacement after the unchanged palette record."""
    path=root/'provenance/FIGURE3_LABEL_2026-09-08.json'
    if not path.exists():return {}
    record=json.loads(path.read_text())
    if (record['status']!='adopted' or record['scientific_values_changed'] is not False
            or record['layout_changed'] is not False
            or record['old_label']!=FIGURE3_OLD_LABEL or record['new_label']!=FIGURE3_NEW_LABEL):
        raise ValueError('Invalid Figure 3 label-only specification')
    rows=record['changed_files']
    if len(rows)!=4 or {r['path'] for r in rows}!=FIGURE3_OUTPUTS|{FIGURE3_SOURCE}:
        raise ValueError('Label exceptions must cover only Figure 3 source and three exports')
    locked={r['path']:r['sha256'] for r in palette['changed_files']}
    locked.update(palette['unchanged_scientific_inputs'])
    for entry in rows:
        name=entry['path']
        if entry['before_sha256']!=locked[name]:
            raise ValueError('Label change does not follow the palette baseline: '+name)
        if sha(root/name)!=entry['sha256']:
            raise ValueError('Label output mismatch: '+name)
    # The predecessor source is recovered by exactly the approved substitution.
    # Even updating the successor hash cannot authorize numerical/layout edits.
    source=(root/FIGURE3_SOURCE).read_bytes()
    new=FIGURE3_NEW_LABEL.encode();old=FIGURE3_OLD_LABEL.encode()
    if source.count(new)!=1 or old in source:
        raise ValueError('Figure 3 must contain exactly the approved new ylabel')
    if hashlib.sha256(source.replace(new,old)).hexdigest()!=locked[FIGURE3_SOURCE]:
        raise ValueError('Figure 3 source changes more than the approved ylabel')
    predecessors=record['unchanged_predecessor_records']
    if set(predecessors)!={'provenance/FIGURE1_ADOPTION_2026-09-08.json',
                          'provenance/FIGURE_PALETTE_2026-09-08.json'}:
        raise ValueError('Wrong Figure 3 predecessor record set')
    for name,digest in predecessors.items():
        if sha(root/name)!=digest:raise ValueError('Historical adoption record changed: '+name)
    return {r['path']:r for r in rows}

def palette_successors(root):
    path=root/'provenance/FIGURE_PALETTE_2026-09-08.json'
    if not path.exists():return {}
    palette=json.loads(path.read_text())
    if palette['status']!='adopted' or palette['scientific_values_changed'] is not False:
        raise ValueError('Invalid figure palette record')
    allowed={str(p.relative_to(root)) for directory in ['figures/core','figures/core_svg']
             for p in (root/directory).iterdir() if p.suffix in {'.pdf','.png','.svg'}}
    allowed.add('scripts/figures/export_formats.py')
    rows=palette['changed_files']
    if len(rows)!=19 or {r['path'] for r in rows}!=allowed:
        raise ValueError('Palette exceptions must cover only 18 panels and their exporter')
    labels=figure3_label_successors(root,palette)
    for entry in rows:
        digest=labels.get(entry['path'],entry)['sha256']
        if sha(root/entry['path'])!=digest:
            raise ValueError('Palette output mismatch: '+entry['path'])
    for key in ['unchanged_scientific_inputs','supporting_files']:
        for name,digest in palette[key].items():
            if name in labels:digest=labels[name]['sha256']
            if sha(root/name)!=digest:raise ValueError('Palette source mismatch: '+name)
    # Preserve the original before-hash so the Figure 1 -> palette -> label
    # chain is checked below, rather than replacing it with a fresh exception.
    return {r['path']:{**r,'sha256':labels.get(r['path'],r)['sha256']} for r in rows}

def verify(root=ROOT, resamples=None):
    record=json.loads((root/'provenance/FIGURE1_ADOPTION_2026-09-08.json').read_text())
    if record['status']!='adopted' or record['primary_pool']!='eligible_union' or record['bootstrap_draws']!=50000:
        raise ValueError('Wrong adoption specification')
    successors=palette_successors(root)
    def expected(path, original):
        successor=successors.get(path)
        if successor is None:return original
        if successor['before_sha256']!=original:
            raise ValueError('Palette does not follow the locked baseline: '+path)
        return successor['sha256']
    for row in record['historical_files']+record['protected_other_files']+record['changed_panel_files']:
        if sha(root/row['path'])!=expected(row['path'],row['sha256']):raise ValueError('File hash mismatch: '+row['path'])
    for path,digest in record['locked_source_sha256'].items():
        if sha(root/path)!=expected(path,digest):raise ValueError('Locked source changed: '+path)
    current=root/'data/processed/core_figures/figure_01_panel_b.csv'
    historical=root/'results/historical_figure1/figure_01_panel_b.csv'
    check_tables(pd.read_csv(current,dtype=str),pd.read_csv(historical,dtype=str))
    if sha(current)!=record['canonical_table_sha256']:raise ValueError('Current table mismatch')
    summary={'passed':True,'adopted':True,'historical_resamples_recovered':False,'other_panel_data_unchanged':True,'palette':'Irises' if successors else 'original',
             'figure3_label_successor':(root/'provenance/FIGURE3_LABEL_2026-09-08.json').exists(),
             'full_resample_output_checked':resamples is not None}
    if resamples is not None:
        resamples=Path(resamples)
        expected=json.loads((root/record['expected_replay_hashes']).read_text())
        for path,digest in expected.items():
            if sha(resamples/path)!=digest:raise ValueError('Replayed output differs: '+path)
        if (resamples/'figure_01_candidate_intervals.csv').read_bytes()!=current.read_bytes():
            raise ValueError('Regenerated intervals do not equal the current figure data')
        tab=pd.read_csv(current)
        for row in tab.itertuples(index=False):
            path=resamples/'resamples'/f'eligible_union__{row.run}__{row.family}.npz'
            with np.load(path,allow_pickle=False) as data:
                if len(data['bootstrap'])!=50000:raise ValueError('Wrong replicate count')
                low,high=np.quantile(data['bootstrap'],[.025,.975],method='linear')
                if max(abs(low-row.ci_low),abs(high-row.ci_high))>2e-15:
                    raise ValueError('Current interval is not the primary resample percentile')
        summary.update(expected_output_files=len(expected),primary_intervals_checked=10)
    return summary

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--resamples',type=Path)
    args=ap.parse_args()
    print(json.dumps(verify(resamples=args.resamples),indent=2))
