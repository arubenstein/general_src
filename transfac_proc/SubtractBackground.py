import sys
import numpy

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
    bg=args[1]
    orig=args[2]

    freq_bg = readSpecProfile( bg )
    freq_orig = readSpecProfile ( orig )
    
    #min background SP and then normalize it

    freq_bg_min = [ { key: max( float( val ),0.01 ) for key,val in i.iteritems() } for i in freq_bg ]
    freq_bg_norm = [ { key: float(val)/sum(i.values()) for key, val in i.iteritems() } for i in freq_bg_min ]
    
    #enrich by doing orig/bg - subt
    enriched = [ { key_orig: max(float( val_orig - dict_bg[key_orig] ),float(0.0) ) for key_orig,val_orig in dict_orig.iteritems() } 
			for dict_bg, dict_orig in zip ( freq_bg_norm, freq_orig ) ]
 
#    #enrich by doing orig/bg - subt2 worked terribly
#    enriched = [ { key_orig: max(float( val_orig - dict_bg[key_orig] + 0.01 ),float(0.0)) for key_orig,val_orig in dict_orig.iteritems() }
#                        for dict_bg, dict_orig in zip ( freq_bg_norm, freq_orig ) ]

    # subt3
#    enriched = [ { key_orig: float( val_orig - dict_bg[key_orig] ) for key_orig,val_orig in dict_orig.iteritems() }
#                        for dict_bg, dict_orig in zip ( freq_bg_norm, freq_orig ) ]
 
#    min = 0.0

#   for pos in enriched:
#        for aa in pos.values():
#            if ( aa < min ):
#                min = aa

#   enriched_min = [ { key: float( val + min ) for key, val in pos.iteritems() } for pos in enriched ]
    
    #normalize enriched SP
    enriched_norm = [ { key: float(val)/sum(i.values()) for key, val in i.iteritems() } for i in enriched ]

    #output transfac file
    tokens=args[2].rsplit('.',1)
    file=tokens[0]
    outfile= '%s_subt.transfac' % (file)
    
    transfac = open(outfile,"w")
            
    transfac.write("ID Matrix\nPO")
    
    for key,val in iter(sorted(enriched_norm[0].iteritems())):
        transfac.write("\t" + key)
    
    transfac.write("\n")
    
    for k in range( len( enriched_norm ) ):
        transfac.write(str(k))
        
        for key,val in iter(sorted(enriched_norm[k].iteritems())):
            transfac.write("\t")
            transfac.write("%0.4f" %val)
            
        transfac.write("\n")

if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'
    
    main(sys.argv)
