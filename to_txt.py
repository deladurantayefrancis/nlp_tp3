import pandas as pd

blog = 'blog'
classe = 'classe'


corpus = pd.read_csv('train_posts.csv', names=[blog, classe])
corpus[blog].to_csv('train_posts.txt', index=False, header=False)