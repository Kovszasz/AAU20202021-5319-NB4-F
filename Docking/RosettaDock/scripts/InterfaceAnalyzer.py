	
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
 
import sys, time, os
import pymol

#pdbs = sys.argv[1:]
pdb_file = sys.argv[2]
output= sys.argv[1]


pdbs=[]
with open(pdb_file,'r') as pdb:
    for p in pdb:
        p=list(p)
        p.pop()
        p=''.join(p)
        pdbs.append(p)

PET_CARBONATOMS=[
    'C35',
    'C78',
    'C47',
    'C10',
    'C36',
    'C34',
    'C66',
    'C32',
    'C8',
    'C3',
    'C13',
    'C22',
    'C14',
    'C19',
    'C71',
    'C57'
]

pymol.finish_launching()
return_dict={}
#return_dict_mid={}
def get_distance(pdb):
    pymol.cmd.load(pdb)
    d=[]
    #PET_mid=pymol.cmd.select("PET_mid",'id 2874')
    #PET_end=pymol.cmd.select("PET_end",'id 2911')
    
    for ca in PET_CARBONATOMS:
        #SER=pymol.cmd.select("SER",'resi 160')
        SER=pymol.cmd.select("SER",'resi 120')
        HG=pymol.cmd.select("HG",'name HG in SER')
        PET=pymol.cmd.select("PET",'name '+ca)
        pet=pymol.cmd.get_distance("HG","PET")
        pymol.cmd.deselect()
        d.append(pet)
        pymol.cmd.deselect()
    pymol.cmd.delete('all')
    return min(d)
    ##END##
    #C71: 2910
    #O26: 2911
    #----------#
    ##MID##
    #C8: 2873
    #O2: 2874
for pdb in pdbs:
    return_dict[pdb]=get_distance(pdb)

res=min(return_dict, key=return_dict.get)
#mid=min(return_dict_mid, key=return_dict_mid.get)
#print('Minimum:',res,'\t',return_dict[res])
#print('Minimum mid:',mid,'\t',return_dict_mid[mid])
#print(return_dict_mid)
filtered=[{'pdb':i,'dist':return_dict[i]} for i in return_dict.keys() if return_dict[i]>2.8 and return_dict[i]<5.3]
#filtered_end=[{i:return_dict_end[i]} for i in return_dict_endq.keys() if return_dict_end[i]>2.8 and return_dict_end[i]<5.3]
#print(filtered_mid)
top10=sorted(filtered, key=lambda k: k['dist'])[:100]
for t in top10:
    print(t['pdb'].replace('.pdb','').split('/')[1],'\t',t['dist'])