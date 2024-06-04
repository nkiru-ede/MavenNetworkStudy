

This repository contains Maven repository data extracted in 2018 by [Benelallam et al](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf). The repo contains the Maven artifacts (Source artifacts), their dependencies (Target artifacts), and their release dates. 

The dataset showing the source artifacts, target artifacts and release dates can be downloaded from here: https://drive.google.com/file/d/1--zotLE4XjxfENuuDY_AezTeTJS4EJU-/view?usp=sharing

To illustrate the growth of Maven repository, across the years, we have included three datasets -  GAV1(GAV1.tsv), GAV2(GAV2.tsv) and GAV3(GAV3.tsv) - the three datasets shows the maven artifacts, their dependencies and release dates.

To get a true sense of the actual growth of the Maven repository, we look further into the aggregation of GAV that ignores version (GA) and artifact id (G) - two data sets show this - GA.tsv contains maven artifacts (without versions), their dependencies and release dates
          - G.tsv contains the maven groups (without versions and artifact id), their dependencies and release dates

[Schema_G.tsv](data/Schema_G.tsv), [Schema_GA.tsv](data/Schema_GA.tsv), [Schema_GAV.tsv](data/Schema_G.tsv)  - outlines the nature of all datasets



Steps to replicate:

## Reproducing Results

### Prerequisites

TODO: Version of Python required, etc. Should switch later to Docker.

### Steps

#### Step 1: Acquire dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) paper and build GAV directed graph

| Input | Output |
| --- | --- |
| [TODO: Zenodo dataset](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) | `data/GAV/GAV1.csv`, `data/GAV/GAV2.csv`, ..., `data/GAV/GAV73.csv` |
| Notes | Files are in TSV format |

#### Step 2: Aggregated GAV graph to GA and G graphs as described in paper section TODO

| Script | Input | Output |
| --- | --- | --- |
| `Project/aggregate_ga.py`, `Project/aggregate_g.py` | `data/GAV/GAV1.csv`, `data/GAV/GAV2.csv`, ..., `data/GAV/GAV73.csv`, `data/test_data` | `data/GA.zip`, `data/G.tsv` |
| Notes | TODO |
| Tests | `tests/test_aggregate_g.py`, `tests/test_aggregate_ga.py` |


[experiments](experiments.md)




