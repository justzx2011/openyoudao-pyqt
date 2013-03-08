#! /usr/bin/env python
'''
Created on Mar 5, 2013

@author: maxingchen
'''
from PyQt4 import QtWebKit
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

import lookup
import inputconfig
import gettext
import gl

class Window(QtGui.QWidget):
    def __init__(self,parent=None): 
        super(Window,self).__init__(parent)
        
        self.setGeometry(600,600,250,250)
        self.setWindowTitle('Open Youdao')
        
        bl=QtGui.QHBoxLayout()
        self.webView=QtWebKit.QWebView()
        bl.addWidget(self.webView)
        
        self.setLayout(bl)
        
        
        self.gettextThread=gettext.gettext(self)
        self.gettextThread.start()
        
        self.lookupThread=lookup.lookup(self)
        self.lookupThread.signal.connect(self.slot)
        self.lookupThread.start()
        
        self.inputconfigThread=inputconfig.inputConfig(self)
        self.inputconfigThread.start()
        
        
    def load(self, address):
        url=QtCore.QUrl(address)
        self.webView.load(url)
        
    def reload(self):
        self.webView.reload()
    
    def slot(self,address):
        self.webView.load(QtCore.QUrl(address))
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.gettextThread.exit()
            self.lookupThread.exit()
            self.inputconfigThread.exit()
            event.accept()
        else:
            event.ignore()
        
def main():
    app=QtGui.QApplication(sys.argv)
    window=Window()
    window.load(gl.homeurl)
    window.show()
    
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()