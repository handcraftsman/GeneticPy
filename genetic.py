import random


def crossover(parent, parent2, get_fitness):
    index = random.randint(0, len(parent.Genes) - 1)
    childGenes = list(parent.Genes)
    childGenes[index] = parent2.Genes[index]
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def mutate(parent, geneSet, get_fitness):
    geneIndex = random.randint(0, len(geneSet) - 1)
    index = random.randint(0, len(parent.Genes) - 1)
    childGenes = list(parent.Genes)
    childGenes[index] = geneSet[geneIndex]
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def generateParent(length, geneSet, get_fitness):
    childGenes = []
    for i in range(0, length):
        geneIndex = random.randint(0, len(geneSet) - 1)
        childGenes.append(geneSet[geneIndex])
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def getBest(get_fitness, display, targetLen, optimalFitness, geneSet):
    random.seed()
    bestParent = generateParent(targetLen, geneSet, get_fitness)
    display(bestParent)

    options = {
        0: lambda p: mutate(p, geneSet, get_fitness),
        1: lambda p: crossover(p, bestParent, get_fitness)
    }

    while bestParent.Fitness < optimalFitness:
        parent = generateParent(targetLen, geneSet, get_fitness)
        attemptsSinceLastImprovement = 0
        while attemptsSinceLastImprovement < 128:
            child = options[random.randint(0, len(options) - 1)](parent)
            if child.Fitness > parent.Fitness:
                parent = child
                attemptsSinceLastImprovement = 0
            attemptsSinceLastImprovement += 1

        if bestParent.Fitness < parent.Fitness:
            bestParent, parent = parent, bestParent
            display(bestParent)

    return bestParent


class Individual:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness
