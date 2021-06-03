#!/bin/bash
#./scripts/commandline.sh @input_files/enzdes.xml input_files/1cex.pdb TESTv1 BHET
ROSETTA=/home/ubuntu/Downloads/rosetta_bin_linux_2020.08.61146_bundle
DESIGN_HOME=/home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes
SERVER='ProteinEngineer 16CPU'

NAME=$2
LIGAND=$3
END_MID=$5

mkdir output/$NAME
mkdir output/$NAME/PDB
mv *.pdb output/$NAME/PDB/
mv *.sc output/$NAME/
exit 1
echo $END
echo $NSTRUCT
echo $NPROC
ENZYME='1CEX'
RESDIR=input_files/experiments/REF/$ENZYME/
cd $DESIGN_HOME
for RESFILE in $RESDIR/*
do
    FILENAME="$(basename $RESFILE)"
    echo $FILENAME
    (enzyme_design.static.linuxgccrelease -nstruct 1 @input_files/experiments/$ENZYME/${LIGAND}${END_MID}/${LIGAND}_design${END_MID}_ref.flags -database $ROSETTA/main/database/ -out::overwrite -out:file:o scorefile_$FILENAME.sc -out::suffix $FILENAME -s $1 -resfile /home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes/$RESFILE > enzyme_design_$FILENAME.log)&
done
enzyme_design.static.linuxgccrelease -nstruct 1 @input_files/experiments/$ENZYME/${LIGAND}${END_MID}/${LIGAND}_design${END_MID}_ref.flags -database $ROSETTA/main/database/ -out::overwrite -out:file:o scorefile_$FILENAME.sc -out::suffix wt -s $1 -resfile /home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes/input_files/resfile_wt > enzyme_design_wt.log
ipython /home/ubuntu/check.py 0.1 enzyme.s "$SERVER: EnzymeDesign for references ${LIGAND}${END_MID} is done!" $0
