#!/usr/bin/env python3
from pathlib import Path
import hashlib, csv, pandas as pd
from boundary_susceptibility.boundary_codes import stabilizer_boundary_response
ROOT=Path(__file__).resolve().parent
required=["README.md","docs/SCIENTIFIC_STORY.md","figures/core/figure_01_panel_b.pdf","figures/core/figure_04_conditioning_contrast.pdf"]
missing=[p for p in required if not (ROOT/p).exists()]
if missing: raise SystemExit(f"missing: {missing}")
expected={( -1,-1):.6,(-1,0):.4,(-1,1):0,(0,-1):.4,(0,0):.2,(0,1):-.2,(1,-1):0,(1,0):-.2,(1,1):-.6}
for code,value in expected.items():
 if abs(stabilizer_boundary_response(*code)-value)>1e-12: raise SystemExit(f"identity failed: {code}")
f1=pd.read_csv(ROOT/"data/processed/core_figures/figure_01_panel_b.csv")
if not (f1.ci_high<0).all(): raise SystemExit("Figure 1 interval sign check failed")
print("verification passed")
