# -*- mode: python -*-

appName = 'PyOne'
appScript = '../PyOne.py'
appIcon = './additionalFiles/appicon.ico'
appVersionInfo = './pyOneVersion.txt'
additionalFiles = './additionalFiles/*.*'
block_cipher = None

a = Analysis([appScript],
             pathex=['E:\\eclipse\\plugins\\org.python.pydev_5.8.0.201706061859\\pysrc\\pydev_sitecustomize', 
                     'F:\\PythonWorkspace\\our-py-lib\\PyOneApplication', 
                     'F:\\PythonWorkspace\\our-py-lib\\PyOneApplication\\src\\package',
                     'F:\\PythonWorkspace\\our-py-lib\\PyOneApplication\\src\\package\\additionalFiles',                     
                     'F:\\PythonWorkspace\\our-py-lib\\PyOneApplication\\src\\resources',                       
                     'F:\\PythonWorkspace\\our-py-lib\\PyOneApplication\\src\\interfaces', 
                     'F:\\PythonWorkspace\\our-py-lib\\PyOneApplication\\src\\core', 
                     'F:\\PythonWorkspace\\our-py-lib\\CommonLib\\src', 
                     'C:\\Python34\\DLLs', 
                     'C:\\Python34\\lib', 
                     'C:\\Python34',
                     'C:\\Python34\\lib\\site-packages', 
                     'C:\\Python34\\lib\\site-packages\\pip-8.1.2-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\youtube_dl-2016.12.1-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\defusedxml-0.5.0-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\wstools-0.4.5-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\six-1.10.0-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\setuptools-28.8.0-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\osa-0.2-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\lxml-3.7.3-py3.4-win32.egg', 
                     'C:\\Python34\\lib\\site-packages\\pysimplesoap-1.16-py3.4.egg',
                     'C:\\Python34\\lib\\site-packages\\zuora_client-1.0-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\httplib2-0.10.3-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\rinse-0.4.0-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\soap2py-1.16-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\xmljson-0.1.7-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\suds_py3-1.3.3.0-py3.4.egg', 
                     'C:\\Python34\\lib\\site-packages\\win32', 
                     'C:\\Python34\\lib\\site-packages\\win32\\lib', 
                     'C:\\Python34\\lib\\site-packages\\Pythonwin',
                     './temp', 
                     '.'],
             hiddenimports=['sip', 
                            'PyQt5', 
                            'PyQt5.Qsci', 
                            'bs4', 
                            'requests',
                            'json', 
                            'urllib3', 
                            'xmlutils', 
                            'xml', 
                            'logging', 
                            'sqlite3', 
                            'http', 
                            'osa', 
                            'pysimplesoap', 
                            'xmljson', 
                            'suds', 
                            'pusher', 
                            'Queue',
                            'queue',
                            'version',
                            'logging'],
             binaries=[],
             datas=[
                 (additionalFiles,'.')
                 ],             
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=appName,
          debug=False,
          strip=False,
          upx=True,
          icon=appIcon,
          version=appVersionInfo,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=appName)
