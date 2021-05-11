import hashlib
import json
import time
import unittest
import pytest
import requests
from Locators.Locators import APIdata_MancalaQuest, ErrorCodes

A = APIdata_MancalaQuest
E = ErrorCodes

def write_data_to_json_file(f, target_data):
    """
    : Функция записывает массив target_data в файл 'f' в формате JSON
    :output example : 'test 12-03-2021 14-57-37.json'
    :param f: test
    :param target_data: json.dumps(getAsyncResponse, indent=2)
    :example: write_data_to_json_file('test', getAsyncResponse)
    :www source: https://stackoverflow.com/questions/9170288/pretty-print-json-data-to-a-file-using-python
    """
    import datetime
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(json.dumps(target_data, indent=2))  # записываем файл
    file.close()  # закрываем файл


def print2file(f, target_data):
    import datetime
    # dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(target_data)  # записываем файл
    file.write('\n')
    file.close()  # закрываем файл


class Logger(object):

    def __init__(self, fileName='', toFile=False, toConsole=False):
        self.fileName = fileName
        self.toFile = toFile
        self.toConsole = toConsole
        return

    def printml(self, *args):
        aa = []
        toprint = ''
        for v in args:
            aa.append(str(v))
            toprint = toprint + str(v) + ' '
        if self.toFile and self.toConsole:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
                print(aa[a])
                # print('\n')
            f.close()
        elif self.toFile:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
            f.close()
        elif self.toConsole:
            for a in range(len(aa)):
                print(aa[a])
        else:
            pass
        return


class API_MancalaQuest:

    @staticmethod
    def tps(userID):
        params = {'gameURL': A.gameURL, 'frontURL': A.frontURL, 'partnerURL': A.partnerURL, 'partnerId': A.partnerID,
                  'gameID': A.gameID, 'userID': userID, 'currency': A.currency}
        response = requests.get(A.DOMAIN_tps, params=params, headers={'Connection': 'close'})
        # print(response)
        print('params = ', params)
        assert response.status_code == 200
        regToken = response.text.split("token=")[1].split("&")[0]
        print('game_%s_IframeUrl = ' % A.gameID, response.text)
        print('game_%s_regToken = ' % A.gameID, regToken)
        return regToken

    @staticmethod
    def testpartnerservice():
        params = {'gameURL': A.gameURL, 'frontURL': A.frontURL, 'partnerURL': A.partnerURL, 'partnerId': A.partnerID,
                  'gameID': A.gameID, 'userID': A.userID, 'currency': A.currency}
        response = requests.get(A.DOMAIN_tps, params=params, headers={'Connection': 'close'})
        # print(response)
        print('params = ', params)
        assert response.status_code == 200
        regToken = response.text.split("token=")[1].split("&")[0]
        iFrameUrl = response.text
        print('game_%s_IframeUrl = ' % A.gameID, response.text)
        print('game_%s_regToken = ' % A.gameID, regToken)
        return regToken, iFrameUrl

    @staticmethod
    def AuthorizationGame(RegToken):
        """
        возвращает параметры: response, balance, balanceReal, coin, currency, printAG
        'response' =
        'balance' =
        'balanceReal' =
        'coin' =
        'currency' =
        'printAG' = function
         """
        HASH = hashlib.md5(('AuthorizationGame/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_AuthorizationGame = ', HASH)
        params_AuthorizationGame = {'Hash': HASH, 'Token': RegToken, 'MobilePlatform': 'false'}
        response_AuthorizationGame = requests.post(A.gameURL + '/auth/AuthorizationGame',
                                                   params={'Hash': HASH, 'Token': RegToken,
                                                           'MobilePlatform': 'false'},
                                                   json=params_AuthorizationGame, headers={'Connection': 'close'})
        response = response_AuthorizationGame.json()
        print('params = ', params_AuthorizationGame)
        assert response_AuthorizationGame.status_code == 200
        print("Response =", response)
        # url = response_AuthorizationGame.url
        balance = response["Balance"]
        balanceReal = response["BalanceReal"]
        coin = response["Coin"]
        currency = response["Currency"]

        def printAG(*b):
            # print('\n')
            print("Balance = %s, Balance Real = %s, Coin = %s, Currency = %s" % b)
            print('--------------------------------------------------------------------------------------------------')

        return response, balance, balanceReal, coin, currency, printAG

    @staticmethod
    def GetSlotInfo(RegToken):
        HASH = hashlib.md5(('GetSlotInfo/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        params_GetSlotInfo = {'Hash': HASH, 'Token': RegToken}
        response_GetSlotInfo = requests.post(A.gameURL + '/games/GetSlotInfo',
                                             params={'Hash': HASH, 'Token': RegToken}, json=params_GetSlotInfo,
                                             headers={'Connection': 'close'})
        response = response_GetSlotInfo.json()
        assert response_GetSlotInfo.status_code == 200
        return response

    @staticmethod
    def CreditDebit(RegToken, betSum=A.betSum, cntLineBet=A.cntLineBet):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(('CreditDebit/' + RegToken + betSum + cntLineBet + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_CreditDebit = ', HASH)
        params_CreditDebit = {'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                              'BetSum': betSum}
        print('params = ', params_CreditDebit)
        response_CreditDebit = requests.post(A.gameURL + '/games/CreditDebit',
                                             params={'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                                                     'BetSum': betSum}, json=params_CreditDebit, timeout=1, headers={'Connection': 'close'})
        print('url = ', response_CreditDebit.url)
        response = response_CreditDebit.json()
        assert response_CreditDebit.status_code == 200
        tokenAsync = response["TokenAsync"]
        # print(response)
        print('CreditDebit_TokenAsync = ', response['TokenAsync'])
        # response_CreditDebit.close()
        return response, tokenAsync

    @staticmethod
    def GetAsyncResponse(RegToken, TokenAsync):
        """
        возвращает параметры: response, resultId, spinId, StonesNumber, OAKLines, printAR, oak_l
        'response' =
        'ResultId' = jsonData.ResultId
        'SpinId' = jsonData.SpinResult.Id
        'StonesNumber' =
        'OAKLines' =
        'printAR' =
        'oak_l' =
         """
        HASH = hashlib.md5(('GetAsyncResponse/' + RegToken + TokenAsync + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponse = ', HASH)
        params_GetAsyncResponse = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync}
        response_GetAsyncResponse = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                  params={'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync},
                                                  json=params_GetAsyncResponse, timeout=1,
                                                  headers={'Connection': 'close'})
        print('url = ', response_GetAsyncResponse.url)
        response = response_GetAsyncResponse.json()
        url = response_GetAsyncResponse.url
        # print('url =', url)
        # print('GetAsyncResponse = ', response)
        assert response_GetAsyncResponse.status_code == 200
        while "Error" in response:
            if response["Error"] == 13:
                print('GetAsyncResponse = ', response)
                response_GetAsyncResponse = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                          params={'Hash': HASH, 'Token': RegToken,
                                                                  'TokenAsync': TokenAsync},
                                                          json=params_GetAsyncResponse,
                                                          timeout=1, headers={'Connection': 'close'})
                response = response_GetAsyncResponse.json()
            else:
                for key in E.error_codes_dictionary:
                    if response["Error"] == key:
                        print(f'\nScript error: {E.error_codes_dictionary[key]} = {key}', )
                        exit()
        else:
            if "MancalaQuestBonusGameId" not in response["SpinResult"]:
                mancalaQuestBonusGameId = ''
            else:
                mancalaQuestBonusGameId = response["SpinResult"]["MancalaQuestBonusGameId"]
            oak = 0
            oak_l = 0
            resultId = response['ResultId']
            spinId = response["SpinResult"]["Id"]
            stonesNumber = response["SpinResult"]["UserSavedState"]["StonesNumber"]
            OAKLines = response["SpinResult"]["OAKLines"]
            totalFreeSpinsCount = response["GameFreeSpins"][0]["TotalFreeSpinsCount"]
            print("Response =", response)
            print("ResultId =", resultId)
            print("SpinId =", spinId)
            print("StonesNumber =", stonesNumber)
            print("TotalFreeSpinsCount =", totalFreeSpinsCount)
            print("MancalaQuestBonusGameId = ", mancalaQuestBonusGameId)
            # print('OAKLines =', OAKLines)
            if len(OAKLines) == 0:
                print('OAKLines = ', 'none')
            else:
                print('OAKLines length = ', len(OAKLines))
                oak = range(len(OAKLines))
                print('oak = ', oak)
                oak_l = len(oak)
                print('len "range oak" =', len(oak))
                for i in oak:
                    print('i = ', i)
                    print('OAKLines # %s = %s' % (i, OAKLines[i]))

        def printAR(coin):
            betSum = response["BetSum"]
            totalWin = response["WinInfo"]["TotalWin"]
            balance = response["WinInfo"]["Balance"]
            balance_before_spin = (balance - totalWin + betSum) * coin
            balance_after_spin = balance * coin
            # print('\n')
            print("BetSum = %s, TotalWin = %s, BalanceBeforeSpin = %s, BalanceAfterSpin = %s" % (
                betSum, totalWin, balance_before_spin, balance_after_spin))
            print(
                '---------------------------------------------------------------------------------------------------------')

        # response_GetAsyncResponse.close()
        return response, resultId, spinId, stonesNumber, totalFreeSpinsCount, mancalaQuestBonusGameId, OAKLines, printAR, oak_l

    @staticmethod
    def GetMancalaQuestGameState(RegToken, ResultId, BonusGameId, SpinId):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(
            ('GetMancalaQuestGameState/' + RegToken + SpinId + BonusGameId + ResultId + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_GetMancalaQuestGameState = ', HASH)
        params_GetMancalaQuestGameState = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                           "BonusGameId": BonusGameId, "SpinId": SpinId}
        response_GetMancalaQuestGameState = requests.post(A.gameURL + '/bonus/GetMancalaQuestGameState',
                                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                                  "BonusGameId": BonusGameId, "SpinId": SpinId},
                                                          json=params_GetMancalaQuestGameState, timeout=1,
                                                          headers={'Connection': 'close'})
        response = response_GetMancalaQuestGameState.json()
        assert response_GetMancalaQuestGameState.status_code == 200
        print(response)
        tokenAsyncGetMancalaQuestGameState = response["TokenAsync"]
        print('GetMancalaQuestGameState_TokenAsync = ', response['TokenAsync'])
        # response_GetMancalaQuestGameState.close()
        return response, tokenAsyncGetMancalaQuestGameState

    @staticmethod
    def GetAsyncResponse_QuestGameState(RegToken, TokenAsyncGetMancalaQuestGameState):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + TokenAsyncGetMancalaQuestGameState + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_GetAsyncResponseQuestGameState = ', HASH)
        params_GetAsyncResponse_QuestGameState = {'Hash': HASH, 'Token': RegToken,
                                                  'TokenAsync': TokenAsyncGetMancalaQuestGameState}
        response_GetAsyncResponse_QuestGameState = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                 params={'Hash': HASH, 'Token': RegToken,
                                                                         'TokenAsync': TokenAsyncGetMancalaQuestGameState},
                                                                 json=params_GetAsyncResponse_QuestGameState, timeout=1,
                                                                 headers={'Connection': 'close'})
        response = response_GetAsyncResponse_QuestGameState.json()
        assert response_GetAsyncResponse_QuestGameState.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_QuestGameState = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                     params={'Hash': HASH, 'Token': RegToken,
                                                                             'TokenAsync': TokenAsyncGetMancalaQuestGameState},
                                                                     json=params_GetAsyncResponse_QuestGameState,
                                                                     timeout=1,
                                                                     headers={'Connection': 'close'})
            response = response_GetAsyncResponse_QuestGameState.json()
        else:
            print('params = ', params_GetAsyncResponse_QuestGameState)
            print("Response =", response)
            ActiveCharacterIndex = response["ActiveCharacterIndex"]
            CharacterIndex = response["CharacterIndex"]
            Cups = response["Cups"]
        # response_GetAsyncResponse_QuestGameState.close()
        return response, ActiveCharacterIndex, CharacterIndex, Cups

    @staticmethod
    def SelectCharacter(RegToken, ResultId, BonusGameId, SpinId, CharacterId):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(
            ('SelectCharacter/' + RegToken + CharacterId + BonusGameId + ResultId + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_SelectCharacter = ', HASH)
        params_SelectCharacter = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                  "BonusGameId": BonusGameId, "SpinId": SpinId, "CharacterId": CharacterId}
        response_SelectCharacter = requests.post(A.gameURL + '/bonus/SelectCharacter',
                                                 params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                         "BonusGameId": BonusGameId, "SpinId": SpinId,
                                                         "CharacterId": CharacterId},
                                                 json=params_SelectCharacter, timeout=1,
                                                 headers={'Connection': 'close'})
        response = response_SelectCharacter.json()
        url = response_SelectCharacter.url
        # print('url = ', url)
        print('params = ', params_SelectCharacter)
        print('response = ', response)
        assert response_SelectCharacter.status_code == 200
        tokenAsyncSelectCharacter = response["TokenAsync"]
        # print(response)
        print('SelectCharacter_TokenAsync = ', response['TokenAsync'])
        # response_SelectCharacter.close()
        return response, tokenAsyncSelectCharacter

    @staticmethod
    def GetAsyncResponse_SelectCharacter(RegToken, tokenAsyncSelectCharacter):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + tokenAsyncSelectCharacter + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseSelectCharacter = ', HASH)
        params_GetAsyncResponse_SelectCharacter = {'Hash': HASH, 'Token': RegToken,
                                                   'TokenAsync': tokenAsyncSelectCharacter}
        response_GetAsyncResponse_SelectCharacter = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                  params={'Hash': HASH, 'Token': RegToken,
                                                                          'TokenAsync': tokenAsyncSelectCharacter},
                                                                  json=params_GetAsyncResponse_SelectCharacter,
                                                                  timeout=1,
                                                                  headers={'Connection': 'close'})
        response = response_GetAsyncResponse_SelectCharacter.json()
        # print('GetAsyncResponse_SelectCharacter = ', response)
        assert response_GetAsyncResponse_SelectCharacter.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_SelectCharacter = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                      params={'Hash': HASH, 'Token': RegToken,
                                                                              'TokenAsync': tokenAsyncSelectCharacter},
                                                                      json=params_GetAsyncResponse_SelectCharacter,
                                                                      timeout=1, headers={'Connection': 'close'})
            response = response_GetAsyncResponse_SelectCharacter.json()
        else:
            print('params = ', params_GetAsyncResponse_SelectCharacter)
            print("response =", response)
            Character = response["Character"]
            print("Character = ", Character)
        # response_GetAsyncResponse_SelectCharacter.close()
        return response, Character

    @staticmethod
    def MakeStep(RegToken, ResultId, BonusGameId, SpinId):
        """
        возвращает параметры: response, tokenAsync
        'tokenAsync' = jsonData.TokenAsync
         """
        HASH = hashlib.md5(
            ('MakeStep/' + RegToken + SpinId + BonusGameId + ResultId + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_MakeStep = ', HASH)
        params_MakeStep = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                           "BonusGameId": BonusGameId, "SpinId": SpinId}
        response_MakeStep = requests.post(A.gameURL + '/bonus/MakeStep',
                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                  "BonusGameId": BonusGameId, "SpinId": SpinId},
                                          json=params_MakeStep, timeout=1,
                                          headers={'Connection': 'close'})
        response = response_MakeStep.json()
        print('params_MakeStep = ', params_MakeStep)
        print('response = ', response)
        assert response_MakeStep.status_code == 200
        tokenAsyncMakeStep = response["TokenAsync"]
        print('MakeStep_TokenAsync = ', response['TokenAsync'])
        # response_MakeStep.close()
        return response, tokenAsyncMakeStep

    @staticmethod
    def GetAsyncResponse_MakeStep(RegToken, tokenAsyncMakeStep):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + tokenAsyncMakeStep + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseMakeStep = ', HASH)
        params_GetAsyncResponse_MakeStep = {'Hash': HASH, 'Token': RegToken,
                                            'TokenAsync': tokenAsyncMakeStep}
        response_GetAsyncResponse_MakeStep = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                           params={'Hash': HASH, 'Token': RegToken,
                                                                   'TokenAsync': tokenAsyncMakeStep},
                                                           json=params_GetAsyncResponse_MakeStep,
                                                           timeout=1,
                                                           headers={'Connection': 'close'})
        response = response_GetAsyncResponse_MakeStep.json()
        # print('GetAsyncResponse_SelectCharacter = ', response)
        assert response_GetAsyncResponse_MakeStep.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_MakeStep = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                               params={'Hash': HASH, 'Token': RegToken,
                                                                       'TokenAsync': tokenAsyncMakeStep},
                                                               json=params_GetAsyncResponse_MakeStep,
                                                               timeout=1, headers={'Connection': 'close'})
            response = response_GetAsyncResponse_MakeStep.json()
        else:
            if "WinStateInfo" not in response:
                FreeSpinCount = 0
                Multiplier = 0
            else:
                FreeSpinCount = response["WinStateInfo"]["FreeSpinCount"]
                Multiplier = response["WinStateInfo"]["Multiplier"]
            print('params_GetAsyncResponse_MakeStep = ', params_GetAsyncResponse_MakeStep)
            print("Response =", response)
            print('FreeSpinCount = ', FreeSpinCount)
            print('Multiplier = ', Multiplier)
            ActiveCharacterIndex = response["ActiveCharacterIndex"]
            # CupIndex = response["CupIndex"]
            # Cups = response["Cups"]
            # Steals = response["Steals"]
            # print("ActiveCharacterIndex = ", ActiveCharacterIndex)
            # print("CupIndex = ", CupIndex)
            # print("Cups = ", Cups)
            # print("Steals = ", Steals)
        # response_GetAsyncResponse_SelectCharacter.close()
        return response, ActiveCharacterIndex, FreeSpinCount, Multiplier

    @staticmethod
    def FreeSpin(RegToken, ResultId, SpinId):
        """
        RegToken :
        ResultId :
        SpinId :
         """
        HASH = hashlib.md5(('FreeSpin/' + RegToken + ResultId + SpinId + A.gameKey).encode('utf-8')).hexdigest()
        print('\n')
        print('hash_FreeSpin = ', HASH)
        params_FreeSpin = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId, "SpinId": SpinId}
        print('params freeSpin= ', params_FreeSpin)
        response_FreeSpin = requests.post(A.gameURL + '/games/FreeSpin',
                                          params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                  "SpinId": SpinId}, json=params_FreeSpin, timeout=1,
                                          headers={'Connection': 'close'})
        response = response_FreeSpin.json()
        print("Response =", response_FreeSpin)
        assert response_FreeSpin.status_code == 200
        url = response_FreeSpin.url
        # print("Response =", response)
        tokenAsyncFreeSpin = response['TokenAsync']
        print('FreeSpin_TokenAsync = ', tokenAsyncFreeSpin)
        response_FreeSpin.close()
        return response, tokenAsyncFreeSpin

    @staticmethod
    def GetAsyncResponse_FreeSpin(RegToken, TokenAsyncFreeSpin):
        HASH = hashlib.md5(
            ('GetAsyncResponse/' + RegToken + TokenAsyncFreeSpin + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseFreeSpin = ', HASH)
        params_GetAsyncResponse_FreeSpin = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsyncFreeSpin}
        print('params getAsyncResponse_FreeSpin= ', params_GetAsyncResponse_FreeSpin)
        response_GetAsyncResponse_FreeSpin = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                           params={'Hash': HASH, 'Token': RegToken,
                                                                   'TokenAsync': TokenAsyncFreeSpin},
                                                           json=params_GetAsyncResponse_FreeSpin, timeout=1,
                                                           headers={'Connection': 'close'})
        response = response_GetAsyncResponse_FreeSpin.json()
        print('GetAsyncResponse_FreeSpin = ', response)
        assert response_GetAsyncResponse_FreeSpin.status_code == 200
        while "Error" in response:
            response_GetAsyncResponse_FreeSpin = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                               params={'Hash': HASH, 'Token': RegToken,
                                                                       'TokenAsync': TokenAsyncFreeSpin},
                                                               json=params_GetAsyncResponse_FreeSpin, timeout=1,
                                                               headers={'Connection': 'close'})
            response = response_GetAsyncResponse_FreeSpin.json()
        else:
            spinIdFs = response['SpinResult']['Id']
            print('spinIdFs = ', spinIdFs)
            print("Response =", response)
            remainingFreeSpinsCount = response["GameFreeSpins"][0]["RemainingFreeSpinsCount"]
            totalFreeSpinsCount = response["GameFreeSpins"][0]["TotalFreeSpinsCount"]
            print("remainingFreeSpinsCount = ", remainingFreeSpinsCount)
            print("totalFreeSpinsCount = ", totalFreeSpinsCount)
            pass
        response_GetAsyncResponse_FreeSpin.close()
        return response, remainingFreeSpinsCount, totalFreeSpinsCount, spinIdFs
