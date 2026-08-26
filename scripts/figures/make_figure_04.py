#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
FIG_BLUE='#245B78'; FIG_TEAL='#2F7C78'; FIG_ORANGE='#B66A3C'; FIG_GRAY='#6F7478'; FIG_GRID='#D9DEE2'; BS=chr(92)
def configure():
    mpl.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':9.6,'axes.labelsize':10.0,'xtick.labelsize':9.2,'ytick.labelsize':9.2,'axes.linewidth':0.75,'xtick.major.width':0.75,'ytick.major.width':0.75,'xtick.major.size':3.0,'ytick.major.size':3.0,'lines.linewidth':1.1,'pdf.fonttype':42,'ps.fonttype':42})
def distance_panel(distance_csv,fit_json,pdf,png):
    df=pd.read_csv(distance_csv); fit=json.loads(fit_json.read_text(encoding='utf-8'))
    d=df.distance.to_numpy(float); y=df.estimate.to_numpy(float); yerr=np.vstack([y-df.ci_low.to_numpy(float),df.ci_high.to_numpy(float)-y])
    xfit=np.linspace(0,16,400); yfit=-float(fit['amplitude'])*np.exp(-xfit/float(fit['decay_length']))
    fig,ax=plt.subplots(figsize=(4.62,2.32))
    ax.errorbar(d,y,yerr=yerr,fmt='o',ms=5.4,mfc=FIG_BLUE,mec=FIG_BLUE,mew=0.9,ecolor=FIG_BLUE,elinewidth=1.0,capsize=2.1,capthick=0.95,linestyle='none',zorder=4)
    ax.plot(xfit,yfit,color=FIG_TEAL,lw=1.65,zorder=2); ax.axhline(0,color=FIG_GRAY,lw=0.72,zorder=0); ax.grid(axis='y',color=FIG_GRID,lw=0.55,zorder=0)
    ax.set_xlim(-0.55,16.55); ax.set_ylim(-0.0545,0.0025); ax.set_xticks([0,1,2,4,8,16]); ax.set_yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05])
    ax.set_xlabel('measurement distance from the cut, $d$',labelpad=3.5); ax.set_ylabel(f'${BS}Delta{BS}chi_{{{BS}rm rel}}(d)$',labelpad=4.0)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.text(0.97,0.08,f'$-A e^{{-d/{BS}xi}}, {BS}quad {BS}xi={fit["decay_length"]:.2f}$ sites',transform=ax.transAxes,ha='right',va='bottom',fontsize=9.5,color=FIG_TEAL)
    ax.text(0.10,0.08,f'${BS}Delta S_m=0$',transform=ax.transAxes,ha='left',va='bottom',fontsize=9.5,color=FIG_GRAY)
    fig.subplots_adjust(left=0.17,right=0.985,bottom=0.23,top=0.97); pdf.parent.mkdir(parents=True,exist_ok=True); fig.savefig(pdf); fig.savefig(png,dpi=400); plt.close(fig)
def contrast_panel(contrast_csv,pdf,png):
    df=pd.read_csv(contrast_csv); rows=df.set_index('condition').loc[['unconditional','central_spectrum_unchanged']]
    x=np.array([0.,1.]); y=rows.estimate.to_numpy(float); yerr=np.vstack([y-rows.ci_low.to_numpy(float),rows.ci_high.to_numpy(float)-y])
    colors=[FIG_ORANGE,FIG_BLUE]
    fig,ax=plt.subplots(figsize=(2.08,2.63))
    ax.bar(x,y,width=0.58,color=colors,edgecolor=colors,linewidth=0.9,zorder=2)
    ax.errorbar(x,y,yerr=yerr,fmt='none',ecolor='#222222',elinewidth=1.0,capsize=2.5,capthick=0.95,zorder=4)
    ax.axhline(0,color=FIG_GRAY,lw=0.75,zorder=1)
    ax.set_xlim(-0.58,1.58); ax.set_ylim(-0.058,0.084)
    ax.set_xticks(x,labels=['unconditional','spectrum\nunchanged'])
    ax.tick_params(axis='x',labelsize=8.8,pad=3.0)
    ax.set_yticks([-0.05,0,0.05]); ax.grid(axis='y',color=FIG_GRID,lw=0.55,zorder=0)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.set_ylabel(f'near-minus-far $D_{{{BS}rm rel}}$',labelpad=0.6)
    ax.text(x[0],y[0]+0.005,f'{y[0]:+.4f}',ha='center',va='bottom',fontsize=9.5,color=FIG_ORANGE)
    ax.text(x[1],y[1]+0.006,f'{y[1]:+.4f}',ha='center',va='bottom',fontsize=9.5,color='white')
    fig.subplots_adjust(left=0.27,right=0.985,bottom=0.23,top=0.96); pdf.parent.mkdir(parents=True,exist_ok=True); fig.savefig(pdf); fig.savefig(png,dpi=400); plt.close(fig)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--distance-csv',type=Path,required=True); ap.add_argument('--contrast-csv',type=Path,required=True); ap.add_argument('--fit-json',type=Path,required=True); ap.add_argument('--distance-pdf',type=Path,required=True); ap.add_argument('--distance-png',type=Path,required=True); ap.add_argument('--contrast-pdf',type=Path,required=True); ap.add_argument('--contrast-png',type=Path,required=True); a=ap.parse_args(); configure(); distance_panel(a.distance_csv,a.fit_json,a.distance_pdf,a.distance_png); contrast_panel(a.contrast_csv,a.contrast_pdf,a.contrast_png)
if __name__=='__main__': main()
