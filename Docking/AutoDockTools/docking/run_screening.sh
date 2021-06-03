#!/bin/bash
VINA=/home/ubuntu/Downloads/autodock_vina_1_1_2_linux_x86/bin/vina
HOME=/home/ubuntu/Thesis/PyRosetta_AutoDockTools/
AUTODOCK=/home/ubuntu/Downloads/autodocksuite/autodock4
AUTOGRID=/home/ubuntu/Downloads/autodocksuite/autogrid4
APBS=/home/ubuntu/Downloads/pymol/bin/apbs
PDB2PQR=/home/ubuntu/Downloads/pymol/bin/pdb2pqr
OUTPUT_PATH=outputs/$2_$1
PDB_PATH=input_receptors/
LIGAND_PATH=input_ligands/
prepare_ligand4.py -l $LIGAND_PATH/$1.pdb -o $OUTPUT_PATH/$1.pdbqt
prepare_receptor4.py -r $PDB_PATH/$2.pdb -A hydrogens -o $OUTPUT_PATH/$2.pdbqt
prepare_flexreceptor4.py -r $OUTPUT_PATH/$2.pdbqt -s $5 -g $OUTPUT_PATH/$2_rigid.pdbqt -x $OUTPUT_PATH/$2_flex.pdbqt
prepare_gpf4.py -l $OUTPUT_PATH/$1.pdbqt -r $OUTPUT_PATH/$2_rigid.pdbqt -x $OUTPUT_PATH/$2_flex.pdbqt  -p npts=$3 -i $OUTPUT_PATH/sample.gpf -o $OUTPUT_PATH/$2.gpf
prepare_dpf4.py -l $OUTPUT_PATH/$1.pdbqt -r $OUTPUT_PATH/$2.pdbqt -p ga_num_evals=$4 -o $OUTPUT_PATH/$1.dpf
cd $OUTPUT_PATH
$AUTOGRID -p $2.gpf -l $2.glg
$AUTODOCK -p $1.dpf -l $1.dlg
$VINA --config config.txt >vina.log
$PDB2PQR --ff=AMBER --chain ../../$PDB_PATH/$2.pdb receptor.pqr
$APBS ../../../apbs.in
cd $HOME/docking
./visualize.py $OUTPUT_PATH/ outputs/analyze/ $1 $2

