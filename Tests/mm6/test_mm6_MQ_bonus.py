import datetime
import hashlib
import random
import time
from datetime import timedelta
import unittest
from random import randint

import pytest
import requests
from parameterized import parameterized
import json
from Locators.Locators import bets, APIdata_MancalaQuest
from Pages.mm6.MancalaQuest_Page import API_MancalaQuest, print2file, Logger

A = APIdata_MancalaQuest
api = API_MancalaQuest
# regToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2MTkwNzcwMTcsImV4cCI6MTYxOTA3ODgxNywiaXNzIjoiaHR0cDovL2lkZW50aXR5c2VydmVyLXRlc3QuY2FyaGVuZ2Uuc3BhY2UiLCJjbGllbnRfaWQiOiJQYXJ0bmVyU2VydmljZSIsIlNlc3Npb25JZGVudGl0eSI6IkdDSElXekRIQXlBbWlDYlIvSTN5bHErVHNYTGtRTHVyd2VkUXNEM3JWZ2JzRnN5UkV1LzZZSE9HYitZVUVFM2F2OTZNNjdreENRbVBHeGFyQldObnhGUFhCcEkwRUdJNFVWdUVrUlhwRUErT3BOT0thNEE0aGZvbjMyZlNMbiszQlJPSjB6WHRHVlpPbnJvY0NRZ1drRzdVd1BycXJRN3FFbC9OY1dHS0t6ZXZJUzZRamlsNU4xcVNlMFhvSTF1WHhjaXpXWjB2MUs0ejI2cHI3cG1Qdlpkb0J5TUVSWDZ1UWIrTWxESEtOdFFFdjFVNnJia3R6TXBXazU1c3RxdGloVUtlSm5Fd1A1SnoxRThoK2dqL24wYnYxOG94eXhPV2R1enhRRk9CMUFIMDh5NGNzcUZ5eEVDTEZ0by9ybHNrbDltOVIwQW05VnNYK0NuU3JYWlRSWVpkMGREbGw2SHdyaHN3S3RkMCtzV25wREhNT0JScEhnZnhyNlZlb0MzT3BQWnpVWnJaeGt0aGpCeUI3NFJ0Uzg4WmF0cm5LSkkwMlVVdDc0ZG9LZDF2dnhyclpKUUFvaklaMk5IRXp4Sm5HYzY5YU4wa3VCM0NkYmpyK2hadjFtcXc1cUp3T2had21DRVFOcFY4RU1ENXVmUkNmcUxlNEtBZFVsdWxTaDdDQjhtV2VTUjJwKzdHVW84V3J6QkEwQ3NqNnNGd2E2WGJpTm8yM3hkeDVhbHo2T2lMODFjNUZlOXlLY0ltY3FrWFdPaHFTQkVsdDBWak9Jei9hRkIyNE9MVnBOOTRyM2x4WkdlYmZmVWVMM01TSVh2YXptTTVIaDZsQ3ZzblVpcEtpdmVqQi84WXdyb0NjOWtSN1RhM2ppQ1FXbVE2Zyt6SjJVV1A4L2t6T01Rc3R4SEtyMFVrZUk0VFVmOGxodnI1SFYwUXdyMklHS2lRTjFpRjVOa01HaEREV3NldVprZ0Y4Z0F4NEdjUVV4d1o4TnJoM1h5ZjRJN0pjWFM2OFpEY21yNzU0M3dmTHgySWwwSWJLOEhkd2JydFRzWDI5SkU2aGZVUlpDTXJHVWc9IiwiR2FtZUlkIjoiMTkwMDEiLCJTbG90VHlwZSI6IjE5IiwiR2FtZVNlcnZpY2VVcmwiOiJodHRwczovL3Rlc3QtbW02bi1hcGkuY2FyaGVuZ2Uuc3BhY2UvIiwiR2FtZVVybCI6Imh0dHBzOi8vc3Rlc3QuemhkdW4uc3BhY2UvbW02bi8iLCJqdGkiOiI2Q0FBRkFCMTFFNkVDRjIxRkY4NjUwMjZGRjNCRTIyQiIsImlhdCI6MTYxOTA3NzAxNywic2NvcGUiOlsiR2VuZXJhdGVKd3RUb2tlbiJdfQ.k_arunsCHJ4bx3wjGXfJfzHuk4fsnQSh4IikXTxQ6_KZWisKlLHbonRGeVW9lC7RUVyK8ec-ed0plGsdaobLyaM4bt7IVJGsDEf0gPP79S07yT3A5xKMYNXzU6m_FL0nd0v1YgJRsAga20uSoRvj8viTPRDMNRF12hPecrPev_MAyi-6KSS7udpdYBfYCo_ozygsFdz0uW8ycoFc3hEvnhnGKlQO2xv7Kqd3ID9vY0-U1cZeBPFt-ig1hTgePLrOn5tpdoZDbnDGMv8P_MwIrbzgEiBB4Bn0aFiO5JtSg4XAXpPW75hyDk9dLZyApHASCK_kouXb0DcWkozG8_Xgbk_ezTzLcshjcEmC1X9QfZpiBx6swB4tgr58qPufov8Sr7f-3mykToJnKKXwsvSoMCMsIbVzvfMNU-2n4zeu_0fXJrt6I0ONVR2qX3FHbwSSCD-IOZLonRukk5EHfWX7JDGNdzeok8BmytiRt8X6uVIYvksTEwNMTeBwEpHBEHAS83nc_IYZ3UhRr-rXqD1957Bh-ODlZdiXNH5j1LiJq394rRVOIfcEo7qvBM8amQ_edO-RPvoEdmaHL0RJeqLy14_ir5s-fIwykq16WTCOPQQm1bcjdtsb72V_Q1XcxzTsdZc3dY8WOE14J8SFTa_7LVapOtafprJNvm6BO0YHIFE'

aa = []
i = 0
r = 0
currency = ''
StonesNumber = 0
freeSpinsCount = 0
FreeSpinCount = 0
totalBets = []
totalWins = []
globalBets = []
globalWins = []
dt_start = time.time()
iFrameUrl = ''

FS_collected_count = []
FS_collected_real_count = []
FS_collected_winnings = []
globalWinsFS = []

FS_collected_count.clear()
FS_collected_real_count.clear()
FS_collected_winnings.clear()

global fileName

dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))


while r < 1:  # выставляем количество раундов (сессий)
    fileName = '../../logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r + 1) + ' {}.json'.format(dt)
    log = Logger(fileName, toFile=True, toConsole=True)
    print2 = log.printml
    print2('\n')
    print2('----- round # %s' % str(r + 1))
    regToken, iFrameUrl = api.testpartnerservice()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    print2(str(authorizationGame))
    balanceRealBefore = balanceReal
    func(balance, balanceReal, coin, currency)

    while i < 15:  # выставляем количество спинов (вращений)
        print2('\n')
        print2('----- spin # %s' % str(i + 1))
        creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
        getAsyncResponse, resultId, spinId, StonesNumber, totalFreeSpinsCount, mancalaQuestBonusGameId, OAKLines, printAR, oak_l = api.GetAsyncResponse(regToken, tokenAsync)
        print2(str(getAsyncResponse))
        printAR(coin)

        if mancalaQuestBonusGameId:
            """
            тут начинается бонусная игра, длится до тех пор, пока в ответе на бонуску не получим, что есть Фри спины
            """
            print('\n')
            getMancalaQuestGameState, tokenAsyncGetMancalaQuestGameState = api.GetMancalaQuestGameState(regToken, resultId, mancalaQuestBonusGameId, spinId)
            getAsyncResponseQuestGameState, activeCharacterIndex, characterIndex, cups = api.GetAsyncResponse_QuestGameState(regToken, tokenAsyncGetMancalaQuestGameState)
            print('\n')
            selectCharacter, tokenAsyncSelectCharacter = api.SelectCharacter(regToken, resultId, mancalaQuestBonusGameId, spinId, CharacterId='1')
            getAsyncResponseSelectCharacter, Character = api.GetAsyncResponse_SelectCharacter(regToken, tokenAsyncSelectCharacter)
            print('\n')

            bg = 1
            while not FreeSpinCount:
                print2('\n')
                print2('----- Mancala Quest bonus game step # %s' % str(bg))
                makeStep, tokenAsyncMakeStep = api.MakeStep(regToken, resultId, mancalaQuestBonusGameId, spinId)
                getAsyncResponse_MakeStep, ActiveCharacterIndex, FreeSpinCount, Multiplier = api.GetAsyncResponse_MakeStep(regToken, tokenAsyncMakeStep)
                print2(str(getAsyncResponse_MakeStep))
                bg = bg + 1
            """
            тут начинаются Фри спины, полученные в результате бонусной игры
            """
            if FreeSpinCount > 0:
                freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
                getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
                print2('\n----- Mancala Quest bonus game free spin # %s' % str(totalFreeSpinsCount - remainingFreeSpinsCount))
                print2(str(getAsyncResponseFreeSpin))
                globalWinsFS.clear()
                FS_collected_count.append(totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок
                globalWinsFS.append(getAsyncResponse["WinInfo"]["CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('globalWinsFS = ', globalWinsFS)
                while remainingFreeSpinsCount > 0:
                    freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                    getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
                    print2('\n----- Mancala Quest bonus game free spin # %s' % str(totalFreeSpinsCount - remainingFreeSpinsCount))
                    print2(str(getAsyncResponseFreeSpin))
                    globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                    print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                    print2('globalWinsFS = ', globalWinsFS)

                print2('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), totalFreeSpinsCount))
                print2('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) / 100, currency, totalFreeSpinsCount))
                FS_collected_winnings.append(sum(globalWinsFS) / 100)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов
                FreeSpinCount = 0

        elif totalFreeSpinsCount:
            """
            тут начинаются Фри спины, полученные в результате выпадения Wild- символов слева и справа
            """
            freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinId)
            getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(regToken, tokenAsyncFreeSpin)
            print2('\n----- Mancala Quest WILD`s free spin # %s' % str(totalFreeSpinsCount - remainingFreeSpinsCount))
            print2(str(getAsyncResponseFreeSpin))
            globalWinsFS.clear()
            FS_collected_count.append(totalFreeSpinsCount)  # сюда помещаем значения totalFreeSpinsCount, которые получает Игрок
            globalWinsFS.append(getAsyncResponse["WinInfo"]["CurrentSpinWin"])  # тут добавляем выигрыш с основного раунда перед фри спинами
            globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
            print2('globalWinsFS = ', globalWinsFS)
            while remainingFreeSpinsCount > 0:
                freeSpin, tokenAsyncFreeSpin = api.FreeSpin(regToken, resultId, spinIdFs)
                getAsyncResponseFreeSpin, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs = api.GetAsyncResponse_FreeSpin(
                    regToken, tokenAsyncFreeSpin)
                print2('\n----- Mancala Quest WILD`s free spin # %s' % str(totalFreeSpinsCount - remainingFreeSpinsCount))
                print2(str(getAsyncResponseFreeSpin))
                globalWinsFS.append(getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('Current freeSpin win = ', getAsyncResponseFreeSpin["WinInfo"]["CurrentSpinWin"])
                print2('globalWinsFS = ', globalWinsFS)

            print2('Player got %s Coins in %s freeSpins' % (sum(globalWinsFS), totalFreeSpinsCount))
            print2('Player got %s %s in %s freeSpins' % (sum(globalWinsFS) / 100, currency, totalFreeSpinsCount))
            FS_collected_winnings.append(
                sum(globalWinsFS) / 100)  # тут сохраняем сколько игрок выиграл в CURRENCY за totalFreeSpinsCount фри спинов

        else:
            pass

        if oak_l > 0:
            aa.append(oak_l)

        i = i + 1
        totalBets.append(getAsyncResponse["BetSum"])
        totalWins.append(getAsyncResponse["WinInfo"]["TotalWin"])

    r = r + 1

    print2('\n----- finished Mancala Quest session after %s spins' % i)
    print2('TotalWins in coins = ', totalWins)
    print2(sum(totalWins))
    print2('TotalBets in coins = ', totalBets)
    print2(sum(totalBets))
    globalBets.append(sum(totalBets))
    totalWins.clear()
    totalBets.clear()
    authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
    globalWins.append(round(balanceReal - (balanceRealBefore - int(A.cntLineBet) / 125 * i), 2))
    print2('GlobalWins in currency %s after %s spins = ' % (currency, i), globalWins)
    print2("Balance =", balance)
    print2("Balance Real =", balanceReal)
    print2('userId =', A.userID)
    i = 0

# fileName = '../../logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r) + ' {}.json'.format(dt)
# log = Logger(fileName, toFile=True, toConsole=True)
# print2 = log.printml

# print2('\n')
print2('\n----- finished Mancala Quest after %s rounds' % r)
print2('total bets = %s' % sum(globalBets) / 100)
print2('total wins = %s' % round(sum(globalWins), 2))
print2('global wins = %s' % globalWins)
print2('free spins collected by player in all (%s) sessions: ' % r, FS_collected_count)
print2('real free spins collected by player in all (%s) sessions: ' % r, FS_collected_real_count)
print2('%s win in each free spins round: ' % currency, FS_collected_winnings)
print2('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))
print2('game_IframeUrl = %s' % iFrameUrl)
print2('the end ...')


if __name__ == "__main__":
    unittest.main()
