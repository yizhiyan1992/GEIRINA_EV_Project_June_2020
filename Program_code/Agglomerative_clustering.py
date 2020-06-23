import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from itertools import cycle
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score

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
num_cluster=[2,3,4,5,6,7,8,9,10,11,12,13,14,15]
S=[]
cal=[]
# Compute Affinity Propagation, K-Means, and Agglomerative
#af = AffinityPropagation(preference=-0.0001).fit(X)
#af=KMeans(n_clusters=10).fit(X)
for i in num_cluster:
    #af=KMeans(n_clusters=10).fit(X)
    af=AgglomerativeClustering(n_clusters=i,affinity='euclidean',linkage='complete').fit(X)
    score=silhouette_score(X,af.labels_,metric='euclidean')
    cal_score=calinski_harabaz_score(X,af.labels_)
    print('Silhouette score', score)
    S.append(score)
    cal.append(cal_score)
plt.plot(num_cluster,cal)
plt.title('Evaluation of Different Cluster Results (the State of Utah)')
plt.xlabel('Number of Cluster')
plt.ylabel('Calinski Harabaz Score')
plt.xticks(range(2,16))
plt.savefig(r'C:/Users/Zhiyan/Desktop/LASicsore.png',dpi=300)
plt.show()

af=AgglomerativeClustering(n_clusters=9,affinity='euclidean',linkage='complete').fit(X)
labels = af.labels_

print(len(labels))

doc=open(r'C:/Users/Zhiyan/Desktop/la_cluster.txt','w')
for i in range(len(labels)):
    doc.write(str(id[i])+','+str(labels[i])+'\n')
doc.close()
# #############################################################################
# Plot result
import matplotlib.pyplot as plt
plt.scatter(x,y,c=labels,s=5,cmap='Paired')
plt.savefig(r'C:/Users/Zhiyan/Desktop/AGG_LA.png',dpi=300,transparent=True)
plt.show()
