import numpy as np
import os
import pandas as pd
import re
import spacy
import sys

from gensim import models, utils
from scipy.spatial import distance
from tqdm import tqdm


FOLDER, RESIZE = sys.argv[1], int(sys.argv[2])
os.makedirs('out', exist_ok=True)

nlp = spacy.load(f'{FOLDER}/spacy.word2vec.model/')
nlp.vocab.vectors.resize((RESIZE, nlp.vocab.vectors.shape[1]))

keys = list(nlp.vocab.vectors.keys())
vectors = np.asarray([nlp.vocab.vectors[key] for key in keys])

dists = 1 - distance.cdist(vectors, vectors, metric='cosine')
n_neighbors = np.sum(dists >= .6, axis=1) - 1  # self is not a neighbor

most_neighbors = np.flip(np.argsort(n_neighbors))
sort_ids = np.flip(np.argsort(dists, axis=1), axis=1)

with open(f'out/voisins_{RESIZE}_{FOLDER}', 'w') as file:
	for idx in tqdm(most_neighbors):
		word = nlp.vocab[keys[idx]].text
		neighbors = ' '.join([nlp.vocab[keys[sort_ids[idx, j+1]]].text
			for j in range(min(14, n_neighbors[idx]))])
		file.write('%-25s %-4s %s\n' % (word, n_neighbors[idx], neighbors))
