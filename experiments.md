# Reproducing Results

## Prerequisites

TODO: version of python required etc. Should switch later to docker. 

## Steps


| Step:    | Acquire dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) paper and build GAV directed graph |
| -------- | ------- |
| input:    | TODO: zenodo dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf)    ||
| output: | `data/GAV/GAV1.csv`, `data/GAV/GAV2.csv` .... `data/GAV/GAV73.csv`   |
| notes:    | files are in tsv   |





| Step:    | Aggregated GAV graph to GA and G graphs as described in paper section TODO |
| -------- | ------- |
| Script:    | `Project/aggregate_ga.py`, `Project/aggregate_g.py` |
| input:  |  ``data/GAV/GAV1.csv`, `data/GAV/GAV2.csv` .... `data/GAV/GAV73.csv` , `data/GAV/test_data`  |
| output: | `data/GA.zip` , `data/G.tsv`   |
| notes:    | TODO   |
| tests:    | `tests/test_aggregate_g.py` , `tests/test_aggregate_ga.py`  |
