import datetime
import time
from datetime import timedelta
import jwt
import pytest
import sys
import argparse

# from Pages.mm6.MancalaQuest_Page import A, Logger
# from conftest import get_param

fileName = ''
r = 0

# dt_start = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
dt_start = time.time()
time.sleep(1)
# dt_spent = timedelta(seconds=round(time.time() - dt_start))
print('Execution took: %s' % timedelta(seconds=round(time.time() - dt_start)))


def gameParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sessions', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=25)
    return parser


gameParams = gameParser()
namespace = gameParams.parse_args(sys.argv[1:])
sessions = namespace.sessions
rounds = namespace.rounds
print(f'sessions = {sessions}')
print(f'rounds = {rounds}')
print(namespace)

aa = []
for a in range(350, 355):
    aa.append(a)
    print(a)


def print2file(f, target_data):
    import datetime
    # dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(target_data)  # записываем файл
    file.write('\n')
    file.close()  # закрываем файл


# dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
# fileName = '../../logs/' + 'gameId _%s userId _%s session _%s -' % (A.gameID, A.userID, 6) + ' {}.json'.format(dt)

# log = Logger(fileName, toFile=True, toConsole=True)
# print2 = log.printml
#
# print2(aa)

"""
jwt example: https://jwt.io/
"""
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2MTkxMTcyMDMsImV4cCI6MTYxOTExOTAwMywiaXNzIjoiaHR0cDovL2lkZW50aXR5c2VydmVyLXRlc3QuY2FyaGVuZ2Uuc3BhY2UiLCJjbGllbnRfaWQiOiJQYXJ0bmVyU2VydmljZSIsIlNlc3Npb25JZGVudGl0eSI6IkdDSElXekRIQXlBbWlDYlIvSTN5bHErVHNYTGtRTHVyd2VkUXNEM3JWZ2JzRnN5UkV1LzZZSE9HYitZVUVFM2F2OTZNNjdreENRbVBHeGFyQldObnhGUFhCcEkwRUdJNFVWdUVrUlhwRUErT3BOT0thNEE0aGZvbjMyZlNMbiszQlJPSjB6WHRHVlpPbnJvY0NRZ1drRVVQYzIyTkhGTDJNTm84MmswbW82bTZXeEpjK3FwdnFDOXFzUW9PaDEyV1RRTUt3TjN1WU5IcThLcHdEcWs3MkUvaTYxWFQraU9HcUhDdTZDUHo0N0dLR3hzaGpQVXgybzcxRkk4b24rNkI0WUgvcEhOdXROWUNrQjl3UWR4eGY1SGpJeWdJU1o2d3Mzb2JEa0dCY0NnN0h0V2FiL2NmTFlEYmxRRE5QYmZvZi9jdzhaT2FnbDkwNVFMU0xpRnYxYnhmb1lmWGJSUk1aNGlUZXZRNHlmcUl4WUg4Z0xqeTRtbTBJcENaTUhtWTFKd0pEU3F2anVQTzE5TUdQYzdRMG5XK3pOWVhEb244MDdGRkQ5WUYycGtaMnpFNDBLb1dRczlVZXhpYURJcDIvZWNsdFZQOG9ZcGh6RHQ2Z0VuTWRtRy9oK1loRG5NOFpZcHl5bm5MTU43UGt6SW43MmcvSmxDcjFYSnRzUHpsL29tMlJya0h2SDg1dGtkS0JRcVI3M3dEeXlkN2pyTHRBdzNCR1owK215SjZyQmVFSTlGOUpnT0lmTkI2a2tWVENNU1psOEFIZ3RVb2VHY1poVzUrVWw1R3pYZU0yUTFyZFNueWF0Q2lvdWhKeEZBZUdlODNVVVhYTStGb0xwQ2twQk5UNE85dFNhYVpMdG5wOUFURlZlQTBMZGFxMGlERzg4UzRlNEhKdldES2hzVjJzc1l1QkRtV3pteXZEMzNwT1NUV2V3SzFXWE40QXlvUzkycERGQ3RxZWE5WnZ0SUNQdmszY3BJYmRCYjBLeGlDRXRNK2c3RWs0bFBnM2pHdDh5bUxjYjlWTGZjVmxxdzdMcE1xV2JhNE81S3ZEalEybUdUQ2dWUUp3R0k9IiwiR2FtZUlkIjoiMTkwMDEiLCJTbG90VHlwZSI6IjE5IiwiR2FtZVNlcnZpY2VVcmwiOiJodHRwczovL3Rlc3QtbW02bi1hcGkuY2FyaGVuZ2Uuc3BhY2UvIiwiR2FtZVVybCI6Imh0dHBzOi8vc3Rlc3QuemhkdW4uc3BhY2UvbW02bi8iLCJqdGkiOiIzMzYyNDg1NjhERjM2QUU4OTNDNTQ3NjY0NDgwMDRBMSIsImlhdCI6MTYxOTExNzIwMywic2NvcGUiOlsiR2VuZXJhdGVKd3RUb2tlbiJdfQ.BDTxMXafAeiDFd3ZFS1xJtzcN1DrkvZbxNQ2VWPK7KSz5r7CYouhhypOFQsEhMuGoydZ1GGgQG2Vnxh6C3WPgLARW-JMrGcF4vA92Tc9zigXNfrzlJUyAmxXix_TmvIxYOWbepYI_VIYWbDVxMt8GUIaZ2c9j6DRM7Ty8PjBaZvAMuq3XB1QysVv_Uh7lndUgIeA-eQX_eXPUu1DYTQPtWDLI5DbqrKMKECs2eiz3VnUV16lrsrwxGd0-pXbvBCApgeXVOezFdR_TdtuCRIeH7ONsstHnE5_iGdK9v0P0SNHFdLyc3FKfIloohJGMUD9mD-mOcFY3D0OhjFLOO2Mjp03Z1kTHXlxd_q8_DVnHKDuLN4sgSMhTaZ4oxDuyvd6_nyQO906C-yktQW8jAgYuniU4JeaNjJAEcqX6SDIl_Esc5pZjeBJenSlHFe68QuDcDv1e9GfzDeGy5K13ZDwhm6h2aacfkkS6a2j5Xf-Dw4n_T6v0VD1ZiRbunQgFRK0V6ujyWuyLTNoruoClEDSZi4aKMQwn6S-ESx9UCgNa5Q20lLWU-ikGtkHdfd-2dXAbVYfGUYrH2rKH7Jv2NQc2x0zDqCtZYhJYTpjKR81G9LWHalu8lK_TPEZHpmo5G3_TBAPYHhZoS6g2wDWPkjLW3efrFTdJ7a0YFWgWP1qEIY'
payload = "{'nbf': 1619117203, 'exp': 1619119003, 'iss': 'http://identityserver-test.carhenge.space', 'client_id': 'PartnerService', 'SessionIdentity': 'GCHIWzDHAyAmiCbR/I3ylq+TsXLkQLurwedQsD3rVgbsFsyREu/6YHOGb+YUEE3av96M67kxCQmPGxarBWNnxFPXBpI0EGI4UVuEkRXpEA+OpNOKa4A4hfon32fSLn+3BROJ0zXtGVZOnrocCQgWkEUPc22NHFL2MNo82k0mo6m6WxJc+qpvqC9qsQoOh12WTQMKwN3uYNHq8KpwDqk72E/i61XT+iOGqHCu6CPz47GKGxshjPUx2o71FI8on+6B4YH/pHNutNYCkB9wQdxxf5HjIygISZ6ws3obDkGBcCg7HtWab/cfLYDblQDNPbfof/cw8ZOagl905QLSLiFv1bxfoYfXbRRMZ4iTevQ4yfqIxYH8gLjy4mm0IpCZMHmY1JwJDSqvjuPO19MGPc7Q0nW+zNYXDon807FFD9YF2pkZ2zE40KoWQs9UexiaDIp2/ecltVP8oYphzDt6gEnMdmG/h+YhDnM8ZYpyynnLMN7PkzIn72g/JlCr1XJtsPzl/om2RrkHvH85tkdKBQqR73wDyyd7jrLtAw3BGZ0+myJ6rBeEI9F9JgOIfNB6kkVTCMSZl8AHgtUoeGcZhW5+Ul5GzXeM2Q1rdSnyatCiouhJxFAeGe83UUXXM+FoLpCkpBNT4O9tSaaZLtnp9ATFVeA0Ldaq0iDG88S4e4HJvWDKhsV2ssYuBDmWzmyvD33pOSTWewK1WXN4AyoS92pDFCtqea9ZvtICPvk3cpIbdBb0KxiCEtM+g7Ek4lPg3jGt8ymLcb9VLfcVlqw7LpMqWba4O5KvDjQ2mGTCgVQJwGI=', 'GameId': '19001', 'SlotType': '19', 'GameServiceUrl': 'https://test-mm6n-api.carhenge.space/', 'GameUrl': 'https://stest.zhdun.space/mm6n/', 'jti': '336248568DF36AE893C54766448004A1', 'iat': 1619117203, 'scope': ['GenerateJwtToken']}"
decoded = jwt.decode(token, options={"verify_signature": False}, algorithms='RS256')
print(decoded)
print(jwt.get_unverified_header(token))

# encoded = jwt.encode(payload, key='', algorithm='RS256')
# print(encoded)

#  https://coderoad.ru/1557571/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F-%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B-Python
