#!/usr/bin/env python3
"""Bounded generation replay and seed collision check; see SIMULATOR_REPLAY_PLAN.md."""
from pathlib import Path
import hashlib, io, json, sys, time, zipfile
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'studies/checkpoint_05/scripts'))
import stabilizer_tableau as tab


def main():
    started=time.perf_counter()
    seeds={};collisions=[];cases=[]
    with zipfile.ZipFile(ROOT/'entanglement-data.zip') as z:
        masks=np.load(io.BytesIO(z.read('checkpoint_05/data/two_qubit_clifford_symplectic_maps.npz')))['masks']
        interventions=pd.read_csv(io.BytesIO(z.read('checkpoint_05/data/measurement_location_intervention/paired_measurement_interventions.csv.gz')),compression='gzip')
        designs=[('primary_scaling',2026082301),('independent_replication',2026082401),('measurement_location_intervention',2026082501)]
        for label,base in designs:
            data=pd.read_csv(io.BytesIO(z.read(f'checkpoint_05/data/{label}/stabilizer_scaling_states.csv.gz')),compression='gzip')
            for row in data.drop_duplicates('trajectory_id').itertuples(index=False):
                args=('checkpoint05',label,base,str(row.protocol),int(row.n),float(row.p_measure),int(row.trajectory_index))
                seed=int.from_bytes(hashlib.blake2b(repr(args).encode(),digest_size=8).digest(),'little')
                if seed in seeds:collisions.append([row.trajectory_id,seeds[seed]])
                seeds[seed]=row.trajectory_id
            selections=[]
            for (protocol,n),cell in data.groupby(['protocol','n']):
                last=int(cell.trajectory_index.max())
                points=[(.20,0),(.34,last)] if label=='primary_scaling' else [(.26,last)]
                for p,tr in points:
                    rows=cell[np.isclose(cell.p_measure,p)&cell.trajectory_index.eq(tr)].sort_values('tau')
                    selections.append((str(protocol),int(n),p,tr,rows))
            for protocol,n,p,tr,rows in selections:
                assert len(rows)>0
                args=('checkpoint05',label,base,protocol,n,p,tr)
                seed=int.from_bytes(hashlib.blake2b(repr(args).encode(),digest_size=8).digest(),'little')
                assert int(tab.stable_seed_u64(*args))==seed
                snaps,meas,rnd,cut=tab.simulate_trajectory_snapshots(n,p,rows.cycle.to_numpy(np.int64),masks,np.uint64(seed),0 if protocol=='z_projective' else 1)
                max_error=0.;comparisons=0
                for j,(row,snap) in enumerate(zip(rows.itertuples(index=False),snaps)):
                    fields=['S_left_neighbor','S_central','S_right_neighbor','P_central','P_left_neighbor','P_right_neighbor','chi_linear','chi_relative','delta_left','delta_right']
                    c=tab.central_observables(snap,n)
                    expected=np.array([getattr(row,k) for k in fields])
                    max_error=max(max_error,float(np.max(abs(c-expected))))
                    assert max_error<2e-12,(label,protocol,n,p,tr,'central',c,expected)
                    for field,got in [('measurements_to_probe',meas[j]),('random_measurements_to_probe',rnd[j]),('cut_measurements_to_probe',cut[j])]:
                        assert getattr(row,field)==got,(label,protocol,n,p,tr,field)
                    halfwidths=sorted(int(k.split('_')[1][1:]) for k in rows.columns if k.startswith('window_h') and k.endswith('_entropy') and '_left_' not in k and '_right_' not in k)
                    features=tab.window_entropy_features(snap,n,np.array(halfwidths,dtype=np.int64))
                    for h,feature in zip(halfwidths,features):
                        for k,v in zip(['entropy','local_stabilizers','left_entropy','right_entropy'],feature):
                            assert getattr(row,f'window_h{h}_{k}')==v
                            comparisons+=1
                    if np.isfinite(row.I3_quarters):
                        tmi=tab.tripartite_information_quarters(snap,n)
                        want=np.array([getattr(row,k) for k in ['S_A','S_B','S_C','S_AB','S_AC','S_BC','S_ABC','I3_quarters']])
                        assert np.array_equal(tmi,want)
                        comparisons+=8
                    comparisons+=13
                intervention_rows=0
                if label=='measurement_location_intervention':
                    selected=interventions[interventions.trajectory_id.eq(rows.iloc[0].trajectory_id)].sort_values(['distance','side'])
                    distances=np.sort(selected.distance.unique()).astype(np.int64)
                    fresh=tab.paired_single_measurement_interventions(snaps[-1],n,distances,2)
                    names=['distance','side','measurement_random','delta_S_central','delta_chi_linear','delta_chi_relative','post_S_central','post_delta_left','post_delta_right']
                    want=selected[names].to_numpy(float)
                    assert fresh.shape==want.shape
                    assert np.max(abs(fresh-want))<2e-12
                    intervention_rows=len(want)
                cases.append(dict(run=label,protocol=protocol,n=n,p=p,trajectory=tr,seed=seed,
                                  probe_records=len(rows),scalar_comparisons=comparisons,
                                  intervention_rows=intervention_rows,max_central_error=max_error,passed=True))
    assert len(cases)==27
    assert len(seeds)==84600 and not collisions
    out=dict(designs=[dict(run=r,base_seed=s) for r,s in designs],seed_count=len(seeds),
             seed_collisions=collisions,cases=cases,case_count=len(cases),
             input_source='entanglement-data.zip',shared_production_simulator=True,
             tolerance=2e-12,elapsed_seconds=time.perf_counter()-started,passed=True)
    path=ROOT/'audits/full-sanity-01/results/simulator_archive_replay.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
