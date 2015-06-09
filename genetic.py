import random

def mutate(parent, geneSet, get_fitness):
   geneIndex = random.randint(0, len(geneSet) -1);
   index = random.randint(0, len(parent.Genes) - 1)
   genes = list(parent.Genes)
   genes[index] = geneSet[geneIndex]
   childGenes = (''.join(genes))
   fitness = get_fitness(childGenes)
   return Individual(childGenes, fitness)

def generateParent(length, geneSet, get_fitness):
    genes = list("")
    for i in range(0,length):
        geneIndex = random.randint(0, len(geneSet) -1);
        genes.append(geneSet[geneIndex])
    childGenes = (''.join(genes))
    fitness = get_fitness(childGenes)
    return Individual(childGenes,fitness)

def getBest(get_fitness, display, targetLen, geneSet):
    random.seed()
    bestParent = generateParent(targetLen, geneSet, get_fitness)
    display(bestParent)

    while bestParent.Fitness < targetLen:
       child = mutate(bestParent, geneSet, get_fitness)

       if child.Fitness > bestParent.Fitness:
          bestParent = child
          display(bestParent)
    return bestParent

class Individual:
   Genes = None
   Fitness = None
   def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness
