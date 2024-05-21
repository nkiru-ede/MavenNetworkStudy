# Reproducing Results

## Prerequisites

TODO: version of python required etc. Should switch later to docker. 

## Steps


| Step:    | Acquire dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) paper and build GAV directed graph |
| -------- | ------- |
| Script:    | `scripts/aquire.py` |
| input:  | TODO: zenodo dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf)    |
| output: | `data/GAV.tsv.zip`   |
| notes:    | TODO   |
| tests:    | `tests/test_aquire.py`   |



| Step:    | Aggregated GAV graph to GA and G graphs as described in paper section TODO |
| -------- | ------- |
| Script:    | `scripts/aggregate.py` |
| input:  |  `data/GAV.tsv.zip`   |
| output: | `data/GA.tsv.zip` , `data/G.tsv.zip`   |
| notes:    | TODO   |
| tests:    | `tests/test_ aggregate.py`   |