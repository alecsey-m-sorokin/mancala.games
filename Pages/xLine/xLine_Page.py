import hashlib
import time
import unittest

import pytest
import requests

from Locators.Locators import APIdata_xLine

A = APIdata_xLine

class API_xLine:

    @staticmethod
    def testpartnerservice():
        params = {'gameURL': A.gameURL, 'frontURL': A.frontURL, 'partnerURL': A.partnerURL, 'partnerId': A.partnerID,
                  'gameID': A.gameID, 'userID': A.userID, 'currency': A.currency}
        response = requests.get(A.DOMAIN_tps, params=params)
        assert response.status_code == 200
        regToken = response.text.split("token=")[1].split("&")[0]
        print('game_%s_IframeUrl = ' % A.gameID, response.text)
        print('game_%s_regToken = ' % A.gameID, regToken)
        return regToken

    @staticmethod
    def AuthorizationGame(RegToken):
        HASH = hashlib.md5(('AuthorizationGame/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        params_AuthorizationGame = {'Hash': HASH, 'Token': RegToken, 'MobilePlatform': 'false'}
        response_AuthorizationGame = requests.post(A.gameURL + '/auth/AuthorizationGame',
                                                   params={'Hash': HASH, 'Token': RegToken,
                                                           'MobilePlatform': 'false'},
                                                   json=params_AuthorizationGame)
        response = response_AuthorizationGame.json()
        assert response_AuthorizationGame.status_code == 200
        print(response)
        return response

    @staticmethod
    def GetSlotInfo(RegToken):
        HASH = hashlib.md5(('GetSlotInfo/' + RegToken + A.gameKey).encode('utf-8')).hexdigest()
        params_GetSlotInfo = {'Hash': HASH, 'Token': RegToken}
        response_GetSlotInfo = requests.post(A.gameURL + '/games/GetSlotInfo',
                                             params={'Hash': HASH, 'Token': RegToken}, json=params_GetSlotInfo)
        response = response_GetSlotInfo.json()
        assert response_GetSlotInfo.status_code == 200
        return response

    @staticmethod
    def CreditDebit(RegToken, betSum=A.betSum, cntLineBet=A.cntLineBet):
        HASH = hashlib.md5(('CreditDebit/' + RegToken + betSum + cntLineBet + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_CreditDebit = ', HASH)
        params_CreditDebit = {'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                              'BetSum': betSum}
        response_CreditDebit = requests.post(A.gameURL + '/games/CreditDebit',
                                             params={'Hash': HASH, 'Token': RegToken, 'CntLineBet': cntLineBet,
                                                     'BetSum': betSum}, json=params_CreditDebit)
        response = response_CreditDebit.json()
        assert response_CreditDebit.status_code == 200
        print('CreditDebit_TokenAsync = ', response['TokenAsync'])
        return response

    @staticmethod
    def GetAsyncResponse(RegToken, TokenAsync):
        """
        возвращает параметры: response
        если :
        'BonusGameId' === null, тогда 'BonusGameId' = "no bonus game" : example : ["SpinResult"]["PuzzleGame"] is None
        иначе :
        'BonusGameId' = jsonData.SpinResult.PuzzleGame.Id
        'SpinId' = jsonData.PuzzleResult.Id

        если :
        'ExtraFreeSpins' === null, тогда 'ExtraFreeSpins' = "no ExtraFreeSpins"
        иначе :
        'ExtraFreeSpins' = jsonData.ExtraFreeSpins
         """
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsync + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponse = ', HASH)
        params_GetAsyncResponse = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync}
        response_GetAsyncResponse = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                  params={'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsync},
                                                  json=params_GetAsyncResponse)
        response = response_GetAsyncResponse.json()
        assert response_GetAsyncResponse.status_code == 200
        while "Error" in response:
            time.sleep(1)
            response_GetAsyncResponse = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                      params={'Hash': HASH, 'Token': RegToken,
                                                              'TokenAsync': TokenAsync}, json=params_GetAsyncResponse)
            response = response_GetAsyncResponse.json()
        else:
            print("ResultId =", response['ResultId'])
            print("SpinId =", response["SpinResult"]["Id"])
        return response

    @staticmethod
    def PuzzleBonusGame(RegToken, ResultId, BonusGameId, SpinId):
        HASH = hashlib.md5(
            ('PuzzleBonusGame/' + RegToken + ResultId + SpinId + BonusGameId + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_PuzzleBonusGame = ', HASH)
        params_PuzzleBonusGame = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId, "BonusGameId": BonusGameId,
                                  "SpinId": SpinId}
        response_PuzzleBonusGame = requests.post(A.gameURL + '/bonus/PuzzleBonusGame',
                                                 params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                         "BonusGameId": BonusGameId, "SpinId": SpinId},
                                                 json=params_PuzzleBonusGame)
        response = response_PuzzleBonusGame.json()
        assert response_PuzzleBonusGame.status_code == 200
        url = response_PuzzleBonusGame.url
        print('PuzzleBonusGame_TokenAsync = ', response['TokenAsync'])
        return response

    @staticmethod
    def GetAsyncResponse_Puzzle(RegToken, TokenAsyncPuzzle):
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsyncPuzzle + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponsePuzzle = ', HASH)
        params_GetAsyncResponse_PuzzleBonusGame = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsyncPuzzle}
        response_GetAsyncResponse_PuzzleBonusGame = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                  params={'Hash': HASH, 'Token': RegToken,
                                                                          'TokenAsync': TokenAsyncPuzzle},
                                                                  json=params_GetAsyncResponse_PuzzleBonusGame)
        response = response_GetAsyncResponse_PuzzleBonusGame.json()
        assert response_GetAsyncResponse_PuzzleBonusGame.status_code == 200
        # GetAsyncResponse_ResultId = response['ResultId']
        return response

    @staticmethod
    def SelectCardBonusGame(RegToken, ResultId, BonusGameId, SpinId, CardIndex, Info):
        HASH = hashlib.md5(
            ('SelectCardBonusGame/' + RegToken + ResultId + SpinId + BonusGameId + A.CardIndex + A.gameKey).encode(
                'utf-8')).hexdigest()
        print('hash_SelectCardBonusGame = ', HASH)
        params_SelectCardBonusGame = {"Hash": HASH, "Token": RegToken, "ResultId": ResultId, "BonusGameId": BonusGameId,
                                      "SpinId": SpinId, "CardIndex": CardIndex, "Info": Info}
        response_SelectCardBonusGame = requests.post(A.gameURL + '/bonus/SelectCardBonusGame',
                                                     params={"Hash": HASH, "Token": RegToken, "ResultId": ResultId,
                                                             "BonusGameId": BonusGameId, "SpinId": SpinId,
                                                             "CardIndex": CardIndex, "Info": Info},
                                                     json=params_SelectCardBonusGame)
        response = response_SelectCardBonusGame.json()
        assert response_SelectCardBonusGame.status_code == 200
        print('SelectCardBonusGame_TokenAsync = ', response['TokenAsync'])
        return response

    @staticmethod
    def GetAsyncResponse_Card(RegToken, TokenAsyncCard):
        HASH = hashlib.md5(('GetAsyncResponse/' + TokenAsyncCard + A.gameKey).encode('utf-8')).hexdigest()
        print('hash_GetAsyncResponseCard = ', HASH)
        params_GetAsyncResponse_SelectCardBonusGame = {'Hash': HASH, 'Token': RegToken, 'TokenAsync': TokenAsyncCard}
        response_GetAsyncResponse_DiceBonusGame = requests.post(A.gameURL + '/games/GetAsyncResponse',
                                                                params={'Hash': HASH, 'Token': RegToken,
                                                                        'TokenAsync': TokenAsyncCard},
                                                                json=params_GetAsyncResponse_SelectCardBonusGame)
        response = response_GetAsyncResponse_DiceBonusGame.json()
        assert response_GetAsyncResponse_DiceBonusGame.status_code == 200
        return response
