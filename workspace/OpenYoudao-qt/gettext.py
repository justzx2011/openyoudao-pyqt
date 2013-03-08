# -*- coding:utf-8 -*-
'''
Created on Mar 5, 2013

@author: maxingchen
'''

from PyQt4 import QtCore
import os
import record_xclip
import gl

class gettext(QtCore.QThread):
    signal=QtCore.pyqtSignal(int)
    
    def __init__(self,parent=None):
        super(gettext,self).__init__(parent)
        
    def run(self):
        # clear the clipboard
        print 'hello'
        os.system("xclip -f /dev/null")  
        if os.path.exists(gl.historydir):  
            os.system("/bin/echo "" > \'" + gl.historydir + "\'")
        else:
            os.system("mkdir  \'" + gl.cachedir + "\'") 
            os.system("mkdir  \'" + gl.subcachedir + "\'") 
            os.system("touch  \'" + gl.cachedirhistory + "\'") 
            os.system("touch  \'" + gl.cachedirorigin + "\'") 
            os.system("touch  \'" + gl.cachedirresult + "\'") 
            os.system("/bin/echo "" > \'" + gl.historydir + "\'")
                
        record_xclip.record_dpy.record_enable_context(record_xclip.ctx, record_xclip.record_callback)            
        record_xclip.record_dpy.record_free_context(record_xclip.ctx)
        self.signal.emit()