#!/usr/bin/python


from rosetta import *
from toolbox import cleanATOM
from rosetta.core.chemical import *

init('-mute core.pack.task core.conformation.Conformation')
from rosetta.core.conformation import *
import os
import sys
from rosetta.core.pose import PDBInfo

def main(argv):

    #args = sys.argv
    with open(argv[0]) as afile:
        pdbs = afile.readlines()
    
    out = open("background_pept_seq","w")

    for p in pdbs:

	basename_p = os.path.basename(p).rstrip()

        pose = pose_from_pdb(p.rstrip())
        pose.update_pose_chains_from_pdb_chains()
	
        chains=pose.split_by_chain()

	seq=""
	
	for i in range(1,chains[2].total_residue() +1):	    
	    amino_acid = chains[2].residue(i).aa()
	    seq+= core.chemical.oneletter_code_from_aa( amino_acid)

	seq += "\n"
	out.write(seq)

if __name__ == "__main__":
    main(sys.argv[1:])
