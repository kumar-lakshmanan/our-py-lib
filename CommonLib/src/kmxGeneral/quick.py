'''
Created on Jul 19, 2015

@author: MUKUND
'''
#import urllib2
import requests
from bs4 import BeautifulSoup
import json
import urllib3



if __name__ == '__main__':

    import py_compile
    py_compile.compile('C:/Python34/Lib/site-packages/dropbox/rest.py')

#     website = 'https://rafflesforex.com.au/'
#     raffleSoup = BeautifulSoup(requests.get(website).text,"html.parser")
#     rafflesfinding = raffleSoup.findAll('h4',style='margin: 10px 0')
#     rafflesRate = rafflesfinding[0].contents[0].split("=")[1].strip()
#         
#     website = 'https://secure.orbitremit.com/api/rates/AUD:INR.json'
#     orbitSoup = BeautifulSoup(requests.get(website).text,"html.parser")
#     orbitVal = json.loads(orbitSoup.contents[0])
#     orbitRate = orbitVal['exchangeRate']['Rate']['exchangeRate']
# 
#     from bs4 import NavigableString
#     website = 'http://www.icicibank.com/nri-banking/money_transfer/money-transfer-rates.page'
#     iciciSoup = BeautifulSoup(requests.get(website).text,"html.parser")
#     l1 = iciciSoup.find_all('div',class_="main-contentz")[0]
#     #l2 = l1.prettify().encode('UTF-8')
#     l3 = l1.find_all('div',class_="table-container")[0]
#     l4 = l1.tbody
#     for each in l4:
#         #print(each.next_sibling.next_element.encode('UTF-8'))
#         #print(each.next_sibling.next_element.next.name)
#         nxt = each.next_sibling
#         if nxt and str(nxt.next_element.next.extract()).strip()=='Australia':
#             print(nxt.encode('UTF-8'))
#             #print(nxt.find_all_next().encode('UTF-8'))
#             print(len(nxt.find_all_next()))
#             print(nxt.td.find_all_next()[0].encode('UTF-8'))
#             print(nxt.td.find_all_next()[0].contents[0].encode('UTF-8').decode('unicode_escape').encode('ascii','ignore'))
            #print ("dd")
#         for e in dir(each):
#             print(e)
        #print(type(each))
        #print (each.encode('UTF-8'))
    #print(l4.prettify().encode('UTF-8'))
    
    #print(l1.prettify().encode('UTF-8'))
    
        
#     print("Raffles: " + rafflesRate)
#     print("Orbit: " + orbitRate)
    
    
    
    
    #//*[@id="latest-rates"]/div[1]/ul[1]/li[6]/div[1]/span
#-----------------------    
    
    
    
#     
#     
#     aud = 600
#     raffles = 46.25
#     money2india = 46.04
#     orbitremit = 46.2752 
#     rafflesRes = (aud * raffles) - (6 * raffles)
#     money2indiaRes = (aud * money2india) - 50
#     orbitremitRes = (aud * orbitremit) - (4 * orbitremit)
#     print ("Raffles: " + str(rafflesRes))
#     print ("Money2India: " + str(money2indiaRes))
#     print ("Orbit: " + str(orbitremitRes))  
#     
#     if rafflesRes>money2indiaRes:
#         if rafflesRes>orbitremitRes:
#             print ("Raffles wins!")
#         else:
#             print ("Orbit wins!")
#     else:
#         if money2indiaRes>orbitremitRes:
#             print ("Money2India wins!")
#         else:
#             print ("Orbit wins!")
#         
#         
#-------------------------------------------------------

# or if you're using BeautifulSoup4:
# from bs4 import BeautifulSoup

    print("test")