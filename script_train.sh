#!/bin/bash

folder=$1
threshold=$2
size=$3

python src/word2vec.py $folder $threshold $size

gzip $folder/word2vec_T-${threshold}_S-${size}.txt
python -m spacy init-model en "$folder/spacy.word2vec.model" --vectors-loc "$folder/word2vec_T-${threshold}_S-${size}.txt.gz"

