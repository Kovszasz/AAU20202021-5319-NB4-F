#!/bin/bash
#./scripts/commandline.sh input_files/1cex_PET_mid_c_D80.pdb  D80
#mv output output_T80D
#mv *.pdb output_T80D
#OUTPUT=output_T80D
#ls $OUTPUT/*.pdb > $OUTPUT/docked_pdbs.txt
#/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py $OUTPUT $OUTPUT/docked_pdbs.txt > T80D_dist.txt
#mkdir output
#./scripts/commandline.sh input_files/1cex_PET_mid_c_R82_D18.pdb  D18R82
#mv output output_R82_D18
#mv *.pdb output_R82_D18

#OUTPUT=output_R82_D18
#ls $OUTPUT/*.pdb > $OUTPUT/docked_pdbs.txt
#/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py $OUTPUT $OUTPUT/docked_pdbs.txt > R82_D18_dist.txt
#mkdir output
#./scripts/commandline.sh input_files/1cex_PET_mid_c_R82_L151_D18.pdb D18R82L151
#mv output output_R82_L151_D18
#mv *.pdb output_R82_L151_D18
#OUTPUT=output_R82_L151_D18
#ls $OUTPUT/*.pdb > $OUTPUT/docked_pdbs.txt
#/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py $OUTPUT $OUTPUT/docked_pdbs.txt > R82_L151_D18_dist.txt

#mkdir output
#./scripts/commandline.sh input_files/1cex_c.pdb WT
#mv output output_WT
#mv *.pdb output_WT
#OUTPUT=output_WT
#ls $OUTPUT/*.pdb > $OUTPUT/docked_pdbs.txt
#/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py $OUTPUT $OUTPUT/docked_pdbs.txt > WT_dist.txt

#mkdir output
#./scripts/commandline5xjh.sh input_files_PETase/5xjh.pdb PETase
#mv output output_PETase
#mv *.pdb output_PETase
OUTPUT=output_PETase
ls $OUTPUT/*.pdb > $OUTPUT/docked_pdbs.txt
/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py $OUTPUT $OUTPUT/docked_pdbs.txt > PETase_dist.txt
