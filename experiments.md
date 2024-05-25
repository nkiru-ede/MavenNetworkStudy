# Reproducing Results

## Prerequisites

TODO: version of python required etc. Should switch later to docker. 

## Steps


| Step:    | Acquire dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) paper and build GAV directed graph |
| -------- | ------- |
| input:    | TODO: zenodo dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf)    ||
| output: | `data/GAV1.zip`, `data/GAV2.zip` , `data/GAV3.zip`   |
| notes:    | files are in tsv   |





| Step:    | Aggregated GAV graph to GA and G graphs as described in paper section TODO |
| -------- | ------- |
| Script:    | `Project/aggregate_ga.py`, `Project/aggregate_g.py` |
| input:  |  `data/GAV1.zip` , `data/GAV2.zip`, `data/GAV3.zip`  |
| output: | `data/GA.zip` , `data/G.tsv`   |
| notes:    | TODO   |
| tests:    | `tests/unittest.py`   |
