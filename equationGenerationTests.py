import unittest
import datetime
import genetic
import operator
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
        if self.isFunction():
            result = "(" + self.Value + "[" + str(self.Left) + "]" \
                     + " [" + str(self.Right) + "]" \
                     + ") "
        else:
            result = str(self.Value) + " "
        return result


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


def getFitness(candidate, expectedTotal):
    usedIndexes = list(sorted(getUsedIndexes(candidate)))

    localCopy = candidate[:]
    if candidate[0].isFunction():
        for i in reversed(usedIndexes):
            element = localCopy[i]
            if element.isFunction():
                leftIndex = element.Left
                rightIndex = element.Right
                left = 0
                if i < leftIndex < len(localCopy):
                    left = localCopy[leftIndex].Value
                right = 0
                if i < rightIndex < len(localCopy):
                    right = localCopy[rightIndex].Value
                op = operator.add
                if element.Value == '-':
                    op = operator.sub
                value = op(left, right)
                localCopy[i] = Node(value)

    total = localCopy[0].Value
    fitness = total if expectedTotal >= total >= 0 \
        else total - expectedTotal if total < 0 \
        else expectedTotal - total
    if fitness == expectedTotal:
        fitness = 1000 - len(usedIndexes)

    return fitness


def displayDot(candidate, startTime):
    result = createDot(candidate.Genes)
    timeDiff = datetime.datetime.now() - startTime
    print("%s\nfitness: %i\t%s" % (";".join(result), candidate.Fitness, str(timeDiff)))


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
                dotCommands.append(str(index) + " -> " + str(leftIndex))
            else:
                if not haveZeroNode:
                    dotCommands.append("zero [label=\"0\"]")
                    haveZeroNode = True
                dotCommands.append(str(index) + " -> zero")
            rightIndex = element.Right
            if index < rightIndex < len(genes):
                stack.append(rightIndex)
                dotCommands.append(str(index) + " -> " + str(rightIndex))
            else:
                if not haveZeroNode:
                    dotCommands.append("zero [label=\"0\"]")
                    haveZeroNode = True
                dotCommands.append(str(index) + " -> zero")

    return dotCommands


def displayRaw(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s\t%s" %
          ((' '.join(map(str, [item for item in candidate.Genes]))),
           candidate.Fitness,
           str(timeDiff),
           candidate.Strategy))


def displayPrefixNotation(candidate, startTime):
    result = createEquation(candidate.Genes)
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" % (result, candidate.Fitness, str(timeDiff)))


def createEquation(genes):
    used = [0 for i in range(0, len(genes))]
    equationWithReferences = visitNode(genes, used, 0)
    for i in range(len(genes)):
        if used[i] == 0:
            continue
        if used[i] == 1:
            equationWithReferences = equationWithReferences.replace("[" + str(i) + "]", "")
    return equationWithReferences


def visitNode(genes, used, index):
    result = ""
    if used[index] == 0:
        element = genes[index]
        if not element.isFunction():
            result += str(element.Value)
        else:
            used[index] = 1
            result += "[" + str(index) + "]"
            result += "(" + element.Value + " "
            leftIndex = element.Left
            if index < leftIndex < len(genes):
                result += visitNode(genes, used, leftIndex)
            else:
                result += " 0"
            rightIndex = element.Right
            if index < rightIndex < len(genes):
                result += " " + visitNode(genes, used, rightIndex)
            else:
                result += " 0"
            result += ")"
    else:
        used[index] = 2
        result += "->[" + str(index) + "]"
    return result


def createGene(index, length, geneset):
    value = geneset[random.randint(0, len(geneset) - 1)]
    if isinstance(value, str):
        left = random.randint(index, length - 1) if index < length else 0
        right = random.randint(index, length - 1) if index < length else 0
        return Node(value, left, right)
    return Node(value)


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


class EquationGenerationTests(unittest.TestCase):
    def test(self):
        geneset = [1, 2, 3, 4, 5, 6, 7, '+', '-']
        minNodes = 5  # (+ (+ ->[a] [a](+ 7 [b]5)) [b])
        expectedTotal = 29
        maxNodes = 30
        optimalValue = 1000 - minNodes
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: displayRaw(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, expectedTotal)
        fnCreateGene = lambda index, length: createGene(index, length, geneset)
        fnCrossover = lambda child, parent: crossover(child, parent)
        fnMutate = lambda child: mutate(child, fnCreateGene)
        best = genetic.getBest(fnGetFitness, fnDisplay, minNodes, optimalValue,
                               createGene=fnCreateGene, maxLen=maxNodes,
                               customMutate=fnMutate, customCrossover=fnCrossover)
        self.assertTrue(best.Fitness >= optimalValue)

    def test_getFitness_given_total_equals_expectedTotal_should_get_1000_minus_total_Nodes_used(self):
        genes = [Node(1)]
        expectedTotal = 1
        result = getFitness(genes, expectedTotal)
        totalNodesUsed = len(genes)
        self.assertEqual(result, 1000 - totalNodesUsed)

    def test_getFitness_given_expectedTotal_GE_total_and_total_GE_0_should_get_total(self):
        total = 5
        genes = [Node(total)]
        expectedTotal = 9
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, total)

    def test_getFitness_given_total_LT_zero_should_get_total_minus_expectedTotal(self):
        total = -5
        genes = [Node(total)]
        expectedTotal = 9
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, total - expectedTotal)

    def test_getFitness_given_total_GT_expectedTotal_should_get_expectedTotal_minus_total(self):
        total = 14
        genes = [Node(total)]
        expectedTotal = 9
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, expectedTotal - total)

    def test_getFitness_given_PLUS_4_7_and_expectedTotal_20_should_get_11(self):
        genes = [Node('+', 1, 2), Node(4), Node(7)]
        expectedTotal = 20
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, 4 + 7)

    def test_getFitness_given_MINUS_7_4_and_expectedTotal_20_should_get_3(self):
        genes = [Node('-', 1, 2), Node(7), Node(4)]
        expectedTotal = 20
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, 7 - 4)

    def test_getFitness_given_PLUS_7_and_a_Left_value_GT_the_size_of_genes_and_expectedTotal_20_should_get_7(self):
        genes = [Node('+', 100, 1), Node(7)]
        expectedTotal = 20
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, 7)

    def test_getFitness_given_PLUS_7_and_a_Right_value_GT_the_size_of_genes_and_expectedTotal_20_should_get_7(self):
        genes = [Node('+', 1, 100), Node(7)]
        expectedTotal = 20
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, 7)

    def test_getFitness_given_PLUS_PLUS_5_4_3_and_expectedTotal_20_should_get_12(self):
        genes = [Node('+', 1, 2), Node('+', 3, 4), Node(5), Node(4), Node(3)]
        expectedTotal = 20
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, 12)

    def test_getFitness_given_PLUS_PLUS_5_4_3_and_other_unreferenced_nodes_should_ignore_the_unreferenced_nodes(self):
        genes = [Node('+', 2, 4), Node(9), Node('+', 6, 8), Node(8), Node(5), Node(7), Node(4), Node(6), Node(3),
                 Node(2)]
        expectedTotal = 20
        fitness = getFitness(genes, expectedTotal)
        self.assertEqual(fitness, 12)


if __name__ == '__main__':
    unittest.main()
