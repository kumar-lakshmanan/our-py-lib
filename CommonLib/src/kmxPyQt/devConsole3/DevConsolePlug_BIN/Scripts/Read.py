from qneport import QNEPort
for each in widget.scene.items():
    #print(str(type(each)))
	if (str(type(each))=="<class 'qneblock.QNEBlock'>"):
		print("\nBlock: "+str(each))
		for port in each.ports():
			print("-------"+str(port.name))
			for connection in port.connections():
				print(">>>>>>>>"+str(connection.port1()))
				print(">>>>>>>>"+str(connection.port2()))