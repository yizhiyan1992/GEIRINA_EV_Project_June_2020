import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from itertools import cycle

f=pd.read_csv(r'C:/Users/Zhiyan/Desktop/Info_UT.csv')
id=f['ID'].values
x=f['Lon'].values
y=f['Lat'].values
x_mean=np.mean(x)
y_mean=np.mean(y)
x-=x_mean
y-=y_mean
X=np.array([[i[0],i[1]] for i in zip(x,y)])

# #############################################################################
# Compute Affinity Propagation, K-Means, and Agglomerative
#af = AffinityPropagation(preference=-0.0001).fit(X)
af=AgglomerativeClustering(n_clusters=10,affinity='euclidean',linkage='complete').fit(X)
#af=KMeans(n_clusters=10).fit(X)
labels = af.labels_

print(len(labels))
doc=open(r'C:/Users/Zhiyan/Desktop/ut_cluster.txt','w')
for i in range(len(labels)):
    doc.write(str(id[i])+','+str(labels[i])+'\n')
doc.close()
# #############################################################################
# Plot result
import matplotlib.pyplot as plt
plt.scatter(x,y,c=labels,s=5,cmap='Paired')
plt.savefig(r'C:/Users/Zhiyan/Desktop/Kmean.png')
plt.show()
