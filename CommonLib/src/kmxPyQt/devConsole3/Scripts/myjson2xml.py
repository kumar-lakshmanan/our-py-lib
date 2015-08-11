#json to xml

import dict2xml
d = {"exchangeRate":{"SendCurrency":{"countryCode":"au","currencyName":"Australian Dollar","currencyCode":"AUD"},"PayoutCurrency":{"countryCode":"in","currencyName":"Indian Rupee","currencyCode":"INR"},"Rate":{"exchangeRate":"46.4806"}}}
print('\nJSON:\n' + str(d))
x = dict2xml.dict2xml(d)
print ('\nXML:\n'+str(x))


# 
# JSON:
# {'exchangeRate': {'PayoutCurrency': {'currencyCode': 'INR', 'countryCode': 'in', 'currencyName': 'Indian Rupee'}, 'Rate': {'exchangeRate': '46.4806'}, 'SendCurrency': {'currencyCode': 'AUD', 'countryCode': 'au', 'currencyName': 'Australian Dollar'}}}
# 
# XML:
# <exchangeRate>
#   <PayoutCurrency>
#     <countryCode>in</countryCode>
#     <currencyCode>INR</currencyCode>
#     <currencyName>Indian Rupee</currencyName>
#   </PayoutCurrency>
#   <Rate>
#     <exchangeRate>46.4806</exchangeRate>
#   </Rate>
#   <SendCurrency>
#     <countryCode>au</countryCode>
#     <currencyCode>AUD</currencyCode>
#     <currencyName>Australian Dollar</currencyName>
#   </SendCurrency>
# </exchangeRate>