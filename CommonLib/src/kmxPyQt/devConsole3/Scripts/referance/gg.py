

def updateFile(rafs,orb,ici):
        f = open("exchange.csv","a")
        nw = dev.ttls.getDateTime()
        data = '"{0}","{1}","{2}","{3}"\n'.format(nw,rafs,orb,ici)
        f.write(data)
        f.close()
        
updateFile(1,2,3)        