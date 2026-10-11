import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
R=Path(__file__).resolve().parents[1];F=R/'paper/figures';F.mkdir(exist_ok=True)
s=json.loads((R/'results/summary.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
blue='#226a91';red='#b13f47';green='#31806a';gray='#74818c'
# Exact witness and intervention location.
fig,ax=plt.subplots(figsize=(7.0,1.85));ax.set_xlim(0,10);ax.set_ylim(0,2);ax.axis('off')
boxes=[(.1,1.07,2.55,.64,'Raw tool argument\n9007199254740993',blue),(3.65,1.07,2.65,.64,'MCP JSON.parse\n9007199254740992',red),(7.3,1.07,2.6,.64,'Integer validation\npasses',red)]
for x,y,w,h,t,col in boxes:
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.07',facecolor=col,edgecolor='none'));ax.text(x+w/2,y+h/2,t,ha='center',va='center',color='white',fontsize=10)
for a,b in [(2.75,3.5),(6.4,7.16)]:ax.add_patch(FancyArrowPatch((a,1.4),(b,1.4),arrowstyle='->',mutation_scale=14,color=gray))
ax.text(1.4,.58,'Check schema and raw argument here',ha='center',color=green,weight='bold',fontsize=9)
ax.text(6.7,.22,'Post-parse logs cannot reconstruct the original value',ha='center',color=red,fontsize=9)
ax.plot([1.4,1.4],[.74,1.00],color=green)
fig.savefig(F/'boundary.pdf',bbox_inches='tight');fig.savefig(F/'boundary.png',bbox_inches='tight',dpi=200);plt.close(fig)
# Local schema exposure, not empirical model-output frequency.
groups=s['groups'];order=['Glaiveai2K','Kubernetes','WashingtonPost','Github_ultra','Github_medium','JsonSchemaStore','Github_hard','Github_trivial','Github_easy','Snowplow']
labels=['GlaiveAI-2K','Kubernetes','Washington Post','GitHub Ultra','GitHub Medium','SchemaStore','GitHub Hard','GitHub Trivial','GitHub Easy','Snowplow']
fig,ax=plt.subplots(figsize=(3.35,3.1));y=np.arange(len(order));rates=[100*groups[k]['hidden_leaves']/groups[k]['leaves'] for k in order]
ax.barh(y,rates,color=blue,height=.63);ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(0,120);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Local projections with a\nhidden-change witness (%)',fontsize=8)
for i,(rate,k) in enumerate(zip(rates,order)):ax.text(rate+1,i,f'{rate:.1f}',va='center',fontsize=7.8)
ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);fig.tight_layout();fig.savefig(F/'exposure.pdf');fig.savefig(F/'exposure.png',dpi=200);plt.close(fig)
# Actual MCP fixture, sources are exact integers and contain no model sampling.
r=json.loads((R/'results/demo.json').read_text());powers=[31,52,53,54,63,64];a=np.zeros((len(powers),9))
for v in r:
 if v['mode']=='native':a[powers.index(v['power']),v['offset']+4]=int(not v['correct'])
from matplotlib.colors import ListedColormap
fig,ax=plt.subplots(figsize=(3.35,2.4));ax.imshow(a,cmap=ListedColormap([green,red]),vmin=0,vmax=1,aspect='auto');ax.set_xticks(range(9),range(-4,5));ax.set_yticks(range(6),[f'$2^{{{e}}}$' for e in powers]);ax.set_xlabel('Offset from power of two');ax.set_ylabel('Identifier center');ax.tick_params(length=0)
for i in range(6):
 for j in range(9):ax.text(j,i,'\u00d7' if a[i,j] else '\u2713',ha='center',va='center',color='white',fontsize=11)
fig.tight_layout();fig.savefig(F/'demo.pdf');fig.savefig(F/'demo.png',dpi=200);plt.close(fig)
# Timing is actual local batches, medians + range rather than fictional error bars.
t=json.loads((R/'results/timing.json').read_text())['rows'];fig,ax=plt.subplots(figsize=(3.35,2.4))
for method,col in [('native',blue),('guard',red),('lossless',green)]:
 sizes=sorted({v['bytes'] for v in t});y=[];lo=[];hi=[]
 for size in sizes:
  vals=[v['us'] for v in t if v['bytes']==size and v['method']==method];m=np.median(vals);y.append(m);lo.append(m-min(vals));hi.append(max(vals)-m)
 ax.errorbar(np.array(sizes)/1024,y,yerr=[lo,hi],marker='o',label=method,color=col,capsize=3,lw=1.4)
ax.set_xlabel('Serialized input (KiB)');ax.set_ylabel('Time (microseconds)');ax.set_yscale('log');ax.legend(frameon=False,fontsize=8);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(F/'timing.pdf');fig.savefig(F/'timing.png',dpi=200);plt.close(fig)
# Derived numbers used in paper; table cells generated directly from results.
lines=['\\begin{tabular}{lrrr}','\\toprule','Pipeline & Accepted & Changed & Rejected \\\\','\\midrule']
for name,label in [('native','Native JS / MCP'),('python_native','Native Python'),('safe','Post-parse integer check'),('library_guard','Library number check'),('payload_guard','Raw-argument guard'),('joint_guard','Schema + argument guard'),('lossless','Lossless JSON')]:
 d=s['methods'][name];lines.append(f"{label} & {d['accepted']:,} & {d['changed']:,} & {d.get('rejected',0):,} \\\\")
lines+=['\\bottomrule','\\end{tabular}'];(R/'paper/table_results.tex').write_text('\n'.join(lines)+'\n')
print('Figures and measured table generated.')
