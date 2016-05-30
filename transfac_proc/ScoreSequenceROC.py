import os
import sys
import numpy
import math
from sklearn import metrics
import matplotlib.pyplot as plt
from pylab import *

def areaUnderCurve ( nCleaved, nUncleaved, scores, outfile, color, type ):
    labels = [1]*nCleaved + [0]*nUncleaved
    fpr, tpr, _ = metrics.roc_curve(labels, scores)
    auc = metrics.auc(fpr,tpr)
    
    plt.plot(fpr, tpr, color, linewidth=2, label='%0.2f'% (auc))
    plt.rcParams.update({'font.size': 8, 'font.weight': 'regular'})
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
#    plt.ylabel('True Positive Rate')
#    plt.xlabel('False Positive Rate')
    
    #turn off ticks and labels along both axes
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelleft='off')

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(1.5, 1.2)

    savefig(outfile,bbox_inches="tight", pad_inches=0.0)

    return auc

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

    #read in arguments
    exp_transfac_file=args[1]
    pred_transfac_file=args[2]
    cleaved_seqs_file=args[3]
    uncleaved_seqs_file=args[4]
 
    #make a name for the score file
    tokens=expTransfacFile.rsplit('.',1)
    file=tokens[0]
    expROC = '%s_roc.png' % (file)

    tokens=predTransfacFile.rsplit('.',1)
    file=tokens[0]
    predROC = '%s_roc.png' % (file)    
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

    expScoresList = []
    predScoresList = []

    #loop through seqs, for each seq generate score using freq_in
    for seq in cleavedList:
        #score = numpy.sum( [ math.log(freq_in[pos][letter]/bg_in[pos][letter],2) for pos,letter in enumerate( seq.strip(),0 ) if freq_in[pos][letter] != 0.0 ] )
	score = numpy.sum( [ expFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if expFreq[pos][letter] != 0.0 ] )
	expScoresList.append( score)
        score = numpy.sum( [ predFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if predFreq[pos][letter] != 0.0 ] )
        predScoresList.append( score)

    for seq in uncleavedList:
        score = numpy.sum( [ expFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if expFreq[pos][letter] != 0.0 ] )
        expScoresList.append( score)
        score = numpy.sum( [ predFreq[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if predFreq[pos][letter] != 0.0 ] )
        predScoresList.append( score)

    #you should end up with a list of seqs (seqsList) and a list of scores (scoresList) that you use to output at the end

    expAuc = areaUnderCurve( len(cleavedList),len(uncleavedList),expScoresList,expROC,'b',"Exp")
    predAuc = areaUnderCurve( len(cleavedList),len(uncleavedList),predScoresList,predROC,'r',"Pred")
    subtAuc = float(expAuc) - float(predAuc)

    pVals_loss = os.path.basename(expTransfacFile).rstrip()
    pVals_loss = pVals_loss.rsplit('.',1)[0]
    pVals_loss = '/Users/arubenstein/Dropbox/Research/Khare/p_Values/%s/100000_loss.txt' % (pVals_loss)

    with open(pVals_loss) as pVals:
        pVals = [ float(val) for val in pVals.read().splitlines() ]

    p_loss = float(sum( val < subtAuc for val in pVals ))/len(pVals)
    
    #writing out results
    dist_out = open(predDist,"w")
    dist_out.write("{0:.3f}\n{1:.3f}\n{2:.3f}\n{3:.6E}".format(expAuc, predAuc, subtAuc,p_loss) )

    #for seq,score in zip(seqsList, scoresList):
    #    dist_out.write("%s\t%s\n" % (seq.strip(),score))

if __name__ == "__main__":
    #infile = '/Users/Aliza/Downloads/sorted_complete.txt'
    #outfile = '/Users/Aliza/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
