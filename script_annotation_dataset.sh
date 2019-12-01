#!/bin/bash

cat annotation_datasets/wordsim353/wordsim353_agreed.txt | tail -n +12 | awk '$4 >= 7 {print $0}' | awk '$1 != "i" {print $1"\t"$2"\t"$3}' | sort -u -k1,1 -k2,3 > out/annotation_dataset.txt

more annotation_datasets/lavi_alternatives/it_ratings.txt annotation_datasets/lavi_alternatives/there_ratings.txt | awk '$4 >= 3.5 {print $0}' | awk '{print $3"\t"$2"\t"$1}' | sort -u -k1,1 -k2,3 >> out/annotation_dataset.txt
