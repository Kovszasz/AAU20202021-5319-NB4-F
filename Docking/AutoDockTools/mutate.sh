#!/bin/bash
cd mutagenezis
ipython csv2yaml.py
python3.6 mutate.py
cd ../docking
ipython docking_screening.py
#ipython global_visualization.py /home/ubuntu/Thesis/PyRosetta_AutoDockTools/docking/outputs | cat state.txt
ipython global_visualization.py /home/ubuntu/Thesis/PyRosetta_AutoDockTools/docking/outputs 1