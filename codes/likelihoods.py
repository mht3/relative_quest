import numpy as np
import math

class NullHypothesis:
    '''
    Class for null hypotheses: eg pairs of individuals are unrelated
    '''
    def __init__(self, lambda_val, t, theta):
        self.lambda_val = lambda_val
        self.t = t
        self.theta = theta

    def log_likelihood(self, s):
        '''
        Calculates the log likelihood of null hypothesis
        params
            s: list
                list of segment lengths
        '''
        # get number of shared segments
        n = len(s)

        # calculate log-likelihood of sharing n segments
        # log of poisson distribution for single iid
        n_p = -self.lambda_val + n * np.log(self.lambda_val) - np.log(float(math.factorial(n)))

        # calculate log-likelihood of set of segments s
        s_p = 0.
        for i in s:
            # exponential approximation log likelihood for segment of length i
            s_p += -(i - self.t) / self.theta - np.log(self.theta)

        likelihood = n_p + s_p
        return likelihood

class AlternateHypothesis:
    '''
    Class for alternate hypotheses: Individuals share 1 or 2 recent ancestors
    '''
    def __init__(self, lambda_val, t, theta, r=35.3, c=22, a=2):
        self.t = t
        # log_likelihood class for population background
        self.L_p = NullHypothesis(lambda_val, t, theta)

        # expected number of recombination events per haploid genome per generation
        self.r = r
        # number of autosomes
        self.c = c
        self.a = a


    def log_likelihood(self, s, d):
        '''
        Calculates the log likelihood of null hypothesis
        params
            s: list
                list of segment lengths
            d: int
                combined number of generations separating 
                individuals from their ancestors
        '''
        n = len(s)
        # go through combinations of number of shared segments
        # inherited from recent ancestors vs from background
        best_likelihood = -np.inf
        best_n_a = None
        for n_a in range(n+1):
            s_a = s[:n_a]
            s_p = s[n_a:]
            # get background likelhood
            L_p_val = self.L_p.log_likelihood(s_p)
            # probability that a shared segment is linger thatn t
            p_d = np.exp(-d * self.t / 100.)
            # get likelihood 2 individuals share n autosomal segments (poisson)
            lambda_val = (self.a * (self.r * d + self.c) * p_d) / (2 ** (d - 1))

            n_a_val = -lambda_val + n * np.log(lambda_val) - np.log(float(math.factorial(n)))

            # exponential likelihood
            s_a_val = 0.
            for i in s_a:
                # exponential approximation log likelihood for segment of length i
                s_a_val += -d * (i - self.t) / 100. - np.log(100. / d)

            # get final log-likelihood for 2 individuals sharing n autosomal segments
            L_a_val = n_a_val + s_a_val

            # add log likelihoods together
            L_r = L_p_val + L_a_val
            # get maximum likelihood based on n_p and n_a combos
            if L_r > best_likelihood:
                best_likelihood = L_r
                best_n_a = n_a

        return best_likelihood, best_n_a