import unittest
import datetime
import genetic


def getFitness(candidate, target):
    fitness = 0
    for i in range(0, len(candidate)):
        if target[i] == candidate[i]:
            fitness += 1
    return fitness


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" % (candidate.Genes, candidate.Fitness, str(timeDiff)))


class StringDuplicationTests(unittest.TestCase):
    def test(self):
        geneset = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.'
        startTime = datetime.datetime.now()
        target = "Not all those who wander are lost."
        fnDisplay = lambda candidate: display(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, target)
        best = genetic.getBest(fnGetFitness, fnDisplay, len(target), geneset)
        self.assertEqual(best.Genes, target)


if __name__ == '__main__':
    unittest.main()
