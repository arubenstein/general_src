import os
import sys
import numpy
import math
from sklearn import metrics
import matplotlib.pyplot as plt
from pylab import *


def plot_hist ( cleaved_l, uncleaved_l, fig, color, sp_pos ):
    ax = fig.add_subplot(sp_pos)
    
    data = [cleaved_l, uncleaved_l]
    numBins = 20
    
    ax.hist(data, numBins, normed=1, histtype='bar', color=color, label=['Cld','Ucld'])    
    
    plt.rcParams.update({'font.size': 20})
    plt.legend(loc='upper center')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on')

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelleft='off')


def readSpecProfile( filename ):
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

def main(args):
    #read in and rename arguments
    expTransfacFile=args[1]
    predTransfacFile=args[2]
    cleavedSeqsFile=args[3]
    uncleavedSeqsFile=args[4]
 
    #make a name for the score file
    tokens=expTransfacFile.rsplit('.',1)
    file=tokens[0]
    exphist = '%s_hist.png' % (file)

    tokens=predTransfacFile.rsplit('.',1)
    file=tokens[0]
    predhist = '%s_hist.png' % (file)    
    predDist = '%s_auc_dist.txt' % (file)   

    #this is the representation of a transfac.  It is a list of dictionaries - each item in the list holds one dictionary for each position
    #each dictionary holds one item per amino acid, the key for the dict is the one letter code for the amino acid and the value is the probability
    expFreq = readSpecProfile( expTransfacFile )
    predFreq = readSpecProfile( predTransfacFile )

    #your code
    #read in list of seqs
    with open(cleavedSeqsFile) as seqs_file:
        cleavedList = seqs_file.readlines()

    with open(uncleavedSeqsFile) as seqs_file:
        uncleavedList = seqs_file.readlines()

    expScoresCList = []
    expScoresUList = []
    predScoresCList = []
    predScoresUList = []

    #loop through seqs, for each seq generate score using freq_in
    for seq in cleavedList:
        #score = numpy.sum( [ math.log(freq_in[pos][letter]/bg_in[pos][letter],2) for pos,letter in enumerate( seq.strip(),0 ) if freq_in[pos][letter] != 0.0 ] )
	    score = numpy.sum( [ expFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if expFreq[pos][letter] != 0.0 ] )
	    expScoresCList.append( score)
        score = numpy.sum( [ predFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if predFreq[pos][letter] != 0.0 ] )
        predScoresCList.append( score)

    for seq in uncleavedList:
        score = numpy.sum( [ expFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if expFreq[pos][letter] != 0.0 ] )
        expScoresUList.append( score)
        score = numpy.sum( [ predFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if predFreq[pos][letter] != 0.0 ] )
        predScoresUList.append( score)

    #you should end up with a list of seqs (seqsList) and a list of scores (scoresList) that you use to output at the end
    
    fig = plt.figure()
 
    plot_hist(expScoresCList, expScoresUList, fig, [(0,0,1.0),(0.788,0.788,1.0)], 211)
    plot_hist(predScoresCList, predScoresUList, fig, [(1.0,0,0),(1.0,0.788,0.788)],212)
    savefig(predhist,bbox_inches="tight", pad_inches=0.0)
 
    #for seq,score in zip(seqsList, scoresList):
    #    dist_out.write("%s\t%s\n" % (seq.strip(),score))

if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
