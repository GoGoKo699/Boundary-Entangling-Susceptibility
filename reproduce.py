#!/usr/bin/env python3
from pathlib import Path
import argparse, subprocess, sys
ROOT=Path(__file__).resolve().parent
def run(cmd): print("+"," ".join(map(str,cmd))); subprocess.run(cmd,check=True)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--core-figures",action="store_true"); a=ap.parse_args(); out=ROOT/"reproduced_figures"; out.mkdir(exist_ok=True)
 if not a.core_figures: ap.error("select --core-figures")
 run([sys.executable,ROOT/"scripts/figures/make_figure_01.py","--csv",ROOT/"data/processed/core_figures/figure_01_panel_b.csv","--pdf",out/"figure_01_panel_b.pdf","--png",out/"figure_01_panel_b.png"])
 run([sys.executable,ROOT/"scripts/figures/make_figure_02.py","--csv",ROOT/"data/processed/core_figures/figure_02_boundary_codes.csv","--outdir",out])
 run([sys.executable,ROOT/"scripts/figures/make_figure_03.py","--csv",ROOT/"data/processed/core_figures/figure_03_size_scaling.csv","--pdf",out/"figure_03_size_scaling.pdf","--png",out/"figure_03_size_scaling.png"])
 run([sys.executable,ROOT/"scripts/figures/make_figure_04.py","--distance-csv",ROOT/"data/processed/core_figures/figure_04_distance_decay.csv","--contrast-csv",ROOT/"data/processed/core_figures/figure_04_conditioning_contrast.csv","--fit-json",ROOT/"data/processed/core_figures/figure_04_distance_fit.json","--distance-pdf",out/"figure_04_distance_decay.pdf","--distance-png",out/"figure_04_distance_decay.png","--contrast-pdf",out/"figure_04_conditioning_contrast.pdf","--contrast-png",out/"figure_04_conditioning_contrast.png"])
if __name__=="__main__": main()
