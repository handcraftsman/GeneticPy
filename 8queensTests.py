import unittest
import datetime
import genetic


class Point:
    Row = None
    Col = None

    def __init__(self, row, col):
        self.Row = row
        self.Col = col


def getFitness(candidate, gene_set):
    board = getBoard(candidate, gene_set)
    rowsWithQueens = {}
    colsWithQueens = {}
    northEastDiagonalsWithQueens = {}
    southEastDiagonalsWithQueens = {}
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'Q':
                rowsWithQueens[row] = 1
                colsWithQueens[col] = 1
                northEastDiagonalsWithQueens[row + col] = 1
                southEastDiagonalsWithQueens[8 - 1 - row + col] = 1

    return len(rowsWithQueens) \
           + len(colsWithQueens) \
           + len(northEastDiagonalsWithQueens) \
           + len(southEastDiagonalsWithQueens)


def getPoint(rowGene, colGene, gene_set):
    rowIndex = gene_set.index(rowGene)
    if rowIndex == -1:
        raise ValueError("'" + rowGene + "' is an invalid gene")
    colIndex = gene_set.index(colGene)
    if colIndex == -1:
        raise ValueError("'" + colGene + "' is an invalid gene")
    return Point(rowIndex, colIndex)


def getBoard(candidate, gene_set):
    board = [['.'] * 8 for i in range(8)]
    for index in range(0, len(candidate), 2):
        point = getPoint(candidate[index], candidate[index + 1], gene_set)
        board[point.Row][point.Col] = 'Q'
    return board


def display(candidate, gene_set, startTime):
    timeDiff = datetime.datetime.now() - startTime
    board = getBoard(candidate.Genes, gene_set)
    for i in range(8):
        print(board[i][0],
              board[i][1],
              board[i][2],
              board[i][3],
              board[i][4],
              board[i][5],
              board[i][6],
              board[i][7]
              )
    print("%s\t%i\t%s" % (candidate.Genes, candidate.Fitness, str(timeDiff)))


class EightQueensTests(unittest.TestCase):
    def test(self):
        geneset = '12345678'
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, geneset, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, geneset)
        best = genetic.getBest(fnGetFitness, fnDisplay, 16, 8 + 8 + 8 + 8, geneset)
        self.assertEqual(best.Fitness, 8 + 8 + 8 + 8)


if __name__ == '__main__':
    unittest.main()
