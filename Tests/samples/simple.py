import datetime
import hashlib
import random
import time
import unittest
from random import randint

import jwt
import pytest
import requests
from parameterized import parameterized
import json
from Locators.Locators import bets, APIdata_MancalaQuest
from Pages.mm6.MancalaQuest_Page import API_MancalaQuest

A = APIdata_MancalaQuest
api = API_MancalaQuest
regToken, iFrameUrl = api.testpartnerservice()
# regToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2MjAzMTE4NTcsImV4cCI6MTYyMDMxMzY1NywiaXNzIjoiaHR0cDovL2lkZW50aXR5c2VydmVyLmNhcmhlbmdlLnNwYWNlIiwiY2xpZW50X2lkIjoiUGFydG5lclNlcnZpY2UiLCJTZXNzaW9uSWRlbnRpdHkiOiJiUStadXQxa05PcldIY2E1aXAwWVFzcC9GcWR3a0FCUUZtTjJ6eEJHWUJyTGZNWGdFYWJBY1ZnMWJHcHZGdjM5ekxOcDVyeWVWbWVRZW9BS3ZaTmp1dDd2MnRCckRzNnk3eTByREFZS3daUEcrRUg0U0t1SUpTQjY1eFVDcUxlZkcyYUUveGZ4MHNjZE15U3FqWUdobHA2NUdnYmliajc4UnpRL2puVEcrendwNDhhQ1k1RDFONzAybHhSV2JsblRMMktjZVUwdWpEVStOZXpwcnpJeDIvYUhIenR0TTVBZ0FrMkpaS2pYMDMxN2ZmeFl1ZU5CcUxVWVZpWitVZDVzRWc2NU9DcVZiSkZyb25OMU8xWVkyeTN6MlRlYWJNUmFRSXVMbkxwUThwb1ZrRDdoUGdPQWE0NHhNdXMxTGFWVUh3QmF5a3kvSjNyd0svN2ZvaU9GMDFKTEk4d3ByNFU5QUxxQmtWQXNIRG9QTnlwUlpud0ZaY0RHeTVubmF4K3g1WjJkU2tLUEtMZXE1OGtxaWVDcVB0eFIrU3J4cDNPL0doeHZYS3BTTFNRWDhkRDBJM3pRWnVKVmRCTDhJUGJxWHUxbkhYNEJ6clJsNUtyRHYvd3JyVlBNcVg5TjdUUzVDMmp1SmpUcGw1bFVPWnRwekZXOTBHZTJ6ajhLcE5RZ2NMdkU3YnprMDZLaWxLNXpod25RVEdEcmNlNW51aTJneEhwQVp3K05OOEcxZzcwT0xxVy9vKytsOTgvZW50YXpJaEU1VUU1TE5xWnJ1eGtMc2NwbE8rNU8xcjcvZWNSdUY1T3Q2Z0MwcFQwTERjYzE3TFJkZllJcGk4TUpreUdES2RuMTdmcldxSEVqeDErelMwTXllSitYZndxU0FHZVpDVVNoV0ZYTkRqaExjNWNtUzFtekd2T1pBVnZpa01VcEFuZ1NGZnRxbytyRWh4SUVUbmhlNW01Sk1LUG4zWGlMeXhFUUtGZlpieE1KQk84OU85NlVoNmh1eGVjS0ZlS3FmRmY0eDhuWUZtMUNncjNra1ZqTGx4KzlHVTM2SkNQaWxxcGhpWHFGcHprPSIsIkdhbWVJZCI6IjE5MDAxIiwiU2xvdFR5cGUiOiIxOSIsIkdhbWVTZXJ2aWNlVXJsIjoiaHR0cHM6Ly90ZXN0LW1tNm4tYXBpLmNhcmhlbmdlLnNwYWNlLyIsIkdhbWVVcmwiOiJodHRwczovL3N0ZXN0LnpoZHVuLnNwYWNlL21tNm4vIiwianRpIjoiRUIxQTUwOTU5QUM0MzQwRTkxNDY4M0U2MEEwMTNENjAiLCJpYXQiOjE2MjAzMTE4NTcsInNjb3BlIjpbIkdlbmVyYXRlSnd0VG9rZW4iXX0.dFkYX-yjf-P1AFecpOL5J4RNQAnCkVwh0wVTY7BLOW-45_QlJM3xzLAwEhDrR50IUMHWGfax8dQUlulubrgmET0w9MGGJSUD6ZzNAbo_2-tksTk7F68QeRmvrv3QWBEkQIGlbTUWpQybZfbwVaDdWfDSZRFqGCOOYJbhVoYHXJBfwr3gR1itJk0xTLpevL3SkkmQHfonOVnT8Fvw0IAVXpY5hbWvFaEsnclG4lLJXS0cnxvPsvogGeoe8uXw8tmcCKBc3CchiNU39ycTDaOjBRt3WLSFwWC7f495JXhFeLzhIFMdgKyeM0PQbf2DiHLQA4UUJ54T2-xCrw_-0q1L6l_HSwJrxNNUGmY3sHx02oyWiX3A4dqY7gNlEvagV09Ha0ffARCrd8gJSkw9Ase3rfq6zr6iQybePk5-UcRI_PkxpNLOsGrVt1RPCuWxTDJQxTPGobe-umnpG2r0B0dvwvJwmMaqgKrqJ-FkSqlG3cHd6jMstHXUZMg5zvoX0p9h1OSD54cuOXVEXYXR2IwTwZ4m8h_80cZyOoJ6hLTBfSB17RHjMSt5Lqkjcwrf03Z_qay7Y5JPV6t0KFRn60d24Uo47MyYtoXMPwebSGRukHTYES0iTHIpL9ZBrjTUbsI5vUI5ls56dQGL_JJm8S7GYMpXEArZ2g9qSsX6pmCcpYE'
authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
balanceRealBefore = balanceReal
func(balance, balanceReal, coin, currency)


def print2file(f, target_data):
    import datetime
    # dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y"))
    # file = open(f + ' {}.txt'.format(dt), 'a')  # открываем куда писать полученные данные
    file = open(f + ' {}.txt'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(target_data)  # записываем файл
    file.close()  # закрываем файл


aa = []
i = 0
StonesNumber = 0
r = 0

fileName = 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, r)
print(fileName)

while StonesNumber < 75:
    print('spin # %s' % str(i + 1))
    print2file(fileName, 'spin # %s' % str(i + 1))
    creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
    getAsyncResponse, resultId, spinId, StonesNumber, totalFreeSpinsCount, mancalaQuestBonusGameId, OAKLines, printAR, oak_l = api.GetAsyncResponse(regToken, tokenAsync)
    if oak_l > 0:
        aa.append(oak_l)
    i = i + 1

print('collected %s stones after %s times' % (StonesNumber, i))
print2file(fileName, 'collected %s stones after %s times' % (StonesNumber, i))
print('OAK lines = ', aa)
print('game_IframeUrl = ', iFrameUrl)
print('the end ...')


if __name__ == "__main__":
    unittest.main()
