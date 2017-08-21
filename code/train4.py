# Written by Felipe Meneguzzi
# Solution to Exercise 3.1 in page 31
# TODO - This is still very incomplete

import thinkbayes
import thinkplot

from thinkbayes import Pmf, Percentile
from train3 import Train2

class TrainCompanies(Train2):
    """Represents hypotheses about how many trains the company has."""

    def __init__(self, hypos, alpha=1.0):
        """Initializes the hypotheses with a power law distribution.

        hypos: sequence of hypotheses
        alpha: parameter of the power law prior
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, hypo ** (-alpha))
        self.Normalize()

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

            hypo: number of trains the company has
            data: train seen
        """
        if hypo < data:
            return 0
        else:
            return 1.0 / hypo