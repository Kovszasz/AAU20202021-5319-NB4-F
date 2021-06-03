#!/bin/bash

APBS=/home/ubuntu/Downloads/pymol/bin/apbs
PDB2PQR=/home/ubuntu/Downloads/pymol/bin/pdb2pqr
DESIGN_HOME=/home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes
OUTPUT=output/$1
cd $DESIGN_HOME

#mkdir output/$1/APBS
#mkdir output/$1/PSE

for PDB in $OUTPUT/PDB/*_relaxed_0001.pdb
do
    FILENAME="$(basename $PDB)"
    ./scripts/decompose_pdb.py $PDB
    APO=$(echo "$FILENAME" | sed "s/.pdb/_apo.pdb/")
    LIGAND=$(echo "$FILENAME" | sed "s/.pdb/_ligand.pdb/")
    $PDB2PQR --ff=AMBER --chain $APO receptor.pqr
    $APBS input_files/apbs.in
    mv map.dx $APO.dx
    mv receptor.pqr $APO.pqr
    mv *.dx $OUTPUT/APBS/
    mv *.pqr $OUTPUT/APBS/
    ./scripts/visualize.py $OUTPUT/APBS/$APO.pqr $FILENAME $2 $OUTPUT/APBS/$APO.dx $LIGAND
    rm *.pdb
    mv *.pse $OUTPUT/PSE/
    mv *.png $OUTPUT/PSE/
done