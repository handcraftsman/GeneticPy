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


def getFitness(candidate, expectedTotal):
    used = {0: [0]}
    localCopy = candidate[:]
    if candidate[0].isFunction():
        for i in reversed(range(len(localCopy))):
            element = localCopy[i]
            iUsed = [i]
            if element.isFunction():
                leftIndex = element.Left
                rightIndex = element.Right
                left = 0
                if i < leftIndex < len(localCopy):
                    left = localCopy[leftIndex].Value
                    iUsed.extend(used[leftIndex])
                right = 0
                if i < rightIndex < len(localCopy):
                    right = localCopy[rightIndex].Value
                    iUsed.extend(used[rightIndex])
                op = operator.add
                if element.Value == '-':
                    op = operator.sub
                value = op(left, right)
                localCopy[i] = Node(value)
            used[i] = iUsed

    total = localCopy[0].Value
    fitness = total if expectedTotal >= total >= 0 \
        else total - expectedTotal if total < 0 \
        else expectedTotal - total
    if fitness == expectedTotal:
        distinctElementsUsed = set(used[0])
        fitness = 1000 - len(distinctElementsUsed)

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
    print("%s\t%i\t%s" %
          ((' '.join(map(str, [item.Value for item in candidate.Genes]))),
           candidate.Fitness,
           str(timeDiff)))


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


def createGene(index, geneset, maxNodes):
    value = geneset[random.randint(0, len(geneset) - 1)]
    if isinstance(value, str):
        left = random.randint(index, maxNodes - 1)
        right = random.randint(index, maxNodes - 1)
        return Node(value, left, right)
    return Node(value)


class EquationGenerationTests(unittest.TestCase):
    def test(self):
        geneset = [1, 2, 3, 4, 5, 6, 7, '+', '-']
        minNodes = 5  # (+ (+ ->[a] [a](+ 7 [b]5)) [b])
        expectedTotal = 29
        maxNodes = 30
        optimalValue = 1000 - minNodes
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: displayPrefixNotation(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, expectedTotal)
        fnCreateGene = lambda index: createGene(index, geneset, maxNodes)
        best = genetic.getBest(fnGetFitness, fnDisplay, minNodes, optimalValue, createGene=fnCreateGene,
                               maxLen=maxNodes)
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
