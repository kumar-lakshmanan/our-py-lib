import general
from bs4 import BeautifulSoup
import json
#For DevConsole

def currentExchangeRate():
        url = 'http://www.xe.com/currencyconverter/convert/?Amount=1&From=AUD&To=INR'
        data = general.readUrl(url)

        bs = BeautifulSoup(data,"html.parser")
        level1 = bs.findAll('td',{"class":"rightCol"})
        for each in level1:
                if(each.find('span',{"class":"uccResCde"})):
                        return each.contents[0].strip()
                        
def orbitExchangeRate():
        url = 'https://secure.orbitremit.com/api/rates/AUD:INR.json'
        data = general.readUrl(url)
        
        orbitSoup = BeautifulSoup(data,"html.parser")
        orbitVal = json.loads(orbitSoup.contents[0])
        orbitRate = orbitVal['exchangeRate']['Rate']['exchangeRate']
        return orbitRate       
        
def rafflesExchangeRate():
        url = 'https://rafflesforex.com.au/'
        data = general.readUrl(url)
        
        raffleSoup = BeautifulSoup(data,"html.parser")
        rafflesfinding = raffleSoup.findAll('h4',style='margin: 10px 0')
        rafflesRate = rafflesfinding[0].contents[0].split("=")[1].strip()
        return rafflesRate

def iciciExchangeRate():        
        url = 'http://www.icicibank.com/nri-banking/money_transfer/money-transfer-rates.page'
        data = general.readUrl(url)
        
        iciciSoup = BeautifulSoup(data,"html.parser")
        l1 = iciciSoup.find_all('div',class_="main-contentz")[0]
        for each in l1.tbody:
                nxt = each.next_sibling
                if nxt and str(nxt.next_element.next.extract()).strip()=='Australia':
                    return str(nxt.td.find_all_next()[0].contents[0].encode('ascii','ignore').decode('utf-8'))
                        
if __name__ == '__main__':
        #print (currentExchangeRate())        
        print (orbitExchangeRate())
        #print (rafflesExchangeRate())
        #print (iciciExchangeRate())