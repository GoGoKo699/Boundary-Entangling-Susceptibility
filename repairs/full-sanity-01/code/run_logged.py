"""Execute one inspected repair verification command without overwriting logs."""
import argparse
import datetime
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
logs = root / 'repairs/full-sanity-01/logs'
logs.mkdir(parents=True, exist_ok=True)
argv = args.command[1:] if args.command[:1] == ['--'] else args.command
if not argv or Path(args.name).name != args.name:
    parser.error('a simple log name and command are required')
if (logs / (args.name + '.log')).exists() or (logs / (args.name + '.json')).exists():
    parser.error('choose a new log name; prior results are preserved')
env = os.environ.copy()
env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           PYTHONHASHSEED='0', MPLBACKEND='Agg')
env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env['PATH']
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
with (logs / (args.name + '.log')).open('x') as stream:
    stream.write('argv: ' + json.dumps(argv) + '\nUTC start: ' + started + '\n')
    stream.flush()
    run = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
usage = resource.getrusage(resource.RUSAGE_CHILDREN)
result = dict(argv=argv, cwd=str(root), start_utc=started,
              end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              wall_seconds=time.monotonic()-t, exit_code=run.returncode,
              user_seconds=usage.ru_utime, system_seconds=usage.ru_stime,
              peak_child_rss_kib=usage.ru_maxrss,
              environment={k: env[k] for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS',
                           'MKL_NUM_THREADS', 'PYTHONHASHSEED', 'MPLBACKEND')})
with (logs / (args.name + '.json')).open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps(result))
sys.exit(run.returncode)
