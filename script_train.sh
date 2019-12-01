#!/bin/bash

threshold=$1
size=$2

folder="model_T-${threshold}_S-${size}"

python src/word2vec.py $folder $threshold $size

gzip $folder/word2vec.txt
python -m spacy init-model en "$folder/spacy.word2vec.model" --vectors-loc "$folder/word2vec.txt.gz"

