import numpy as np

def xcorr_coef(ts1,ts2,tson,tsoff,binwidth,reject_at):

    duration=tsoff-tson
    trainc=np.sort(np.concatenate((ts1,ts2)))
    t1,t2=[ts1,ts2]
    if any(np.diff(trainc)<reject_at):
        rm_spikes = trainc[np.append(np.diff(trainc)<reject_at,False)]
        t1,t2=[x[~np.isin(x,rm_spikes)] for x in [ts1,ts2]]

    # align and bin
    hbin=np.arange(0,duration+binwidth,binwidth)
    t1,t2 = [x[(x>tson)&(x<(tson+duration))]-tson for x in [t1,t2]]
    b=[np.histogram(x,hbin)[0] for x in [t1,t2]]
    
    # correlate
    R=np.correlate(b[0],b[1],'valid')
    
    # statistics
    N = len(hbin)
    N_A = sum(b[0])
    N_B = sum(b[1])
    E = N_A*N_B/N
    Rc = (R-E)*((N_A*N_B)**-0.5);
    sig_cutoff = 4*(N**-0.5)
    
    return (Rc,sig_cutoff)
