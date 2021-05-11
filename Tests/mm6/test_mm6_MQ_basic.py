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
from Locators.Locators import bets, APIdata_MancalaQuest
from Pages.MancalaQuest_Page import API_MancalaQuest

A = APIdata_MancalaQuest
api = API_MancalaQuest
regToken, iFrameUrl = api.testpartnerservice()
# regToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2MTkwNzcwMTcsImV4cCI6MTYxOTA3ODgxNywiaXNzIjoiaHR0cDovL2lkZW50aXR5c2VydmVyLXRlc3QuY2FyaGVuZ2Uuc3BhY2UiLCJjbGllbnRfaWQiOiJQYXJ0bmVyU2VydmljZSIsIlNlc3Npb25JZGVudGl0eSI6IkdDSElXekRIQXlBbWlDYlIvSTN5bHErVHNYTGtRTHVyd2VkUXNEM3JWZ2JzRnN5UkV1LzZZSE9HYitZVUVFM2F2OTZNNjdreENRbVBHeGFyQldObnhGUFhCcEkwRUdJNFVWdUVrUlhwRUErT3BOT0thNEE0aGZvbjMyZlNMbiszQlJPSjB6WHRHVlpPbnJvY0NRZ1drRzdVd1BycXJRN3FFbC9OY1dHS0t6ZXZJUzZRamlsNU4xcVNlMFhvSTF1WHhjaXpXWjB2MUs0ejI2cHI3cG1Qdlpkb0J5TUVSWDZ1UWIrTWxESEtOdFFFdjFVNnJia3R6TXBXazU1c3RxdGloVUtlSm5Fd1A1SnoxRThoK2dqL24wYnYxOG94eXhPV2R1enhRRk9CMUFIMDh5NGNzcUZ5eEVDTEZ0by9ybHNrbDltOVIwQW05VnNYK0NuU3JYWlRSWVpkMGREbGw2SHdyaHN3S3RkMCtzV25wREhNT0JScEhnZnhyNlZlb0MzT3BQWnpVWnJaeGt0aGpCeUI3NFJ0Uzg4WmF0cm5LSkkwMlVVdDc0ZG9LZDF2dnhyclpKUUFvaklaMk5IRXp4Sm5HYzY5YU4wa3VCM0NkYmpyK2hadjFtcXc1cUp3T2had21DRVFOcFY4RU1ENXVmUkNmcUxlNEtBZFVsdWxTaDdDQjhtV2VTUjJwKzdHVW84V3J6QkEwQ3NqNnNGd2E2WGJpTm8yM3hkeDVhbHo2T2lMODFjNUZlOXlLY0ltY3FrWFdPaHFTQkVsdDBWak9Jei9hRkIyNE9MVnBOOTRyM2x4WkdlYmZmVWVMM01TSVh2YXptTTVIaDZsQ3ZzblVpcEtpdmVqQi84WXdyb0NjOWtSN1RhM2ppQ1FXbVE2Zyt6SjJVV1A4L2t6T01Rc3R4SEtyMFVrZUk0VFVmOGxodnI1SFYwUXdyMklHS2lRTjFpRjVOa01HaEREV3NldVprZ0Y4Z0F4NEdjUVV4d1o4TnJoM1h5ZjRJN0pjWFM2OFpEY21yNzU0M3dmTHgySWwwSWJLOEhkd2JydFRzWDI5SkU2aGZVUlpDTXJHVWc9IiwiR2FtZUlkIjoiMTkwMDEiLCJTbG90VHlwZSI6IjE5IiwiR2FtZVNlcnZpY2VVcmwiOiJodHRwczovL3Rlc3QtbW02bi1hcGkuY2FyaGVuZ2Uuc3BhY2UvIiwiR2FtZVVybCI6Imh0dHBzOi8vc3Rlc3QuemhkdW4uc3BhY2UvbW02bi8iLCJqdGkiOiI2Q0FBRkFCMTFFNkVDRjIxRkY4NjUwMjZGRjNCRTIyQiIsImlhdCI6MTYxOTA3NzAxNywic2NvcGUiOlsiR2VuZXJhdGVKd3RUb2tlbiJdfQ.k_arunsCHJ4bx3wjGXfJfzHuk4fsnQSh4IikXTxQ6_KZWisKlLHbonRGeVW9lC7RUVyK8ec-ed0plGsdaobLyaM4bt7IVJGsDEf0gPP79S07yT3A5xKMYNXzU6m_FL0nd0v1YgJRsAga20uSoRvj8viTPRDMNRF12hPecrPev_MAyi-6KSS7udpdYBfYCo_ozygsFdz0uW8ycoFc3hEvnhnGKlQO2xv7Kqd3ID9vY0-U1cZeBPFt-ig1hTgePLrOn5tpdoZDbnDGMv8P_MwIrbzgEiBB4Bn0aFiO5JtSg4XAXpPW75hyDk9dLZyApHASCK_kouXb0DcWkozG8_Xgbk_ezTzLcshjcEmC1X9QfZpiBx6swB4tgr58qPufov8Sr7f-3mykToJnKKXwsvSoMCMsIbVzvfMNU-2n4zeu_0fXJrt6I0ONVR2qX3FHbwSSCD-IOZLonRukk5EHfWX7JDGNdzeok8BmytiRt8X6uVIYvksTEwNMTeBwEpHBEHAS83nc_IYZ3UhRr-rXqD1957Bh-ODlZdiXNH5j1LiJq394rRVOIfcEo7qvBM8amQ_edO-RPvoEdmaHL0RJeqLy14_ir5s-fIwykq16WTCOPQQm1bcjdtsb72V_Q1XcxzTsdZc3dY8WOE14J8SFTa_7LVapOtafprJNvm6BO0YHIFE'
authorizationGame, balance, balanceReal, coin, currency, func = api.AuthorizationGame(regToken)
balanceRealBefore = balanceReal
func(balance, balanceReal, coin, currency)

aa = []
i = 0
StonesNumber = 0
while StonesNumber < 70:
    print('spin # %s' % str(i + 1))
    creditDebit, tokenAsync = api.CreditDebit(regToken, A.betSum, A.cntLineBet)
    getAsyncResponse, resultId, spinId, StonesNumber, OAKLines, printAR, oak_l = api.GetAsyncResponse(regToken, tokenAsync)
    if oak_l > 0:
        aa.append(oak_l)
    i = i + 1

print('collected %s stones after %s times' % (StonesNumber, i))
print('OAK lines = ', aa)
print('game_IframeUrl = ', iFrameUrl)
print('the end ...')


if __name__ == "__main__":
    unittest.main()
