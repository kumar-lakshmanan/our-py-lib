def convertToRaw(text):
        """Returns a raw string representation of text"""
        escape_dict={'\a':r'\a',
                     '\b':r'\b',
                     '\c':r'\c',
                     '\f':r'\f',
                     '\n':r'\n',
                     '\r':r'\r',
                     '\t':r'\t',
                     '\v':r'\v',
                     '\'':r'\'',
                     '\"':r'\"'}
        new_string=''
        for char in text:
                try: 
                        new_string += escape_dict[char]
                except KeyError: 
                        new_string += char
        return new_string+'--ddsd'

import os
import codecs
#print(os.path.sep)
d=r"Scripts/plugs\umx.ui".encode('utf-8')
#d=d.encode('raw_unicode_escape')
#d="%r" % d
#d=os.path.normpath(d)
#d=convertToRaw(d).replace(os.path.sep,'/')
#print(d)
#print(os.path.exists(d))
