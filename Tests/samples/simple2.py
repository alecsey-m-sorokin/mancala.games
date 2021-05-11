import datetime
import hashlib
import random
import time
import unittest
from random import randint

import pytest
import requests
from parameterized import parameterized
import json
from Locators.Locators import APIdata_PortalMaster, DOM_PortalMaster, bets
from Pages.PortalMaster_Page import API_PortalMaster

D = DOM_PortalMaster
A = APIdata_PortalMaster
api = API_PortalMaster
regToken = api.testpartnerservice()
# regToken = 'acb5f210-50ff-42b0-b66d-7835787d698b'
authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
print("Balance =", balance)
print("Balance Real =", balanceReal)
totalBets = []
totalWins = []


# @parameterized.expand([('1', '25'), ('2', '25'), ('3', '25'), ('4', '25'), ('5', '25')])


def write_data_to_disk(f, target_data):
    # https://stackoverflow.com/questions/9170288/pretty-print-json-data-to-a-file-using-python
    import datetime
    """ Функция записывает массив target_data в файл 'f'
        example - write_data_to_disk('test', json.dumps(getAsyncResponse, indent=2))
    """
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(target_data)  # записываем файл
    file.close()  # закрываем файл


creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)  # ставка ! CreditDebit # resultId = tokenAsync
getAsyncResponse, resultId, spinId, scatterCrystalGame, spheres, spheresSpinId, scattersForReplace, printAR = api.GetAsyncResponse(regToken, tokenAsync)  # асинхронный ответ ! GetAsyncResponse
trade_low_actionType = 0
trade_mid_actionType = 0
if getAsyncResponse["SpinResult"]["ScatterCrystalGame"]["Id"] is None:
    print("ScatterCrystalGame =", scatterCrystalGame)
else:
    print('\n')
    print(getAsyncResponse)
    print("ScatterCrystalGame =", scatterCrystalGame)
    print("Spheres =", spheres)
    print("SpheresSpinId =", spheresSpinId)
    print("ScattersForReplace =", scattersForReplace)
    if spheres[0] > 0:  # тут проверяем, что есть хоть 1 сфера нижнего уровня и заканчиваем спин
        trade_low_actionType = '2'  # Finish : ActionType = 2
        scatterCrystalBonusGame = api.ScatterCrystalBonusGame(regToken, resultId, scatterCrystalGame, spinId,
                                                              ActionType=2,
                                                              ScatterPositionRow=0,
                                                              ScatterPositionColumn=0,
                                                              LevelSphere='-1',
                                                              Info='false')
        tokenAsyncScatter = scatterCrystalBonusGame['TokenAsync']
        getAsyncResponseScatter = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)  # асинхронный ответ ! GetAsyncResponse_Scatter
        print(getAsyncResponseScatter)

    if spheres[0] == 3:  # тут проверяем, что есть 3 сферы нижнего уровня и меняем 3 сферы на 1 сферу среднего уровня
        trade_low_actionType = '0'  # Trade : ActionType = 0
        scatterCrystalBonusGame = api.ScatterCrystalBonusGame(regToken, resultId, scatterCrystalGame, spinId,
                                                              ActionType=trade_low_actionType,
                                                              ScatterPositionRow=0,
                                                              ScatterPositionColumn=0,
                                                              LevelSphere='1',
                                                              Info='false')

    if spheres[1] > 0:  # тут проверяем, что есть хоть 1 сфера среднего уровня
        trade_mid_actionType = '1'  # Replace : ActionType = 1
        scatterCrystalBonusGame = api.ScatterCrystalBonusGame(regToken, resultId, scatterCrystalGame, spinId,
                                                              ActionType=trade_mid_actionType,
                                                              ScatterPositionRow=0,
                                                              ScatterPositionColumn=0,
                                                              LevelSphere='-1',
                                                              Info='false')
        tokenAsyncScatter = scatterCrystalBonusGame['TokenAsync']
        getAsyncResponseScatter = api.GetAsyncResponse_Scatter(regToken, tokenAsyncScatter)  # асинхронный ответ ! GetAsyncResponse_Scatter
        print(getAsyncResponseScatter)

    if spheres[1] == 2:  # тут проверяем, что есть 2 сферы среднего уровня и меняем 2 сферы на 1 сферу высшего уровня
        trade_mid_actionType = '0'  # Trade : ActionType = 0
        scatterCrystalBonusGame = api.ScatterCrystalBonusGame(regToken, resultId, scatterCrystalGame, spinId,
                                                              ActionType=trade_mid_actionType,
                                                              ScatterPositionRow=0,
                                                              ScatterPositionColumn=0,
                                                              LevelSphere='2',
                                                              Info='false')

    else:
        pass


print('the end ...')

# write_data_to_disk('test', json.dumps(getAsyncResponse, indent=2))

if __name__ == "__main__":
    unittest.main()
