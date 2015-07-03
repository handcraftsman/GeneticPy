import unittest
import datetime
import genetic
import random


class Node:
    Value = None
    Left = None
    Right = None

    def __init__(self, value, left=None, right=None):
        self.Value = value
        self.Left = left
        self.Right = right

    def isFunction(self):
        return self.Left is not None

    def __str__(self):
        result = self.Value
        if self.isFunction():
            result += "([" + str(self.Left) + "]"
            if self.Right is not None:
                result += ",[" + str(self.Right) + "]"
            result += ")"
        return result + " "


class Operation:
    Func = None
    HasLeft = None
    HasRight = None

    def __init__(self, func, hasLeft, hasRight):
        self.Func = func
        self.HasLeft = hasLeft
        self.HasRight = hasRight


def getUsedIndexes(candidate):
    used = {0: [0]}
    if candidate[0].isFunction():
        for i in reversed(range(len(candidate))):
            element = candidate[i]
            iUsed = [i]
            if element.isFunction():
                leftIndex = element.Left
                rightIndex = element.Right
                if i < leftIndex < len(candidate):
                    iUsed.extend(used[leftIndex])
                if rightIndex is not None:
                    if i < rightIndex < len(candidate):
                        iUsed.extend(used[rightIndex])
            used[i] = iUsed
    return set(used[0])


def getFitness(candidate, geneset, rules):
    usedIndexes = getUsedIndexes(candidate)

    localCopy = candidate[:]
    notUsed = list(set(range(len(candidate))) - usedIndexes)
    for i in notUsed:
        localCopy[i] = None

    fitness = 0
    for rule in rules:
        if getFitnessForRule(localCopy, rule[0], rule[1], geneset) == rule[2]:
            fitness += 1

    if fitness == len(rules):
        fitness = 1000 - len(usedIndexes)

    return fitness


def getFitnessForRule(candidate, a, b, geneset):
    if candidate[0].isFunction():
        localCopy = candidate[:]
        for i in reversed(range(len(localCopy))):
            element = localCopy[i]
            if element is None:
                continue
            if element.isFunction():
                leftIndex = element.Left
                rightIndex = element.Right
                left = None
                if i < leftIndex < len(localCopy):
                    left = localCopy[leftIndex].Value
                right = None
                if rightIndex is not None:
                    if i < rightIndex < len(localCopy):
                        right = localCopy[rightIndex].Value

                value = element.Value
                if isinstance(element.Value, str):
                    gene = geneset[element.Value]
                    value = gene.Func(left if left is not None else 0,
                                      right if right is not None else 0)
                localCopy[i] = Node(value)
            else:
                localCopy[i] = Node(geneset[element.Value].Func(a, b))
        result = localCopy[0].Value
    else:
        result = geneset[candidate[0].Value].Func(a, b)
    return result


def displayDot(candidate, startTime):
    result = createDot(candidate.Genes)
    timeDiff = datetime.datetime.now() - startTime
    print("%s\nfitness: %i\t%s\t%s" % (";".join(result), candidate.Fitness, str(timeDiff), candidate.Strategy))


def createDot(genes):
    dotCommands = []
    added = [False for i in range(0, len(genes))]
    stack = [0]
    haveZeroNode = False
    while len(stack) > 0:
        index = stack.pop()
        if added[index]:
            continue
        added[index] = True
        element = genes[index]
        if not element.isFunction():
            dotCommands.append(str(index) + " [label=\"" + str(element.Value) + "\"]")
        else:
            dotCommands.append(str(index) + " [label=\"" + element.Value + "\"]")
            leftIndex = element.Left
            if index < leftIndex < len(genes):
                stack.append(leftIndex)
                dotCommands.append(str(leftIndex) + " -> " + str(index))
            else:
                if not haveZeroNode:
                    dotCommands.append("zero [label=\"0\"]")
                    haveZeroNode = True
                dotCommands.append("zero -> " + str(index))
            rightIndex = element.Right
            if rightIndex is not None:
                if index < rightIndex < len(genes):
                    stack.append(rightIndex)
                    dotCommands.append(str(rightIndex) + " -> " + str(index))
                else:
                    if not haveZeroNode:
                        dotCommands.append("zero [label=\"0\"]")
                        haveZeroNode = True
                    dotCommands.append("zero -> " + str(index))

    return dotCommands


def displayRaw(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" %
          ((' '.join(map(str, [str(item) for item in candidate.Genes]))),
           candidate.Fitness,
           str(timeDiff)))


def mutate(childGenes, fnCreateGene):
    childIndexesUsed = list(getUsedIndexes(childGenes))
    index = childIndexesUsed[random.randint(0, len(childIndexesUsed) - 1)]
    childGenes[index] = fnCreateGene(index, len(childGenes))


def crossover(child, parent):
    usedParentIndexes = list(sorted(getUsedIndexes(parent)))
    usedChildIndexes = list(getUsedIndexes(child))

    if len(usedParentIndexes) == 1 and len(usedChildIndexes) == 1:
        # node 0 has no child nodes, just copy it
        child[0] = parent[0]
        return

    while True:
        parentIndex = usedParentIndexes[random.randint(0, len(usedParentIndexes) - 1)]
        childIndex = usedChildIndexes[random.randint(0, len(usedChildIndexes) - 1)]
        if parentIndex != 0 or childIndex != 0:
            # don't copy the root to the root
            break

    unusedChildIndexes = list(sorted(set(range(childIndex, len(child))) - set(usedChildIndexes)))
    unusedChildIndexes.insert(0, childIndex)

    mappedIndexes = {}
    nextIndex = 0
    for pIndex in usedParentIndexes:
        if pIndex < parentIndex:
            continue
        if len(unusedChildIndexes) > nextIndex:
            mappedIndexes[pIndex] = unusedChildIndexes[nextIndex]
        else:
            mappedIndexes[pIndex] = len(child) + nextIndex - len(unusedChildIndexes)
        nextIndex += 1

    for parentIndex in mappedIndexes.keys():
        node = parent[parentIndex]
        childIndex = mappedIndexes[parentIndex]
        childNode = Node(node.Value, node.Left, node.Right)
        if childIndex < len(child):
            child[childIndex] = childNode
        else:
            child.append(childNode)
        left = node.Left
        if left is not None:
            childNode.Left = mappedIndexes[left] if left in mappedIndexes else 0
        right = node.Right
        if right is not None:
            childNode.Right = mappedIndexes[right] if right in mappedIndexes else 0


def createGene(index, length, geneset):
    keys = list(geneset.keys())
    key = keys[random.randint(0, len(keys) - 1)]
    op = geneset[key]
    left = random.randint(index, length - 1) if op.HasLeft else None
    right = random.randint(index, length - 1) if op.HasRight else None
    return Node(key, left, right)


class OperationGenerationTests(unittest.TestCase):
    geneset = None

    @classmethod
    def setUpClass(cls):
        cls.geneset = {'A': Operation(lambda a, b: a, False, False),
                       'B': Operation(lambda a, b: b, False, False),
                       'AND': Operation(lambda a, b: a & b, True, True),
                       'NOT': Operation(lambda a, b: a == 0, True, False)}

    def test_generate_OR(self):
        minNodes = 6  # not( and( not(a), not(b)))
        rules = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        maxNodes = 20
        optimalValue = 1000 - minNodes
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: displayDot(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, self.geneset, rules)
        fnCreateGene = lambda index, length: createGene(index, length, self.geneset)
        fnMutate = lambda child: mutate(child, fnCreateGene)
        best = genetic.getBest(fnGetFitness, fnDisplay, minNodes, optimalValue, createGene=fnCreateGene,
                               maxLen=maxNodes, customMutate=fnMutate, customCrossover=crossover)
        self.assertTrue(best.Fitness >= optimalValue)

    def test_generate_XOR(self):
        minNodes = 9  # and( not( and(a, b)), not( and( not(a), not(b))))
        rules = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        maxNodes = 50
        optimalValue = 1000 - minNodes
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: displayDot(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, self.geneset, rules)
        fnCreateGene = lambda index, length: createGene(index, length, self.geneset)
        fnMutate = lambda child: mutate(child, fnCreateGene)
        best = genetic.getBest(fnGetFitness, fnDisplay, minNodes, optimalValue, createGene=fnCreateGene,
                               maxLen=maxNodes, customMutate=fnMutate, customCrossover=crossover)
        self.assertTrue(best.Fitness >= optimalValue)

    def test_generate_XOR_with_addition(self):
        minNodes = 5  # and( 1, +(a, b))
        geneset = {'A': Operation(lambda a, b: a, False, False),
                   'B': Operation(lambda a, b: b, False, False),
                   'AND': Operation(lambda a, b: a & b, True, True),
                   'NOT': Operation(lambda a, b: a == 0, True, False),
                   '+': Operation(lambda a, b: a + b, True, True),
                   '1': Operation(lambda a, b: 1, False, False)}
        rules = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        maxNodes = 50
        optimalValue = 1000 - minNodes
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: displayDot(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, geneset, rules)
        fnCreateGene = lambda index, length: createGene(index, length, geneset)
        fnMutate = lambda child: mutate(child, fnCreateGene)
        best = genetic.getBest(fnGetFitness, fnDisplay, minNodes, optimalValue, createGene=fnCreateGene,
                               maxLen=maxNodes, customMutate=fnMutate, customCrossover=crossover)
        self.assertTrue(best.Fitness >= optimalValue)

    def test_getFitness_given_base_node_is_A_and_1_matching_rule_should_return_1(self):
        rules = [[0, 0, 0], [0, 1, 1]]
        genes = [Node('A')]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1)

    def test_getFitness_given_base_node_is_B_and_1st_2_rules_match_should_return_2(self):
        rules = [[0, 0, 0], [0, 1, 1], [1, 0, 1]]
        genes = [Node('B')]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 2)

    def test_getFitness_given_base_node_is_NOT_with_Left_node_out_of_bounds_and_1st_rule_matches_should_return_1(self):
        rules = [[1, 1, 1], [0, 0, 0]]
        genes = [Node('NOT', 100, 0)]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1)

    def test_getFitness_given_base_node_is_NOT_with_Left_node_A_and_2nd_rule_matches_should_return_1(self):
        rules = [[0, 0, 0], [1, 1, 1]]
        genes = [Node('NOT', 100, 0)]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1)

    def test_getFitness_given_base_node_is_AND_with_both_nodes_out_of_bounds_and_0_matching_rules_should_return_0(self):
        rules = [[1, 0, 1]]
        genes = [Node('AND', 100, 100)]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 0)

    def test_getFitness_given_all_rules_pass_and_1_gene_should_return_1000_minus_1(self):
        rules = [[0, 0, 0]]
        genes = [Node('AND', 100, 100)]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1000 - len(genes))

    def test_getFitness_given_all_rules_pass_and_2_genes_but_only_1_used_should_return_1000_minus_1(self):
        rules = [[0, 0, 0]]
        genes = [Node('AND', 100, 100), Node('B')]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1000 - 1)

    def test_getFitness_given_all_rules_pass_and_3_genes_but_only_2_used_should_return_1000_minus_2(self):
        rules = [[0, 0, 0]]
        genes = [Node('AND', 2, 100), Node('AND', 2, 2), Node('B')]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1000 - 2)

    def test_getFitness_given_all_rules_pass_with_NOT_2_NOT_1_NOT_2_B_A_should_return_1000_minus_2(self):
        rules = [[0, 0, 0]]
        genes = [Node('NOT', 2), Node('NOT', 1), Node('NOT', 2), Node('B'), Node('A')]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1000 - 2)

    def test_getFitness_given_rules_and_genes_for_XOR_should_get_1000_minus_9(self):
        rules = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        # and( not( and(a, b)), not( and( not(a), not(b))))
        genes = [Node('AND', 1, 2), Node('NOT', 3), Node('NOT', 4), Node('AND', 5, 6), Node('AND', 7, 8),
                 Node('NOT', 7), Node('NOT', 8), Node('A'), Node('B')]
        result = getFitness(genes, self.geneset, rules)
        self.assertEqual(result, 1000 - 9)


if __name__ == '__main__':
    unittest.main()
