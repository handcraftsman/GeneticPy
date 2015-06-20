import unittest
import datetime
import genetic


def getFitness(candidate):
    board = getBoard(candidate)
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


def getBoard(candidate):
    board = [['.'] * 8 for i in range(8)]
    for index in range(0, len(candidate), 2):
        board[candidate[index]][candidate[index + 1]] = 'Q'
    return board


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    board = getBoard(candidate.Genes)
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
    print("%s\t%i\t%s" % (''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


class EightQueensTests(unittest.TestCase):
    def test(self):
        geneset = [0, 1, 2, 3, 4, 5, 6, 7]
        optimalValue = 8 + 8 + 8 + 8
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate)
        best = genetic.getBest(fnGetFitness, fnDisplay, 16, optimalValue, geneset)
        self.assertEqual(best.Fitness, optimalValue)


if __name__ == '__main__':
    unittest.main()
