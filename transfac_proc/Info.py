import sys
import numpy
import math

def bits( firstList ):

    b = [ (aa*math.log(aa,2)) for aa in firstList if aa != 0.0 ]
    return numpy.sum(b) + math.log(20,2)
    
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
    infile=args[1]
    
    tokens=infile.rsplit('.',1)
    file=tokens[0]
    outfile= '%s_info.txt' % (file)
    
    
    freq_in = readSpecProfile( infile )

    info = [ bits(pos.values()) for pos in freq_in ]
    ave_info = numpy.sum(info)/len(info)

    dist_out = open(outfile,"w")

    dist_out.write('{0}\n'.format(info))
    dist_out.write('{0}\n'.format(ave_info))

    dist_out.close();
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
