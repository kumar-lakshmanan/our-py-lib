import currencyRates
#For DevConsole

def showHistory():        
        f = open("exchange.csv","r")
        lines = f.readlines()
        for eachLine in lines:
                print(eachLine)
        f.close()
        
def updateFile(rafs,orb,ici,cr):
        f = open("exchange.csv","a")
        nw = parent.ttls.getDateTime()
        data = '"{0}","{1}","{2}","{3}","{4}"\n'.format(nw,rafs,orb,ici,cr)
        f.write(data)
        f.close()
        
def exchangeRate(parent=None):
    
    amount=500
    
    iciciRate=currencyRates.iciciExchangeRate()
    rafflesRate=currencyRates.rafflesExchangeRate()
    orbitRate=currencyRates.orbitExchangeRate()
    currentRate=currencyRates.currentExchangeRate()

    xr = float(rafflesRate)
    xo = float(orbitRate)
    xi = float(iciciRate)
    cr = float(currentRate)
    
    raffles = (amount * xr) - (6 * xr)
    orbit = (amount * xo) - (4 * xo)
    icici =  (amount * xi) - (50)

    print('\n')
    print("Current Exchange Rate: " + str(currentRate))
    print("Exchange Rate Raffles: " + str(xr))
    print("Exchange Rate Orbit: " + str(xo))
    print("Exchange Rate ICICI: " + str(xi))    
    print('\n')
    print("For 500 AUD Raffles: " + str(raffles))
    print("For 500 AUD Orbit: " + str(orbit))
    print("For 500 AUD ICICI: " + str(icici))    
    print('\n')
    
    updateFile(xr,xo,xi,cr)

if __name__ == '__main__':
        exchangeRate()    
        #showHistory()