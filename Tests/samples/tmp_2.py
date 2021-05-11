import logging
import threading
import time

from Locators.Locators import APIdata_PortalMaster, DOM_PortalMaster, bets
from Pages.PortalMaster_Page import API_PortalMaster, ScatterCrystalActionType, LevelSphere

D = DOM_PortalMaster
A = APIdata_PortalMaster
api = API_PortalMaster

a = [795, 796, 797]
empty_list = []


def thread_function(ids):
    print('\n')
    print('userId # %s' % ids)
    regToken = api.tps(ids)
    logging.info("Thread %s: starting", ids)
    time.sleep(2)
    logging.info("Thread %s: finishing", ids)


for i in range(len(a)):
    empty_list.append(a[i])

for i in range(len(a)):
    a[i] = threading.Thread(target=thread_function, args=(a[i],))
    a[i].start()
