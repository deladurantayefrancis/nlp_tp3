#!/bin/bash

thresholds="50,100"
sizes="100,200,300"

for t in {50..100..50}
do
    for s in {100..300..100}
    do
        folder="model_T-${t}_S-${s}"
        for resize in {10000..30000..10000}
        do
            python src/voisins.py $folder $resize
        done
    done
done

