# -*- coding: utf-8 -*-
# %%
sdir = 'Z:\\Calvin\\Analysis\\corfas_ATA\\CW89Mg1'
bl='Block-5'
mch=32 # max channel recorded in this block
sdval=3 # spike threshold in SD
    
import os
import h5py
import numpy as np

mf = h5py.File(os.path.join(sdir,bl+'.mat'),'r')


print(sdir,bl)



fs = mf['data']['streams']['STRM']['fs'][0][0]
strm = np.array(mf['data']['streams']['STRM']['data'])
print('strm: ',len(strm))

t = np.linspace(1/fs,1/fs*(len(strm)),len(strm))

rec_start=mf['data']['epocs']['Swep']['onset'][0][0]
rec_end=mf['data']['epocs']['Swep']['offset'][0][-2]+np.mean(np.diff(mf['data']['epocs']['Swep']['offset'][0][-5:-1]))

#car = np.mean(strm,axis=1)

# %%
from scipy.stats import zscore

for ch in range(1,mch+1):
    sel=(t>=rec_start)&(t<=rec_end)
    
    s=zscore(strm[sel,ch])    
    
    loc=np.where(s>sdval)[0]
    tcross_pos=loc[np.concatenate(([True],[np.diff(loc)>(fs/1000)][0]),axis=0)]
    loc=np.where(s<-sdval)[0]
    tcross_neg=loc[np.concatenate(([True],[np.diff(loc)>(fs/1000)][0]),axis=0)]
    
    pn = np.argmax([len(tcross_pos),len(tcross_neg)])
    if pn==0:
        tcross=tcross_pos
        sign=1
    else:
        tcross=tcross_neg
        sign=-1
    
    print('tcross: ',len(tcross))

    if not(os.path.exists(os.path.join(sdir,bl))):
        os.mkdir(os.path.join(sdir,bl))
    np.save(os.path.join(sdir,bl,'ts_ch'+str(ch)+'.npy'),t[sel][tcross])
    
    wf_all=np.empty((int(np.ceil(0.001*fs))*2+1,len(tcross)))
    for n,i in enumerate(tcross):
        tsn = t[sel][i]
        wfi_end = i+int(np.ceil(0.001*fs))
        wfi_start = i-int(np.ceil(0.001*fs))
        wft = t[sel][wfi_start:wfi_end+1]
        wfv = strm[sel,ch][wfi_start:wfi_end+1]
        wf_all[:,n]=wfv
        # if not(os.path.exists(os.path.join(sdir,bl,'temp'))):
            # os.mkdir(os.path.join(sdir,bl,'temp'))
        # np.save(os.path.join(sdir,bl,'temp','spike'+str(n)+'.npy'),wfv)
        print(n,len(tcross))
    
    np.save(os.path.join(sdir,bl,'wf_ch'+str(ch)+'.npy'),wf_all)