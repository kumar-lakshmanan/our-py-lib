from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#For DevConsole
import sqlite3
import os
import mysqlite
import sip

class SqliteCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.parent=parent   
		self.settings=self.parent.settings		
		self.uiFile=mysqlite.__file__.replace(".py",".ui")
		super(SqliteCls, self).__init__(self.parent)		
		loadUi(self.uiFile, self)
		
		self.textBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

		self.font = self.textBrowser.font()
		self.font.setFamily("Courier")
		self.font.setPointSize(10)

		self.conn = sqlite3.connect(self.settings.devConsDB)		
		self.conn.isolation_level = None
		self.cur = self.conn.cursor()	  
		self.doExecute("select * from sqlite_master WHERE type='table';")
		#insert intro stocks values ('2006-01-05','BUY','RHAT',100,35.14);
		#select * from stocks;
	
	def doUpdate(self, data):
		self.textBrowser.moveCursor(QtGui.QTextCursor.End)
		self.textBrowser.setCurrentFont(self.font)
		self.textBrowser.insertPlainText(str(data)+'\n')
		sb = self.textBrowser.verticalScrollBar()
		sb.setValue(sb.maximum())

	def doRun(self):		
		data = self.lineEdit.text()
		if sqlite3.complete_statement(data):   
			self.doExecute(data)
			self.lineEdit.setText('')

	def doInsert(self, table, values):
		qry="insert into " + table + " values " + str(values) + ";";
		print(qry)
		self.doExecute(qry)
		
	def doExecute(self, data):
		self.doUpdate(">>> "+data)
		if sqlite3.complete_statement(data):			 
			try:
				data = data.strip()
				self.cur.execute(data)
				if data.lstrip().upper().startswith("SELECT"):
					self.doUpdate(self.cur.fetchall())
			except sqlite3.Error as e:
				self.doUpdate("An error occurred:"+str(e.args[0]))

if (__name__=="__main__"):
	if(not hasattr(dev,'SqliteClsObj') or sip.isdeleted(dev.SqliteClsObj)):
		dev.SqliteClsObj = SqliteCls(dev)
	dev.SqliteClsObj.show()
	print("TEST")
	dev.SqliteClsObj.raise_()