#!/home/ubuntu/Downloads/pymol/bin/python3

#useful colorizing pymol scripts https://pymolwiki.org/index.php/Ramp_New

import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI
 
import sys, time, os
import pymol
import re

print('Visualization has been started')
print(sys.argv)
input_path=sys.argv[1]
output=sys.argv[2]
ligand=sys.argv[3]
map_=sys.argv[4]
input_ligand=sys.argv[5]
mutant=re.findall('[A-Z][^A-Z]*', input_path.split('_')[-5])
mutations = [int(i) for i in mutant[0].split(',')[1::2]]


pymol.finish_launching()

pymol.cmd.load(input_path,'receptor')
#pymol.cmd.select('receptor','not organic')

pymol.cmd.load(map_,'map')

#Annotate relevant residues
if input_path.find('5XJH')>-1:
    pymol.cmd.select(name='catalytic_triad',selection='resi 160+206+237')
else:    
    pymol.cmd.select(name='catalytic_triad',selection='resi 120+175+188')
pymol.cmd.show('sticks','catalytic_triad')
pymol.cmd.color ('blue', "catalytic_triad")

#Annotate mutated residues
selection_string='resi '
print(len(mutations))
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
pymol.cmd.load(input_ligand)
pymol.cmd.select('ligand','organic')
pymol.cmd.select('br_','all within 8 of ligand')
pymol.cmd.show('sticks','br_')
pymol.cmd.color('grey','br_')
pymol.cmd.orient('ligand')
pymol.cmd.set_view('0.229980931,   -0.098047607,    0.968243361,-0.471604466,    0.859059334,    0.199009135,-0.851292491,   -0.502397239,    0.151327386,0.000077881,    0.000029787, -121.497497559,5.986613274,   57.268852234,   25.369915009,-2955.979248047, 3198.967041016,  -20.000000000')
#pymol.cmd.png(output+''.join(mutant)+'_ligand.png',1500,1000,300)
#pymol.cmd.orient('receptor')
pymol.cmd.png(output+''.join(mutant)+'.png',1500,1000,300)
pymol.cmd.save(output+''.join(mutant)+'_ESO.pse')
