#!/bin/bash

cat data/train_posts.txt |\
    #head -n 1000 |\
    tr ' ' '\012' | sort | uniq -c | sort -k1,1nr > out/word_freqs.txt
