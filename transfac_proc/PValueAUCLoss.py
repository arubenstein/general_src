import sys
import random
import numpy
import math
from sklearn import metrics

def area_under_curve ( nCleaved, nUncleaved, scores ):
    labels = [1]*nCleaved + [0]*nUncleaved
    fpr, tpr, _ = metrics.roc_curve(labels, scores)
    auc = metrics.auc(fpr,tpr)
    
    return auc

def read_spec_profile( filename ):
    with open(filename) as transfac_file:
        transfac = transfac_file.readlines()

    motifWidth = len(transfac)-2

    aaAlpha = transfac[1].split()[1:]

    freq = [{k: 0.0 for k in aaAlpha} for i in range(motifWidth)]

    t_read = transfac[2:]

    for pos,line in enumerate( t_read,0 ):
        for aa_ind,f in enumerate( line.split()[1:], 0):
            freq[pos][aaAlpha[aa_ind]] = float(f)
    return freq
 
def shuffleSP( conc_SPs,n_pos ):
    selected = random.sample(conc_SPs,n_pos)

    shuffled = []
    for pos in selected:
	keys = pos.keys()
    	random.shuffle(keys)
    	shuffled.append( dict( zip(keys, pos.values()) ) )

    return shuffled

def main(args):
    in_SPs=args[1]
    outfile = args[2]
    n_pos = int(args[3])
    compfile = args[4]
    cleaved_file=args[5]
    uncleaved_file=args[6]
    with open( in_SPs ) as f_list_SPs:
	list_SPs = f_list_SPs.readlines() 
    
    conc_SPs = []
    for SP in list_SPs:
    	freq_in = read_spec_profile( SP.strip() )
	conc_SPs.extend( freq_in )

    freq_comp = read_spec_profile( compfile )

    outfile_loss = outfile + "_loss.txt"

    dist_loss = open(outfile_loss,"w")

    #read in list of seqs
    with open(cleaved_file) as seqs_file:
        cleaved_seqs = seqs_file.readlines()

    with open(uncleaved_file) as seqs_file:
        uncleaved_seqs = seqs_file.readlines()

    for i in range(1,100001):
	freq_rand = shuffleSP( conc_SPs,n_pos )
        
	exp_scores = []
        pred_scores = []

        #loop through seqs, for each seq generate score using freq_in
        for seq in cleaved_seqs:
            score = numpy.sum( [ freq_comp[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if freq_comp[pos][letter] != 0.0 ] )
            exp_scores.append( score)
            score = numpy.sum( [ freq_rand[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if freq_rand[pos][letter] != 0.0 ] )
            pred_scores.append( score)

        for seq in uncleaved_seqs:
            score = numpy.sum( [ freq_comp[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if freq_comp[pos][letter] != 0.0 ] )
            exp_scores.append( score)
            score = numpy.sum( [ freq_rand[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if freq_rand[pos][letter] != 0.0 ] )
            pred_scores.append( score)

        exp_auc = area_under_curve( len(cleaved_seqs),len(uncleaved_seqs),exp_scores )
        pred_auc = area_under_curve( len(cleaved_seqs),len(uncleaved_seqs),pred_scores )
        subt_auc = float(exp_auc) - float(pred_auc)

        dist_loss.write('{0}\n'.format(subt_auc))
    
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
