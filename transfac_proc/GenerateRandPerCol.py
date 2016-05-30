import sys
import random
import numpy
import math
from sklearn import metrics

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
    sE = -1.0 * numpy.sum( [ p * math.log(p,2) for p in firstList if p != 0.0 ] )
    return sE

def JSDivergence( firstList, secondList ):

    firstSE = shannonEntropy( firstList )

    secondSE = shannonEntropy( secondList )
	
    combList = [ 0.5 * fL + 0.5 * sL for fL,sL in zip(firstList, secondList) ]

    combSE = shannonEntropy( combList )

    return combSE - 0.5 * firstSE - 0.5 * secondSE

def KL( firstList, secondList ):
    kl = numpy.sum( [ p * math.log( p / ( 0.5 * ( p + q ) ), 2 ) for p, q in zip( firstList, secondList ) if p != 0.0 ] )
    return kl

def JSDivergence2( firstList, secondList ):
    return 0.5 * KL( firstList, secondList) + 0.5 * KL( secondList, firstList )

def cosineDist( firstList, secondList):

    dotP = numpy.dot(firstList, secondList)

    sqrt_1 = math.sqrt( numpy.sum( numpy.power( firstList,2 ) ) )
    sqrt_2 = math.sqrt( numpy.sum( numpy.power( secondList,2 ) ) ) 
    
    return dotP/(sqrt_1 * sqrt_2)

def frobDist( firstList, secondList):

    diff_lists = numpy.subtract(firstList,secondList)
    terms = numpy.power( diff_lists,2)
    return math.sqrt( numpy.sum( terms ) )
    
def aveAbsDist( firstList, secondList ):

    diff_lists = numpy.fabs( numpy.subtract( firstList, secondList) )
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

def shuffleSP( list_freq,n_pos ):
    selected = random.sample(list_freq,n_pos)

    shuffled = []
    for pos in selected:
        random.shuffle(pos)
        shuffled.append(pos)

    return shuffled

def main(args):
    infile_list=args[1]
    outfile = args[2]
    n_pos = int(args[3])
    compfile = args[4]
    with open( infile_list ) as f_list_SP:
	list_SP = f_list_SP.readlines() 
    
    list_freq = []
    for SP in list_SP:
    	freq_in = readSpecProfileList( SP.strip() )
	list_freq.extend( freq_in )

    freq_comp = readSpecProfileList( compfile )

    outfile_cosine = outfile + "_cosine_"
    outfile_frob = outfile + "_frob_"
    outfile_aad = outfile + "_aad_"
    outfile_jsd = outfile + "_jsd_"
    outfile_auc = outfile + "_auc_"


    for i in range(0,n_pos):
        str_ind = str( i + 1 ) + ".txt"
        dist_cosine = open(outfile_cosine + str_ind,"a")
        dist_frob = open(outfile_frob + str_ind,"a")
        dist_aad = open(outfile_aad + str_ind,"a")
        dist_jsd = open(outfile_jsd + str_ind,"a")
        dist_auc = open(outfile_auc + str_ind,"a")
	freq_comp_i = [ freq_comp[i] ]    
        for n_rand in range(0,100000):
            freq_shuff = shuffleSP( list_freq,1 )
        
            nda_freq_shuff = numpy.array( [ freq_shuff] )
            nda_freq_comp = numpy.array( [ freq_comp_i ] )
            flat_freq_shuff = numpy.ndarray.flatten( nda_freq_shuff )
            flat_freq_comp = numpy.ndarray.flatten( nda_freq_comp )
            jsd1 = [ JSDivergence ( i, g ) for i,g in zip( freq_shuff, freq_comp_i )]
            auc = [ areaUnderCurve ( i, g ) for i, g in zip( freq_shuff, freq_comp_i )]
            s_c = cosineDist( flat_freq_shuff, flat_freq_comp )
            s_f = frobDist( flat_freq_shuff, flat_freq_comp )
            s_a = aveAbsDist( flat_freq_shuff, flat_freq_comp )
            ave_jsd = numpy.sum(jsd1) / len(jsd1)
            ave_auc = numpy.sum(auc) / len(auc) 
        
            dist_cosine.write('{0}\n'.format(s_c))
            dist_frob.write('{0}\n'.format(s_f))
            dist_aad.write('{0}\n'.format(s_a))
            dist_jsd.write('{0}\n'.format(ave_jsd))
            dist_auc.write('{0}\n'.format(ave_auc))

	dist_cosine.close()
        dist_frob.close()
        dist_aad.close()
        dist_jsd.close()
        dist_auc.close()    
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
