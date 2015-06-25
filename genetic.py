import random


def crossover(parent, parent2, get_fitness):
    destIndex = random.randint(0, len(parent.Genes) - 1)
    srcIndex = destIndex if len(parent2.Genes) > destIndex else random.randint(0, len(parent2.Genes) - 1)
    childGenes = list(parent.Genes)
    childGenes[destIndex] = parent2.Genes[srcIndex]
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def mutate(parent, geneSet, get_fitness, createGene):
    index = random.randint(0, len(parent.Genes) - 1)
    childGenes = list(parent.Genes)
    if geneSet is not None:
        geneIndex = random.randint(0, len(geneSet) - 1)
        childGenes[index] = geneSet[geneIndex]
    else:
        childGenes[index] = createGene(index)
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def generateParent(minLength, maxLength, geneSet, get_fitness, createGene):
    childGenes = []
    length = random.randint(minLength, maxLength)
    if geneSet is not None:
        for i in range(0, length):
            geneIndex = random.randint(0, len(geneSet) - 1)
            childGenes.append(geneSet[geneIndex])
    else:
        for i in range(0, length):
            childGenes.append(createGene(i))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def getBest(get_fitness, display, minLen, optimalFitness, geneSet=None, createGene=None, maxLen=None):
    random.seed()
    if geneSet is None and createGene is None:
        raise ValueError('must specify geneSet or createGene')
    if geneSet is not None and createGene is not None:
        raise ValueError('cannot specify both geneSet and createGene')
    if maxLen is None:
        maxLen = minLen
    bestParent = generateParent(minLen, maxLen, geneSet, get_fitness, createGene)
    display(bestParent)

    options = {
        0: lambda p: mutate(p, geneSet, get_fitness, createGene),
        1: lambda p: crossover(p, bestParent, get_fitness)
    }

    while bestParent.Fitness < optimalFitness:
        parent = generateParent(minLen, maxLen, geneSet, get_fitness, createGene)
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
