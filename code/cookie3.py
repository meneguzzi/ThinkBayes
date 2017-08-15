from os import path
import sys

# Solution to Exercise 1 in page 19

from cookie2 import Cookie

class CookieNoReplacement(Cookie):
    def __init__(self,hypos):
        Cookie.__init__(self,hypos)

    def Update(self, data):
        """Updates the PMF with new data, removing the cookies

                data: string cookie type
                """

        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()

        # After computing the posterior, update the mixes without one of the data
        for hypo in self.Values():
            mix = self.mixes[hypo]
            mix[data] -= 1/self.Total()


def main():
    hypos = ['Bowl 1', 'Bowl 2']

    pmf = Cookie(hypos)

    pmf.Update('vanilla')

    for hypo, prob in pmf.Items():
        print hypo, prob

    pmf = Cookie(hypos)

    dataset = ['vanilla', 'chocolate', 'vanilla']
    for data in dataset:
        pmf.Update(data)

    for hypo, prob in pmf.Items():
        print hypo, prob

    pmf = CookieNoReplacement(hypos)

    dataset = ['vanilla', 'chocolate', 'vanilla']
    for data in dataset:
        pmf.Update(data)

    for hypo, prob in pmf.Items():
        print hypo, prob


if __name__ == '__main__':
    main()
