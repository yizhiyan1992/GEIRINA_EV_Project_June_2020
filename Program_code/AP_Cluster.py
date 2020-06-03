import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AffinityPropagation
from itertools import cycle

f=pd.read_csv(r'C:/Users/Zhiyan/Desktop/nodes.csv')
x=f['Lon'].values
y=f['Lat'].values
x_mean=np.mean(x)
y_mean=np.mean(y)
x-=x_mean
y-=y_mean
X=np.array([[i[0],i[1]] for i in zip(x,y)])
plt.scatter(x,y)
plt.savefig(r'C:/Users/Zhiyan/Desktop/p.png')

# #############################################################################
# Compute Affinity Propagation
af = AffinityPropagation(preference=-0.5).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
n_clusters_ = len(cluster_centers_indices)
affinity=af.affinity_matrix_
affinity=pd.DataFrame(affinity)
#affinity.to_csv(r'C:/Users/Zhiyan/Desktop/A_matrix.csv')
# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=3)
    print(X[class_members])
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.savefig(r'C:/Users/Zhiyan/Desktop/p3.png')
plt.show()
