	
#!/home/ubuntu/Downloads/pymol/bin/python3
#
#   Usage: superimposition.py STATIC MOBILE
#   Utrecht @ 2009
#   Joao Rodrigues
#
# http://pldserver1.biochem.queensu.ca/~rlc/work/pymol/
###############################################
 
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI
 
from matplotlib import pyplot as plt
import matplotlib.pylab as pylab
import sys, time, os
import pymol
import json

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}

pylab.rcParams.update(params)

pdb_file = sys.argv[2]
output= sys.argv[1]
pymol.finish_launching()
return_dict_end={}
return_dict_mid={}

pdbs=[]
with open(pdb_file,'r') as pdb:
    for p in pdb:
        p=list(p)
        p.pop()
        p=''.join(p)
        pdbs.append(p)

def get_distance(pdb):
    pymol.cmd.load(pdb)
    SER=pymol.cmd.select("SER",'resi 120')
    HG=pymol.cmd.select("HG",'name HG in SER')
    if pdb.find('mid')>-1:
        PET_mid=pymol.cmd.select("PET_mid",'name C8')
    elif pdb.find('end')>-1:
        PET_end=pymol.cmd.select("PET_end",'name C71')
    elif pdb.find('BHET')>-1:
        BHET=pymol.cmd.select("BHET",'name C8')
    else:
        PET_end=pymol.cmd.select("PET_end",'name C71')
        PET_mid=pymol.cmd.select("PET_mid",'name C8')
    #print(PET_mid,'\t',PET_end,'\t',SER,'\t',pdb)
    if pdb.find('BHET')>-1:
        try:
            end=pymol.cmd.get_distance("HG","BHET")
        except:
            end=None
        mid=None
    else:
        try:
            end=pymol.cmd.get_distance("HG","PET_end")
        except:
            end=None
        try:
            mid=pymol.cmd.get_distance("HG","PET_mid")
        except:
            mid=None
    


    pymol.cmd.deselect()
    pymol.cmd.delete('all')
    return mid,end
    ##END##
    #C71: 2910
    #O26: 2911
    #----------#
    ##MID##
    #C8: 2873
    #O2: 2874
fig, ax = plt.subplots( nrows=1, ncols=1 )
for pdb in pdbs:
    if pdb.find('description')==-1:
        mid,end=get_distance(pdb)
        if mid:
            return_dict_mid[pdb]=mid
        if end:
            return_dict_end[pdb]=end
if end:
    end=min(return_dict_end, key=return_dict_end.get)
    ax.hist(return_dict_end.values(),bins=300)
    with open(output+'.json', 'w') as fp:
        json.dump(return_dict_end, fp)
if mid:
    mid=min(return_dict_mid, key=return_dict_mid.get)
    ax.hist(return_dict_mid.values(),bins=300)
    with open(output+'.json', 'w') as fp:
        json.dump(return_dict_mid, fp)

ax.set_xlabel(r'Ser-OH <-> C=O distance [$\AA$]')
ax.set_ylabel('Frequency')
#plt.show()
fig.savefig(output)
plt.close(fig)
#print(return_dict_mid)
#filtered_mid=[{i:return_dict_mid[i]} for i in return_dict_mid.keys() if return_dict_mid[i]>2.8 and return_dict_mid[i]<5.3]
#print(filtered_mid)

if end:
    for i in return_dict_end.keys():
        if return_dict_end[i]<5:
            p=i.split('/')
            print(p[-1])
if mid:
    for i in return_dict_mid.keys():
        if return_dict_mid[i]<5:
            p=i.split('/')
            print(p[-1])