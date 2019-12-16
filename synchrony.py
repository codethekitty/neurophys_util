import numpy as np
from scipy.stats import poisson


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




def burst_ps(spiketrain,interval):

    crit=10
    ls=np.array(spiketrain)
    r=len(ls)/interval #expected sfr
    
    i=0
    j=i+2
    burst=[]
    while (i<len(ls))&(j<len(ls)):
        actual=j-i+1
        expected=(ls[j]-ls[i])*r
        P=-np.log2(poisson.pmf(actual,expected))
        if (P>crit)&(j<len(ls)-1)&(actual>expected):
            j+=1
            burst.append([P,actual,ls[i],ls[j]])
        else:
            i+=1
            j=i+2
    burst=np.array(burst)
    burst2=[]
    if np.size(burst,axis=0)>1:
        u,ix,c = np.unique(burst[:,2],return_counts=True,return_inverse=True)
        for i in range(len(u)):
            b=burst[ix==i,:]
            if c[i]>1:
                burst2.append(b[np.argmax(b[:,0]),:])
            else:
                burst2.append(b[0])
        burst2=np.array(burst2)
    burst3=[]
    if np.size(burst2,axis=0)>1:
        u,ix,c = np.unique(burst2[:,3],return_counts=True,return_inverse=True)
        for i in range(len(u)):
            b=burst2[ix==i,:]
            if c[i]>1:
                burst3.append(b[np.argmax(b[:,0]),:])
            else:
                burst3.append(b[0])
        burst3=np.array(burst3)
    
    return burst3