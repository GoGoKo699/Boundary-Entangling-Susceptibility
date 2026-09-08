#!/usr/bin/env python3
"""Audit existing Checkpoint04 extensions directly from archived row purities.

No repository estimator imports and no new bootstrap. Archived CI support is
reported as archived only. This also tests selected compact decomposition tables.
"""
import csv
from collections import defaultdict
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import time
import zipfile

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audits/full-sanity-01/results'
COEFF={'haar_or_clifford_2design':(.4,0,0,.4),'cartan_xy_pi8':(1/3,1/4,-1/12,1/3),'cartan_xx_pi4':(4/9,1/9,-2/9,4/9)}
def mean(xs):
    xs=list(xs);return math.fsum(xs)/len(xs)
def write(path,rs):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def main():
    start=time.perf_counter();sources={};points=[];gates=[];discrepancies=[]
    selected=list(csv.DictReader((ROOT/'studies/checkpoint_04/results/intervention_cross_architecture.csv').open()))
    decomposition=list(csv.DictReader((ROOT/'studies/checkpoint_04/results/response_stencil_decomposition.csv').open()))
    with zipfile.ZipFile(ROOT/'entanglement-data.zip') as z:
        def read(name):
            b=z.read(name);sources[name]=hashlib.sha256(b).hexdigest()
            if name.endswith('.gz'):b=gzip.decompress(b)
            return list(csv.DictReader(io.StringIO(b.decode())))
        archived=read('checkpoint_04/analysis/consolidated/intervention_cross_architecture.csv')
        archived_gates=read('checkpoint_04/analysis/consolidated/gate_space_universality_bootstrap.csv')
        for folder,run,variant in [('primary_rank4','primary_rank4','equalized_rank4'),('independent_seed_rank4','independent_rank4','equalized_rank4'),('posthoc_rank2','posthoc_rank2','equalized_rank2')]:
            raw=read('checkpoint_04/data/intervention/'+folder+'/state_response_rows.csv.gz')
            grouped=defaultdict(list)
            for r in raw:
                if r['split']=='confirmatory' and r['variant']==variant and float(r['p_measure']) in [.08,.24]:
                    grouped[(r['family'],int(r['n']),int(float(r['tau'])),float(r['p_measure']))].append(r)
            for family in sorted({key[0] for key in grouped}):
                cells=sorted({(n,t) for f,n,t,p in grouped if f==family and (f,n,t,.08) in grouped and (f,n,t,.24) in grouped})
                shifts=[]
                for n,t in cells:
                    d={key:mean(float(r[key]) for r in grouped[(family,n,t,.24)])-mean(float(r[key]) for r in grouped[(family,n,t,.08)]) for key in ['P_L','P_A','P_Lb','P_R']}
                    fac=2**(n//2)/(2**(n//2)-1)
                    shifts.append((fac,d))
                A=mean(d['P_L']+d['P_R'] for fac,d in shifts);B=mean(d['P_Lb'] for fac,d in shifts)
                WA=mean(fac*(d['P_L']+d['P_R']) for fac,d in shifts);WB=mean(fac*d['P_Lb'] for fac,d in shifts)
                target=next(r for r in archived_gates if r['run']==run and r['family']==family and r['pair_label']=='0.08-0.24')
                err=max(abs(A-float(target['delta_neighbor_sum'])),abs(B-float(target['delta_noncontiguous'])),abs(4*A-5*B-float(target['gate_space_margin'])))
                assert err<2e-12
                gates.append(dict(run=run,family=family,cells=len(cells),A=A,B=B,margin=4*A-5*B,D_weighted_A=WA,D_weighted_B=WB,D_weighted_margin=4*WA-5*WB,archived_point_error=err,archived_noncontig_ci_low=float(target['noncontig_ci_low']),archived_margin_ci_low=float(target['margin_ci_low']),archived_joint_claim=target['all_local_dressed_gates_suppressed']))
                for probe,coeff in COEFF.items():
                    contributions=[mean(fac*((1-coeff[1])*d['P_A'] if j==1 else -coeff[j]*d[key]) for fac,d in shifts) for j,key in enumerate(['P_L','P_A','P_Lb','P_R'])]
                    reconstructed=math.fsum(contributions)
                    direct=mean(mean(float(r['probe_'+probe+'_delta_linear_norm']) for r in grouped[(family,n,t,.24)])-mean(float(r['probe_'+probe+'_delta_linear_norm']) for r in grouped[(family,n,t,.08)]) for n,t in cells)
                    assert abs(reconstructed-direct)<1e-12
                    expected=next(r for r in archived if r['run']==run and r['family']==family and r['probe']==probe)
                    assert abs(direct-float(expected['estimate']))<1e-12
                    small=next((r for r in selected if r['run']==folder and r['family']==family and r['probe']==probe),None)
                    old=next((r for r in decomposition if run=='primary_rank4' and r['family']==family and r['probe']==probe),None)
                    points.append(dict(run=run,family=family,probe=probe,cells=len(cells),direct=direct,reconstructed=reconstructed,archived_estimate=float(expected['estimate']),compact_estimate=float(small['estimate']) if small else '',compact_error=abs(direct-float(small['estimate'])) if small else '',compact_decomposition=float(old['reconstruction']) if old else '',compact_decomposition_error=abs(reconstructed-float(old['reconstruction'])) if old else ''))
                    if small and abs(direct-float(small['estimate']))>2e-11:discrepancies.append(dict(table='intervention_cross_architecture.csv',run=run,family=family,probe=probe,recomputed=direct,stored=float(small['estimate'])))
                    if old and abs(reconstructed-float(old['reconstruction']))>2e-11:discrepancies.append(dict(table='response_stencil_decomposition.csv',run=run,family=family,probe=probe,recomputed=reconstructed,stored=float(old['reconstruction'])))
    write(OUT/'figure1_extension_points.csv',points);write(OUT/'figure1_extension_gate_criteria.csv',gates)
    compact=[]
    for line,row in enumerate(selected,2):
        run='independent_rank4' if row['run']=='independent_seed_rank4' else row['run']
        fresh=next(r for r in points if r['run']==run and r['family']==row['family'] and r['probe']==row['probe'])
        compact.append(dict(file='studies/checkpoint_04/results/intervention_cross_architecture.csv',line=line,run=row['run'],family=row['family'],probe=row['probe'],stored=float(row['estimate']),record_reconstruction=fresh['direct'],difference=float(row['estimate'])-fresh['direct']))
    write(OUT/'figure1_compact_table_discrepancies.csv',compact)
    result={'runtime_s':time.perf_counter()-start,'archive_response_point_checks':len(points),'all_archive_points_and_exact_decompositions_pass':True,'compact_table_discrepancies':discrepancies,'source_sha256':sources,'intervals':'Archived interval endpoints inspected, no new extension bootstrap performed.'}
    (OUT/'figure1_extension_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
