#!/usr/bin/env python3
from pathlib import Path
import argparse
import numpy as np, pandas as pd
import matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
BLUE='#245B78'; ORANGE='#B66A3C'; LIGHT='#F3F4F4'
mpl.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':9.4,'xtick.labelsize':9.2,'ytick.labelsize':9.2,'axes.linewidth':.75,'xtick.major.size':0,'ytick.major.size':0,'pdf.fonttype':42,'ps.fonttype':42})
def mat(df,col):
 out=np.empty((3,3));
 for i,dl in enumerate([1,0,-1]):
  for j,dr in enumerate([-1,0,1]): out[i,j]=float(df[(df.delta_L==dl)&(df.delta_R==dr)].iloc[0][col])
 return out
def draw(a,pdf,limit,fmt,corner=False,reverse=False,ylabels=True):
 cmap=LinearSegmentedColormap.from_list('m',[ORANGE,LIGHT,BLUE] if reverse else [BLUE,LIGHT,ORANGE],N=256); norm=TwoSlopeNorm(vmin=-limit,vcenter=0,vmax=limit)
 fig,ax=plt.subplots(figsize=(2.28,2.28)); ax.imshow(a,cmap=cmap,norm=norm,aspect='equal')
 ax.set_xticks([0,1,2],labels=[r'$-1$',r'$0$',r'$+1$']); ax.set_yticks([0,1,2],labels=[r'$+1$',r'$0$',r'$-1$'] if ylabels else ['','',''])
 ax.set_xticks(np.arange(-.5,3,1),minor=True); ax.set_yticks(np.arange(-.5,3,1),minor=True); ax.grid(which='minor',color='white',lw=1); ax.tick_params(which='minor',bottom=False,left=False)
 for i in range(3):
  for j in range(3):
   v=a[i,j]; c='white' if abs(v)>=.58*limit else '#222'; number=fmt(v)
   if corner and (i,j) in {(0,2),(2,0)}:
    ax.text(j,i-.15,number,ha='center',va='center',fontsize=10.2,color=c)
    ax.text(j,i+.23,r'$S_m\,\mathrm{peak}$' if (i,j)==(0,2) else r'$S_m\,\mathrm{dip}$',ha='center',va='center',fontsize=9.1,color=c)
   else: ax.text(j,i,number,ha='center',va='center',fontsize=10.2,color=c)
 fig.subplots_adjust(left=.19,right=.985,bottom=.15,top=.985); fig.savefig(pdf); plt.close(fig)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--csv',type=Path,required=True); ap.add_argument('--outdir',type=Path,required=True); a=ap.parse_args(); a.outdir.mkdir(parents=True,exist_ok=True); df=pd.read_csv(a.csv)
 draw(mat(df,'display_response'),a.outdir/'figure_02_response_matrix.pdf',.6,lambda x:r'$0$' if abs(x)<5e-12 else rf'${x:+.1f}$',True,True,True)
 draw(mat(df,'display_probability_slope'),a.outdir/'figure_02_redistribution_matrix.pdf',.025,lambda x:r'$0.000$' if abs(x)<.0005 else rf'${x:+.3f}$',False,False,False)
if __name__=='__main__': main()
