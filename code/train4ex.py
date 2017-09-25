# Written by Felipe Meneguzzi
# Solution to Exercise 3.1 in page 31
# TODO - This is still very incomplete

"""**Exercise 3.1.** To write a likelihood function for the locomotive problem, we had to
   answer this question: "If the railroad has N locomotives, what is the probability
   that we see number 60?"

   The answer depends on what sampling process we use when we observe the locomotive.
   In this chapter, I resolved the ambiguity by specifying that there is only one train-operating
   company (or only one that we care about).

    But suppose instead that there are many companies with different numbers of trains. And suppose
    that you are equally likely to see any train operated by any company. In that case, the likelihood
    function is different because you are more likely to see a train operated by a large company.

    As an exercise, implement the likelihood function for this variation of the locomotive problem,
    and compare the results.

    Note from Felipe: the key question here is, how do you compute the total number of trains in a railroad
    given that you saw a train (or a sequence of trains) and their number, and assuming that there are C companies
    with N_c trains in each company.

    So, we need to implement the likelihood of seeing a train $n \in N_c$.
    Now that changes is that our hypothesis space has to account for the number of companies and the
    number of trains in each company has.
    This is now the ```companies``` value, which states the proportion of locomotives each company has as a total.
    With this I compute the likelihood as
    $P(n \mid N) = \frac{|{c \mid c \in C \land n \leq N_c}|}{N}$

    Assuming I have $C$ companies, each of which with $N_c$ trains
"""

import thinkbayes
import thinkplot

from thinkbayes import Pmf, Percentile
from train3 import Train2, MakePosterior

class TrainCompanies(Train2):
    """Represents hypotheses about how many total trains here are, and the fraction of these trains owned by companies."""

    def __init__(self, hypos, companies=[0.2, 0.2, 0.2, 0.4], alpha=1.0):
        """Initializes the hypotheses with a power law distribution.

        hypos: sequence of hypotheses
        alpha: parameter of the power law prior
        companies: list of fractions
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, hypo ** (-alpha))
        self.Normalize()
        self.companies = companies
        total = sum(companies)
        if total == 0:
            raise ValueError('total distribution of trains is zero.')
        factor = float(1)/total
        for i in range(len(companies)):
            self.companies[i] *= factor


    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

            hypo: number of trains the company has
            data: train seen
        """
        trains_per_company = [None] * len(self.companies)
        for i in range(len(self.companies)):
            trains_per_company[i] = hypo * self.companies[i]

        locomotives_with_number = sum(1 for N in trains_per_company if data <= N)

        return float(locomotives_with_number) / hypo


def main():
    dataset = [30, 60, 90]

    for high in [500, 1000, 2000]:
        suite = MakePosterior(high, dataset, TrainCompanies)
        suite.name = str(high)
        print high, suite.Mean()
        thinkplot.Pmf(suite)

    thinkplot.Save(root='train3ex',
                   xlabel='Number of trains',
                   ylabel='Probability')

    interval = Percentile(suite, 5), Percentile(suite, 95)
    print interval


if __name__ == '__main__':
    main()