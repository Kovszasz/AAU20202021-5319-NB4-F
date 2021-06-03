#!/bin/bash
./scripts/commandline.sh input_files/experiments/1CEX/BHET/1cex_BHET_c.pdb TEST_cst BHET enzyme_design
#./scripts/commandline.sh input_files/experiments/1CEX/PET_mid/1cex_PET_mid_c.pdb PET_mid_v4 PET enzyme_design _mid
#./scripts/commandline.sh input_files/experiments/1CEX/PET_end/1cex_PET_end_c.pdb PET_end_v4 PET enzyme_design _end
#./scripts/postprocessing.sh input_files/experiments/1CEX/BHET/1cex_BHET_c.pdb BHET_v4 BHET
#./scripts/postprocessing.sh input_files/experiments/1CEX/PET_mid/1cex_PET_mid_c.pdb PET_mid_v4 PET _mid
#./scripts/postprocessing.sh input_files/experiments/1CEX/PET_end/1cex_PET_end_c.pdb PET_end_v4 PET _end
#curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"Postprocessing is done!\"}" --url 'https://api.spontit.com/v3/push'