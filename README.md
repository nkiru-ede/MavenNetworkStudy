

This repository contains Maven repository data extracted in 2018 by [Benelallam et al](https://ieeexplore.ieee.org/iel7/8804710/8816727/08816814.pdf). The repo contains the Maven artifacts (Source artifacts), their dependencies (Target artifacts), and their release dates. 

The dataset showing the source artifacts, target artifacts and release dates can be downloaded from here: https://drive.google.com/file/d/1--zotLE4XjxfENuuDY_AezTeTJS4EJU-/view?usp=sharing

To illustrate the growth of Maven repository, across the years, we have included three datasets -  GAV1(GAV1.tsv), GAV2(GAV2.tsv) and GAV3(GAV3.tsv) - the three datasets shows the maven artifacts, their dependencies and release dates.

To get a true sense of the actual growth of the Maven repository, we look further into the aggregation of GAV that ignores version (GA) and artifact id (G) - two data sets show this - GA.tsv contains maven artifacts (without versions), their dependencies and release dates
          - G.tsv contains the maven groups (without versions and artifact id), their dependencies and release dates

[Schema_G.txt](data/Schema_G.txt), [Schema_GA.txt](data/Schema_GA.txt), [Schema_GAV.txt](data/Schema_GAV)  - outlines the nature of all datasets



Steps to replicate:
1. Download the 'Project' folder
2. Download dataset containing the source and target artifacts via the link into the project folder - https://drive.google.com/file/d/1--zotLE4XjxfENuuDY_AezTeTJS4EJU-/view?usp=sharing
3. Ensure that your project directory look like this
my_project/
├── run_dataanalysis.bat
├── dataAnalysis.py
├── requirements.txt
├── 2018dataset.csv


5. execute 'run_dataanalysis.bat'

Steps to unit testing:
1. Download unittest folder
2. Ensure the downloaded folder look like [test_steps.md]




4. Unit Test: can be run with the run_tests.bat or running the command run_tests.bat from command prompt




