import unittest
import datetime
import genetic

def getFitness(candidate, target):
   fitness = 0
   for i in range(0, len(candidate)):
       if target[i] == candidate[i]:
           fitness += 1
   return(fitness)

def display(candidate, target, startTime):
    timeDiff = datetime.datetime.now() - startTime
    fitness = getFitness(candidate, target)
    print ("%s\t%i\t%s" % (candidate, fitness, str(timeDiff)))

class StringDuplicationTests(unittest.TestCase):
    def test(self):
        geneset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."
        startTime = datetime.datetime.now()
        target = "Not all those who wander are lost."
        fnDisplay = lambda candidate: display(candidate, target, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, target)
        best = genetic.getBest(fnGetFitness, fnDisplay, len(target), geneset)
        self.assertEqual(best, target)

if __name__ == '__main__':
    unittest.main()
