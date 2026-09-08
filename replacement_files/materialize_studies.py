#!/usr/bin/env python3
"""Materialize checked original-study records and source, without running them."""
from pathlib import Path
import argparse,json
from boundary_susceptibility.records import RecordBundle

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('reproduced_studies'))
    a=p.parse_args()
    with RecordBundle() as data:
        report=data.verify()
        data.materialize(a.output)
    print(json.dumps({**report,'output':str(a.output.resolve())},indent=2))
if __name__=='__main__':main()
