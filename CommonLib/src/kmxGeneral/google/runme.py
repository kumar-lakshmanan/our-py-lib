'''
Created on Aug 21, 2015

@author: MUKUND
'''

import os
print(os.getcwd())
# 
# flow = client.flow_from_clientsecrets(
#      'kmxserver.json',
#      scope='https://www.googleapis.com/auth/drive.metadata.readonly',
#      redirect_uri='http://www.example.com/oauth2callback')


# print(flow)

# import urllib.request
# 
# url = 'https://www.googleapis.com/tasks/v1/users/@me/lists?key=AIzaSyD3lRApddioETwBUe8CHk2GqTt1aeAWgo4'
# res = urllib.request.urlopen(url).read()
# print(res)



#service = build('api_name', 'api_version', ...)


import pywin32
 

rootDir = '..'

for each in os.listdir(rootDir):
    p = os.path.join(rootDir,each)
    if os.path.isdir(p):
        print(p)



