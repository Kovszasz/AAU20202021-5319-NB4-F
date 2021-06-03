#!/bin/bash
#./scripts/commandline.sh @input_files/enzdes.xml input_files/1cex.pdb TESTv1 BHET
ROSETTA=/home/ubuntu/Downloads/rosetta_bin_linux_2020.08.61146_bundle
DESIGN_HOME=/home/ubuntu/Thesis/RosettaDesign/small_molecule_interface_design/enzdes
SERVER='ProteinEngineer 16CPU'

NAME=$2
LIGAND=$3
END_MID=$4
#enzyme_design.static.linuxgccrelease -nstruct 10 -parser:protocol $1 @input_files/$LIGAND_design.flags -database $ROSETTA/main/database/ -out::overwrite -out:file:o scorefile.sc -s $2
###rosetta_scripts.static.linuxgccrelease -nstruct 10 -parser:protocol $1 @input_files/enzdes_flags -database $ROSETTA/main/database/ -out::overwrite -out:file:o scorefile.sc -s $2
NPROC=`grep 'physical id' /proc/cpuinfo | sort -u | wc -l`
END=`expr $NPROC - 1`
NSTRUCT=`expr 10000 / $END`
echo $END
echo $NSTRUCT
echo $NPROC

######## ----- POST PROCESSING ------- ###############
#Generate filter tresholds
python3.6 scripts/set_filter_values.py --scorefile output/$NAME/scorefile.sc --export_as_req_file input_files/experiments/1CEX/${LIGAND}${END_MID}/default_req_filter1.txt --specify_filter_params SR_6_interf_E_1_2, --filter_rate 1

mv *.sc output/$NAME
./scripts/DesignSelect.pl -d output/$NAME/scorefile.sc -c input_files/experiments/1CEX/${LIGAND}${END_MID}/default_req_filter1.txt -tag_column last > output/$NAME/filtered_designs.sc 
awk 'FNR > 1 {printf $NF ".pdb\n"}' output/$NAME/filtered_designs.sc > output/$NAME/filtered_pdbs.txt
####### ------ FAST RELAXATION ------- #############
cd $DESIGN_HOME/output/$NAME/PDB
mpirun relax.mpi.linuxgccrelease -out:suffix _relaxed @$DESIGN_HOME/input_files/experiments/1CEX/${LIGAND}${END_MID}/fast_relax_flags -out::overwrite -out:file:o scorefile_relax.sc -list ../filtered_pdbs.txt  > ../fast_relaxation.log
wait $process_id
#curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"$SERVER : FastRelaxation is done!\"}" --url 'https://api.spontit.com/v3/push'
cd $DESIGN_HOME/output/$NAME/PDB
ls *_relaxed_0001.pdb > ../relaxed_filtered_pdbs.txt

##### ------- INTERFACE ANALYZER ------- #########
mpirun InterfaceAnalyzer.mpi.linuxgccrelease -interface A_X -compute_packstat -pack_separated -score:weights ligandprime -no_nstruct_label -out:file:score_only ../design_interfaces_pre.sc -l ../relaxed_filtered_pdbs.txt -extra_res_fa ../../../input_files/experiments/1CEX/${LIGAND}${END_MID}/$LIGAND.params  -overwrite> ../interface_analysis.log
wait $process_id
#curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"$SERVER : InterfaceAnalyzer is done!\"}" --url 'https://api.spontit.com/v3/push'
cd $DESIGN_HOME
rm output/$NAME/*.fasta
tail --lines=+2 output/$NAME/design_interfaces_pre.sc > output/$NAME/design_interfaces.sc
python3.6 scripts/set_filter_values.py --scorefile output/$NAME/design_interfaces.sc --export_as_req_file input_files/experiments/1CEX/${LIGAND}${END_MID}/default_req_filter2.txt --specify_filter_params dG_separated, --score_file_sorting dG_separated --filter_rate 1
./scripts/DesignSelect.pl -d output/$NAME/design_interfaces.sc -c input_files/experiments/1CEX/${LIGAND}${END_MID}/default_req_filter2.txt -tag_column last > output/$NAME/postprocessed_designs.sc
awk -v NAME=$NAME '{printf "output/" NAME "/PDB/" $NF ".pdb\n"}' output/$NAME/postprocessed_designs.sc > output/$NAME/pre_postprocessed_pdbs.txt
find output/BHET_v2/PDB/ -type f -name "*.pdb" -regextype posix-awk -not -regex ".*_relaxed_*." > output/$NAME/all_original_pdb.txt
/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py output/$NAME/${LIGAND}${END_MID}_all output/$NAME/all_original_pdb.txt >  output/$NAME/all_original_distance.txt
/home/ubuntu/Downloads/pymol/bin/python3 scripts/InterfaceAnalyzer.py output/$NAME/${LIGAND}${END_MID}_filtered output/$NAME/pre_postprocessed_pdbs.txt > output/$NAME/postprocessed_pdbs.txt
#exit 1
######## ----- BIOINFORMATICAL ANALYSIS ------- ###############
cat output/$NAME/postprocessed_pdbs.txt | awk -F_ '{print $2}' | sed 's/....$//g' > output/$NAME/output_file_tags
cat output/$NAME/postprocessed_pdbs.txt | xargs -n1 -P1 -I% \
bash -c "$ROSETTA/tools/protein_tools/scripts/clean_pdb.py --nopdbout output/$NAME/PDB/% A"
mv *.fasta output/$NAME
cat output/$NAME/*.fasta > output/$NAME/designed_sequences.fasta
bash -c "$ROSETTA/tools/protein_tools/scripts/clean_pdb.py --nopdbout $1 A"
mv *.fasta output/$NAME
cat output/$NAME/*$LIGAND*.fasta > output/$NAME/designed_sequences_with_native.fasta
###-------ONLY THE MUTATIONS-------#######
ipython scripts/fastareducer.py input_files/resfile output/$NAME/designed_sequences
ipython scripts/fastareducer.py input_files/resfile output/$NAME/designed_sequences_with_native
cd output/$NAME
/home/ubuntu/Downloads/seq2logo-2.1/Seq2Logo.py -S 17 -f  designed_sequences.fasta
/home/ubuntu/Downloads/seq2logo-2.1/Seq2Logo.py -p 1800x500 -f designed_sequences_only_mutations.fasta
#(clustalw2 -align -infile=designed_sequences.fasta -outfile=designed_sequences.aln>clustal_log.log)&
#mpirun clustalw-mpi -align -infile=designed_sequences.fasta -outfile=designed_sequences.aln>clustal_log.log
#wait $process_id
#mpirun clustalw-mpi -align -infile=designed_sequences_only_mutations.fasta -outfile=designed_sequences_only_mutations.aln>clustal_log.log
#wait $process_id
#curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"$SERVER : MSA is done!\"}" --url 'https://api.spontit.com/v3/push'

#ipython /home/ubuntu/check.py 0.1 clustalw2 "MSA is done!"

####-----  PLOTTING ------###### https://www.rosettacommons.org/demos/latest/tutorials/analysis/Analysis#the-score-file
###PLOT original####
cd $DESIGN_HOME
$ROSETTA/main/tools/protein_tools/scripts/score_vs_rmsd.py --native $1 output/$NAME/PDB/*_@\([0-9]|[0-9][0-9]|[0-9][0-9][0-9]\).pdb --term=total --table="output/$NAME/rmsd_score_all.txt"
sort -n -k2 output/${NAME}/rmsd_score_all.txt | awk '{print $2 "\t" $3 "\t" $NF}' > output/${NAME}/score_rmsd_all.dat
gnuplot -e "set terminal png size 400,300; set output 'output/${NAME}/${NAME}_score_vs_RMSD_all.png'; plot 'output/${NAME}/score_rmsd_all.dat' u 2:1;"

###PLOT filtered###
$ROSETTA/main/tools/protein_tools/scripts/score_vs_rmsd.py --native $1 output/$NAME/PDB/*_relaxed_* --term=total --table="output/$NAME/rmsd_score.txt"
sort -n -k2 output/${NAME}/rmsd_score.txt | awk '{print $2 "\t" $3 "\t" $NF}' > output/${NAME}/score_rmsd.dat
gnuplot -e "set terminal png size 400,300; set output 'output/${NAME}/${NAME}_score_vs_RMSD.png'; plot 'output/${NAME}/score_rmsd.dat' u 2:1;"


############ ----------- RANDOM SCRIPTS  --------------- ####################
#enzyme_design.static.linuxgccrelease -nstruct 10 -parser:protocol input_files/enzdes.xml @input_files/enzdes_flags -database /home/ubuntu/Downloads/rosetta_bin_linux_2020.08.61146_bundle/main/database/ -out::overwrite -out:file:o scorefile_TEST.sc -s input_files/1cex.pdb
#https://github.com/SiegelLab/core

#relax.static.linuxgccrelease  -out:suffix _relaxed @input_files/fast_relax_flags -out::overwrite -out:file:o scorefile_relax_TEST.sc -list test_pdbs.txt 
#(InterfaceAnalyzer.static.linuxgccrelease -interface A_X -compute_packstat -pack_separated -score:weights ligandprime -no_nstruct_label -out:file:score_only ../design_interfaces.sc -l ../filtered_pdbs.txt -extra_res_fa ../../../input_files/BHET.params > ../interface_analysis.log)&
#cat output/TESTv2/filtered_pdbs.txt | awk -F_ '{print $2}' | sed 's/....$//g' > output/TESTv2/output_file_tags

#cat output/TESTv2/filtered_pdbs.txt | xargs -n1 -P1 -I% \
#bash -c "/home/ubuntu/Downloads/rosetta_bin_linux_2020.08.61146_bundle/tools/protein_tools/scripts/clean_pdb.py --nopdbout output/TESTv2/PDB/% A"


####Rename pdb files
#n=1
#for entry in *.pdb
#do
#  cp $entry output/$NAME/PDB/1cex_$n.pdb
#  n=$(expr $n + 1)
#done
#rm *.pdb

#enzyme_design.static.linuxgccrelease -nstruct 1 @input_files/PET_design_mid.flags -database /home/ubuntu/Downloads/rosetta_bin_linux_2020.08.61146_bundle/main/database/ -out::overwrite -out:file:o scorefile.sc -s input_files/1cex_PET_mid.pdb 