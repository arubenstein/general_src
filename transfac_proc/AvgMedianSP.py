import sys
import numpy

def main(args):
    infile=args[1]
    outfile=args[2]

    #open list of transfac files
    with open(infile) as afile:
        spec_profiles = afile.readlines()

    #open first transfac file to initialize several parameters( motifWidth, aaAlpha, and freq)
    with open(spec_profiles[0].strip()) as transfac_file:
        transfac = transfac_file.readlines()

    motifWidth = len(transfac)-2

    aaAlpha = transfac[1].split()[1:]
    
    #preinitialize freq (SP)
    freq = [{k: [] for k in aaAlpha} for i in range(motifWidth)]
    
    #loop through SPs
    for sp in spec_profiles:
        with open(sp.strip()) as transfac_file:
            transfac = transfac_file.readlines()

        aaAlpha = transfac[1].split()[1:]

        t_read = transfac[2:]

        for pos,line in enumerate( t_read,0 ):
            for aa_ind,f in enumerate( line.split()[1:], 0):
                freq[pos][aaAlpha[aa_ind]].append(float(f))



    #take median values of frequencies
    freqMatrix = [{k: numpy.median(d[k]) for k in d} for d in freq] 
    
    #normalize averaged SP
    normFreq = []

    for dc in freqMatrix:
        listFreq = dc.values()
	sumFreq = numpy.sum(listFreq) 
        d = listFreq/sumFreq
        normFreq.append({k:d[ind] for ind,k in enumerate(dc)})

    #write transfac
    transfac = open(outfile,"w")
            
    transfac.write("ID Matrix\nPO")
    
    for key,val in iter(sorted(normFreq[0].iteritems())):
        transfac.write("\t" + key)
    
    transfac.write("\n")
    
    for k in range(motifWidth):
        transfac.write(str(k))
        
        for key,val in iter(sorted(normFreq[k].iteritems())):
            transfac.write("\t")
            transfac.write("%0.4f" %val)
            
        transfac.write("\n")

if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'
    
    main(sys.argv)
