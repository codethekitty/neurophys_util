import numpy as np

def tracerf(rf):
    
    sigpos=np.mean(rf[:,0])+2*np.std(rf[:,0])
    rft = rf>sigpos
    
    thrs=[]
    for j,x in enumerate(rft):
        c=False
        i=0
        while (~c)&(i<(np.size(rf,axis=1)-2)):
            c=x[i]&x[i+1]&x[i+2]
            i+=1
        thrs.append(i)      
    
    tsel1=set(np.where(thrs==np.min(np.array(thrs)))[0])
    tsel2=set([np.argmax(np.sum(rf,axis=1))])
    
    if tsel1&tsel2:
        thrindex = int(np.median(list(tsel1&tsel2)))
    else:
        thrindex = int(np.median(list(tsel1)))
    
    return (np.array(thrs),thrindex)




def rfborder(M):
    m=M[:,0]
    crit = np.mean(m)+4*np.std(m)
    mt = 1*(M>crit)
    b=[]
    for i in mt:
        ix=np.where(i==1)[0]
        if len(ix)==0:
            ix=np.size(M,axis=1)
        elif len(ix)>1:
            ix2=np.where(np.diff(ix)==1)[0]
            if len(ix2)>0:
                ix=ix[np.where(np.diff(ix)==1)[0]][0]
            else:
                ix=ix[-1]
        else:
            ix=ix[0]
        b.append(ix)
    b=np.array(b).clip(max=len(m))
    return b
