# relative_quest
Relative Quest is a tool that explores kinship using GERMLINE combined with Estimations of Recent Shared Ancestry (ERSA). GERMLINE is an algorithm for determining the length and number of shared segments of IBD between pairs of individuals. ERSA
takes in the length and number of shared segments between individuals and estimates the shared ancestry using a maximum-likelihood estimation. Our goal is to encapsulate these methods into a command line tool similar to the ```plink --genome``` command. 


## Code Structure
```relative_quest/``` contains:

```code/```:

- ```ersa.py```: Main code for ERSA MLE calculations. 
- ```ibd_results.py```: Function to visualize IBD predictions from both plink and relative quest. 
- ```likelihoods.py```: Helper python file for `ersa.py`. Calculates the log-likelihoods for the null and alternate hypothesis. 

```data/```:

- ```test/```: Location of test inputs for GERMLINE and ERSA 
- ```1000Genomes```: Location for all 1000Genomes data. See "Instructions" on how to download this data.

## Instructions

To do (installing germline, test example, dataset)

### Test Example

To do (instructions for lwk dataset)

### Dataset

Download 1000Genomes [here](https://drive.google.com/file/d/1CPK7M0g62NIsAbrEgZ3WhLuMi04KhnXu/view?usp=sharing).

Sample GERMLINE input files (.map & .ped) can be found [here](https://drive.google.com/file/d/1Hzw5Z9CKX2gBfwGjbbKBB7des02fDM8y/view?usp=sharing)

LWK GERMLINE input files (.map & .ped): [here](https://drive.google.com/file/d/1ybhXOl5O1cu3g8gcYnR5w41RaI6PtfWS/view?usp=sharing)

## Remaining Work

To do (remaining work and challenges)
