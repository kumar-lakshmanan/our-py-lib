'''
Created on Oct 24, 2015

@author: MUKUND
'''
import sys

class cryption(object):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        self.parent = parent

    def isCryptionDefault(self):
        return not len(sys.argv)>1 
        
    def encrypt(self, text):
            code = int(sys.argv[1] if(len(sys.argv)>1) else 4132)
            cipher=''
            for each in text:
                    c = (ord(each)+code) % 126
                    if c < 32: 
                            c+=31
                    cipher += chr(c)
            return cipher
    
    def decrypt(self, text):
            code = int(sys.argv[1] if(len(sys.argv)>1) else 4132)
            plaintext=''
            for each in text:
                    p = (ord(each)-code) % 126    
                    if p < 32:
                            p+=95
                    plaintext += chr(p)
            return plaintext         