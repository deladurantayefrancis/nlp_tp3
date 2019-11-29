import os
import pandas as pd
import spacy

from gensim import models, utils
from tqdm import tqdm


# globals
blog = 'blog'
classe = 'class'

# folder used to save the model
os.makedirs('model', exist_ok=True)


class MyCorpus(object):
	"""An interator that yields sentences (lists of str)."""

	def __iter__(self):
		corpus = pd.read_csv('train_posts.csv', names=[blog, classe])
		for line in tqdm(corpus[blog]):
			yield utils.simple_preprocess(line)


sentences = MyCorpus()
model = models.Word2Vec(sentences=sentences)
model.wv.save_word2vec_format('./model/word2vec.txt')
