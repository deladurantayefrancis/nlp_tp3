import pandas as pd
import re

from tqdm import tqdm


blog = 'blog'
classe = 'classe'


corpus = pd.read_csv('data/train_posts.csv', names=[blog, classe])
with open('data/train_posts.txt', 'w') as file:
	for entry in tqdm(corpus[blog]):
		entry = re.sub(r'^["\']', '', entry)
		file.write(re.sub(r'["\']$', '', entry) + '\n')
