#!/usr/bin/env python

"""Convenience module to import necessary values from score files, find intersection of values, etc."""
import sys
import os
import glob

class ScoreFileParseError(Exception):
    def __init___(self, filename,error_msg):
        Exception.__init__(self,"trouble parsing score file: {0}\n{1}".format(filename,error_msg))
        self.filename = filename

def read_vals(filename, scoretype, repl_orig=False, rmsd=None, list_energies=None, weights=None, scales=None, offsets=None, trim=True): 
    """Read values from a filename to return a scores_dict of structure { filename : (rmsd, sum(list_energies)) }"""
    if scoretype != "amber" and scoretype != "rosetta":
        error_str="Scoretype must be either amber or rosetta, not " + scoretype
        raise ValueError(error_str)
    with open(filename) as f:
        lines = f.read().splitlines()

    if not rmsd:
        sys.stderr.write("Warning: no column for rmsd supplied: defaulting to rmsd\n")
        rmsd = "rmsd"

    if not list_energies:
        list_energies = []
        if scoretype == "amber":
            sys.stderr.write("Warning: no columns list_energies supplied: defaulting to tot\n")
            list_energies.append("tot")
        elif scoretype == "rosetta":
            sys.stderr.write("Warning: no columns list_energies supplied: defaulting to total_score\n")
            list_energies.append("total_score")	

    for (ind, e_name) in enumerate(list_energies):
        list_energies[ind]= e_name.lower()

    tokens = lines.pop(0).split()

    if tokens[0] == "SEQUENCE:":
        tokens = lines.pop(0).split() #column header line

    #will throw ValueError if energy_name is not found
    try:
	indices = [tokens.index(e_name) for e_name in list_energies]
    
        rmsd_ind = tokens.index(rmsd)
        desc_ind = tokens.index("description")
    except ValueError as e:
        raise ScoreFileParseError(filename, str(e))

    ##temporary hacky thing to add elec14 to elec - elec MUST BE first in list of energies and first in weights, etc.
    if scoretype == "amber" and "elec" in list_energies:
	elec14_ind = tokens.index("elec_14")
    else:
	elec14_ind = None
 
    if any(ind > len(line.split()) for ind in indices for line in lines):
        raise ScoreFileParseError(filename, "Broken lines exist") 
    
    values_dict = extract_data(lines, rmsd_ind, desc_ind, indices, scoretype, weights, scales, offsets, elec14_ind=elec14_ind, trim=trim)

    if repl_orig:
        values_dict = replace_rmsd_orig(values_dict, filename)

    if len(values_dict.keys()) < 2:
        print "Warning: only one value present in {0}. Rejecting values_dict.".format(filename)
        values_dict = None

    return values_dict

def replace_rmsd_orig(scores_dict, filename):
    """Replace the rmsd in the scores_dict with the original rmsd's of the structures"""
    filename_orig = find_orig_score_file(filename) 
    
    with open(filename_orig) as f:
        lines = f.read().splitlines()

    lines.pop(0)

    tokens = lines.pop(0).split() #column header line

    try:
        rmsd_ind = tokens.index("rmsd")
        desc_ind = tokens.index("description")
    except ValueError as e:
        raise ScoreFileParseError(filename, str(e))

    scores_dict_orig = extract_data(lines, rmsd_ind, desc_ind, [], "rosetta")

    scores_dict_orig_inter, scores_dict_inter = scores_intersect([scores_dict_orig,scores_dict])

    for score, (energy, rmsd) in scores_dict_inter.items():
	scores_dict_inter[score] = (scores_dict_inter[score][0],scores_dict_orig_inter[score][1])

    return scores_dict_inter

def filter_scores_by_rmsd(scores_dict, rmsd_cutoff=50.0):
    """Filter scores in the scores_dict by given rmsd_cutoff"""
    new_dict = { filename : (val[0], val[1]) for filename, val in scores_dict.items() if val[1] < rmsd_cutoff }
    return new_dict

def filter_pdbs_by_rmsd(pdbs_dict, rmsd_cutoff=50.0):
    """Filter scores in the pdbs in the pdbs_dict by given rmsd_cutoff"""
    new_pdbs_dict = {}

    for pdb in pdbs_dict.keys():
        new_pdbs_dict[pdb] = filter_scores_by_rmsd(pdbs_dict[pdb], rmsd_cutoff)

    return new_pdbs_dict

def extract_data(lines, rmsd_ind, desc_ind, indices, scoretype, weights=None, scales=None, offsets=None, elec14_ind=None, trim=True):
    """Extract data from lines into scores_dict of structure { filename : (rmsd, energy) }"""
    if not weights and not scales and not offsets:
	weights = [ 1 for i in indices ]
	scales = [ 1 for i in indices ]
	offsets = [ 0 for i in indices ]
    elif len(weights) != len(indices) != len(scales) != len(offsets):
    	error_str="Length of weights ({0}) and scales ({2}) and offsets ({3}) must be identical to length of energies({1})".format(len(weights),len(indices), len(scales), len(offsets))
        raise ValueError(error_str)
    #try:
    if elec14_ind:
	weights + [weights[0]]
	scales + [scales[0]]
	offsets + [scales[0]]
	indices + [elec14_ind]

    if not trim:
        values_dict = {
            line.split()[desc_ind] :
            (sum(((float(line.split()[i]) / s + o) * w) for w,i,s,o in zip(weights,indices,scales,offsets)),
            float(line.split()[rmsd_ind]))
            for line in lines}
    elif scoretype == "amber":
        values_dict = {
            line.split()[desc_ind][8:-5]:
            (sum(((float(line.split()[i]) / s + o) * w) for w,i,s,o in zip(weights,indices,scales,offsets)),
            float(line.split()[rmsd_ind]))
            for line in lines}
    else:
        values_dict = {
            line.split()[desc_ind][0:-5]:
            (sum(((float(line.split()[i]) / s + o) * w) for w,i,s,o in zip(weights,indices,scales,offsets)),
            float(line.split()[rmsd_ind])) 
            for line in lines}
#    except ValueError as e:
#        raise ScoreFileParseError(filename, str(e))

    return values_dict

def find_score_files(path):
    """Simple method to find all score files in the current directory"""
    pathname = path + "/*.sc"
    return glob.glob(pathname)

def find_native_score_file(pathname):
    """Simple method to replace the decoy part of the path name with native 
    so as to find the native version of the file"""
    return pathname.replace("decoy","native")

def find_orig_score_file(pathname):
    """Simple method to replace the title part of the path name with orig_scores
    so as to find the orig_scores version of the file"""
    head,tail = os.path.split(os.path.split(pathname)[0])
    
    to_rep = tail[0:12] + "Rosetta_orig_scores"
    
    filename = os.path.basename(pathname)
    
    to_repf = filename[0:4]+".sc"

    return (pathname.replace(tail,to_rep)).replace(filename, to_repf)

def scores_intersect(list_scores_dict):
    """Finds intersecting scores from each dict and returns two dicts composed only of intersection"""
    shared_scores = set.intersection(*(set(d.keys()) for d in list_scores_dict))

    list_dicts_new = []

    for d in list_scores_dict:
        list_dicts_new.append({k : v for k,v in d.items() if k in shared_scores})

    return list_dicts_new 

def pdbs_scores_intersect(list_pdbs_dict):
    """Finds intersecting pdbs from each dict and returns two dicts composed only of intersection.
    Only returns intersecting scores within each pdb"""
    shared_pdbs = set.intersection(*(set(d.keys()) for d in list_pdbs_dict))

    list_dicts_new = [{} for d in list_pdbs_dict]
 
    for pdb in shared_pdbs:
        list_scores_dict = [d[pdb]for d in list_pdbs_dict]
        list_scores_dicts_new = scores_intersect(list_scores_dict)
        
        for ind,d in enumerate(list_scores_dicts_new):
	    list_dicts_new[ind][pdb]= d

    return list_dicts_new

def pdbs_intersect(list_pdbs_dict):
    """Finds intersecting pdbs from each dict and returns two dicts composed only of intersection"""
    shared_pdbs = set.intersection(*(set(d.keys()) for d in list_pdbs_dict))

    list_dicts_new = []

    for d in list_pdbs_dict:
        list_dicts_new.append({k : v for k,v in d.items() if k in shared_pdbs})

    return list_dicts_new

def read_dir(path, scoretype, repl_orig=False, rmsd=None, list_energies=None, weights=None, scales=None, offsets=None):
    """Reads all scorefiles in a given directory and returns a pdb dictionary with a scores dict for each pdb"""
    score_files = find_score_files(path)

    if not score_files:
	raise ScoreFileParseError("Cannot find any score files in: "+path)

    pdbs_dict = {os.path.basename(filename)[0:4]: read_vals(filename, scoretype, repl_orig, rmsd=rmsd, list_energies=list_energies, weights=weights, scales=scales, offsets=offsets) for filename in score_files} 

    #filter None values (due to only 1 value in the scores_dict)
    pdbs_dict = {k:v for k,v in pdbs_dict.items() if v}

    return pdbs_dict

def read_dec_nat(decoy_path, scoretype,repl_orig=False, rmsd=None, list_energies=None, weights=None, scales=None, offsets=None):
    """Reads all scorefiles in both native and decoy dirs and returns pdb dictionaries with a scores dict for each pdb"""
    dec_dict = read_dir(decoy_path, scoretype, repl_orig)
    nat_dict = read_dir(find_native_score_file(decoy_path), scoretype, rmsd=rmsd, list_energies=list_energies, weights=weights, scales=scales, offsets=offsets)

    return dec_dict,nat_dict

def find_perc (scores_dict):

    list_vals = [ v[0] for v in scores_dict.values() ]

    #find percentile values
    energies_sorted = sorted(list_vals)
   
    perc_high = float(energies_sorted[int(len(energies_sorted) * 0.95) ])
    perc_low = float(energies_sorted[int(len(energies_sorted) * 0.05) ])
    return perc_low, perc_high

def norm_vals (scores_dict, perc_low, perc_high):

    #normalize x
    norm_scores_dict = {k : ((float(v[0]) - perc_low) / (perc_high - perc_low), v[1]) for k,v in scores_dict.items()}

    return norm_scores_dict

def filter_norm (scores_dict_1, low_also = True):

    if low_also:
        low = -1.5
    else:
        low = -100.0

    filtered_scores = { k : (energy, rmsd) for k, (energy, rmsd) in scores_dict_1.items() if energy < float(2.5) 
								    and energy > low 
							            and energy < float(2.5) 
								    and energy > low }

    return filtered_scores

def filter_unnorm (scores_dict, low_also = True): 

    if low_also:
        low = -1.5
    else:
        low = -100.0

    x_perc_low, x_perc_high = find_perc(scores_dict)

    norm_dict = norm_vals(x_perc_low, x_perc_high, scores_dict) 

    filtered_norm_scores = { k : (energy, rmsd) for k, (energy, rmsd) in scores_dict_1.items() if energy < float(2.5) 
                                                                    and energy > low
                                                                    and energy < float(2.5)       
                                                                    and energy > low }

    [ filt_norm, filt_unnorm ] = scores_intersect([filtered_norm_scores,scores_dict])

    return filt_unnorm

def norm_pdbs (pdbs_dict, perc_pdbs_dict=None):
    new_dict = {}

    for pdb, scores_dict in pdbs_dict.items():
        if perc_pdbs_dict:
	    perc_low, perc_high = find_perc(perc_pdbs_dict[pdb])
	else:
            perc_low, perc_high = find_perc(scores_dict)

        new_dict[pdb] = norm_vals(scores_dict,perc_low,perc_high) 
 
    return new_dict

def filter_norm_pdbs (pdbs_dict, low_also = True):
    new_dict = {}

    for pdb, scores_dict in pdbs_dict.items():
        new_dict[pdb] = filter_norm(scores_dict, low_also)

    return new_dict

def filter_unnorm_pdbs (pdbs_dict, low_also = True):
    new_dict = {}
 
    for pdb, scores_dict in pdbs_dict.items():
        new_dict[pdb] = filter_unnorm(scores_dict, low_also) 
 
    return new_dict

def get_energies (scores_dict):
    energies = [ e[0] for e in scores_dict.values() ]
    return energies

def get_rmsd (scores_dict):
    rmsd = [ e[1] for e in scores_dict.values() ]
    return rmsd

def convert_disc(scores_dict):
    disc = [ [("rmsd",e[1]),("",e[0])] for e in scores_dict.values() ]
    return disc

def merge_scores_dicts(list_scores_dict):
    list_new_dicts = scores_intersect(list_scores_dict)

    merged = {k: (sum(d[k][0] for d in list_new_dicts),rmsd) for k,(energy, rmsd) in list_new_dicts[0].items()}

    return merged

def merge_pdbs_dicts(list_pdbs_dict):
    list_new_dicts = pdbs_intersect(list_pdbs_dict)

    merged = {}

    for pdb in list_new_dicts[0].keys():
        merged[pdb] = merge_scores_dicts([ d[pdb] for d in list_new_dicts ])

    return merged

def weight_dict(scores_dict, w):
    new_sd = {}
    for filename, (energy, rmsd) in scores_dict.items():
        new_sd[filename] = (energy*w, rmsd)
    return new_sd 

def print_scores_dict(scores_dict):
    for key in sorted(scores_dict):
        s = "{0} : {1} , {2}".format(key, scores_dict[key][0], scores_dict[key][1])
        print s

def write_scores_dict_score_file(scores_dict, score_file_name):
    with open(score_file_name,'w') as sf:
        sf.write("SEQUENCE\n")
        sf.write("SCORE: rms score\n")
        for k,(energy,rmsd) in scores_dict.items():
            sf.write("SCORE: {0} {1}\n".format(rmsd, energy))
