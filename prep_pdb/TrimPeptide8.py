#!/usr/bin/python


from rosetta import *
from toolbox import cleanATOM


init('-mute core.pack.task core.conformation.Conformation')
from rosetta.core.conformation import *
import os
import sys
from rosetta.core.pose import PDBInfo

def main(argv):

    #args = sys.argv
    with open(argv[0]) as afile:
        pdbs = afile.readlines()
    
    with open(argv[1]) as afile:
        d = { item[0] : [item[1].split(","),item[2].split(","),item[3].split(",")] for item in (line.split() for line in afile) }

    for p in pdbs:

	basename_p = os.path.basename(p).rstrip()

	all_chains = d[basename_p][0]
	prot_chains = d[basename_p][1]
	pept_chains = d[basename_p][2]

        cleanATOM(p.rstrip())
	
	filename = p.split('.')[0] + ".clean.pdb"
	
        pose = pose_from_pdb(filename.rstrip())
        pose.update_pose_chains_from_pdb_chains()
	
        chains=pose.split_by_chain()
        
	newpose = Pose()
	newpose.pdb_info( PDBInfo( newpose ) )

	#iterate through all chains in protein by iterating through the list if chain is found in list of protein chains append it to newpose by appending after seqpos
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

	num_res_extra = chains[idx_pept].total_residue() - 8
	print num_res_extra
	num_res_offset = num_res_extra/2 + 1
	print num_res_offset	

	print newpose.pdb_info()	

	newpose.append_residue_by_jump(chains[idx_pept].residue(num_res_offset),newpose.total_residue(), "","",1)
        newpose.pdb_info().number(newpose.total_residue(),1)
        newpose.pdb_info().chain(newpose.total_residue(),'B')	

	for ind,i in zip(range(2,9),range(num_res_offset+1,num_res_offset+8)):
            newpose.append_polymer_residue_after_seqpos(chains[idx_pept].residue(i), newpose.total_residue(),0)	
	    newpose.pdb_info().number(newpose.total_residue(),ind)
	    newpose.pdb_info().chain(newpose.total_residue(),'B')
	
	print chains[idx_pept]
	
	print newpose	
	
	newpose.pdb_info().obsolete(0)
	
	print newpose.pdb_info()
	tokens=p.split('.')
	file=tokens[0]
	print '%sTrimmedPep.pdb' % (file)
        newpose.dump_pdb('%sTrimmedPep.pdb' % (file.rstrip()))
                    

if __name__ == "__main__":
    main(sys.argv[1:])
