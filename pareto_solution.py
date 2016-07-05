#!/usr/bin/env python

import copy
import os
import sys
from customIO import scorefileparse
import argparse
from shutil import copyfile

def dominates(row, rowCandidate):
    return all(r <= rc for r, rc in zip(row, rowCandidate))

def cull(pts, dominates):
    dominated = []
    cleared = []
    remaining = pts
    while remaining:
        candidate = remaining[0]
        new_remaining = []
        for other in remaining[1:]:
            [new_remaining, dominated][dominates(candidate, other)].append(other)
        if not any(dominates(other, candidate) for other in new_remaining):
            cleared.append(candidate)
        else:
            dominated.append(candidate)
        remaining = new_remaining
    return cleared, dominated

def gen_ranks(list_energies):
    indices = list(range(len(list_energies)))
    indices.sort(key=lambda x: list_energies[x])
    output = [0] * len(indices)
    for i, x in enumerate(indices):
        output[x] = i
    return output

def find_pareto(dec_inter1, dec_inter2, pdb):

    d1e = scorefileparse.get_energies(dec_inter1[pdb])
    d2e = scorefileparse.get_energies(dec_inter2[pdb])

    r1 = scorefileparse.get_rmsd(dec_inter1[pdb])

    d1e_ranks = gen_ranks(d1e)
    d2e_ranks = gen_ranks(d2e)

    pts = map(list, zip(d1e_ranks, d2e_ranks))

    cleared, dominated = cull(pts, dominates)

    cleared_d = dict(cleared)
    

    pts_r = zip(d1e_ranks,d2e_ranks,r1,sorted(dec_inter1[pdb].keys()))

    pareto_equal_min = min([ e1+e2 for e1,e2 in cleared_d.items() ])
    list_pts =  [ (rosetta,amber,r,key) for rosetta,amber,r,key in pts_r if amber+rosetta == pareto_equal_min ]
    min_filename = find_lowest_point( list_pts )

    return min_filename

def find_lowest_point( list_pts ):
    first_rank_list = [ p[0] for p in list_pts ]
    second_rank_list = [ p[1] for p in list_pts ]
    min_rank = min(first_rank_list + second_rank_list)
    min_point = [ key for e1, e2, r, key in list_pts if min_rank == e1 or min_rank == e2 ][0]
    return min_point

def find_lowest_energy( score_dict ):
    #sorts dict by first item in tuple (energies), retrieves lowest energy item and extracts its key (filename)
    lowest_energy_key = sorted(score_dict.items(), key=lambda x: x[1][0])[0][0]
    return lowest_energy_key

def main(input_dir_rosetta_sf, input_dir_amber_sf, input_dir_rosetta_pdb, input_dir_amber_pdb, output_dir, n_results, alternate_rmsd, start_ind_desc_amber, start_ind_desc_rosetta, end_ind_desc_amber, end_ind_desc_rosetta, add_pdb_to_path):

    if alternate_rmsd is True:
        d1 = scorefileparse.read_dir(input_dir_rosetta_sf, 'rosetta', repl_orig=False, rmsd='total_score', start_ind_desc=start_ind_desc_rosetta, end_ind_desc=end_ind_desc_rosetta)
        d2 = scorefileparse.read_dir(input_dir_amber_sf, 'amber', repl_orig=False, rmsd='tot', start_ind_desc=start_ind_desc_amber, end_ind_desc=end_ind_desc_amber)
    else:
	d1 = scorefileparse.read_dir(input_dir_rosetta_sf, 'rosetta', repl_orig=False, start_ind_desc=start_ind_desc_rosetta, end_ind_desc=end_ind_desc_rosetta)
        d2 = scorefileparse.read_dir(input_dir_amber_sf, 'amber', repl_orig=False, start_ind_desc=start_ind_desc_amber, end_ind_desc=end_ind_desc_amber)
    
    dec_norm1 = scorefileparse.norm_pdbs(d1)
    dec_norm2 = scorefileparse.norm_pdbs(d2)
    
    [dec_inter1, dec_inter2] = scorefileparse.pdbs_scores_intersect([dec_norm1, dec_norm2])       
    
    dec1_cp = copy.deepcopy(dec_inter1)
    dec2_cp = copy.deepcopy(dec_inter2)

    try:
        os.mkdir( os.path.join(output_dir,"rosetta") )
    except OSError:
        pass
    try:
        os.mkdir( os.path.join(output_dir,"amber") )
    except OSError:
        pass
    try:
        os.mkdir( os.path.join(output_dir,"combined") )
    except OSError:
        pass
    
    for pdb in sorted(dec_inter1.keys()):
        for i in range(1,n_results+1):
            rosetta_lowest_energy = find_lowest_energy( dec_inter1[pdb] )
            amber_lowest_energy = find_lowest_energy( dec_inter2[pdb] )
            pareto_lowest_energy = find_pareto(dec1_cp, dec2_cp, pdb)
	    
	    if add_pdb_to_path == "True": 
                path_p = pdb
	    else:
		path_p = "" 
	    
            if end_ind_desc_rosetta == 1000:
                r_suffix = ".pdb"
            else:
                r_suffix = "_0001.pdb"

	    if start_ind_desc_amber is None:
                a_prefix = "min_NoH_"
            else:
		a_prefix = "min_"

            if end_ind_desc_amber is None:
                a_suffix = ".pdb"
            else:
                a_suffix = ".pdb.pdb"
	
	    #copy rosetta file
            src = os.path.join(input_dir_rosetta_pdb, path_p, rosetta_lowest_energy + r_suffix)
            dst = os.path.join(output_dir,"rosetta","{0}_{1}.pdb".format(pdb,i)) 
            copyfile(src, dst)
            #copy amber file
            src = os.path.join(input_dir_amber_pdb, path_p, a_prefix + amber_lowest_energy + a_suffix) 
            dst = os.path.join(output_dir,"amber","{0}_{1}.pdb".format(pdb,i))
            copyfile(src, dst)
            #copy pareto file
            src = os.path.join(input_dir_rosetta_pdb, path_p, pareto_lowest_energy + r_suffix)
            dst = os.path.join(output_dir,"combined","{0}_{1}.pdb".format(pdb,i))
            copyfile(src, dst)

            #delete from original scoredict so that next round will get the next-lowest
            dec_inter1[pdb].pop(rosetta_lowest_energy)
            dec_inter2[pdb].pop(amber_lowest_energy)
            dec1_cp[pdb].pop(pareto_lowest_energy)
            dec2_cp[pdb].pop(pareto_lowest_energy)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--input_dir_rosetta_sf', help="directory for rosetta input score files")
    parser.add_argument ('--input_dir_amber_sf', help="directory for amber input score files")
    parser.add_argument ('--input_dir_rosetta_pdb', help="directory for rosetta input pdbs")
    parser.add_argument ('--input_dir_amber_pdb', help="directory for amber input pdbs")

    parser.add_argument('--output_dir', help='directory for output structures')

    parser.add_argument('--n_results', type=int, help='number of lowest-scoring results to copy')
   
    parser.add_argument('--alternate_rmsd', type=bool, help='should alternate placeholder for rmsd be used')    

    parser.add_argument('--start_ind_desc_rosetta', type=int)
    parser.add_argument('--end_ind_desc_rosetta', type=int)
    parser.add_argument('--start_ind_desc_amber', type=int)
    parser.add_argument('--end_ind_desc_amber', type=int)

    parser.add_argument('--add_pdb_to_path', default="True", type=bool, help='should pdb name be added to the end of the input paths?')
 
    args = parser.parse_args()

    main(args.input_dir_rosetta_sf, args.input_dir_amber_sf, args.input_dir_rosetta_pdb, args.input_dir_amber_pdb, args.output_dir, args.n_results, args.alternate_rmsd, args.start_ind_desc_amber, args.start_ind_desc_rosetta, args.end_ind_desc_amber, args.end_ind_desc_rosetta, args.add_pdb_to_path)
