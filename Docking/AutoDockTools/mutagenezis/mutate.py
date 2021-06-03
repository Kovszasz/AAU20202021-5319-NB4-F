from pyrosetta import *
from pyrosetta.teaching import *
import yaml
from pyrosetta.rosetta.core.io.pdb import dump_pdb
import matplotlib.pyplot as plt
import numpy as np
import pickle
init()

with open('config.yaml') as c:
    config = yaml.load(c)

def binary_saver(obj,name): #We store the results and other important variables binary. It is easer and faster to read and save.
    f=''
    outfile=open(f+name,'wb')
    pickle.dump(obj,outfile)
    outfile.close()


AMINOACIDS={
	'A':'ALA',
	'R':'ARG',
	'N':'ASN',
	'D':'ASP',
	'B':'ASX',
	'C':'CYS',
	'E':'GLU',
	'Q':'GLN',
	'Z':'GLX',
	'G':'GLY',
	'H':'HIS',
	'I':'ILE',
	'L':'LEU',
	'K':'LYS',
	'M':'MET',
	'F':'PHE',
	'P':'PRO',
	'S':'SER',
	'T':'THR',
	'W':'TRP',
	'Y':'TYR',
	'V':'VAL'
	}

#Plot variables
mutants=[]
energies=[]


AAsequence = config['MUTAGENEZIS']
pdb = config['INPUT']['PDB']
AA={}
TRESHOLD=1000

base_pos=16
pose=pose_from_pdb(pdb+'.pdb')
#pymover = PyMOLMover()
#pymover.apply(pose)
scorefxn = get_fa_scorefxn() 
#pymover.send_energy(pose)
#pymover.send_energy(pose, fa_elec)
#pymover.update_energy(True) 
#pymover.apply(pose)
#pyobs = PyMOLObserver()
#pyobs.add_type(pyobs.energy_observer)
#pyobs.attach(pose)
#Energy minimization
movemap = MoveMap()
movemap.set_bb(True)
#scorefxn = create_score_function('talaris2014')
tolerance = 0.01
min_type = 'dfpmin'
minmover = MinMover(movemap, scorefxn, min_type, tolerance, True)
reference_pose = pose.clone()
minmover.apply(reference_pose)
reference=scorefxn(reference_pose)
print('WT minimized energy:\t',reference)
def change(ref,mutant):
    return ref-mutant

def evaluate_feasibility(mutant,mutation_positions):
    #Side-chain packaging
    print('Side-chain packaging starts')
    task_pack = standard_packer_task(mutant)
    task_pack.restrict_to_repacking()
    task_pack.temporarily_fix_everything()
    if len(mutation_positions)>0:
        for pos in mutation_positions:
            task_pack.temporarily_set_pack_residue(pos-base_pos, True)
        pack_mover = PackRotamersMover(scorefxn, task_pack)
        pack_mover.apply(mutant)
    minmover.apply(mutant)
    mutant_energy_score = scorefxn(mutant)
    print('Mutant energy after rotamer mover\t:',mutant_energy_score)
    if abs(change(reference,mutant_energy_score))< TRESHOLD:
        return mutant_energy_score
    else:
        return False

def mutate(mutation):
    mutant = pose.clone()
    mutation_positions=[]
    filename=''
    label=''
    for point_mutation in mutation:
        toolbox.mutants.mutate_residue( mutant, point_mutation['pos']-base_pos, point_mutation['aa'])
        mutation_positions.append(point_mutation['pos'])
        filename=filename+str(point_mutation['pos'])+point_mutation['aa']+'_'
        #label=label+point_mutation['from']+str(point_mutation['pos'])+point_mutation['aa']+'_'
        label=label+str(point_mutation['pos'])+point_mutation['aa']+'_'
    eval_=evaluate_feasibility(mutant,mutation_positions)
    if eval_:
        #print(mutant.sequence())
        dump_pdb(mutant,'../docking/input_receptors/'+pdb+'_'+filename+'.pdb')
    energies.append(reference-eval_)
    l=label.replace('_','+')
    if len(l)<2:
        l='WT_'
    mutants.append(l[:-1])
#MonteCarlo simulations
#kT = 1.0
#mc = MonteCarlo(scorefxn=scorefxn, init_pose=pose,temperature=kT)
#mc.boltzmann(pose)
#dmutate_residue( pose, 182, 'A')

for mutant in AAsequence:
	mutate(mutant['MUTANT'])

plt.gcf().subplots_adjust(bottom=0.15)

fig = plt.figure()
ax=fig.add_subplot()
plt.xticks(rotation=45)
ax.bar(mutants,energies)
ax.set_ylabel('\u0394\u0394G[kcal/mol]')
ax.set_xticks(np.arange(len(mutants)))
plt.tight_layout()
plt.savefig('mutation_ddG_energies.png')