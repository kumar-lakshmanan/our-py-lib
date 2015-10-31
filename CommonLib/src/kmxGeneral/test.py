'''
Created on Oct 31, 2015

@author: MUKUND
'''
import getpass

if __name__ == '__main__':
    k = '4.0.0.0'
    d = k.split('.')
    print(int(d[0])+1)
    print(getpass.getuser())