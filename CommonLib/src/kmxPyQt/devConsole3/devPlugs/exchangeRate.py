import requests
from bs4 import BeautifulSoup
import json

def exchangeRate(parent=None):
    
    amount=500
    
    iciciRate=0
    rafflesRate=0
    orbitRate=0
    
    website = 'https://rafflesforex.com.au/'
    raffleSoup = BeautifulSoup(requests.get(website).text,"html.parser")
    rafflesfinding = raffleSoup.findAll('h4',style='margin: 10px 0')
    rafflesRate = rafflesfinding[0].contents[0].split("=")[1].strip()
         
    website = 'https://secure.orbitremit.com/api/rates/AUD:INR.json'
    orbitSoup = BeautifulSoup(requests.get(website).text,"html.parser")
    orbitVal = json.loads(orbitSoup.contents[0])
    orbitRate = orbitVal['exchangeRate']['Rate']['exchangeRate']    
    
    website = 'http://www.icicibank.com/nri-banking/money_transfer/money-transfer-rates.page'
    iciciSoup = BeautifulSoup(requests.get(website).text,"html.parser")
    l1 = iciciSoup.find_all('div',class_="main-contentz")[0]
    for each in l1.tbody:
        nxt = each.next_sibling
        if nxt and str(nxt.next_element.next.extract()).strip()=='Australia':
            iciciRate = str(nxt.td.find_all_next()[0].contents[0].encode('UTF-8').decode('unicode_escape').encode('ascii','ignore').decode('utf-8'))
            break;
        
        
    xr = float(rafflesRate)
    xo = float(orbitRate)
    xi = float(iciciRate)
    
    raffles = (amount * xr) - (6 * xr)
    orbit = (amount * xo) - (4 * xo)
    icici =  (amount * xi) - (50)

    print('\n')
    print("Exchange Rate Raffles: " + str(xr))
    print("Exchange Rate Orbit: " + str(xo))
    print("Exchange Rate ICICI: " + str(xi))    
    print('\n')
    print("For 500AUD Raffles: " + str(raffles))
    print("For 500AUD Orbit: " + str(orbit))
    print("For 500AUD ICICI: " + str(icici))    
    print('\n')
    
    
# Exchange Rate Raffles: 46.4
# Exchange Rate Orbit: 46.2337
# Exchange Rate ICICI: 45.81
    
    
exchangeRate()    