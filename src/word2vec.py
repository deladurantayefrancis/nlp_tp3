import os
import pandas as pd
import spacy
import sys
import time

from tqdm import tqdm

from gensim import models, utils
from gensim.models.phrases import Phrases, Phraser


# command line arguments
thresholds, sizes = sys.argv[1], sys.argv[2]

thresholds = [int(t) for t in thresholds.split(',')]
sizes = [int(s) for s in sizes.split(',')]


with open('data/train_posts.txt', 'r') as file:
	sentences = file.readlines()

sentences = [utils.simple_preprocess(sent) for sent in sentences]


for threshold in thresholds:
	start = time.time()
	phrases = Phrases(sentences, threshold=THRESHOLD)
	bigram = Phraser(phrases)
	sents = [bigram[sent] for sent in sentences]
	print(f'phraser_{threshold}:', time.time() - start)

	for size in sizes:
		FOLDER = f'model_T-{threshold}_S-{size}'
		os.makedirs(FOLDER, exist_ok=True)
		start = time.time()
		model = models.Word2Vec(sentences=sents, size=SIZE)
		model.wv.save_word2vec_format(f'{FOLDER}/word2vec.txt')
		print(f'word2vec_{size}:', time.time() - start)
