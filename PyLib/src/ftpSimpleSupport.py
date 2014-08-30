import ftplib
import sys, os

class simpleFtp():


    def __init__(self,host='r117',uid='cgapps',password='thepulse'):
        """
        Create a FTP Instance.Besure to Close it when you complete your operations

        Eg 1:

            ftpsrcfile = 'd:/sim/RIG_TNNL_TINKXX.ma'
            ftpdestifile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'

            myFtp = ftpSimpleSupport.simpleFtp('r117')
            myFtp.sfSendFile(ftpsrcfile,ftpdestifile)
            myFtp.sfQuit()

        Eg 2:

            ftpsrcfile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'
            ftpdestifile = 'd:/sim/RIG_TNNL_TINKXX.ma'

            myFtp = ftpSimpleSupport.simpleFtp()
            myFtp.sfGetFile(ftpsrcfile,ftpdestifile)
            myFtp.sfQuit()

        """

        self.ftpInstance = ftplib.FTP()
        self.ftpInstance.connect(host)
        self.ftpInstance.login(uid,password)


    def sfCreateFolder(self, path):
        '''
        Create Folder

        Eg:

        ftpdesti = '/ROOT/EXISITING/FOLDER/NEWFOLDER'

        myFtp = ftpSimpleSupport.simpleFtp('r117')
        myFtp.sfCreateFolder(ftpdesti)
        myFtp.sfQuit()

        '''
        try:
            np = self.ftpInstance.mkd(path) ;
            return 'Folder Created'
        except ftplib.error_perm:
            return "Folder Create Failed"


    def sfCreateFolders(self,path):
        '''
        Create Folders

        Eg:

        ftpdesti = '/ROOT/NEWFOLDER/NEWFOLDER/NEWFOLDER'

        myFtp = ftpSimpleSupport.simpleFtp('r117')
        myFtp.sfCreateFolders(ftpdesti)
        myFtp.sfQuit()

        '''
        try:
            pParts = path.split('/')
            pth = ''
            created = 0
            for i in range(1, len(pParts)):
                pth += '/'+pParts[i]
                self.sfCreateFolder(pth)
                created = 1
            if created:
                return 'Folders Created'
            else:
                return 'No Folders Created. Path might already exist.'
        except ftplib.error_perm:
            return "Folders Create Failed"


    def sfFileSend(self,srcpath,destpath):
        """
        Send a local file to server

        Eg:

        ftpsrcfile = 'd:/sim/RIG_TNNL_TINKXX.ma'
        ftpdestifile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'

        myFtp = ftpSimpleSupport.simpleFtp('r117')
        myFtp.sfSendFile(ftpsrcfile,ftpdestifile)
        myFtp.sfQuit()

        """
        try:
            sfile = open(srcpath,'rb') ;
        except IOError:
            return "Could not open source file"

        try:
            np = self.ftpInstance.storbinary("STOR "+destpath,sfile);
            sfile.close() ;
            return np
        except ftplib.error_perm:
            sfile.close() ;
            return "Could not send file"


    def sfFileGet(self,srcpath,destpath):
        """
        Get a server file to local

        Eg:

        ftpsrcfile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'
        ftpdestifile = 'd:/sim/RIG_TNNL_TINKXX.ma'

        myFtp = ftpSimpleSupport.simpleFtp('r117')
        myFtp.sfGetFile(ftpsrcfile,ftpdestifile)
        myFtp.sfQuit()

        """

        try:
            sfile = open(destpath,'wb') ;
        except IOError:
            return "Could not open destination file"
        try:
            np = self.ftpInstance.retrbinary("RETR "+srcpath,sfile.write);
            sfile.close() ;
            return np
        except ftplib.error_perm:
            sfile.close();
            return "Could not send file"


    def sfFileRename(oldpath, newpath):
        """
           Description: The function renames an existing File to a new file

            Eg:
                serverOldFile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINK.ma'
                serverNewFile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'

                myFtp = ftpSimpleSupport.simpleFtp('r117')
                myFtp.sfRenameFile(serverOldFile,serverNewFile)
                myFtp.sfQuit()

        """

        try:
            np = self.ftpInstance.rename(oldpath,newpath) ;
            return "Renamed!";
        except ftplib.error_perm:
            return "Renaming file failed"



    def sfFileDelete(serverFile) :
        """

            Description: The function test if a file exists on the server

            Eg:
                serverFile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'

                myFtp = ftpSimpleSupport.simpleFtp('r117')
                result = myFtp.sfDeleteFile(serverFile)
                myFtp.sfQuit()

        """
        try:
            np = ftp.delete(serverFile) ;
            return np
        except ftplib.error_perm:
            return "Deleting file failed"


    def sfIsFileExist(self,serverFile,SearchHidden=False):
        """

            Description: The function test if a file exists on the server

            Eg:
                serverFile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'

                myFtp = ftpSimpleSupport.simpleFtp('r117')
                result = myFtp.sfIsFileExist(serverFile)
                myFtp.sfQuit()

                if result == 1:
                    print "File Exist!"

                if result == 0:
                    print "File Does Not Exist!"

        """

        parentDir = os.path.dirname(serverFile);
        fileList = self.sfListDir(parentDir,SearchHidden);
        if serverFile in fileList:
            return 1;
        else:
            return 0;

##
##    def sfIsFolderExist(self,serverFile,SearchHidden=False):
##        """
##
##            Description: The function test if a file exists on the server
##
##            Eg:
##                serverFile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG/RIG_TNNL_TINKXX.ma'
##
##                myFtp = ftpSimpleSupport.simpleFtp('r117')
##                result = myFtp.sfIsFileExist(serverFile)
##                myFtp.sfQuit()
##
##                if result == 1:
##                    print "File Exist!"
##
##                if result == 0:
##                    print "File Does Not Exist!"
##
##        """
##
##        fileList = self.sfListDir(serverFile,SearchHidden);
##        if serverFile in fileList:
##            return 1;
##        else:
##            return 0;
##

    def sfListDir(self, serverFilePath='', Hidden=False, DefaultRoot='/'):
        """
            Description: The function list all the files present inside the given serverFilePath

            Eg:
                serverFile = '/PROJECTS/WORK/TNNL/CHARACTERS/TINKXX/RIG'

                myFtp = ftpSimpleSupport.simpleFtp('r117')
                fileList = myFtp.sfListDir(serverFile)
                myFtp.sfQuit()

                print fileList

        """

        if (Hidden):
            if serverFilePath == '': serverFilePath = DefaultRoot
            alllist = self.ftpInstance.nlst("-a "+serverFilePath)
            return alllist
        else:
            if (serverFilePath == ''): serverFilePath = DefaultRoot
            alllist = self.ftpInstance.nlst(serverFilePath)
            return alllist;


    def sfQuit(self):
        try:
            self.ftpInstance.quit()
        except:
            print 'Problem on closing FTP'

    def unitTest(self):
        print self.sfListDir('/home/aswamy/PROJECTS/T2L')
        print self.sfCreateFolders('/home/aswamy/PROJECTS/zzdef/zz')
        print self.sfIsFileExist('/home/aswamy/PROJECTS/zzdef/zz')

if __name__ == '__main__':
    f = simpleFtp('192.168.28.42','aswamy','swamy123')
    f.unitTest()
    f.sfQuit()


