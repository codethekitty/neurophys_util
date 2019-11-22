import glob,os
import numpy as np
from ttankpy.extract import getspikes,getwf,getepocs


def listallblocks(dir_name):
    allblocks = glob.glob(os.path.join(dir_name,'*.mat'))
    allblocks = [os.path.basename(x) for x in allblocks]
    return allblocks

def loadallinfo(dir_name):
    allblocks = listallblocks(dir_name)
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    info={}
    for i,x in enumerate(allblocks):
        out=getspikes(os.path.join(dir_name,x))
        a.extend(out['ch'])
        b.extend(out['ts'])
        c.extend([i]*len(out['ch']))
        d.extend(out['ts_sw'])
        e.extend(out['trial'])
        print(x)
    info['ch']=np.array(a)
    info['ts']=np.array(b)
    info['bl']=np.array(c)
    info['ts_sw']=np.array(d)
    info['trial']=np.array(e)
    return info
    
def loadallspikes(dir_name):
    allblocks = listallblocks(dir_name)
    wfall=np.empty((int(1e7),30))
    wfall[:]=np.nan
    c=0
    for x in allblocks:
        out=getwf(os.path.join(dir_name,x))
        wfall[c:c+np.size(out,axis=1),:]=np.transpose(out)
        c+=np.size(out,axis=1)+1
        print(x)
    
    wfall=wfall[np.sum(~np.isnan(wfall),axis=1)==30,:]
    return wfall

def loadallepocs(dir_name):
    allblocks = listallblocks(dir_name)
    epocs={}
    for i,x in enumerate(allblocks):
        epocs[i]=getepocs(os.path.join(dir_name,x))
    return epocs