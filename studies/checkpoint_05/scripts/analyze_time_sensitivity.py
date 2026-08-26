#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,sys
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from analyze_checkpoint05 import fe_fit

def s32(*x):return int.from_bytes(hashlib.blake2b(repr(x).encode(),digest_size=8).digest(),'little')&0xffffffff

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--bootstrap',type=int,default=1000)
 a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True);rows=[]
 for run,rel in [('primary','data/primary_scaling/stabilizer_scaling_states.csv.gz'),('replication','data/independent_replication/stabilizer_scaling_states.csv.gz')]:
  d=pd.read_csv(a.root/rel)
  for (prot,n,tau),sub in d.groupby(['protocol','n','tau']):
   r,_,_=fe_fit(sub,'chi_relative',a.bootstrap,s32(run,prot,n,tau),min_per_p=5,min_levels=3)
   r.update(run=run,protocol=prot,n=n,tau=tau);rows.append(r)
 out=pd.DataFrame(rows);out.to_csv(a.outdir/'fixed_spectrum_time_sensitivity.csv',index=False)
 print(out.to_string(index=False))
if __name__=='__main__':main()
