
#!/bin/bash
#./scripts/commandline.sh @input_files/enzdes.xml input_files/1cex.pdb TESTv1 BHET
ROSETTA=/home/ubuntu/Downloads/rosetta_bin_linux_2020.08.61146_bundle
DESIGN_HOME=/home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes
SERVER='ProteinEngineer 16CPU'

NAME=$2
LIGAND=$3
END_MID=$5
#enzyme_design.static.linuxgccrelease -nstruct 10 -parser:protocol $1 @input_files/$LIGAND_design.flags -database $ROSETTA/main/database/ -out::overwrite -out:file:o scorefile.sc -s $2
###rosetta_scripts.static.linuxgccrelease -nstruct 10 -parser:protocol $1 @input_files/enzdes_flags -database $ROSETTA/main/database/ -out::overwrite -out:file:o scorefile.sc -s $2
#NPROC=`grep 'physical id' /proc/cpuinfo | sort -u | wc -l`
#END=`expr $NPROC - 1`
#NSTRUCT=`expr 10000 / $END`
echo $END
echo $NSTRUCT
echo $NPROC
ENZYME='1CEX'
RESDIR=input_files/experiments/REF/$ENZYME/
#####Calculating ddG values of the mutations
for RESFILE in $RESDIR/*
do
    FILENAME="$(basename $RESFILE)"
    echo $FILENAME
    python3.6 scripts/ddG.py --in_pdb /home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes/input_files/native_pdbs/1cex.pdb --res $FILENAME --repack_radius 8.0 
done



