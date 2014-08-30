#-------------------------------------------------------------------------------
# Name:        myFTPServer
#
# Author:      lkumaresan
#
# Created:     09/11/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#
#   My Simple FTP Server (Not CLIENT its SERVER) to server files. with user authentication.
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


from pyftpdlib import ftpserver
auth = ftpserver.DummyAuthorizer()
auth.add_user('user1', 'root', '/', perm='elradfmw')
hdl = ftpserver.FTPHandler
hdl.authorizer = auth
address = ('192.168.1.2',21)
ftpd = ftpserver.FTPServer(address,hdl)
ftpd.serve_forever()