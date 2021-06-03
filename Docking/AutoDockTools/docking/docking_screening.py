
import os,sys,subprocess
from os import listdir
from os.path import isfile, join
import asyncio
from bash import Command
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import traceback
import shlex
import shutil

ligand_path='input_ligands/'
receptor_path= 'input_receptors/'
pdbs = [f.replace('.pdb','') for f in listdir(receptor_path) if isfile(join(receptor_path, f))]
ligands = [f.replace('.pdb','') for f in listdir(ligand_path) if isfile(join(ligand_path, f))]

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

RESIDUES_WITHIN_8A={
'1CEX':{
   "38":"TYR",
    "40":"ARG",
    "41":"GLY",
    "42":"SER",
    "43":"THR",
    "44":"GLU",
    "45":"THR",
    "48":"LEU",
    "49":"GLY",
    "50":"THR",
    "51":"LEU",
    "52":"GLY",
    "77":"TYR",
    "79":"ALA",
    "80":"THR",
    "81":"LEU",
    "82":"GLY",
    "83":"ASP",
    "84":"ASN",
    "85":"ALA",
    "89":"GLY",
    "119":"TYR",
    "120":"SER",
    "121":"GLN",
    "122":"GLY",
    "123":"ALA",
    "124":"ALA",
    "147":"PHE",
    "148":"GLY",
    "149":"TYR",
    "150":"THR",
    "175":"ASP",
    "176":"LEU",
    "177":"VAL",
    "178":"CYS",
    "181":"SER",
    "182":"LEU",
    "183":"ILE",
    "184":"VAL",
    "185":"ALA",
    "186":"ALA",
    "188":"HIS",
    "189":"LEU",
    "190":"ALA",
    "191":"TYR",
    "192":"GLY"
    },
    '5XJH':{
    '85':'PRO',
    '86':'GLY',
    '87':'TYR',
    '88':'THR',
    '89':'ALA',
    '90':'ARG',
    '93':'SER',
    '116':'THR',
    '117':'LEU',
    '118':'ASP',
    '119':'GLN',
    '120':'PRO',
    '123':'ARG',
    '159':'TRP',
    '160':'SER',
    '161':'MET',
    '162':'GLY',
    '163':'GLY',
    '164':'GLY',
    '183':'ALA',
    '184':'PRO',
    '185':'TRP',
    '186':'ASP',
    '187':'SER',
    '206':'ASP',
    '207':'SER',
    '208':'ILE',
    '209':'ALA',
    '210':'PRO',
    '214':'SER',
    '237':'HIS',
    '238':'SER',
    '241':'ASN'
    }
}

#cmd=['./run_screening.sh']
_1CEX={
    'BHET':{
        'center_x' : 12.4592459165,
        'center_y' : 58.018604641,
        'center_z' : 18.6816832525,
        'size_x' : 13,
        'size_y' : 12,
        'size_z' : 11,
    },
    '2HE_MHET_4':{
        'center_x' : 12.4592459165,
        'center_y' : 58.018604641,
        'center_z' : 18.6816832525,
        'size_x' : 90.7,
        'size_y' : 74.7,
        'size_z' : 122.7,
    },
    'PET':{
        'center_x' : 12.4592459165,
        'center_y' : 58.018604641,
        'center_z' : 18.6816832525,
        'size_x' : 26,
        'size_y' : 14,
        'size_z' : 22,
    }
}
_5XJH={
    'BHET':{
        'center_x' : -3.249,
        'center_y' : 25.239,
        'center_z' : -29.093,
        'size_x' : 13,
        'size_y' : 12,
        'size_z' : 11
        #'size_x' : 90.7,
        #'size_y' : 74.7,
        #'size_z' : 122.7,
    },
    '2HE_MHET_4':{
        'center_x' : -3.249,
        'center_y' : 25.239,
        'center_z' : -29.093,
        'size_x' : 90.7,
        'size_y' : 74.7,
        'size_z' : 122.7
    },
    'PET':{
        'center_x' : 12.4592459165,
        'center_y' : 58.018604641,
        'center_z' : 18.6816832525,
        'size_x' : 90.7,
        'size_y' : 74.7,
        'size_z' : 122.7,
    }
}
CONFIG={
    'receptor' : '',
    'ligand' : '',
    'cpu' : 16,
    'center_x' : 12.4592459165,
    'center_y' : 58.018604641,
    'center_z' : 18.6816832525,
    'size_x' : 13,
    'size_y' : 12,
    'size_z' : 11,
    'out' : ''
}

#ligands =['BHET']
space="40,40,46"
ga_num_evals ="250000"

def write_config(path,*args,**kwargs):
    f =open(path+'config.txt','w')
    for i in kwargs.keys():
        f.write(i+' = '+str(kwargs[i])+'\n')
    f.close()

def write_gpf_sample(path,receptor,receptor_meta,*args,**kwargs):
    content="""npts 40 40 46
gridfld {receptor}_rigid.maps.fld spacing 0.375
receptor_types A C HD N OA SA ligand_types C HD N A NA OA receptor {receptor}_rigid.pdbqt gridcenter {gridx} {gridy} {gridz} smooth 0.5
map {receptor}_rigid.C.map
map {receptor}_rigid.HD.map
map {receptor}_rigid.N.map
map {receptor}_rigid.A.map
map {receptor}_rigid.NA.map
map {receptor}_rigid.OA.map
elecmap {receptor}_rigid.e.map dsolvmap {receptor}_rigid.d.map dielectric -0.1465""".format(receptor=receptor,gridx=receptor_meta['center_x'],gridy=receptor_meta['center_y'],gridz=receptor_meta['center_z'])
    print(content)
    f =open(path+'sample.gpf','w')
    f.write(content)
    f.close()



def run_docking(cmd):
    subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return True

def run(command, timeout=None, **kwargs):
    """Run a command then return: (status, output, error)."""
    def target(**kwargs):
        try:
            command = shlex.split(command)
            print(command)
            process = subprocess.Popen(command, **kwargs)
            output, error = process.communicate()
            status = process.returncode
        except:
            error = traceback.format_exc()
            status = -1
    # default stdout and stderr
    if 'stdout' not in kwargs:
        kwargs['stdout'] = subprocess.PIPE
    if 'stderr' not in kwargs:
        kwargs['stderr'] = subprocess.PIPE
    # thread
    thread = threading.Thread(target=target, kwargs=kwargs)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        process.terminate()
        thread.join()
    return status, output, error


@asyncio.coroutine
def main(operation,arg):
    yield from loop.run_in_executor(p,operation ,arg )

def get_residues(pdb,pdbtype):
    name=pdb.split('_')
    name.pop(0)
    name.pop()
    result_string=''
    for mutation in name:
        RESIDUES_WITHIN_8A[pdbtype][mutation[:-1]]=AMINOACIDS[mutation[-1]]
    for res in RESIDUES_WITHIN_8A[pdbtype].keys():
        result_string=result_string+RESIDUES_WITHIN_8A[pdbtype][res]+res+','
    return result_string[:-1]


p = ProcessPoolExecutor(16) # Create a ProcessPool with 2 processes
pool = multiprocessing.Pool(16)
#pdbs=['hsg1']
command = Command()
for ligand in ligands:
    for pdb in pdbs:
        #cmd=['./run_screening.sh']
        cmd='./run_screening.sh'
        print('Docking:\t',pdb,' with:\t',ligand)
        if os.path.exists('outputs/'+pdb+'_'+ligand):
            shutil.rmtree('outputs/'+pdb+'_'+ligand)
        os.mkdir('outputs/'+pdb+'_'+ligand)
        receptor = pdb
        if receptor =='5XJH_':
            receptor_meta = _5XJH[ligand]
            #flexible_residues ="TYR87,TRP159,SER160,MET161,TRP185,ILE208,HIS237,SER238,ASN241"
            #flexible_residues ="TYR38,ARG40,GLY"
            flexible_residues = get_residues(receptor,'5XJH')
        else:
            receptor_meta = _1CEX[ligand]
            flexible_residues = get_residues(receptor,'1CEX')
        config = CONFIG
        config['ligand']=ligand+'.pdbqt'
        config['receptor']=receptor+'.pdbqt'
        config['out']=ligand+'_vina.pdbqt'
        config['center_x']=receptor_meta['center_x']
        config['center_y']=receptor_meta['center_y']
        config['center_z']=receptor_meta['center_z']
        config['size_x']=receptor_meta['size_x']
        config['size_y']=receptor_meta['size_y']
        config['size_z']=receptor_meta['size_z']
        write_config('outputs/'+receptor+'_'+ligand+'/',**CONFIG)
        write_gpf_sample('outputs/'+receptor+'_'+ligand+'/',receptor,receptor_meta)
        for i in [ligand,receptor,space,ga_num_evals,flexible_residues]:
            #cmd.append(i)
            cmd=cmd+' '+i
        #commands.append(cmd)
        #t=threading.Thread(target=run_docking,kwargs={'thread':'Thread_'+pdb,'cmd':cmd})
        #t.start()
        print(cmd)
        command.add_command(cmd)
    
    #run_docking(cmd)

    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main(command.run,cmd))
pool.map(command.run, command.commands)

