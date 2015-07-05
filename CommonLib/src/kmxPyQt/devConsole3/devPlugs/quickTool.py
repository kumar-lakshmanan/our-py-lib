#For DevConsole
import kmxNodeGraphTester
import imp
imp.reload(kmxNodeGraphTester)

def quickTool(parent):
        print("Quick tool executed!")
        parent.treeWidget.clear()
        parent.execPlugin()
        
        parent.tester = kmxNodeGraphTester.TesterWindow(None)
        parent.tester.show()