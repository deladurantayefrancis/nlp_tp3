#!/bin/bash

cat wordsim353_sim_rel/wordsim353_agreed.txt | tail -n +12 | awk '$4 >= 7 {print $0}' | awk '{print $1"\t"$2"\t"$3"\t"}' | sort -u -k1,1 -k2,3 > cleaned_data.txt
