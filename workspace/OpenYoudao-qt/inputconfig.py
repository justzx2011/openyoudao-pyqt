# -*- coding:utf-8 -*-
'''
Created on Mar 5, 2013

@author: maxingchen
'''

from PyQt4 import QtCore
import os
import sqlite3
from time import sleep
import gl

class inputConfig(QtCore.QThread):
    def __init__(self,parent=None):
        super(inputConfig,self).__init__(parent)
        
    def run(self):
        print 'inputConfig starts'
        while True :
            gl.prebaseurl = gl.baseurl
            conn = sqlite3.connect(gl.datadir)
            c = conn.cursor()
            c1 = conn.cursor()
            c.execute("select value from ItemTable where key = 'dict' ")
            c1.execute("select value from ItemTable where key = 'keyword' ")
            r = c.fetchone()
            r1 = c1.fetchone()
            print str(r[0]).split('\x00')
            gl.baseurl = "".join(str(r[0]).split('\x00'))  # str to string
            if(gl.prebaseurl != gl.baseurl):
                stext = "".join(str(r1[0]).split('\x00')) 
                c.close()
                c1.close()
                conn.close()
                print stext
                os.system("/bin/echo -e  \'" + stext + "\' >> \'" + gl.historydir + "\'")
            sleep(1)
        
        