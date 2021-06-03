#!/usr/bin/env python
# :noTabs=true:
# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available under license.
# (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org. Questions about this can be
# (c) addressed to University of Washington CoMotion, email: license@uw.edu.

## @file: compute_ddG.py
##
## @brief: 	 Compute ddGs of mutation
## @details: Use the Rosetta membrane framework to compute the ddG of unfolding of 
## a membrane protein in Rosetta (uses packer, mutate.py from Evan Baugh)
##
## @author: Rebecca F. Alford (rfalford12@gmail.com)

# Tools
import sys, os
#import commands
import random
from optparse import OptionParser, IndentedHelpFormatter
_script_path_ = os.path.dirname( os.path.realpath(__file__) )

# Rosetta-specific imports
import pyrosetta.rosetta.protocols.membrane
from pyrosetta import *
#from pyrosetta import create_score_function
from pyrosetta.rosetta.core.pack.task import TaskFactory
from pyrosetta.rosetta.utility import vector1_bool
from pyrosetta.rosetta.core.chemical import aa_from_oneletter_code
from pyrosetta.rosetta.protocols.minimization_packing import PackRotamersMover
from pyrosetta.rosetta.core.pose import PDBInfo
from pyrosetta.rosetta.core.chemical import VariantType
from pyrosetta.rosetta.core.import_pose import pose_from_file

###############################################################################

## @brief Main - Add Membrane to Pose, Compute ddG
def main( args ):
	
    parser = OptionParser(usage="usage: %prog [OPTIONS] [TESTS]")
    parser.set_description(main.__doc__)

    #input options
    parser.add_option('--in_pdb', '-p',
       action="store",
       help="Input PDB file.", )

    parser.add_option('--in_span', '-s',
       action="store",
       help="Input spanfile.", )
				  
    parser.add_option('--out', '-o',
       action="store", default='ddG.out',
       help="Output filename with pose residue numbering. Default: 'ddG.out'", )
									
    parser.add_option('--res', '-r',
       action="store",
       help="Pose residue number to mutate.", )

    parser.add_option('--mut', '-m',
       action="store",
       help="One-letter code of residue identity of the mutant. Example: A181F would be 'F'", )

    parser.add_option('--repack_radius', '-a', 
        action="store", default=0, 
        help="Repack the residues within this radius",)

    parser.add_option('--output_breakdown', '-b', 
        action="store", default="scores.sc", 
        help="Output mutant and native score breakdown by weighted energy term into a scorefile", )

    #parse options
    (options, args) = parser.parse_args(args=args[1:])
    global Options
    Options = options

    # Check the required inputs (PDB file, spanfile) are present
    if ( not Options.in_pdb or not Options.res ):
	    sys.exit( "Must provide flags '-in_pdb', and '-res'! Exiting..." )

    # Initialize Rosetta options from user options. 
    rosetta_options = " -run:constant_seed -in:ignore_unrecognized_res"
    init( extra_options=rosetta_options )
	
    # Load Pose, & turn on the membrane
    pose = pose_from_file( Options.in_pdb )

    # Add Membrane to Pose
    #add_memb = rosetta.protocols.membrane.AddMembraneMover()
    #add_memb.apply( pose )
    
    # Setup in a topology based membrane
    #init_mem_pos = rosetta.protocols.membrane.MembranePositionFromTopologyMover()
    #init_mem_pos.apply( pose )

    # check the user has specified a reasonable value for the pH
    sfxn = rosetta.core.scoring.ScoreFunction()

    # Create a smoothed membrane full atom energy function (pH 7 calculations)
    sfxn = create_score_function( "beta_nov15")


    res=[int(i)-16 for i in Options.res.split(',')[1::2]]
    mut=[i for i in Options.res.split(',')[0::2]]
    print('MUT!!!!!!:\t',mut)
    print(res)
    # Repack the native rotamer and residues within the repack radius 
    native_res=[]
    for r in res:
        native_res.append(pose.residue( r ).name1())
    repacked_native = mutate_residue( pose, res[0], native_res[0], Options.repack_radius, sfxn )
    if len(res)>1:
        for r in range(len(res[1:])):
            repacked_native = mutate_residue( repacked_native, res[r], native_res[r], Options.repack_radius, sfxn )

    # to output score breakdown, start by printing the score labels in
    # the top of the file
    print_score_labels_to_file( repacked_native, sfxn, Options.output_breakdown )

    # Compute mutations
    if ( mut ):
        with open( Options.out, 'a' ) as f:
            ddGs = compute_ddG( repacked_native, sfxn, res, mut, Options.repack_radius, Options.output_breakdown )
            f.write( Options.in_pdb + " " + Options.res + " " + str(ddGs[0]) + " " + str(ddGs[1]) + " " + str(ddGs[2]) + " " + str(ddGs[3]) + "\n" )
        f.close()
    else:
        AAs = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        for aa in AAs:
            with open( Options.out, 'a' ) as f:
                ddGs = compute_ddG( repacked_native, sfxn, int( Options.res ), aa, Options.repack_radius, Options.output_breakdown )
                f.write( str(ddGs[0]) + " " + str(ddGs[1]) + " " + str(ddGs[2]) + " " + str(ddGs[3]) + "\n" )
            f.close

###############################################################################

## @brief Compute ddG of mutation in a protein at specified residue and AA position
def compute_ddG( pose, sfxn, resnum, aa, repack_radius, sc_file ): 

    # Score Native Pose
    native_score = sfxn( pose )

    # Perform Mutation at residue <resnum> to amino acid <aa>
    #for mutation in resnum:
    mutated_pose = mutate_residue( pose, resnum[0], aa[0], repack_radius, sfxn )
    if len(resnum)>1:
        for m in range(len(resnum[1:])):
            mutated_pose = mutate_residue( mutated_pose, resnum[m], aa[m], repack_radius, sfxn )

    # Score Mutated Pose
    mutant_score = sfxn( mutated_pose )

    # If specified the user, print the breakdown of ddG values into a file  
    print_ddG_breakdown( pose, mutated_pose, sfxn, resnum, aa, sc_file )

	# return scores
    return aa, round( mutant_score, 3 ), round( native_score, 3 ), round ( mutant_score - native_score, 3 )

###############################################################################

# @brief Replace the residue at <resid> in <pose> with <new_res> and allows
# repacking within a given <pack_radius> 
def mutate_residue( pose, mutant_position, mutant_aa, pack_radius, pack_scorefxn ):

    if pose.is_fullatom() == False:
        IOError( 'mutate_residue only works with fullatom poses' )

    test_pose = Pose()
    test_pose.assign( pose )

    # Create a packer task (standard)
    task = TaskFactory.create_packer_task( test_pose )

    # the Vector1 of booleans (a specific object) is needed for specifying the
    #    mutation, this demonstrates another more direct method of setting
    #    PackerTask options for design
    aa_bool = vector1_bool()

    # PyRosetta uses several ways of tracking amino acids (ResidueTypes)
    # the numbers 1-20 correspond individually to the 20 proteogenic amino acids
    # aa_from_oneletter returns the integer representation of an amino acid
    #    from its one letter code
    # convert mutant_aa to its integer representation
    mutant_aa = aa_from_oneletter_code( mutant_aa )

    # mutation is performed by using a PackerTask with only the mutant
    #    amino acid available during design
    # to do this, construct a Vector1 of booleans indicating which amino acid
    #    (by its numerical designation, see above) to allow
    for i in range( 1 , 21 ):
        # in Python, logical expression are evaluated with priority, thus the
        #    line below appends to aa_bool the truth (True or False) of the
        #    statement i == mutant_aa
        aa_bool.append( i == mutant_aa )

    # modify the mutating residue's assignment in the PackerTask using the
    #    Vector1 of booleans across the proteogenic amino acids
    task.nonconst_residue_task( mutant_position
        ).restrict_absent_canonical_aas( aa_bool )

    # prevent residues from packing by setting the per-residue "options" of
    #    the PackerTask
    center = pose.residue( mutant_position ).nbr_atom_xyz()
    for i in range( 1, pose.total_residue() + 1 ): 
        dist = center.distance_squared( test_pose.residue( i ).nbr_atom_xyz() );  
        # only pack the mutating residue and any within the pack_radius
        if i != mutant_position and dist > pow( float( pack_radius ), 2 ) :
            task.nonconst_residue_task( i ).prevent_repacking()

    # apply the mutation and pack nearby residues
    packer = PackRotamersMover( pack_scorefxn , task )
    packer.apply( test_pose )

    return test_pose

###############################################################################
#@brief Print ddG breakdown from the pose
# Extract weighted energies from the native and mutated pose. Calculate the ddG
# of each and print the component-wise ddG vlaues
def print_ddG_breakdown( native_pose, mutated_pose, sfxn, resnum, aa, fn ): 

    # Extract scores
    tmp_native = native_pose.energies().total_energies().weighted_string_of( sfxn.weights() )
    tmp_mutant = mutated_pose.energies().total_energies().weighted_string_of( sfxn.weights() )

    # Parse out scores
    array_native = list(filter( None, tmp_native.split(' ') ))
    array_mutant = list(filter( None, tmp_mutant.split(' ') ))

    # Pull out only the scores from these arrays
    native_scores = []
    for i in range( len(array_native) ): 
        if ( i % 2 != 0 ): 
            native_scores.append( float( array_native[i] ) )

    mutant_scores = []
    for i in range( len(array_mutant) ): 
        if ( i % 2 != 0 ): 
            mutant_scores.append( float( array_mutant[i] ) )

    # Make a label for the mutation
    res=res=[int(i)-16 for i in Options.res.split(',')[1::2]]
    native_res=[]
    for r in res:
        native_res.append(native_pose.residue( r ).name1())
    mut_label=''
    for nr in range(len(native_res)):
        mut_label =mut_label+','+ native_res[nr] + str(resnum[nr]) + aa[nr]

    # Calculate ddG of individual components
    ddGs = []
    ddGs.append( mut_label )
    for i in range( len( mutant_scores ) ): 
        ddG_component = mutant_scores[i] - native_scores[i]
        ddGs.append( round( ddG_component, 3 ) )

    ddGs_str = convert_array_to_str( ddGs ) 
    with open( fn, 'a' ) as f:
        f.write( ddGs_str + "\n" )
    f.close()

###############################################################################
#@brief Get header for ddG breakdown output
# Save the score labels, to be printed at the top of the output breakdown file
def print_score_labels_to_file( native_pose, sfxn, fn ): 

    tmp_native = native_pose.energies().total_energies().weighted_string_of( sfxn.weights() )
    array_native = filter( None, tmp_native.split(' ') )
    array_native=list(array_native)
    labels = []
    labels.append( 'mutation ' ) # Append field for mutation label
    for i in range( len(list(array_native)) ): 
        if ( i % 2 == 0 ): 
            
            labels.append( array_native[i].translate(str.maketrans('','',':')) )

    labels_str = convert_array_to_str( labels )
    with open( fn, 'a' ) as f:
        f.write( labels_str + "\n" )
    f.close()


###############################################################################
#@brief Convert an array to a space deliminted string
# Save the score labels, to be printed at the top of the output breakdown file
def convert_array_to_str( array ): 

    linestr = ""
    for elem in array: 
        if ( linestr == "" ): 
            linestr = linestr + str( elem )
        else: 
            linestr = linestr + " " + str( elem )

    return linestr


if __name__ == "__main__" : main(sys.argv)
