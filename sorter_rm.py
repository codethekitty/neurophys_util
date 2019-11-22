from pylab import *

exp = 'M418_1'
rm = 17

import os
scdir = os.path.join('Z:\Calvin\Analysis\corfas_ATA',exp,'sorter','sortcode.npy')
L=load(scdir);

L.item().pop(rm)

save(scdir,L.item())

#%%