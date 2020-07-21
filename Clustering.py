from keras.preprocessing.text import Tokenizer
import pandas as pd
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
## read the whole file

data_frame = pd.read_csv('C:/Users/imonb/Box/Imon Banerjee\'s Files/Tina_SSRI/Training_data/train_df.csv')


docs = list(data_frame['SNIPPET'])
# create the tokenizer
t = Tokenizer(num_words = 100)
# fit the tokenizer on the documents
t.fit_on_texts(docs)
# summarize what was learned
print(t.word_counts)
print(t.document_count)
print(t.word_index)
print(t.word_docs)
# integer encode documents
encoded_docs = t.texts_to_matrix(docs, mode='count')
X_embedded = TSNE(n_components=2).fit_transform(encoded_docs)

## clustering 
# #############################################################################
# Compute clustering with Means

k_means = KMeans(init='k-means++', n_clusters=6, n_init=10)
k_means.fit(encoded_docs)
k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)

k_means_labels_train = pairwise_distances_argmin(encoded_docs, k_means_cluster_centers)
## Visualization

fig = plt.figure(figsize=(8, 3))

for k in range(0,5):
    my_members = k_means_labels_train == k
    cluster_center = k_means_cluster_centers[k]
    plt.plot(X_embedded[my_members, 0], X_embedded[my_members, 1], 'w', marker='.')
    plt.plot(cluster_center[0], cluster_center[1], 'o',
            markeredgecolor='k', markersize=6)
plt.show()

## test


data_testing  = pd.read_csv('C:/Users/imonb/Box/Imon Banerjee\'s Files/Tina_SSRI/Training_data/test_df.csv')


test_encoded_docs = t.texts_to_matrix(list(list(data_testing ['SNIPPET'])), mode='count')


k_means_labels = pairwise_distances_argmin(test_encoded_docs, k_means_cluster_centers)



data_testing['Cluster_labels'] = k_means_labels


data_testing.to_csv('C:/Users/imonb/Box/Imon Banerjee\'s Files/Tina_SSRI/Training_data/cluster_df.csv')
