#!/bin/bash

more alternatives_dataset/it_ratings.txt alternatives_dataset/there_ratings.txt | awk '{if($3=="hypernym" || $3=="hyponym" || $3=="cohyponym")  print $0}' | awk '$4 >= 3.5 {print $0}' | awk '{print $3"\t"$2"\t"$1}' | sort -u -k1,1 -k2,3 > cleaned_data.txt
