import os
import sys
import numpy as np
import math
from sklearn import metrics
import matplotlib.pyplot as plt
from pylab import *

def binarizeList ( firstList ):
    binary_freq = []
    for val in firstList:
	if val > .10:
	    binary_freq.append( 1 )
        else:
	    binary_freq.append( 0 )
    return binary_freq

def areaUnderCurve ( firstList, secondList ):
    binary_freq = binarizeList( firstList )
    fpr, tpr, _ = metrics.roc_curve(binary_freq, secondList)
    auc = metrics.auc(fpr,tpr)
    return auc

def shannonEntropy( firstList ):
    sE = -1.0 * np.sum( [ p * math.log(p,2) for p in firstList if p != 0.0 ] )
    return sE

def JSDivergence( firstList, secondList ):

    firstSE = shannonEntropy( firstList )

    secondSE = shannonEntropy( secondList )
	
    combList = [ 0.5 * fL + 0.5 * sL for fL,sL in zip(firstList, secondList) ]

    combSE = shannonEntropy( combList )

    return combSE - 0.5 * firstSE - 0.5 * secondSE

def KL( firstList, secondList ):
    kl = np.sum( [ p * math.log( p / ( 0.5 * ( p + q ) ), 2 ) for p, q in zip( firstList, secondList ) if p != 0.0 ] )
    return kl

def JSDivergence2( firstList, secondList ):
    return 0.5 * KL( firstList, secondList) + 0.5 * KL( secondList, firstList )

def cosineDist( firstList, secondList):

    dotP = np.dot(firstList, secondList)

    sqrt_1 = math.sqrt( np.sum( np.power( firstList,2 ) ) )
    sqrt_2 = math.sqrt( np.sum( np.power( secondList,2 ) ) ) 
    
    return dotP/(sqrt_1 * sqrt_2)

def frobDist( firstList, secondList):

    diff_lists = np.subtract(firstList,secondList)
    terms = np.power( diff_lists,2)
    return math.sqrt( np.sum( terms ) )
    
def aveAbsDist( firstList, secondList ):

    diff_lists = np.fabs( np.subtract( firstList, secondList) )
    return sum( diff_lists ) / len( diff_lists )
    
def readSpecProfileList( filename ):
    with open(filename) as transfac_file:
        transfac = transfac_file.readlines()

    motifWidth = len(transfac)-2

    aaAlpha = transfac[1].split()[1:]

    freq = [{k: 0.0 for k in aaAlpha} for i in range(motifWidth)]

    t_read = transfac[2:]

    for pos,line in enumerate( t_read,0 ):
        for aa_ind,f in enumerate( line.split()[1:], 0):
            freq[pos][aaAlpha[aa_ind]] = float(f)

    freqList = [ [ val for key,val in sorted(pos.iteritems()) ] for pos in freq ]

    return freqList

def main(args):
    infile=args[1]
    infile_gold = args[2]
    if len(args) > 3:
	suffix = int(args[3])
    else:
	suffix = 0

    gold = os.path.basename(infile_gold).rstrip()
    gold = gold.rsplit('.',1)[0]
    pVals_gold = '/Users/arubenstein/Dropbox/Research/Khare/p_Values/%s/100000_' % (gold)

    tokens=infile.rsplit('.',1)
    file=tokens[0]
    
    if suffix != 1:
	outfile= '%s_dist.txt' % (file)
        outfile_heat= '%s_heat.png' % (file)
    else:
        outfile= '%s_dist_%s.txt' % (file, gold)
        outfile_heat= '%s_heat_%s.png' % (file,gold)
    
    pVals_cosine = '%scosine' % (pVals_gold) 
    pVals_frob = '%sfrob' % (pVals_gold)
    pVals_aad = '%saad' % (pVals_gold)
    pVals_jsd = '%sjsd' % (pVals_gold)
    pVals_auc = '%sauc' % (pVals_gold)

    freq_in = readSpecProfileList( infile )
    freq_gold = readSpecProfileList( infile_gold )
    nda_freq_in = np.array( [ freq_in] )
    nda_freq_gold = np.array( [ freq_gold] )
    flat_freq_in = np.ndarray.flatten( nda_freq_in )
    flat_freq_gold = np.ndarray.flatten( nda_freq_gold )
#    [print i for i,g in zip(freq_ind, freq_gold)]    
    c = [ cosineDist( i, g ) for i,g in zip( freq_in, freq_gold ) ]
    f = [ frobDist( i, g ) for i,g in zip( freq_in, freq_gold ) ]
    a = [ aveAbsDist( i, g ) for i,g in zip( freq_in, freq_gold ) ]
    jsd1 = [ JSDivergence ( i, g ) for i,g in zip( freq_in, freq_gold )]  
    jsd2 = [ JSDivergence2 ( i, g ) for i, g in zip( freq_in, freq_gold )]
    auc = [ areaUnderCurve ( i, g ) for i, g in zip( freq_gold, freq_in )]
    s_c = cosineDist( flat_freq_in, flat_freq_gold )
    s_f = frobDist( flat_freq_in, flat_freq_gold )
    s_a = aveAbsDist( flat_freq_in, flat_freq_gold ) 
    #s_c = np.sum(c) / len(c)
    #s_f = np.sum(f) / len(f)
    #s_a = np.sum(a) / len(a)
    ave_jsd = np.sum(jsd1) / len(jsd1)
    ave_auc = np.sum(auc) / len(auc)

    c.append(s_c)
    f.append(s_f)
    a.append(s_a)
    jsd1.append(ave_jsd)
    auc.append(ave_auc)

    pVals_cosine_list = []
    pVals_frob_list = []
    pVals_aad_list = []
    pVals_jsd_list = []
    pVals_auc_list = []

    for i in range(0,len(c)):
	if ( i == len(c)-1 ):
	    suff = ".txt"
        else:
	    suff = "_" + str(i+1)+".txt"
	with open(pVals_cosine+suff) as pVals:
            l = [ float(val) for val in pVals.read().splitlines() ]
            pVals_cosine_list.append( sorted(l) )
	with open(pVals_frob+suff) as pVals:
	    l = [ float(val) for val in pVals.read().splitlines() ]
            pVals_frob_list.append( sorted(l) )
        with open(pVals_aad+suff) as pVals:
            l = [ float(val) for val in pVals.read().splitlines() ]
	    pVals_aad_list.append( sorted(l) )
	with open(pVals_jsd+suff) as pVals:
            l = [ float(val) for val in pVals.read().splitlines() ]
            pVals_jsd_list.append( sorted(l) )
        with open(pVals_auc+suff) as pVals:
            l = [ float(val) for val in pVals.read().splitlines() ]
            pVals_auc_list.append( sorted(l) )

    #p_cosine = sum( val < s_c for val in pVals_cosine_list )/float(10000)
    #p_frob = sum( val < s_f for val in pVals_frob_list )/float(10000)
    #p_aad = sum( val < s_a for val in pVals_aad_list )/float(10000)
    #p_jsd = sum( val < ave_jsd for val in pVals_jsd_list )/float(10000)
    #p_auc = sum( val < ave_auc for val in pVals_auc_list )/float(10000)

    dist_out = open(outfile,"w")

    #dist_out.write('{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'.format(c, f, a, jsd1, jsd2,auc))
   
    p_cosine = []
    p_frob = []
    p_aad = []
    p_jsd = []
    p_auc = []
 
    for i in range(0, len(c)):
        len_pVals = float(len(pVals_cosine_list[0]))
        p_cosine.append(sum( val > c[i] for val in pVals_cosine_list[i] )/len_pVals)
        p_frob.append(sum( val < f[i] for val in pVals_frob_list[i] )/len_pVals)
        p_aad.append(sum( val < a[i] for val in pVals_aad_list[i] )/len_pVals)
        p_jsd.append(sum( val < jsd1[i] for val in pVals_jsd_list[i] )/len_pVals)
        p_auc.append(sum( val > auc[i] for val in pVals_auc_list[i] )/len_pVals)
#        dist_out.write('{0:e}\t{1:e}\t{2:e}\t{3:e}\t{4:e}\n'.format(p_cosine,p_frob,p_aad,p_jsd,p_auc))
    dist_out.write("\t".join(map(str,c)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,f)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,a)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,jsd1)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,auc)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,p_cosine)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,p_frob)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,p_aad)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,p_jsd)))
    dist_out.write("\n")
    dist_out.write("\t".join(map(str,p_auc)))
    dist_out.write("\n")

    p_jsd_trunc = p_jsd[0:-1]
    data = np.array(p_jsd_trunc).reshape(1,len(p_jsd_trunc))

    data = np.ma.masked_greater(data, 0.05)

    fig, ax = plt.subplots()

    cmap2 = plt.cm.Blues_r
    cmap2.set_bad(color="white")

    heatmap = ax.pcolormesh(data, cmap=cmap2,edgecolor="black",vmin=0.0,vmax=0.05)

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



    # want a more natural, table-like display
    ax.invert_yaxis()
    width=0.225*len(p_jsd_trunc)
    height=0.225
    fig.set_size_inches(width, height)
    savefig(outfile_heat,bbox_inches="tight", pad_inches=0.0)

#    dist_out.write('{0}\n'.format(s_c))
#    dist_out.write('{0}\n'.format(s_f))
#    dist_out.write('{0}\n'.format(s_a)) 
#    dist_out.write('{0}\n'.format(ave_jsd))
#    dist_out.write('{0}\n'.format(ave_auc))

if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
