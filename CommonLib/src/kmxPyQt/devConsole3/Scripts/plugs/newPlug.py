'''
#For DevConsole
'''

class NewplugCls():
    
    def __init__(self):
        print("NewplugCls is ready!")
        
    def doThisActivity(self):
        print("Ready to do this activity")        

if __name__ == '__main__':
    parent.NewplugClsObj = NewplugCls()
    parent.NewplugClsObj.doThisActivity()
