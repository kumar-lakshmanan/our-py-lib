#For DevConsole

class myApplicationModule():
        
        def __init__(self):
                print("Initialized!")
                
        def doProcessing(self, input):
                result = 0
                
                operation = input['operation']
                val1 = int(input['val1'])
                val2 = int(input['val2'])
                
                print("Operation Requested: " + operation)
                print("Value1: " + str(val1))
                print("Value2: " + str(val2))
                
                if(operation=='add'):
                        result = val1+val2
                elif(operation=='sub'):
                        result = val1-val2
                elif(operation=='mul'):
                        result = val1*val2

                print("Operation Completed: " + str(result))                        
                return str(result)
                        