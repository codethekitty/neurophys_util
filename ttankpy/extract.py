import h5py
import numpy as np


def getepocs(file_path):
    mf = h5py.File(file_path,'r')
    
    var=list(mf['data']['epocs'])
    dat={}
    for n in var:
        if n!='Tick':
            c=mf['data']['epocs'][n]['data'][0]
            dat[n]=c
    dat['SW_on'] = mf['data']['epocs']['Swep']['onset'][0]
    dat['SW_off'] = mf['data']['epocs']['Swep']['offset'][0]
    dat['S1_on'] = mf['data']['epocs']['Lev1']['onset'][0]
    dat['S1_off'] = mf['data']['epocs']['Lev1']['offset'][0]
    dat['S1_on'] = mf['data']['epocs']['Lev1']['onset'][0]
    dat['S1_off'] = mf['data']['epocs']['Lev1']['offset'][0]
    
    if np.isin('ETyp',list(mf['data'])):
        dat['E_on'] = mf['data']['epocs']['ETyp']['onset'][0]
        dat['E_off'] = mf['data']['epocs']['ETyp']['offset'][0]

    return dat


def getspikes(file_path):

    epocs = getepocs(file_path)
    mf = h5py.File(file_path,'r')

    ch = mf['data']['snips'][list(mf['data']['snips'])[0]]['chan']
    ts = mf['data']['snips'][list(mf['data']['snips'])[0]]['ts']
    spikes={'ch':ch[0],'ts':ts[0]}
    
    bins = epocs['SW_on']
    ts_c = spikes['ts']
    s = np.digitize(ts_c,bins)
    
    spikes['trial']=s-1
    
    # spiketime calculate
    spikes['ts_sw']=np.empty(len(spikes['ts']))
    for t in range(0,np.max(spikes['trial'])+1):
        spikes['ts_sw'][spikes['trial']==t]=spikes['ts'][spikes['trial']==t]-epocs['SW_on'][t]
    spikes['ts_sw']=np.nan_to_num(spikes['ts_sw'])
    
    return spikes

def getstrm(file_path):
    
    mf = h5py.File(file_path,'r')
    fs = mf['data']['streams']['STRM']['fs'][0][0]
    strm = np.array(mf['data']['streams']['STRM']['data'])
    t = np.linspace(1/fs,1/fs*(len(strm)),len(strm))
    
    return (strm,t,fs)

def getwf(file_path):
    mf = h5py.File(file_path,'r')
#    wf=np.array(mf['data']['snips']['CSPK']['data'])
    wf=np.array(mf['data']['snips'][list(mf['data']['snips'])[0]]['data'])
    return wf