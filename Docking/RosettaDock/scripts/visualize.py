#!/home/ubuntu/Downloads/pymol/bin/python3

#useful colorizing pymol scripts https://pymolwiki.org/index.php/Ramp_New

import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI
 
import sys, time, os
import pymol
import re

print('Visualization has been started')
session=sys.argv[1]
input_top10=sys.argv[2]
output=sys.argv[3]
#mutant=re.findall('[A-Z][^A-Z]*', input_path.split('_')[-5])
#mutations = [int(i) for i in mutant[0].split(',')[1::2]]
top10=[]
with open(input_top10,'r') as t10:
    for line in t10:
        line=line.replace('\n','')
        top10.append(line)

mutant=input_top10.replace('_selected_pdbs.txt','')
pymol.cmd.load(session)
pymol.cmd.delete('ligand')
#pymol.cmd.color ('yellow', "mutations")
#pymol.cmd.set_view('0.147362635,   -0.242211416,    0.958960295,-0.035849728,    0.967602551,    0.249903813,-0.988430858,   -0.071204647,    0.133903190,0.000131145,   -0.000365995, -137.132797241, 12.780108452,   56.377689362,   27.014999390, 26.608133316,  247.548248291,  -20.000000000')
#pymol.cmd.set_view('-0.445236176,    0.076614164,    0.892122328,-0.046323445,    0.993024051,   -0.108397953,-0.894209087,   -0.089589447,   -0.438588172,0.000174581,   -0.000388540, -107.746391296,8.714427948,   54.416435242,   19.239639282, -2.782570601,  218.157577515,  -20.000000000 ')
pymol.cmd.set_view(' -0.816344142,    0.571938157,    0.080327086,\
     0.426861137,    0.503798008,    0.750978231,\
     0.389051825,    0.647353351,   -0.655417383,\
     0.000000000,    0.000000000, -210.444213867,\
    -1.250177383,   14.044010162,  -18.724597931,\
   165.915832520,  254.972595215,  -20.000000000')
for t in top10:
    print(t)
    pymol.cmd.load(t)
    pymol.cmd.hide('everything','not organic and model '+t.split('/')[1].replace('.pdb',''))
pymol.cmd.select('top10','organic')
pymol.cmd.select('best','organic and model '+top10[0].split('/')[1].replace('.pdb',''))
#pymol.cmd.color('black','best')
pymol.cmd.set('stick_transparency',1,'top10')
#pymol.cmd.png(output+''.join(mutant)+'_ligand.png',1500,1000,300)
#pymol.cmd.orient('receptor')
pymol.cmd.png(mutant+'apo.png',1500,1000,300)
pymol.cmd.set('stick_transparency',0.7,'top10')
pymol.cmd.set('stick_transparency',0,'best')
pymol.cmd.png(mutant+'liganded.png',1500,1000,300)
pymol.cmd.save(output+''.join(mutant)+'_ESO.pse')
#with transparency
#pymol.cmd.set('stick_transparency',0.8,'top10')
#pymol.cmd.set('transparency',0.3,'receptor')
#pymol.cmd.png(mutant+'apo-transparent.png',1500,1000,300)
#pymol.cmd.set('stick_transparency',0.8,'top10')
#pymol.cmd.set('stick_transparency',0,'best')
#pymol.cmd.png(mutant+'liganded-transparent.png',1500,1000,300)
