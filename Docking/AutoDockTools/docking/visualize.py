#!/home/ubuntu/Downloads/pymol/bin/python3

#useful colorizing pymol scripts https://pymolwiki.org/index.php/Ramp_New

import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI
 
import numpy as np
import sys, time, os
import pymol
print('Visualization has been started')
print(sys.argv)
input_path=sys.argv[1]
output=sys.argv[2]
ligand=sys.argv[3]
mutant=sys.argv[4]

mutations = [int(i[:-1]) for i in mutant.split('_')[1:-1]]


pymol.finish_launching()

pymol.cmd.load(input_path+'receptor.pqr')
pymol.cmd.load(input_path+'map.dx')

#Select the docked state closest to the catalytic triad
#SER=pymol.cmd.select("SER",'resi 120')
#HG=pymol.cmd.select("HG",'name HG in SER')
#hg_coord=pymol.cmd.get_coords('HG', 1)
#l=pymol.cmd.select("l",'organic')
#centerofmass sele ,4
#dist_state={}
#for s in range(1,10):
#    com=pymol.cmd.centerofmass('l',s)
#    p1 = np.array(com)
#    p2=np.array([  -2.159,  64.702,   7.672])

#Annotate relevant residues
if input_path.find('5XJH')>-1:
    pymol.cmd.select(name='catalytic_triad',selection='resi 160+206+237')
else:    
    pymol.cmd.select(name='catalytic_triad',selection='resi 120+175+188')
pymol.cmd.show('sticks','catalytic_triad')
pymol.cmd.color ('blue', "catalytic_triad")

#Annotate mutated residues
selection_string='resi '
if len(mutations)>0:
    for m in mutations:
        selection_string=selection_string+str(m)+"+"
    pymol.cmd.select(name='mutations',selection=selection_string[:-1])
    pymol.cmd.show('sticks','mutations')
    pymol.cmd.color ('red', "mutations")
else:
    print('It\'s a wild-type')

#Colorizing isosurface
pymol.cmd.ramp_new('e_pot_color', 'map', [-5, 0, 5], ['red', 'white', 'blue'])
pymol.cmd.set('surface_color', 'e_pot_color')
pymol.cmd.set('surface_ramp_above_mode')
pymol.cmd.show('surface')
pymol.cmd.load(input_path+ligand+'_vina.pdbqt')
pymol.cmd.select('br_','all within 8 of '+ligand+'_vina')
pymol.cmd.show('sticks','br_')
#pymol.cmd.color('grey','br_')
pymol.cmd.orient('receptor')
pymol.cmd.save(output+mutant+'_'+ligand+'ESO.pse')
