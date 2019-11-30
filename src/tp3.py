import numpy as np
import os
import pandas as pd
import re
import spacy
import sys

from gensim import models, utils
from scipy.spatial import distance
from tqdm import tqdm


FOLDER = sys.argv[1]
nlp = spacy.load(f'{FOLDER}/spacy.word2vec.model/')


keys = list(nlp.vocab.vectors.keys())
vectors = np.asarray([nlp.vocab.vectors[key] for key in keys])
#vectors = vectors[:50000]



"""
with open('data/common_words.txt', 'r') as file:
	words = file.readlines()
words = np.asarray([re.sub(r'\n', '', word) for word in words])
vec = np.asarray([nlp(word).vector for word in words.tolist()])

#for word in words.tolist():
#	print(word, '-', nlp(word).vector)
dists = 1 - distance.cdist(vec, vectors, metric='cosine')
n_neighbors = np.sum(dists >= .6, axis=1)
most_neighbors = np.flip(np.argsort(n_neighbors))
sort_ids = np.flip(np.argsort(dists, axis=1), axis=1)[:, 1:]  # to remove <self> from neighbor list

most_neighbors = np.flip(np.argsort(n_neighbors))
with open('out/voisins2', 'w') as file:
	for i, word_idx in enumerate(most_neighbors):
		word = words[word_idx]
		neighbor_cnt = n_neighbors[word_idx] - 1  # to remove <self> from the count
		neighbors = ' '.join([nlp.vocab[keys[sort_ids[word_idx, j]]].text
			for j in range(min(neighbor_cnt, 14))])
		file.write('%-20s' % word)
		file.write(f'{neighbor_cnt} {neighbors}\n')
"""




batch_size = 1024
n_batches = int(np.ceil(vectors.shape[0] / batch_size))

n_neighbors = np.zeros(vectors.shape[0], dtype=np.int)

for batch_idx in tqdm(range(n_batches)):
	start = batch_idx * batch_size
	end = start + batch_size

	vec = vectors[start:end]
	dists = 1 - distance.cdist(vec, vectors, metric='cosine')

	n_neighbors[start:end] = np.sum(dists >= .6, axis=1)


most_neighbors = np.flip(np.argsort(n_neighbors))

vec = vectors[most_neighbors[:batch_size]]
dists = 1 - distance.cdist(vec, vectors, metric='cosine')
sort_ids = np.flip(np.argsort(dists, axis=1), axis=1)[:, 1:]  # to remove <self> from neighbor list

with open('out/voisins', 'w') as file:
	for i, word_idx in enumerate(most_neighbors):
		word = nlp.vocab[keys[word_idx]].text
		neighbor_cnt = n_neighbors[word_idx] - 1  # to remove <self> from the count
		neighbors = ' '.join([nlp.vocab[keys[sort_ids[i, j]]].text
			for j in range(min(neighbor_cnt, 14))])
		file.write('%-20s' % word)
		file.write(f'{neighbor_cnt} {neighbors}\n')

