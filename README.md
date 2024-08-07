

This repository contains Maven repository data extracted in 2018 by [Benelallam et al](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf). The repo contains the Maven artifacts (Source artifacts), their dependencies (Target artifacts), and their release dates. 

To illustrate the growth of Maven repository, across the years, we have included three datasets -  GAV1(GAV1.tsv), GAV2(GAV2.tsv) and GAV3(GAV3.tsv) - the three datasets shows the maven artifacts, their dependencies and release dates.

To get a true sense of the actual growth of the Maven repository, we look further into the aggregation of GAV that ignores version (GA) and artifact id (G) - two data sets show this - GA.tsv contains maven artifacts (without versions), their dependencies and release dates
          - G.tsv contains the maven groups (without versions and artifact id), their dependencies and release dates

[Schema_G.tsv](Project/data/Schema_GA.tsv), [Schema_GA.tsv](Project/data/Schema_GA.tsv), [Schema_GAV.tsv](Project/data/Schema_GAV.tsv)  - outlines the nature of all datasets


Steps to replicate:

## Reproducing Results

### Prerequisites

Use Python version 3.*, tested with 3.12.2

Install git (any version)

Run the below commands to install git lfs and pull datasets links_all and release_all 
```sh
git lfs install
git lfs pull
```

Note: To install dependencies on MacOs, you may need to use 'brew' command

### Steps

#### Step 1: Acquire dataset from [Benellallam et al paper](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) paper and build GAV directed graph

| Input | Output |
| --- | --- |
| [TODO: Zenodo dataset](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) | `Project/data/GAV` |
| Script | Project/datawrang.py|

#### Step 2: Aggregated GAV graph to GA and G graphs as described in paper section TODO

| Script | Input | Output |
| --- | --- | --- |
| `Project/aggregate_ga.py`, `Project/aggregate_g.py` |`Project/data/GAV` |`Project/data/GA.csv`, `Project/data/G.csv`, `Project/plot`
| Tests |test/test_data |`test\test_aggregate_ga.py`, `test_aggregate_g.py`


#### Step 3: Compute Transitive Closures for GAV/GA/G
| Script | Input | Output |
| --- | --- | --- |
| RemoveLoops_Cycles.py |  [TODO: Zenodo dataset](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf) | `Project/data/cleaned_data`|
| SCC.py|Project/data/cleaned_data|Project/data/condensed_dag|
| Transitive_deps.py|Project/data/condensed_dag|Project/data/transitive_dependencies
| `datawrang_trans.py` | `Project/data/transitive_dependencies` | `Project/data/GAV`|
| `Project/aggregate_ga.py`, `Project/aggregate_g.py` | Project/data/GAV| `Project/data/GA.csv`, `Project/data/G.csv`, `Project/plot`|



### Running the Project on a Windows Machine



1. **Ensure Python is installed**:
   - If not installed, download and install Python from [python.org](https://www.python.org/downloads/).


2. **Open Command Prompt**:
   - Press `Win + R`, type `cmd`, and press `Enter`.

3. - Navigate to the directory where you want to clone the repository and execute command: 

```sh
git clone https://github.com/nkiru-ede/MavenNetworkStudy.git
```


4. Navigate to the repository directory:
   ```sh
   cd MavenNetworkStudy\Project
   ```

5. Install dependencies:

```sh
pip install -r requirements.txt

or 

pip3 install -r requirements.txt

```

6. Run the python scripts


```sh
python datawrang.py
python aggregate_ga.py
python aggregate_g.py

```


7. Run tests

```sh
cd test
python test_aggregate_ga.py
python test_aggregate_g.py

```




### Running the Project on a MacOS

1. MacOS usually comes with a Python pre-installed, you can check installed version by executing below command:

```sh
python --version
```

2. - Navigate to the directory where you want to clone the repository and execute command: 

```sh
git clone https://github.com/nkiru-ede/MavenNetworkStudy.git
```


3. Navigate to the repository directory:
   ```sh
   cd MavenNetworkStudy\Project
   ```

4. Install dependencies:

```sh
pip install -r requirements.txt

or 

pip3 install -r requirements.txt

```

5. Run the python scripts


```sh
python datawrang.py
python aggregate_ga.py
python aggregate_g.py

```










