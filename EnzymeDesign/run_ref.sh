#!/bin/bash
#./scripts/reference.sh input_files/experiments/1CEX/BHET/1cex_BHET_c.pdb BHET_selected_no_movemap_v1 BHET enzyme_design 
#./scripts/reference.sh input_files/experiments/1CEX/PET_mid/1cex_PET_mid_c.pdb PET_mid_selected_no_movemap_v1 PET enzyme_design _mid
#./scripts/reference.sh input_files/experiments/1CEX/PET_end/1cex_PET_end_c.pdb PET_end_selected_no_movemap_v1 PET enzyme_design _end
#./scripts/postprocessing_ref.sh input_files/experiments/1CEX/BHET/1cex_BHET_c.pdb BHET_selected_no_movemap_v1 BHET
#./scripts/postprocessing_ref.sh input_files/experiments/1CEX/PET_mid/1cex_PET_mid_c.pdb PET_mid_selected_no_movemap_v1 PET _mid
#./scripts/postprocessing_ref.sh input_files/experiments/1CEX/PET_end/1cex_PET_end_c.pdb PET_end_selected_no_movemap_v1 PET _end

./scripts/apbs.sh output_exp PET_end
#./scripts/apbs.sh PET_end_selected_no_movemap_v1 PET_end
#./scripts/apbs.sh PET_mid_selected_no_movemap_v1 PET_mid
#./ddg.sh
#------for PETase-------#
#./scripts/reference.sh input_files/experiments/5XJH/BHET/5xjh_BHET_c.pdb BHET_ref_5xjh_v3 BHET enzyme_design 
#./scripts/reference.sh input_files/experiments/5XJH/PET_mid/5xjh_PET_mid_c.pdb PET_mid_ref_5xjh_v3 PET enzyme_design _mid
#./scripts/reference.sh input_files/experiments/5XJH/PET_end/5xjh_PET_end_c.pdb PET_end_ref_5xjh_v3 PET enzyme_design _end
#./scripts/postprocessing_ref.sh input_files/experiments/5XJH/BHET/5xjh_BHET_c.pdb BHET_ref_5xjh_v3 BHET
#./scripts/postprocessing_ref.sh input_files/experiments/5XJH/PET_mid/5xjh_PET_mid_c.pdb PET_mid_ref_5xjh_v3 PET _mid
#./scripts/postprocessing_ref.sh input_files/experiments/5XJH/PET_end/5xjh_PET_end_c.pdb PET_end_ref_5xjh_v3 PET _end
