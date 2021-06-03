from matplotlib import pyplot as plt
from os import listdir
import sys, time, os
import numpy as np
import numpy as np
import pickle 

print('Visualization has been started')
print(sys.argv)
main_input_path=sys.argv[1]
state=sys.argv[2]


def read_vina_log(input_path):
    with open(input_path+'vina.log','r') as vina:
        for lines in vina:
            #if lines.find('   2 ')>-1:
            if lines.find('   '+str(state)+' ')>-1:
                line=lines.split(' ')
                return_data=[]
                for l in line:
                    if l!='':
                        return_data.append(float(l))
                return return_data

def split_sample(sample):
    sample=sample.split('__')
    return sample

def binary_saver(obj,name): #We store the results and other important variables binary. It is easer and faster to read and save.
    f=''
    outfile=open(f+name,'wb')
    pickle.dump(obj,outfile)
    outfile.close()



RMSD_ub=[]
RMSD_lb=[]
affinity=[]
plot_data_x=[]
heatmap={}
for input_path in listdir('outputs/'):
    if input_path!='analyze':
        raw_data=read_vina_log(main_input_path+'/'+input_path+'/')
        plot_data_x.append(input_path)
        print(input_path)
        print(raw_data)
        RMSD_ub.append(raw_data[3])
        RMSD_lb.append(raw_data[2])
        affinity.append(raw_data[1]*-1)
        res= split_sample(input_path)
        receptor = res[0]
        ligand=res[1]
        if receptor in heatmap.keys():
            heatmap[receptor].update({ligand:raw_data[1]}) #saving raw data for heatmap visualization
        else:
            heatmap[receptor]={ligand:raw_data[1]}
print('Saving binary data')
binary_saver(affinity,'affinity')
binary_saver(plot_data_x,'affinity_label')
binary_saver([RMSD_lb,RMSD_ub],'RMSDs')

xlabel='Mutants vs wild-tpye'
#ylabels=['Affinity [kcal/mol]','RMSD']

fig, (ax1, ax2) = plt.subplots(2)
plt.xticks(rotation=45)
ax1.bar(plot_data_x,affinity)
ax1.set_ylabel(' - Affinity [kcal/mol]')
ax1.set_xticks(np.arange(len(plot_data_x)))
ax2.bar(plot_data_x,RMSD_lb,color='blue',alpha=0.5,label='Lower bound')
ax2.bar(plot_data_x,RMSD_ub,color='red',alpha=0.5,label='Upper bound')
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.tight_layout()
plt.savefig(main_input_path+'/analyze/mutation_total_energies.png')

#Heatmap between mutants and ligands

HeatMapValues=[]
for i in heatmap.keys():
    row=[]
    for j in heatmap[i].keys():
        row.append(heatmap[i][j])
    HeatMapValues.append(row)
HeatMapValues=np.array(HeatMapValues)

fig, ax = plt.subplots()
im = ax.imshow(HeatMapValues)
ax.set_yticks(np.arange(len(heatmap.keys())))
ax.set_xticks(np.arange(len(heatmap[list(heatmap.keys())[0]].keys())))
ax.set_yticklabels(heatmap.keys())
ax.set_xticklabels(heatmap[list(heatmap.keys())[0]].keys())
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
for i in range(len(heatmap.keys())):
    for j in range(len(heatmap[list(heatmap.keys())[0]].keys())):
        text = ax.text(j, i, HeatMapValues[i, j],
                       ha="center", va="center", color="w")
fig.tight_layout()


plt.savefig('heatmap.png')