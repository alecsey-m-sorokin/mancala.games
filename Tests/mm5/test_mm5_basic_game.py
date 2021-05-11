import datetime
from datetime import timedelta
import time
import unittest
from random import randint
import pytest
from parameterized import parameterized
from Locators.Locators import APIdata_PortalMaster, DOM_PortalMaster, bets
from Pages.PortalMaster_Page import API_PortalMaster

D = DOM_PortalMaster
A = APIdata_PortalMaster
api = API_PortalMaster


# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])

def goto(linenum):
    global line
    line = linenum


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

while r < 50:  # выставляем количество раундов (сессий)
    print('\n')
    print('round # %s' % str(r + 1))
    regToken = api.testpartnerservice()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency)

    while i < 250:  # выставляем количество спинов (вращений)
        print('\n')
        print('spin # %s' % str(i + 1))
        creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum,
                                                  A.cntLineBet)  # ставка ! CreditDebit # resultId = tokenAsync
        getAsyncResponse, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace, printAR = api.GetAsyncResponse(
            regToken, tokenAsync)  # асинхронный ответ ! GetAsyncResponse
        trade_low_actionType = 0
        trade_mid_actionType = 0
        if getAsyncResponse["SpinResult"]["ScatterCrystalGame"]["Id"] is None:
            print("ScatterCrystalGame =", scatterCrystalGame, '\n')
        else:
            print('\n')
            print(getAsyncResponse)
            print("ScatterCrystalGame =", scatterCrystalGame)
            print("Spheres =", spheres)
            print("SpheresSpinId =", spheresSpinId)
            print("ScattersForReplace =", scattersForReplace)

            if spheres in ([0, 0], [1, 0], [2, 0], [3, 0]):  # тут проверяем, что есть определенная комбинация сфер 1 уровня и заканчиваем спин
                trade_low_actionType = '2'  # Finish : ActionType = 2
                scatterCrystalBonusGame, tokenAsyncScatter = api.ScatterCrystalBonusGame(regToken, resultId,
                                                                                         scatterCrystalGame, spinId,
                                                                                         ActionType=trade_low_actionType,
                                                                                         ScatterPositionRow='0',
                                                                                         ScatterPositionColumn='0',
                                                                                         LevelSphere='-1',
                                                                                         Info='false')
                getAsyncResponseScatter, freeSpinCount = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)  # асинхронный ответ ! GetAsyncResponse_Scatter
                print(getAsyncResponseScatter)

            else:
                pass

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])
        printAR(coin)

    r = r + 1

    print('finished Portal Master session after %s spins' % i)
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
print('finished Portal Master after %s rounds' % r)
print('total bets = ', sum(globalBets) / 125)
print('total wins = ', round(sum(globalWins), 2))
print('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print('the end')

if __name__ == "__main__":
    unittest.main()
