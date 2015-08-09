import xmlrpc.client
server = xmlrpc.client.Server("http://counterbolt.com/php/cbxmlrpc/sys_server.php")
#result = server.RemoteCalls.rpiIPUpdate(("public","PYTHON123","PythonTest"))
result1 = server.RemoteCalls.listMethods()
result = server.RemoteCalls.runPython('/home/kmatrix/public_html/python/myscript.py')
print(result1)
print(result)
print('done')