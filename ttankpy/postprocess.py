from ttankpy.superblock import loadallinfo,loadallepocs,listallblocks

import numpy as np
import os

def assignsortcode(sdir):

    sortcode = np.load(os.path.join(sdir,'sorter','sortcode.npy'),allow_pickle=True).item()
    
    spikes = loadallinfo(sdir)
    
    sp = np.empty(len(spikes['bl']))
    for ch in sortcode:
        sp[spikes['ch']==ch]=sortcode[ch]
    spikes['sortcode']=sp
    
    return spikes


def sequenceepocs(sdir):
    
    if os.path.exists(os.path.join(sdir,'sorter','blindex.npy')):
        blindex = np.load(os.path.join(sdir,'sorter','blindex.npy'),allow_pickle=True)
    else:
        blindex = listallblocks(sdir)
    
    bl = [int(x[6:x.find('.mat')]) for x in blindex]
    sequence = dict(zip(range(len(bl)),bl))    
    return sequence


def getspiketrains(sdir):
    
    epocs = loadallepocs(sdir)
    seq = sequenceepocs(sdir)
    spikes = assignsortcode(sdir)
    
    
#    bins = [x['SW_on'] for x in epocs.values()]
#    trial=[]
#    for i in np.unique(spikes['bl']):
#        ts_c = spikes['ts'][spikes['bl']==i]
#        s=np.digitize(ts_c,bins[i])
#        trial.extend(s-1)
#    spikes['trial']=np.array(trial)
    

    spiketrain={'spikes':spikes,'epocs':epocs,'sequence':seq}
    
    return spiketrain


