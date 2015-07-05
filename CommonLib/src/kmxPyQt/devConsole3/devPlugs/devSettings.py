#For DevConsole

def devSettings(parent):
        print("--------------------------")
        print("Modifying Dev Environment Dynamically")
        print("--------------------------")
        
        print("Refreshing Tools!")
        parent.treeWidget.clear()
        parent.execPlugin()

        print("--------------------------")
        print("Dev Modification Completed!")        
        print("--------------------------")
