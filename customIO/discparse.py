#/usr/bin/env python

"""Convenience module to import necessary values from disc files, find intersection of values, etc."""

import os
import glob
import subprocess
import scorefileparse
import string
import random

class DiscParseError(Exception):
    def __init___(self, filename,error_msg):
        Exception.__init__(self,"trouble parsing disc file: {0}\n{1}".format(filename,error_msg))
        self.filename = filename

def read_vals(filename):

    with open(filename) as f:
        lines = f.read().splitlines()[0:-2]

    try:
        values_dict = { 
	        os.path.basename(line.split()[0])[0:4] :
                map(float,line.split()[1:]) for line in lines}
    except ValueError as e:
	raise DiscParseError(filename, str(e))

    return values_dict

def read_dir(path):
    """Reads first discfile in a given directory and returns a pdb dictionary with a list of discs for each pdb"""
    pathname = path + "/*.disc"
    disc_files = glob.glob(pathname)

    if not disc_files:
        raise DiscParseError("Cannot find any disc files in: "+path)

    pdbs_dict = read_vals(disc_files[0])

    return pdbs_dict

def best_of_5(scores_dict):
    values = scores_dict.values()
    energies = [ e[0] for e in values ]
    lowest_energies = sorted(energies)[0:5]
    lowest_rmsd = min([ r for e,r in values if e in lowest_energies])
    return lowest_rmsd

def scores_dict_to_metrics(scores_dict):
    temp_fn = "temp_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) + ".txt"
    scorefileparse.write_scores_dict_score_file(scores_dict, temp_fn)
    #if not os.path.isfile("~/git_repos/bakerlab_scripts/boinc/score_energy_landscape.py"):
    #    raise OSError("disc scoring script not found. please clone bakerlab_script repo and place it in ~/git_repos/")
    output = subprocess.check_output(os.path.expanduser("~/git_repos/bakerlab_scripts/boinc/score_energy_landscape.py -abinitio_scorefile {0} -rms 1.0 -temp 1".format(temp_fn)), shell=True)
    lines = output.splitlines()
    metr_tr = { "PNear" : "PNear", "SampledRMS" : "SRMS" , "WeightedRMS" : "WRMS", "tyka_discrimination.py" : "Disc", "calcbinnedboltz.pl" : "BinBoltz_old", "calc1dboltzmann.pl" : "BinBoltz" }
    metrics = { metr_tr[token] : float(lines[1].split()[ind]) for ind,token in enumerate(lines[0].split()) }
    os.remove(temp_fn)
    #metrics["Best5"] = best_of_5(scores_dict)
    return metrics

def pdbs_dict_to_metrics(pdbs_dict,scoretype="rosetta"):
    metrics_pdbs_dict = { pdb : scores_dict_to_metrics(scores_dict) for pdb, scores_dict in pdbs_dict.items() }
    return metrics_pdbs_dict

def show_scores_dict_metrics(scores_metrics_dict,pdb="", filename=None):
    output = '\t'.join([pdb] + [ str(t) for m, t in sorted(scores_metrics_dict.items()) ])
    if filename is not None:
        with open( filename, 'a') as f:
            f.write(output+"\n")
    else:
        print output
def show_pdbs_dict_metrics(pdbs_metrics_dict, filename=None):
    keys = pdbs_metrics_dict[pdbs_metrics_dict.keys()[0]].keys()
    output = '\t'.join(["PDB"] + sorted(keys))
    if filename is not None:
        with open( filename, 'w') as f:
            f.write(output + "\n")
    else:
        print output
    for pdb, metric in sorted(pdbs_metrics_dict.items()):
        show_scores_dict_metrics(metric, pdb, filename)


    
