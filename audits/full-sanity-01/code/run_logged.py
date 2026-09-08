#!/usr/bin/env python3
"""Run one audit command with explicit argv, output log and wall/resource record."""
import argparse, datetime, json, os, pathlib, resource, subprocess, sys, time

p=argparse.ArgumentParser()
p.add_argument('name')
p.add_argument('command',nargs=argparse.REMAINDER)
a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[3]
audit=root/'audits/full-sanity-01'
(audit/'logs').mkdir(exist_ok=True)
argv=a.command[1:] if a.command[:1]==['--'] else a.command
if not argv: p.error('command required')
env=os.environ.copy()
env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONHASHSEED='0',MPLBACKEND='Agg')
env['PATH']=str(pathlib.Path(sys.executable).parent)+os.pathsep+env['PATH']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.monotonic()
with (audit/'logs'/f'{a.name}.log').open('w') as f:
    f.write('argv: '+json.dumps(argv)+'\nUTC start: '+start+'\n');f.flush()
    done=subprocess.run(argv,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
seconds=time.monotonic()-t
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
entry=dict(name=a.name,argv=argv,cwd=str(root),start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=seconds,exit_code=done.returncode,user_seconds=usage.ru_utime,system_seconds=usage.ru_stime,peak_child_rss_kib=usage.ru_maxrss,thread_environment={k:env[k] for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','PYTHONHASHSEED','MPLBACKEND']})
(audit/'logs'/f'{a.name}.json').write_text(json.dumps(entry,indent=2)+'\n')
print(json.dumps(entry))
sys.exit(done.returncode)
