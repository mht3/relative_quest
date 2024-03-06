# Relative Quest

## Overview
Relative Quest is a tool that explores kinship using GERMLINE combined with Estimations of Recent Shared Ancestry (ERSA). GERMLINE is an algorithm for determining the length and number of shared segments of IBD between pairs of individuals. ERSA
takes in the length and number of shared segments between individuals and estimates the shared ancestry using a maximum-likelihood estimation. Our goal is to encapsulate these methods into a command line tool similar to the ```plink --genome``` command. 

## Team
The members working on this project are:
1. Aashish Bhole, Grad Student, Computer Science and Engineering
2. Arjun Badami, Grad Student, Computer Science and Engineering
3. Matthew Taylor, Grad Student, Computer Science and Engineering

## Code Structure
```relative_quest/``` contains:

```codes/```:

- ```ersa.py```: Main code for ERSA calculations given the output data from GERMLINE. 
- ```ibd_results.py```: Function to visualize IBD predictions from both plink and relative quest. 
- ```likelihoods.py```: Helper python file for `ersa.py`. Calculates the log-likelihoods for the null and alternate hypothesis. 

```data/```:

- ```test/```: Location of test inputs for GERMLINE and ERSA 
- ```1000Genomes/```: Location for all 1000Genomes data. See "Instructions" on how to download this data.

## Instructions

First, install the required Python libraries using pip. We recommend creating a virtual pip or conda environment first before running this command. 

```
pip install -r requirements.txt
```

you can install `relative_quest` with the following command:

```
python setup.py install
```

Note: if you do not have root access, you can run the command above with additional options to install locally:
```
python setup.py install --user
```

If the install was successful, typing `relative_quest --help` should show a useful message.

## Basic usage

The basic usage of `relative_quest` is:

```
relative_quest in.ped in.map --out out_prefix
```


### Test Example
`relative_quest` takes a .ped file and a .map file as input (both are required). Here are the commands you can run
to create these files:

To create .ped and .map files from bfiles/vcf, use the script provided:
```
./create_ped_files.sh <input_genotype_data_file> <output_directory_prefix>
```

Example: To create .ped and .map files from a bfile for test data ps2_ibd.lwk in the ped_maps directory, the command would be:
```
./create_ped_files.sh data/plink/ps2_ibd.lwk ped_maps/lwk
```

Once the .ped and .map files have been generated, you can run the `relative_quest` command with the file parameters

### Dataset

Download 1000Genomes [here](https://drive.google.com/file/d/1CPK7M0g62NIsAbrEgZ3WhLuMi04KhnXu/view?usp=sharing).

Sample GERMLINE input files (.map & .ped) can be found [here](https://drive.google.com/file/d/1Hzw5Z9CKX2gBfwGjbbKBB7des02fDM8y/view?usp=sharing)

LWK GERMLINE input files (.map & .ped): [here](https://drive.google.com/file/d/1ybhXOl5O1cu3g8gcYnR5w41RaI6PtfWS/view?usp=sharing)

## Remaining Work

1. Polish the README.md
2. Parse the ERSA output dictionary to give kinship/IBD values
3. Add comparison of Relative Quest results with Plink for a subset of population from 1000 Genomes
