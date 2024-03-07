import numpy as np
from scipy import stats
import pandas as pd
from .likelihoods import NullHypothesis, AlternateHypothesis

class ERSA:
    def __init__(self, match_file, threshold=2.5, \
                 theta=3.12, max_d=10, alpha=0.1, out='ersa_ibd.genome'):
        '''
        params
            match_file: string
                path to the GERMLINE output .match file.
            threshold: float
                minimum segment length threshold in cM.
            theta: float
                mean shared segment length in given population cM.
                Used for null hypothesis
            max_d: int
                max combined number of generations separating 
                individuals from their ancestors
            alpha: float
                likelihood ratio test significance level to reject null hypothesis
            out: string
                output filename

        '''
        # segment length > 2.5 cM achieves false-negative 
        # rate < 1% based upon germline.
        self.threshold = threshold
        self.theta = theta
        # read match file as pandas df
        self.read_germline(match_file)

        # number of autosomes
        self.c = 22
        # expected number of recombination events per haploid genome per generation (from McVean et all 2004)
        self.r = 35.3
        # number of shared ancestors
        self.a = 2
        self.alpha = alpha
        self.max_d = max_d
        self.out = out
        # prep Null and Alternate Hypothesis
        self.H_0 = NullHypothesis(lambda_val=self.lambda_val, t=self.threshold, theta=self.theta)
        self.H_A = AlternateHypothesis(lambda_val=self.lambda_val, t=self.threshold, \
                                       theta=self.theta, r=self.r, c=self.c, a=self.a)

    
    def read_germline(self, filename):
        '''
        Reads the germline output file into a pandas dataframe.

        Columns:
            FID1:         Family ID 1
            IID1:         Individual ID 1
            FID2:         Family ID 2
            IID2:         Individual ID 2
            CHR:          Chromosome
            bp_start:     Segment start (bp)
            bp_end:       Segment end (bp)
            snp_start:    Segment start (SNP)
            snp_end:      Segment end (SNP)
            total_snp:    Total SNPs in segment
            length:       Genetic length of segment
            length_unit:  Units for genetic length (cM or MB)
            snp_mismatch: Mismatching SNPs in segment
            homozygous1:  1 if Individual 1 is homozygous in match; 0 otherwise
            homozygous2:  1 if Individual 2 is homozygous in match; 0 otherwise
        '''
        germline_cols = ['FID1', 'IID1', 'FID2', 'IID2', 'CHR', 'bp_start', 'bp_end', \
                         'snp_start', 'snp_end', 'total_snp', 'length', 'length_unit', \
                         'snp_mismatch', 'homozygous1', 'homozygous2']
        df = pd.read_csv(filename, sep='\s+', names=germline_cols)
        # filter out values less than threshold
        df = df[df['length'] >= self.threshold]

        # make sure all lengths are in centiMorgan like in the paper
        assert (np.all(df['length_unit'] == 'cM') or np.all(df['length_unit'] == 'MB')), \
            'All segment lengths must be in cM or MB'

        # create smaller dataframe to work with later
        self.data = {}
        for i, pair in df.iterrows():
            iid_1 = pair['IID1']
            iid_2 = pair['IID2']
            # make key in sorted order eg. NA06993-NA07056 will always be the key regardless of which iid is first
            if iid_1 < iid_2:
                data_key = iid_1 + '-' + iid_2
            else:
                data_key = iid_2 + '-' + iid_1
            length = pair['length']

            # add segment length to list of segment lengths for pairs of individuals
            if self.data.get(data_key, -1) == -1:
                self.data[data_key] = []
            
            self.data[data_key].append(length)

        # sort in ascending order of length
        self.lambda_val = 0.
        for pair in self.data:
            self.data[pair] = sorted(self.data[pair], reverse=True)
            self.lambda_val += len(self.data[pair])
        # get lambda: mean of number segments shared in population
        if len(self.data) > 0:
            self.lambda_val /= len(self.data)

    @staticmethod
    def likelihood_ratio_test(h_0, h_A, alpha):
        '''
        Likelihood ratio test. Returns True if we reject the null hypothesis and False otherwise
        params
            h_0: float
                null_hypothesis 
            h_A: float
                Alternative hypothesis
            alpha: float
                likelihood ratio test significance level to reject null hypothesis
        '''
        # wilk's theorem
        ratio = -2 * h_0 + 2 * h_A 
        # get probability associated with chisquared
        # degrees of freedom is difference in parameters from alternate hypothesis and null hypotheses
        chisquare_prob = stats.chi2.cdf(ratio, 2)
        # area under the chi-squared distribution tail greater than the calculated statistic
        p = 1 - chisquare_prob
        if p < alpha:
            return True
        else:
            return False

    def confidence_interval(self, h_As, best_h_A):
        '''
        Returns lower and upper bounds for d for the alternate hypothesis
        params
            h_As: list
                All alternative hypothesis found for different d values
            best_h_A: float
                Best Alternative hypothesis
        '''
        lower_d = np.inf
        upper_d = -np.inf
        lower_found = False
        upper_found = False
        for h_A, d in h_As:
            reject_hypothesis = self.likelihood_ratio_test(h_A, best_h_A, self.alpha)
            if reject_hypothesis == False:
                if d < lower_d:
                    lower_d = d
                    lower_found = True
                elif d > upper_d:
                    upper_d = d
                    upper_found = True
        if lower_found and upper_found:
            return lower_d, upper_d
        else:
            return None, None

    def predict_ibd(self):
        unrelated_pairs = []
        related_pairs = {}
        for pair in self.data:
            # list of segment lengths for individuals
            s = self.data[pair]

            # get null hypothesis log likelihood
            h_0_likelihood = self.H_0.log_likelihood(s)

            # get alternate hypothesis likelihood. Depends on max_d
            best_h_A_likelihood = -np.inf
            # best estimate for combined number of generations separating 
            # individuals from their ancestors
            best_d = None
            # estimated number of shared segments inherited from recent ancestors
            best_n_a = None
            # test out different combined generations from 1 to the maximum (defaults to 10)
            alternate_likelihoods = []
            for d in range(1, self.max_d+1):
                h_A_likelihood, n_a = self.H_A.log_likelihood(s, d)
                alternate_likelihoods.append((h_A_likelihood, d))
                if h_A_likelihood > best_h_A_likelihood:
                    best_h_A_likelihood = h_A_likelihood
                    best_d = d
                    best_n_a = n_a
            
            # logic for rejecting the null hypothesis
            reject_null = self.likelihood_ratio_test(h_0_likelihood, best_h_A_likelihood, self.alpha)
            if reject_null == True:
                lower_d, upper_d = self.confidence_interval(alternate_likelihoods, best_h_A_likelihood)
                related_pairs[pair] = {'d': best_d, 'lower_d' : lower_d, 'upper_d': upper_d, 'n_a': best_n_a,\
                                       'total': len(s), 's': s}
                # TODO Estimate relationship

                # self.estimate_relationship()
            else:
                unrelated_pairs.append(pair)

        # TODO write file same as plink format
        relative_predictions = {}
        for pair in related_pairs:
            d = related_pairs[pair]['d']
            n_a = related_pairs[pair]['n_a']
            if d==4 and n_a > 25:
                if relative_predictions.get('First Cousins', -1) == -1:
                    relative_predictions['First Cousins'] = []
                relative_predictions['First Cousins'].append(pair)
            elif d==2 and n_a > 75:
                if relative_predictions.get('Siblings', -1) == -1:
                    relative_predictions['Siblings'] = []
                relative_predictions['Siblings'].append(pair)
            elif d==3 and n_a > 50:
                if relative_predictions.get('Avuncular', -1) == -1:
                    relative_predictions['Avuncular'] = []
                relative_predictions['Avuncular'].append(pair)
            elif d==6 and n_a > 10:
                if relative_predictions.get('Second Cousins', -1) == -1:
                    relative_predictions['Second Cousins'] = []
                relative_predictions['Second Cousins'].append(pair)
        print(relative_predictions)

if __name__ == '__main__':
    # germline outputs a .match file
    match_file = '../data/test/germline/expected.match'
    ersa = ERSA(match_file, threshold=2.5)
    ersa.predict_ibd()
