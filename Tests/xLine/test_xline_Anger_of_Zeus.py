import datetime
import time
import unittest

import pytest
from parameterized import parameterized
from Locators.Locators import APIdata_xLine, bets
from Pages.xLine.xLine_Page import API_xLine

A = APIdata_xLine
api = API_xLine

regToken = api.testpartnerservice()
# regToken = 'acb5f210-50ff-42b0-b66d-7835787d698b'
api.AuthorizationGame(regToken)


# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])

"""
в данном скрипте мы накапливаем игровые фри спины, собирая PUZZLE's
"""

i = 1
p = 0
freeSpinsCount = 0
while freeSpinsCount == 0:
    creditDebit = api.CreditDebit(regToken, A.betSum, A.cntLineBet)  # ставка ! CreditDebit # resultId = tokenAsync
    tokenAsync = creditDebit["TokenAsync"]
    # time.sleep(1)
    getAsyncResponse = api.GetAsyncResponse(regToken, tokenAsync)  # асинхронный ответ ! GetAsyncResponse
    resultId = getAsyncResponse['ResultId']
    if getAsyncResponse["SpinResult"]["PuzzleGame"] is None:
        bonusGameId = "no PUZZLE game"
        print("BonusGameId =", bonusGameId)
        print('betSum = %s , cntLineBet = %s' % (A.betSum, A.cntLineBet))
    else:
        bonusGameId = getAsyncResponse["SpinResult"]["PuzzleGame"]["Id"]
        print('\n', "BonusGameId =", bonusGameId, '\n')
        spinId = getAsyncResponse["SpinResult"]["Id"]
        puzzleBonusGame = api.PuzzleBonusGame(regToken, resultId, bonusGameId, spinId)  # Получаем картинку ПАЗЛА в бонусной игре ! PuzzleBonusGame
        tokenAsyncPuzzle = puzzleBonusGame['TokenAsync']
        # time.sleep(1)
        getAsyncResponse_Puzzle = api.GetAsyncResponse_Puzzle(regToken, tokenAsyncPuzzle)  # асинхронный ответ в бонусной игре ! GetAsyncResponse
        freeSpinsCount = getAsyncResponse['FreeSpinsCount']
        print(getAsyncResponse_Puzzle)
        p = p + 1
        print('collected %s puzzles' % p)

    i = i + 1
    BetSum = 'Bet Sum = ' + str(getAsyncResponse["BetSum"])
    WinSum = 'Win Sum = ' + str(getAsyncResponse["WinInfo"]["WinSum"])
    Credit_before_spin = 'CREDIT before spin = ' + str(getAsyncResponse["WinInfo"]["Balance"] - getAsyncResponse["WinInfo"]["WinSum"] + getAsyncResponse["BetSum"])
    Credit_after_spin = 'CREDIT after spin  = ' + str(getAsyncResponse["WinInfo"]["Balance"])
    print('\n', 'i = ', i, '\n', BetSum, '\n', WinSum, '\n', Credit_before_spin, '\n', Credit_after_spin, '\n', 'freeSpinsCount = ', freeSpinsCount, '\n', 'collected puzzles = ', p, '\n')

    if freeSpinsCount > 0:
        print('finished PUZZLE`s after %s times' % i)
        break

if __name__ == "__main__":
    unittest.main()
