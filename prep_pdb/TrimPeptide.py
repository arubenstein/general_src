#!/usr/bin/python


from rosetta import *
from toolbox import cleanATOM


init('-mute core.pack.task core.conformation.Conformation')
from rosetta.core.conformation import *
import os
import sys
from rosetta.core.pose import PDBInfo

def main(argv):

    #open list of pdbs
    with open(argv[0]) as afile:
        pdbs = afile.readlines()
    
    #open chain id dictionary
    with open(argv[1]) as afile:
        d = { item[0] : [item[1].split(","),item[2].split(","),item[3].split(","),item[4],item[5]] for item in (line.split() for line in afile) }

    #loop through pdbs
    for p in pdbs:
        #get the pdb name of the pdb in question
	basename_p = os.path.basename(p).rstrip()

	#create lists of chain ids from d
	all_chains = d[basename_p][0]
	prot_chains = d[basename_p][1]
	pept_chains = d[basename_p][2]

	#clean pdb
        cleanATOM(p.rstrip())
	
	#new filename consisting of the path name + .clean.pdb
	filename = p.rsplit('.',1)[0] + ".clean.pdb"
	
	#input the pose, split it by chain, and create a new pose with the correct PDBInfo
        pose = pose_from_pdb(filename.rstrip())
        pose.update_pose_chains_from_pdb_chains()
	
        chains=pose.split_by_chain()
	print len(chains)
	newpose = Pose()
	newpose.pdb_info( PDBInfo( newpose ) )

	#iterate through all chains in protein by iterating through the list of all_chains
	#if chain is found in list of protein chains append it to newpose by appending after seqpos
	pdb_counter = 0
	for idx, chain in enumerate(all_chains): 
	    if chain in prot_chains: 
		newpose.append_residue_by_jump(chains[idx+1].residue(1),newpose.total_residue(),"","",0)
        	pdb_counter+=1
		newpose.pdb_info().number(newpose.total_residue(),pdb_counter)
                newpose.pdb_info().chain(newpose.total_residue(),'A')
		for i in range(2,chains[idx+1].total_residue()+1):
                    newpose.append_polymer_residue_after_seqpos(chains[idx+1].residue(i), newpose.total_residue(),0)
		    pdb_counter+=1
                    newpose.pdb_info().number(newpose.total_residue(),pdb_counter)
	            newpose.pdb_info().chain(newpose.total_residue(),'A')
	
	#then check list of peptide chains and append to newpose after jump
	idx_pept = all_chains.index( pept_chains[0])+1
	
	#determine which res to start and end from using the dict
	pdb_num_res_start = int(d[basename_p][3])
	pdb_num_res_end = int(d[basename_p][4])
	
	num_res_start = chains[ idx_pept ].pdb_info().pdb2pose( pept_chains[0], pdb_num_res_start )
	num_res_end = chains[ idx_pept ].pdb_info().pdb2pose( pept_chains[0], pdb_num_res_end )
	
	print num_res_start
	print num_res_end
	#append first residue of the trimmed peptide	
	newpose.append_residue_by_jump(chains[idx_pept].residue(num_res_start),newpose.total_residue(), "","",1)
        newpose.pdb_info().number(newpose.total_residue(),1)
        newpose.pdb_info().chain(newpose.total_residue(),'B')	

	#append remaining residues of the trimmed peptide
	for ind,i in zip(range(2,num_res_end+(2-num_res_start)),range(num_res_start+1,num_res_end+1)):
            newpose.append_polymer_residue_after_seqpos(chains[idx_pept].residue(i), newpose.total_residue(),0)	
	    newpose.pdb_info().number(newpose.total_residue(),ind)
	    newpose.pdb_info().chain(newpose.total_residue(),'B')
	
	newpose.pdb_info().obsolete(0)
	
	#output Trimmed pdb
	tokens=p.rsplit('.',1)
	file=tokens[0]
	print '%sTrimmedPep.pdb' % (file)
        newpose.dump_pdb('%sTrimmedPep.pdb' % (file.rstrip()))
                    

if __name__ == "__main__":
    main(sys.argv[1:])
