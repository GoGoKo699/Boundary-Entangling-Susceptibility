#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys,json,hashlib,time,os
from pathlib import Path
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
os.environ['NUMEXPR_NUM_THREADS']='1'
import pandas as pd
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from run_physical_stabilizer_arm import worker

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--clifford-path',type=Path,required=True);ap.add_argument('--measurement-protocol',required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--p',type=float,required=True);ap.add_argument('--trajectories',type=int,default=80);ap.add_argument('--start-index',type=int,default=0);ap.add_argument('--discovery-trajectories',type=int,default=40);ap.add_argument('--probe-taus',nargs='+',type=float,default=[6,8]);ap.add_argument('--gate-count',type=int,default=12);ap.add_argument('--base-seed',type=int,default=2026082107);args=ap.parse_args()
 args.outdir.mkdir(parents=True,exist_ok=True); rows=[];t=time.time();cliff=str(args.clifford_path.resolve());taus=tuple(args.probe_taus)
 for j,tr in enumerate(range(args.start_index,args.start_index+args.trajectories)):
  rows.extend(worker((args.n,args.p,tr,taus,args.base_seed,args.discovery_trajectories,args.measurement_protocol,cliff,args.gate_count)))
  if (j+1)%10==0: print(f'{j+1}/{args.trajectories} start={args.start_index} {time.time()-t:.1f}s',flush=True)
 df=pd.DataFrame(rows).sort_values(['measurement_protocol','n','p_measure','trajectory_index','tau'])
 df.to_csv(args.outdir/'physical_stabilizer_states.csv.gz',index=False,compression='gzip')
 manifest={'purpose':'independent-seed replication cell, sequential safe runner','dynamics':'uniform two-qubit Clifford','initial_state':'random single-qubit stabilizer product','measurement_protocols':[args.measurement_protocol],'sizes':[args.n],'p_values':[args.p],'trajectory_start_index':args.start_index,'trajectories_in_chunk':args.trajectories,'discovery_trajectories_per_cell':args.discovery_trajectories,'probe_taus':list(taus),'gate_count':args.gate_count,'base_seed':args.base_seed,'rows':len(df),'clifford_table_sha256':hashlib.sha256(args.clifford_path.read_bytes()).hexdigest(),'matching_principle':'within fixed (n,tau,Schmidt rank), the complete nonzero central spectrum is exactly flat and identical','max_spectrum_flatness_error':float(df.spectrum_flatness_max_abs.max()),'max_rank_power_of_two_error':float(df.rank_power_of_two_error.max()),'elapsed_seconds':time.time()-t}
 (args.outdir/'simulation_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2),flush=True)
if __name__=='__main__':main()
