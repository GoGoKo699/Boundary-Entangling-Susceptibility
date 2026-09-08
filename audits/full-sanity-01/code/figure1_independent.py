#!/usr/bin/env python3
"""Independent Figure 1 record audit, using stdlib CSV and original spectra.

No repository Python imports. Shares the immutable records and the observable
definition; it is not a new physical simulation. Reconstructs references from
discovery eigenvalues, masks from full physical spectra, and responses from
neighboring purities rather than the stored response column.
"""
import csv
from collections import defaultdict, Counter
from fractions import Fraction
import gzip
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import platform
import time
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'audits/full-sanity-01/results'
FAMILIES = ['haar_z', 'clifford_z', 'floquet_cartan_z', 'haar_random_pauli', 'haar_weak_z_eta06']

def avg(x):
    x = list(x)
    return math.fsum(x) / len(x)

def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def exact_survival(patterns):
    """Inclusion-exclusion computed directly from sets of trajectory IDs."""
    N = len(patterns)
    columns = len(patterns[0])
    p = Fraction(0)
    for k in range(columns + 1):
        for subset in itertools.combinations(range(columns), k):
            avoid = sum(not any(pattern[j] for j in subset) for pattern in patterns)
            p += (-1)**k * Fraction(avoid, N)**N
    return p

def main():
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = {}
    checks = defaultdict(float)
    split_counts = {}; degeneracy = []; ref_rows = []; cell_rows = []; contrast_rows = []; prob_rows = []
    all_selected = {}; all_original = {}; seed_rows = []
    with zipfile.ZipFile(ROOT / 'entanglement-data.zip') as z:
        def read(name):
            b = z.read(name); sources[name] = hashlib.sha256(b).hexdigest(); return b
        def rows(name):
            b = read(name)
            if name.endswith('.gz'): b = gzip.decompress(b)
            return list(csv.DictReader(io.StringIO(b.decode())))
        def array(name):
            with np.load(io.BytesIO(read(name)), allow_pickle=False) as f:
                assert f.files == ['spectra']; return f['spectra'].copy()
        for run, folder, split, ntraj, base in [('primary','primary_rank4',12,24,2026081804), ('independent','independent_seed_rank4',8,16,2026081805)]:
            pre = 'checkpoint_04/data/intervention/' + folder + '/'
            data = rows(pre + 'state_response_rows.csv.gz')
            dm = rows(pre + 'discovery_spectrum_metadata.csv.gz'); ds = array(pre + 'discovery_spectra.npz')
            pm = rows(pre + 'physical_spectrum_metadata.csv.gz'); ps = array(pre + 'physical_spectra.npz')
            refs = json.loads(read(pre + 'equalization_reference_spectra.json'))
            original = {r['state_id']: r for r in data if r['variant'] == 'original'}
            equalized = {r['state_id']: r for r in data if r['variant'] == 'equalized_rank4'}
            assert len(original) + len(equalized) == len(data)
            assert len(pm) == len(ps) == len(original) and len(dm) == len(ds)
            for meta in pm:
                assert meta['split'] == ('discovery' if int(meta['trajectory_index']) < split else 'confirmatory')
                assert 0 <= int(meta['trajectory_index']) < ntraj
            assert all(0 <= int(r['trajectory_index']) < split for r in dm)
            assert len(dm) == split * 5 * 3 * 3 * 2
            grouped = defaultdict(list)
            physical_by_key = {(r['family'],r['n'],r['p_measure'],r['trajectory_index'],r['tau']): (r,lam) for r,lam in zip(pm,ps)}
            for meta, lam in zip(dm,ds):
                assert np.count_nonzero(lam > 1e-12) == int(meta['rank_1e12'])
                key = tuple(meta[k] for k in ['family','n','p_measure','trajectory_index','tau'])
                _, physical = physical_by_key[key]
                checks['discovery_vs_regenerated_physical_spectrum_error'] = max(checks['discovery_vs_regenerated_physical_spectrum_error'],float(np.max(abs(physical-lam))))
                if int(meta['rank_1e12']) >= 4:
                    grouped[f"{meta['family']}|n{meta['n']}|tau{float(meta['tau']):g}"].append((meta,lam))
            assert set(grouped) == set(refs)
            for key, group in sorted(grouped.items()):
                target = [avg(lam[j] / math.fsum(lam[:4]) for _,lam in group) for j in range(4)]
                total = math.fsum(target); target = [v / total for v in target]
                err = max(abs(a-b) for a,b in zip(target,refs[key])); checks['reference_reconstruction_error'] = max(checks['reference_reconstruction_error'],err)
                counts = dict(sorted(Counter(float(meta['p_measure']) for meta,_ in group).items()))
                ref_rows.append(dict(run=run,cell=key,discovery_rows=len(group),counts_by_p=json.dumps(counts),reference=json.dumps(target),max_error=err))
            degeneracy_counts = defaultdict(Counter)
            for meta, lam in zip(pm,ps):
                r = original[meta['state_id']]; k = int(meta['rank_1e12']); n = int(meta['n'])
                assert np.count_nonzero(lam > 1e-12) == k
                assert (r['state_id'] in equalized) == (k >= 4)
                checks['physical_purity_from_spectrum_error'] = max(checks['physical_purity_from_spectrum_error'], abs(math.fsum(lam*lam)-float(r['pre_purity'])))
                checks['spectrum_normalization_error'] = max(checks['spectrum_normalization_error'], abs(math.fsum(lam)-1))
                if meta['split']=='confirmatory' and float(meta['p_measure']) in [.08,.24] and k >= 4:
                    counts = degeneracy_counts[meta['family']]; counts['eligible'] += 1
                    counts['degenerate_selected_gap_1e-10'] += int(np.min(lam[:3]-lam[1:4]) < 1e-10)
                    counts['rank4_boundary_gap_1e-10'] += int(k > 4 and abs(lam[3]-lam[4]) < 1e-10)
                    counts['nonflat_1e-10'] += int(np.max(lam[:k])-np.min(lam[:k]) > 1e-10)
                for v in [r] + ([equalized[r['state_id']]] if k>=4 else []):
                    P=float(v['pre_purity']); PL=float(v['P_L']); PR=float(v['P_R']); D=2**(n//2)
                    y = D/(D-1)*(1-0.4*(PL+PR)/P)
                    checks['stored_response_vs_neighbor_purities_error'] = max(checks['stored_response_vs_neighbor_purities_error'],abs(y-float(v['probe_haar_or_clifford_2design_delta_linear_norm'])/P))
                    if v['variant']=='equalized_rank4':
                        ref=refs[f"{meta['family']}|n{n}|tau{float(meta['tau']):g}"]
                        checks['equalized_reference_purity_error']=max(checks['equalized_reference_purity_error'],abs(P-math.fsum(t*t for t in ref)))
                        v['independent_response'] = y
            degeneracy += [dict(run=run,family=f,**dict(c)) for f,c in sorted(degeneracy_counts.items())]
            split_counts[run] = {'physical_states':len(pm),'discovery_states':len(dm),'equalized_states':len(equalized),'confirmation_cut':split}
            all_selected[run] = [r for r in equalized.values() if r['split']=='confirmatory' and float(r['p_measure']) in [.08,.24]]
            all_original[run] = [r for r in original.values() if r['split']=='confirmatory' and float(r['p_measure']) in [.08,.24]]
            for family,n,p,tr in itertools.product(FAMILIES,[10,12,14],[.08,.16,.24],range(ntraj)):
                tup = ('checkpoint04_trajectory',base,family,n,p,tr)
                seed=int.from_bytes(hashlib.blake2b(repr(tup).encode(),digest_size=8).digest(),'little') & 0xffffffff
                seed_rows.append(dict(run=run,family=family,n=n,p=p,tr=tr,seed=seed))
    assert len({r['seed'] for r in seed_rows})==len(seed_rows)
    canonical=list(csv.DictReader((ROOT/'data/processed/core_figures/figure_01_panel_b.csv').open()))
    for family in FAMILIES:
        run_cells={}
        for run in all_selected:
            g=defaultdict(list)
            for r in all_selected[run]:
                if r['family']==family:g[(int(r['n']),int(float(r['tau'])),float(r['p_measure']))].append(r)
            run_cells[run]=g
        supports=[{(n,t) for n,t,p in g if (n,t,.08) in g and (n,t,.24) in g} for g in run_cells.values()]
        common=set.intersection(*supports)
        assert len(common)==(4 if family=='clifford_z' else 6)
        for run,g in run_cells.items():
            deltas=[]
            for n,tau in sorted(common):
                means={p:avg(r['independent_response'] for r in g[(n,tau,p)]) for p in [.08,.24]}
                deltas.append(means[.24]-means[.08])
                for p in [.08,.24]:
                    cell_rows.append(dict(run=run,family=family,n=n,tau=tau,p=p,eligible=len(g[(n,tau,p)]),mean=means[p],contrast=means[.24]-means[.08]))
            estimate=avg(deltas); target=next(r for r in canonical if r['run']==run and r['family']==family)
            checks['canonical_point_error']=max(checks['canonical_point_error'],abs(estimate-float(target['estimate'])))
            contrast_rows.append(dict(run=run,family=family,cells=len(common),estimate=estimate,canonical=float(target['estimate']),minimum_cell_contrast=min(deltas),maximum_cell_contrast=max(deltas)))
            for pool in ['eligible_union','all_confirmatory']:
                survival=Fraction(1); clusters=0; eligible_rows=0
                for n in sorted({n for n,t in common}):
                    times=sorted(t for nn,t in common if nn==n)
                    for p in [.08,.24]:
                        by_time={t:{int(r['trajectory_index']) for r in g[(n,t,p)]} for t in times}
                        if pool=='eligible_union':ids=set.union(*by_time.values())
                        else:ids={int(r['trajectory_index']) for r in all_original[run] if r['family']==family and int(r['n'])==n and float(r['p_measure'])==p}
                        patterns=[tuple(i in by_time[t] for t in times) for i in sorted(ids)]
                        survival*=exact_survival(patterns);clusters+=len(ids);eligible_rows+=sum(sum(p) for p in patterns)
                prob_rows.append(dict(run=run,family=family,pool=pool,clusters=clusters,eligible_rows=eligible_rows,exact_rejection_probability=float(1-survival)))
    for name,val in checks.items(): assert val < 2e-11,(name,val)
    write_csv(OUT/'figure1_independent_cells.csv',cell_rows)
    write_csv(OUT/'figure1_independent_points.csv',contrast_rows)
    write_csv(OUT/'figure1_independent_references.csv',ref_rows)
    write_csv(OUT/'figure1_independent_rejection.csv',prob_rows)
    write_csv(OUT/'figure1_independent_degeneracy.csv',degeneracy)
    result={'passed':True,'checks':dict(checks),'split_counts':split_counts,'trajectory_seed_count':len(seed_rows),'seed_collisions':0,'source_sha256':sources,'runtime_s':time.perf_counter()-started,'environment':{'python':platform.python_version(),'numpy':np.__version__},'independence':'No repository code imports; shares original records and response definition. Discovery and full spectrum records inspected, not fresh state generation.'}
    (OUT/'figure1_independent_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
