winTitle = dev.parent.windowTitle()
newWinTile = winTitle + " Scripted!"
dev.win.setWindowTitle('PyInter')
dev.parent.setWindowTitle(newWinTile)

from devPlugs import nodes
dev.parent.parent.parseModulesCore(nodes)
