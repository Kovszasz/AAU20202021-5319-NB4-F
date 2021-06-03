#!/home/ubuntu/Downloads/pymol/bin/python3

#useful colorizing pymol scripts https://pymolwiki.org/index.php/Ramp_New

import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI
 
import sys, time, os
import pymol

PDB=sys.argv[1]
filename=PDB.split('/').pop()
pymol.finish_launching()

pymol.cmd.load(PDB)

organic=pymol.cmd.select('organic_',' organic')
#pymol.cmd.delete('organic_')
enzyme=pymol.cmd.select('enzyme','not organic')
pymol.cmd.save(filename.replace('.pdb','')+'_apo.pdb','enzyme')
#pymol.cmd.reinitialize()
#pymol.cmd.load(PDB)
enzyme=pymol.cmd.select('enzyme','not organic')
#pymol.cmd.delete('enzyme')
organic=pymol.cmd.select('organic_',' organic')
pymol.cmd.save(filename.replace('.pdb','')+'_ligand.pdb','organic_')


