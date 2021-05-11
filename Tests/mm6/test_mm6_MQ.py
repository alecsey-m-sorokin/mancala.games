import datetime
from datetime import timedelta
import time
import unittest
from random import randint
import pytest
from parameterized import parameterized
from Locators.Locators import bets, APIdata_MancalaQuest
from Pages.MancalaQuest_Page import API_MancalaQuest

A = APIdata_MancalaQuest
api = API_MancalaQuest


# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])

r = 0
i = 0
freeSpinCount = 0
freeSpinsCount = 0
totalBets = []
totalWins = []
globalBets = []
globalWins = []
globalWinsFS = []
dt_start = time.time()

while r < 1:  # выставляем количество раундов (сессий)
    print('\n')
    print('round # %s' % str(r + 1))
    regToken = api.testpartnerservice()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency)

    while i < 1:  # выставляем количество спинов (вращений)
        print('\n')
        print('spin # %s' % str(i + 1))
        creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)  # ставка ! CreditDebit # resultId = tokenAsync
        getAsyncResponse, resultId, spinId, StonesNumber, OAKLines, printAR = api.GetAsyncResponse(regToken, tokenAsync)  # асинхронный ответ ! GetAsyncResponse
        if getAsyncResponse["SpinResult"]["OAKLines"] is None:
            print("OAKLines =", OAKLines, '\n')
        else:
            print('\n')
            print(getAsyncResponse)
            print("OAKLines =", OAKLines)
            print("StonesNumber =", StonesNumber)

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
        printAR(coin)

    r = r + 1

    print('finished "Mancala Quest" session after %s spins' % i)
    print(totalWins)
    print(sum(totalWins))
    print(totalBets)
    print(sum(totalBets))
    globalBets.append(sum(totalBets))
    totalWins.clear()
    totalBets.clear()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) / 125 * i), 2))
    print(globalWins)
    print("Balance =", balance)
    print("Balance Real =", balanceReal)
    i = 0

print('\n')
print('finished Mancala Quest after %s rounds' % r)
print('total bets = ', sum(globalBets) / 125)
print('total wins = ', round(sum(globalWins), 2))
print('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print('the end')

if __name__ == "__main__":
    unittest.main()
