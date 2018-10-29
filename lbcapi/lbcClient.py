from lbcapi import lbcApi as lbc
import json
import re
import numpy as np

HMAC_KEY = "dadd31167030f944efba3a55a75bb113"
HMAC_SECRET = "5f19cfe858e05875378920e9aaab62cc9132d2533569c0d9508944b14f0535bf"
CURRENCY = "VES"
PAYMENT_METHOD = "transfers-with-specific-bank"
URL = "https://localbitcoins.com/sell-bitcoins-online/" + \
    CURRENCY + "/" + PAYMENT_METHOD + "/.json"
PATH = '/home/oneberenjena/Documents/KryptoPay/kryptoPayBeta/src/assets/fees/'
pattern = re.compile(
    "^.*(mercantil|Mercantil|MERCANTIL|M E R C A N T I L|m e r c a n t i l|banesco|Banesco|BANESCO).*$")
    
def apiCall(hmac_key, hmac_secret, currency, payment_method, url):
    connection = lbc.hmac(HMAC_KEY, HMAC_SECRET)
    tradesData = connection.call("GET", url)

    if tradesData.status_code != 200:
        return None

    print("?////////////////////////////////////////////////////////////////////")
    print(tradesData.json())
    print("?////////////////////////////////////////////////////////////////////")
    return tradesData.json()


def parseInfo(tradesData):
    pricesList = []

    trades = tradesData['data']['ad_list']

    for trade in trades:
        tradeInfo = trade['data']
        if bool(pattern.match(tradeInfo['bank_name'])):
            pricesList.append(float(tradeInfo['temp_price']))
    
    print(pricesList)
    return pricesList


def getCoef(priceList):
    mean = np.mean(priceList)
    sd = np.std(priceList)
    coef = 0

    while mean - coef*sd < 50:
        coef += 0.1

    return coef


def cleanPrices(priceList):
    plist = np.array(priceList)
    sd = np.std(plist)
    mean = np.mean(plist)

    coef = getCoef(plist)

    plist_final = [x for x in priceList if (x > mean - coef*sd)]
    plist_final = [x for x in plist_final if (x < mean + coef*sd)]

    return plist.tolist()


def calculateMean(priceList):
    nPrices = len(priceList)
    mean = float(sum(priceList)) / nPrices
    return mean


def outputAsJSON(mean):
    jsonObj = {
        'name': 'Bitcoin',
        'value': mean
    }
    return json.dumps(jsonObj, ensure_ascii=False)
    # with open(PATH + 'prices.json', 'w') as file:
    #     json.dump(jsonObj, file, ensure_ascii=False)


def main():
    tradesData = apiCall(HMAC_KEY, HMAC_SECRET, CURRENCY, PAYMENT_METHOD, URL)
    priceList = parseInfo(tradesData)
    priceListClean = cleanPrices(priceList)
    mean = calculateMean(priceListClean)
    #print(outputAsJSON(mean))
    return outputAsJSON(mean)


if __name__ == '__main__':
    main()
