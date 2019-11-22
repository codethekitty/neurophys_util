sdir='Z:\\Calvin\\Analysis\\corfas_ATA\\M638'
artifact_rejection = True
crit=4

import os,sys
sys.path.append('Z:\\Calvin\\Analysis\\py_def')


# %%
from ttankpy.superblock import loadallinfo,loadallspikes,listallblocks
import numpy as np
if not(os.path.exists(os.path.join(sdir,'sorter'))):
    os.mkdir(os.path.join(sdir,'sorter'))
blindex = listallblocks(sdir)
np.save(os.path.join(sdir,'sorter','blindex.npy'),blindex)
    
# %%
#from ttankpy.extract import getspikes,getwf

print('loading spike info...')
spikes = loadallinfo(sdir)
print('\n')
print('loading waveforms...')
wfct = loadallspikes(sdir)
print('\n')
wfc=np.transpose(wfct)

# %%
chall=np.unique(spikes['ch'])

if os.path.exists(os.path.join(sdir,'sorter','sortcode.npy')):
    l=np.load(os.path.join(sdir,'sorter','sortcode.npy'),allow_pickle=True)
    sortcode=l.item()
    sortfin=list(sortcode)
    chrest=chall[np.where(~(np.isin(chall,sortfin)))[0]]
	
else:
    sortcode={}
    chrest=chall
    
    
# %%
if len(chrest)>0:
    ch=int(np.min(chrest))
    mchrest=np.max(chrest)
else:
    ch=0
    mchrest=0
while (ch<=mchrest):
    if ch in chrest:  
        sp = spikes['ts'][spikes['ch']==ch]
        wf = wfc[:,spikes['ch']==ch]
        
        n_sample = input('channel %d [500/%d]: ' %(ch,len(sp)))
        if n_sample is '':
            n_sample=500
        else:
            n_sample=int(n_sample)
        

        if artifact_rejection:
            p2pamp = [max(x)-min(x) for x in np.transpose(wf)]
            avg_noise_lv = [np.sqrt(np.mean(x**2)/30) for x in np.transpose(wf)]
            amprej=0.001
            ind = ((avg_noise_lv> (np.mean(avg_noise_lv)+np.std(avg_noise_lv)*crit)) |  (np.array(p2pamp)>amprej)) # 4 SD rejection
            wf[:,ind]=np.mean(np.array(avg_noise_lv)[np.array(p2pamp)<=amprej])
            indloc=np.where(ind)[0]
            print('%d artifacts rejected at %d SD' %(len(indloc),crit))
        
        from numpy.random import randint
        import matplotlib.pyplot as plt
        
        #center=int(len(wf)/2)
        center=10
        if np.mean(wf[:int(len(wf)/2),:])>np.mean(wf[int(len(wf)/2):,:]):
            wf=-wf
        
        
        if n_sample>0:
            print('displaying',n_sample,'of',np.size(wf,axis=1),'spikes')
            rseed=randint(0,np.size(wf,axis=1),n_sample)
            wf_sel = wf[:,np.isin(np.arange(0,np.size(wf,axis=1)),rseed)]
            b=n_sample
        else:
            b=np.size(wf,axis=1)
            print('displaying all',b,'spikes')
            wf_sel=wf
            
        
        if len(sp)>100:
            plt.figure(figsize=[8,6])
            plt.subplot(221)
            for i in range(np.size(wf_sel,axis=1)):
                wf_sel[:,i]=np.roll(wf_sel[:,i],10-np.argmin(wf_sel[:,i]))
                plt.plot(wf_sel[:,i])
            
            plt.subplot(222)
            plt.hist(np.diff(sp),np.arange(0,0.1,0.001))
            
            from sklearn.decomposition import PCA
            pca = PCA(len(wf))
            pca.fit(wf_sel)
            
            plt.subplot(223)
            plt.hist(pca.components_[0,:],b)
            plt.xlabel('PCA1: %.2f' % pca.explained_variance_ratio_[0])
            
            plt.subplot(224)
            plt.plot(pca.components_[0,:],pca.components_[1,:],'.')
            plt.xlabel('PCA1: %.2f' % pca.explained_variance_ratio_[0])
            plt.ylabel('PCA2: %.2f' % pca.explained_variance_ratio_[1])
            plt.title('%.2f' % sum(pca.explained_variance_ratio_[0:2]))
            
            plt.show()
        
        
    # %
        N = input('N cluster [1]: ')
        if N is '':
            N=1
        else:
            N=int(N)
        
        if N>1:
            npc = input('dimension [1]: ')
            if npc is '':
                npc=1
            else:
                npc=int(npc)
        
        wf_sel=wf
        
        if N>1:
            plt.figure(figsize=[10,3])
            co=plt.rcParams['axes.prop_cycle'].by_key()['color']
            
            pca = PCA(npc)
            pca.fit(wf_sel)
            
            pca_result=pca.components_.copy()
            from sklearn.cluster import KMeans
            km=KMeans(n_clusters=N,random_state=0).fit(np.transpose(pca_result))
            plt.subplot(122)
            
            if npc==1:
                for k in range(N):
                    plt.hist(pca_result[0,km.labels_==k],b)
                    plt.xlabel('PCA1: %.2f' % pca.explained_variance_ratio_[0])
            else:
                for k in range(N):
                    plt.plot(pca.components_[0,km.labels_==k],pca.components_[1,km.labels_==k],'.')
                    plt.xlabel('PCA1: %.2f' % pca.explained_variance_ratio_[0])
                    plt.ylabel('PCA2: %.2f' % pca.explained_variance_ratio_[1])
                
            plt.subplot(121)
            for k in range(N):
        #        plt.plot(wf_sel[:,km.labels_==k],co[k])
                x=wf_sel[:,km.labels_==k]
                mu=np.mean(x,axis=1)
                sdpos=np.mean(x,axis=1)+2*np.std(x,axis=1)
                sdneg=np.mean(x,axis=1)-2*np.std(x,axis=1)
        #        plt.plot(mu,co[k+2])
                plt.plot(sdpos,co[k])
                plt.plot(sdneg,co[k])    
            plt.show()   
        
        #plt.close('all')
        if N>1:
            for k in range(N):
                print('unit %d:' % k,sum(km.labels_==k),'spikes')
            sortcode[ch]=km.labels_
        else:
            print('unit 0:',len(sp),'spikes')
            sortcode[ch]= np.zeros(len(sp))
        if artifact_rejection:
            sortcode[ch][indloc]=9
            
        tocont=input('continue? (Y/n/m)')
        if (tocont=='')|(tocont=='y'):
            ch+=1
            np.save(os.path.join(sdir,'sorter','sortcode.npy'),sortcode)
        if tocont=='m':
            ch+=1
            sortcode[ch]= np.zeros(len(sp))
            print('unit 0:',len(sp),'spikes')
            np.save(os.path.join(sdir,'sorter','sortcode.npy'),sortcode)
            
        print('\n')
    else:
        ch+=1
        
#%%
print('saving spiketrain data...')
from ttankpy.postprocess import getspiketrains
S=getspiketrains(sdir)
np.save(os.path.join(sdir,'spiketrain.npy'),S)


