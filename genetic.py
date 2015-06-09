import random

def mutate(parent, geneSet):
   geneIndex = random.randint(0, len(geneSet) -1);
   index = random.randint(0, len(parent) - 1)
   genes = list(parent)
   genes[index] = geneSet[geneIndex]
   return(''.join(genes))

def generateParent(length, geneSet):
    genes = list("")
    for i in range(0,length):
        geneIndex = random.randint(0, len(geneSet) -1);
        genes.append(geneSet[geneIndex])
    return(''.join(genes))

def getBest(get_fitness, display, targetLen, geneSet):
    random.seed()
    bestParent = generateParent(targetLen, geneSet)
    bestFitness = get_fitness(bestParent)
    display(bestParent)

    while bestFitness < len(bestParent):
       child = mutate(bestParent, geneSet)
       childFitness = get_fitness(child)

       if childFitness > bestFitness:
          bestFitness = childFitness
          bestParent = child
          display(bestParent)
    return bestParent
