#!/usr/bin/env python3
"""Independent Figure 4 record audit, using exact fractions and CSV dictionaries.

No scientific or estimator module from the repository is imported. This shares
the archived entropy records, and uses the Haar purity-transfer identity; it
does not independently regenerate the physical large-system trajectories.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import io
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import platform
import time
import zipfile

DISTANCES = (0, 1, 2, 4, 8, 16)


def mean(xs):
    return sum(xs, F(0)) / len(xs)


@lru_cache(None)
def purity(s):
    return F(1, 2**s)


@lru_cache(None)
def responses(n, sl, sm, sr):
    # E[P'_m] from the independently derived two-copy twirl, then normalize
    # linear entropy and divide by the INPUT purity of this particular state.
    dimension = 2 ** (n // 2)
    pp = F(2, 5) * (purity(sl) + purity(sr))
    linear = F(dimension, dimension - 1) * (purity(sm) - pp)
    return linear, linear / purity(sm)


def endpoint(records, pre, conditional):
    groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        if not conditional or r['ds'] == 0:
            groups[r['id']][r['d']].append(r['y'])
    result = {}
    for tid, dd in groups.items():
        n = pre[tid]['n']
        far = [mean(v) for d, v in dd.items() if d >= n // 4]
        if 0 in dd and far:
            result[tid] = mean(dd[0]) - mean(far)
    return result


def summarize(values, pre):
    cells = defaultdict(dict)
    for tid, v in values.items():
        cells[(pre[tid]['n'], pre[tid]['p'])][tid] = v
    rows = []
    for (n, p), vv in sorted(cells.items()):
        values = list(vv.values())
        rows.append({'n': n, 'p': p, 'trajectories': len(values),
                     'estimate': float(mean(values)),
                     'positive': sum(v > 0 for v in values),
                     'negative': sum(v < 0 for v in values),
                     'zero': sum(v == 0 for v in values)})
    return rows, float(mean([mean(list(v.values())) for v in cells.values()]))


def write_csv(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    bundle = args.root / 'entanglement-data.zip'
    manifest = json.loads((args.root/'data/record_bundle_manifest.json').read_text())
    actual_hash = hashlib.sha256(bundle.read_bytes()).hexdigest()
    assert actual_hash == manifest['sha256']
    source_hashes = {}
    with zipfile.ZipFile(bundle) as z:
        def load(member):
            b = z.read(member)
            source_hashes[member] = hashlib.sha256(b).hexdigest()
            return list(csv.DictReader(io.StringIO(gzip.decompress(b).decode())))
        prefix = 'checkpoint_05/data/measurement_location_intervention/'
        pre_raw = load(prefix+'stabilizer_scaling_states.csv.gz')
        raw = load(prefix+'paired_measurement_interventions.csv.gz')
    pre = {}
    max_pre_error = 0.0
    for r in pre_raw:
        tid = r['trajectory_id']
        assert tid not in pre
        n, sl, sm, sr = map(int, [r['n'], r['S_left_neighbor'], r['S_central'], r['S_right_neighbor']])
        yl, yr = responses(n, sl, sm, sr)
        max_pre_error = max(max_pre_error, abs(float(yr)-float(r['chi_relative'])), abs(float(yl)-float(r['chi_linear'])))
        assert r['protocol'] == 'z_projective' and float(r['tau']) == 10
        pre[tid] = {'n': n, 'p': float(r['p_measure']), 's': (sl, sm, sr), 'linear': yl, 'relative': yr}
    records = []
    records_by_id = defaultdict(list)
    keys = set()
    max_post_error = 0.0
    entropy_changes = Counter()
    geometry_counts = Counter()
    deterministic = 0
    for r in raw:
        tid = r['trajectory_id']; base = pre[tid]
        n, d, side = map(int, [r['n'], r['distance'], r['side']])
        key = (tid, d, side)
        assert key not in keys
        keys.add(key)
        assert n == base['n'] and float(r['p_measure']) == base['p']
        assert int(r['axis']) == 2 and side in (-1, 1)
        site = n//2-1-d if side == -1 else n//2+d
        assert 0 <= site < n
        geometry_counts[n] += 1
        sm = int(r['post_S_central'])
        sl, sr = sm-int(r['post_delta_left']), sm-int(r['post_delta_right'])
        assert sm-base['s'][1] == int(r['delta_S_central'])
        changes = tuple(a-b for a,b in zip((sl,sm,sr),base['s']))
        assert all(ds in (-1,0) for ds in changes)
        entropy_changes[changes] += 1
        yl, yr = responses(n, sl, sm, sr)
        dyl, dyr = yl-base['linear'], yr-base['relative']
        max_post_error = max(max_post_error, abs(float(dyl)-float(r['delta_chi_linear'])), abs(float(dyr)-float(r['delta_chi_relative'])))
        if int(r['measurement_random']) == 0:
            deterministic += 1
            assert changes == (0,0,0) and dyl == dyr == 0
        if changes[1] == 0:
            assert dyr <= 0
            # Exact equality iff both neighboring purities are unchanged.
            assert (dyr == 0) == (changes[0] == 0 and changes[2] == 0)
        rr = {'id':tid, 'n':n, 'p':base['p'], 'd':d, 'side':side, 'ds':changes[1], 'y':dyr}
        records.append(rr); records_by_id[tid].append(rr)
    assert max(max_pre_error, max_post_error) < 1e-12
    assert len(raw) == 75600 and len(pre) == 5400
    for tid, rr in records_by_id.items():
        n=pre[tid]['n']
        expected={(d,s) for d in (0,1,2,4,8,16,32,64) for s in (-1,1) if d<n//2}
        assert {(r['d'],r['side']) for r in rr} == expected

    original_uncond = endpoint(records, pre, False)
    original_cond = endpoint(records, pre, True)
    strict, common = {}, {}
    strict_pairs = common_sides = 0
    strict_side_positive = strict_side_negative = 0
    asymmetric_original = disjoint_original = 0
    positive_examples = []
    support_rows = []
    profiles = {'original': defaultdict(dict), 'common': defaultdict(dict)}
    for tid, rr in records_by_id.items():
        lookup = {(r['d'], r['side']):r for r in rr}
        n=pre[tid]['n']
        keep = [s for s in (-1,1) if lookup[(0,s)]['ds']==lookup[(n//4,s)]['ds']==0]
        if keep:
            pair_y = [lookup[(0,s)]['y']-lookup[(n//4,s)]['y'] for s in keep]
            strict[tid] = mean(pair_y); strict_pairs += len(keep)
            strict_side_positive += sum(y > 0 for y in pair_y)
            strict_side_negative += sum(y < 0 for y in pair_y)
            for s,y in zip(keep,pair_y):
                if y > 0:
                    positive_examples.append({'trajectory_id':tid,'side':s,'near_distance':0,
                                              'far_distance':n//4,'near_change':float(lookup[(0,s)]['y']),
                                              'far_change':float(lookup[(n//4,s)]['y']),
                                              'near_minus_far':float(y),'central_entropy_change_both':0})
        if tid in original_cond:
            sides_n={s for s in (-1,1) if lookup[(0,s)]['ds']==0}
            sides_f={s for s in (-1,1) if lookup[(n//4,s)]['ds']==0}
            asymmetric_original += sides_n != sides_f
            disjoint_original += not bool(sides_n & sides_f)
        common_keep=[s for s in (-1,1) if all(lookup[(d,s)]['ds']==0 for d in DISTANCES)]
        if common_keep:
            common[tid] = common_keep
            common_sides += len(common_keep)
        for d in DISTANCES:
            values=[lookup[(d,s)]['y'] for s in (-1,1) if lookup[(d,s)]['ds']==0]
            if values: profiles['original'][d][tid] = mean(values)
            if common_keep:
                profiles['common'][d][tid] = mean([lookup[(d,s)]['y'] for s in common_keep])

    endpoint_rows=[]; endpoints={}
    for label,values in [('original_unconditional', original_uncond),('original_conditional', original_cond),('strict_same_side',strict)]:
        cellrows, pooled = summarize(values,pre)
        endpoint_rows.extend([{'estimand':label, **r} for r in cellrows])
        endpoints[label]={'estimate':pooled,'trajectories':len(values),'all_cell_estimates_negative':all(r['estimate']<0 for r in cellrows)}
    profile_rows=[]; profile_means={}
    for label,dd in profiles.items():
        profile_means[label]={}
        for d,values in sorted(dd.items()):
            cellrows,pooled=summarize(values,pre)
            profile_means[label][d]=pooled
            profile_rows.append({'population':label,'distance':d,'estimate':pooled,'trajectories':len(values),
                                 'nonzero_trajectories':sum(v != 0 for v in values.values())})
            support_rows.extend([{'population':label,'distance':d,**r} for r in cellrows])
    canon=list(csv.DictReader((args.root/'data/processed/core_figures/figure_04_conditioning_contrast.csv').open()))
    assert abs(endpoints['original_unconditional']['estimate']-float(canon[0]['estimate'])) < 1e-12
    assert abs(endpoints['original_conditional']['estimate']-float(canon[1]['estimate'])) < 1e-12
    for r in csv.DictReader((args.root/'data/processed/core_figures/figure_04_distance_decay.csv').open()):
        assert abs(profile_means['original'][int(r['distance'])]-float(r['estimate'])) < 1e-12
    assert strict_pairs == 7945 and len(strict) == 4786
    assert common_sides == 6008 and len(common) == 4025
    write_csv(args.output/'figure4_endpoints_by_cell.csv',endpoint_rows)
    write_csv(args.output/'figure4_profiles.csv',profile_rows)
    write_csv(args.output/'figure4_support_by_cell.csv',support_rows)
    if positive_examples:
        write_csv(args.output/'figure4_positive_individual_pairs.csv',positive_examples)
    summary={'passed':True,'source_sha256':source_hashes,'bundle_sha256':actual_hash,
             'source_dependency':'Original entropy and intervention records; no raw tableau simulation replay',
             'code_dependency':'Python standard library only; exact Fraction arithmetic; no original module imports',
             'rows':len(raw),'pre_states':len(pre),'geometry_counts':dict(geometry_counts),
             'deterministic_interventions':deterministic,'max_pre_response_error':max_pre_error,
             'max_post_response_error':max_post_error,
             'entropy_change_counts':{str(k):v for k,v in sorted(entropy_changes.items())},
             'endpoints':endpoints,'strict_side_pairs':strict_pairs,
             'strict_side_pair_positive_effects':strict_side_positive,'strict_side_pair_negative_effects':strict_side_negative,
             'original_conditional_different_side_sets':asymmetric_original,
             'original_conditional_disjoint_side_sets':disjoint_original,
             'common_side_pre_states':common_sides,'common_pre_states':len(common),
             'common_magnitude_ratios':{str(d):abs(y/profile_means['common'][0]) for d,y in profile_means['common'].items()},
             'uncertainty_scope':'No bootstrap is regenerated by this independent exact record calculation',
             'python':platform.python_version(),'elapsed_seconds':time.monotonic()-start}
    (args.output/'figure4_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
