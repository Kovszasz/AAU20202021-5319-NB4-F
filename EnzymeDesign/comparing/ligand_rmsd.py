%matplotlib inline
# %%
from matplotlib import pyplot as plt
import sys


scorefiles=sys.argv[1].split(',')
pdbs=sys.argv[2]
legend_labels=sys.argv[3].split(',')

LIGAND_ENERGY=64
LIGAND_RMSD=69


def read_scorefile(line):
    line=list(line)
    line.pop()
    line=''.join(line)
    l=line.split(' ')
    split_line=[]
    for c in l:
        if c!='':
            split_line.append(c)
    return split_line

poses={}
for pdb in range(len(pdbs)):
    poses[legend_labels[pdb]]=[]
    with open(pdbs[pdb],'r') as p:
        for line in p:
            line=list(line)
            line.pop()
            line=''.join(line)
            poses[legend_labels[pdb]].append(line)


data={}
for scorefile in range(len(scorefiles)):
    with open(scorefiles[scorefile],'r') as sc:
        c=0
        for line in sc:
            rsc=read_scorefile(line)
            if c==0:
                data[legend_labels[scorefile]]={'Liganded/Apo RMSD':[],'Docking energy':[]}
            else:
                if rsc[-1] in poseslegend_labels[scorefile]:
                    data[legend_labels[scorefile]]['Liganded/Apo RMSD'].append(read_scorefile(line)[LIGAND_RMSD])
                    data[legend_labels[scorefile]]['Docking energy'].append(read_scorefile(line)[LIGAND_ENERGY])


for d in data.keys():
    plt.scatter(data[d]['Liganded/Apo RMSD'],data[d]['Docking energy'],label=d,alpha=0.7)

