import sys
from Bio import SeqIO
from Bio.Seq import Seq
path_to_resfile=sys.argv[1]
path_to_fasta=sys.argv[2]
base=17
mutation_positions=[]
with open(path_to_resfile,'r') as rf:
    for pos in rf:
        pos=pos.split(' ')
        try:
            p=int(pos[0])
            mutation_positions.append(p)
        except:
            pass

def record2mutant(record):
    return_string=''
    for m in mutation_positions:
        return_string=return_string+record.seq[m-base]
    return return_string

fasta=SeqIO.parse(path_to_fasta+'.fasta',"fasta")

new_sequences=[]
for record in fasta:
    record.seq=Seq(record2mutant(record))
    new_sequences.append(record)



SeqIO.write(new_sequences, path_to_fasta+'_only_mutations.fasta', "fasta")