#!/bin/bash

folder=$1

python src/word2vec.py $folder

gzip $folder/word2vec.txt
python -m spacy init-model en "$folder/spacy.word2vec.model" --vectors-loc "$folder/word2vec.txt.gz"

