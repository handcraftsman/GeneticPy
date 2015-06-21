import unittest
import datetime
import genetic
import csv


class Rule:
    Item = None
    Other = None
    Stringified = None

    def __init__(self, item, other, stringified):
        self.Item = item
        self.Other = other
        self.Stringified = stringified

    def __eq__(self, another):
        return hasattr(another, 'Item') and \
               hasattr(another, 'Other') and \
               self.Item == another.Item and \
               self.Other == another.Other

    def __hash__(self):
        return hash(self.Item) * 397 ^ hash(self.Other)

    def __str__(self):
        return self.Stringified


def getFitness(candidate, rules):
    rulesThatPass = 0
    for rule in rules:
        if candidate[rule.Item] != candidate[rule.Other]:
            rulesThatPass += 1

    return rulesThatPass


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" % (''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


def loadData(localFileName):
    # expects: AA,BB;CC;DD where BB, CC and DD are the initial column values in other rows
    with open(localFileName, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {row[0]: row[1].split(';') for row in reader if row}
        return mydict


def buildLookup(items):
    itemToIndex = {}
    index = 0
    for key in sorted(items):
        itemToIndex[key] = index
        index += 1
    return itemToIndex


def buildRules(items):
    itemToIndex = buildLookup(items.keys())
    rulesAdded = {}
    rules = []
    keys = sorted(list(items.keys()))

    for key in sorted(items.keys()):
        keyIndex = itemToIndex[key]
        adjacentKeys = items[key]
        for adjacentKey in adjacentKeys:
            if adjacentKey == '':
                continue
            adjacentIndex = itemToIndex[adjacentKey]
            temp = keyIndex
            if adjacentIndex < temp:
                temp, adjacentIndex = adjacentIndex, temp
            ruleKey = keys[temp] + "->" + keys[adjacentIndex]
            rule = Rule(temp, adjacentIndex, ruleKey)
            if rule in rulesAdded:
                rulesAdded[rule] += 1
            else:
                rulesAdded[rule] = 1
                rules.append(rule)

    for k, v in rulesAdded.items():
        if v == 1:
            print("rule %s is not bidirectional" % k)

    return rules


class GraphColoringTests(unittest.TestCase):
    def test(self):
        states = loadData("adjacent_states.csv")
        rules = buildRules(states)
        colors = ["Orange", "Yellow", "Green", "Blue"]
        colorLookup = {}
        for color in colors:
            colorLookup[color[0]] = color
        geneset = list(colorLookup.keys())
        optimalValue = len(rules)
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, rules)
        best = genetic.getBest(fnGetFitness, fnDisplay, len(states), optimalValue, geneset)
        self.assertEqual(best.Fitness, optimalValue)

        keys = sorted(states.keys())

        for index in range(len(states)):
            print(keys[index] + " is " + colorLookup[best.Genes[index]])


if __name__ == '__main__':
    unittest.main()
