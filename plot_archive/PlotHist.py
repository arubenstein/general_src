import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import sys

def main( args ):
    
    inp_file=args[1]
    #WT_counts=args[2]
    
    token=inp_file.rsplit('.',1)[0]
    out_fig = '%s_bar.png' % (token)

    title = token.split("\\")[-1]


    with open( inp_file ) as f:
        filenames = f.readlines()

    #with open( WT_counts ) as f:
    #    WT_lines = f.readlines()

    #WT_dict = { line.split()[0] : float(line.split()[1]) for line in WT_lines }
    
    fig,axarr = plt.subplots( len(filenames), 2, sharex=True, sharey=True, squeeze=False )

    plt.rcParams.update({'font.size': 10})

    for ind,filename in enumerate(filenames):
        with open (filename.strip() ) as f:
            counts = f.readlines()
        counts.pop(0)

        title = os.path.basename(filename).strip()

        counts_f = [ float(f.strip().split()[-1]) for f in counts ]

        mu=np.mean(counts_f)
        sigma=np.std(counts_f)


        threshold = mu+100*sigma

        if sigma != 0:

            #counts_filt = [ f for f in counts_f if (f - mu)/sigma < 10 ]
            counts_filt = [ f for f in counts_f if f < 100 ]
            outliers = [ f for f in counts_f if (f - mu)/sigma > 10 ]

        else:
            counts_filt = counts_f
            outliers = []

        min_c = np.amin(counts_filt)
        max_c = np.amax(counts_filt)
        mu=np.mean(counts_filt)
        sigma=np.std(counts_filt)
        
        text='Min: %.3f\nMax: %.3f\nAvg: %.3f\nStdev: %.3f' % (min_c,max_c,mu,sigma)

        #for o in outliers:
        #    text+='\nOut: %.3f' % (o)
        text+='\nOut: %f' % (len(outliers))

        #if title in WT_dict:
        #    text+='\n\nWT Count: %.3f' %( WT_dict[title] )

        ax = axarr[ind,0]
        # the histogram of the data
        if len(counts_filt) > 1:
            #n, bins, patches = ax.hist(counts_filt, 50, normed=True,facecolor='green', log=True ,alpha=0.75)
            n, bins, patches = ax.hist(counts_filt, 50, normed=False,facecolor='green', log=True, alpha=0.75)
        else:
            ax.text(0.5,0.5,"Only one data point in dataset",
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=10, color='green',
                transform=ax.transAxes)

        ax.set_xlabel('Counts')
        ax.set_ylabel('Number of Counts')
        ax.set_title(title,fontsize=8)

        ax = axarr[ind,1]

        ax.text(0.5, 0.5, text,
           horizontalalignment='center',
           verticalalignment='center',
           fontsize=10, color='red',
           transform=ax.transAxes)

        plt.rcParams.update({'font.size': 10})

    fig.set_size_inches(2*4, len(filenames)*4)

    plt.tight_layout(pad=1.08, h_pad=0.2, w_pad=0.2, rect=None)

    fig.savefig(out_fig)


if __name__ == "__main__":
    main(sys.argv)
