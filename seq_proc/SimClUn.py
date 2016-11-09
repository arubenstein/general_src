#!/usr/bin/env python

"""For each sequence in a given pool, check its hamming distance for all cleaved sequences in all other pools"""
import itertools
import argparse
import conv
import seq_IO
import numpy as np

def write_file(outfile, outfile_dist, list_sims, labels, status):
    out = open(outfile, "w")
    out_dist = open(outfile_dist, "w")
    out_dist.write("Seq1,Seq2,Dist\n")
    for sims,label,stat in zip(list_sims,labels,status):
        out.write("{0},{1}\n".format(label,stat))
        out_dist.write("{0},{1}\n".format(label,stat))
        distances = [ d for s1, s2, d in sims ]
        out.write("Average: {0}\n".format(sum(distances)/len(distances)))
        out.write("Max: {0}\n".format(max(distances)))
        out.write("Min: {0}\n".format(min(distances)))
        over_25 = sum(1 for d in distances if d >= 0.25)
        over_50 = sum(1 for d in distances if d >= 0.5)
        over_75 = sum(1 for d in distances if d >= 0.75)
        out.write("N > 0.25 {0}/{1} = {2:.2f}\n".format(over_25,len(distances),float(over_25)/len(distances)))
        out.write("N > 0.50 {0}/{1} = {2:.2f}\n".format(over_50,len(distances),float(over_50)/len(distances)))
        out.write("N > 0.75 {0}/{1} = {2:.2f}\n".format(over_75,len(distances),float(over_75)/len(distances)))

        out_dist.write("\n".join("{0},{1},{2}".format(s1,s2,d) for (s1, s2, d) in sims))
        out_dist.write("\n")

def main(list_sequence_names, output_prefix):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    labels = [] #labels for list_sequences
    status = []

    for [filename, label, stat] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename)
        list_sequences.append(sequences)
        labels.append(label)
	status.append(stat)

    outfile_cl = '%ssim_cleaved.csv' % (output_prefix)
    outfile_uncl = '%ssim_uncleaved.csv' % (output_prefix)

    outfile_dist_cl = '%sdist_sim_cleaved.csv' % (output_prefix)
    outfile_dist_uncl = '%sdist_sim_uncleaved.csv' % (output_prefix)

    cleaved_seqs = [ (s,l) for s, l, stat in zip(list_sequences, labels, status) if stat == "CLEAVED" ]
    uncleaved_seqs = [ (s,l) for s, l, stat in zip(list_sequences, labels, status) if stat == "UNCLEAVED" ]
    cleaved_sims = []
    uncleaved_sims = []
    for seqs, label in zip(list_sequences, labels):
	cl = [ seq for s,l in cleaved_seqs for seq in s if l != label ]
        cleaved_sims.append([(seq1, seq2, 1.0 - conv.hamdist(seq1, seq2, all_threading=True)/float(min(len(seq1),len(seq2)))) for seq1, seq2 in itertools.product(seqs, cl) ] ) 

        uncl = [ seq for s,l in uncleaved_seqs for seq in s if l != label ]
        uncleaved_sims.append([(seq1, seq2, 1.0 - conv.hamdist(seq1, seq2, all_threading=True)/float(min(len(seq1),len(seq2)))) for seq1, seq2 in itertools.product(seqs, uncl) ] )
    write_file(outfile_cl, outfile_dist_cl, cleaved_sims, labels, status)
    write_file(outfile_uncl, outfile_dist_uncl, uncleaved_sims, labels, status)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=3, action='append', help="text file which contains sequences and the label you want to use for the set and status (CLEAVED/UNCLEAVED)")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)
