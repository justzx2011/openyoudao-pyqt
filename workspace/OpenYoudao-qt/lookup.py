# -*- coding:utf-8 -*-
'''
Created on Mar 5, 2013

@author: maxingchen
'''

from PyQt4 import QtCore
import os
import gl
import fusionyoudao
import fusionicb

class lookup(QtCore.QThread):
    signal=QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(lookup,self).__init__(parent)
        
    def run(self):
        pre_text = ""
        text = ""
        # 监视history.txt变化
        cmd = "tail -f " + gl.historydir 
        if(gl.baseurl == ""):
            gl.baseurl = gl.baseurlyoudao
        myfile = os.popen(cmd)
        while True:
            text = myfile.readline().strip('\r\n\x00')
            if (pre_text != text or gl.prebaseurl != gl.baseurl) and text != "" :  # 或者不一定对lzt
                pre_text = text
                print gl.lock
                gl.prebaseurl = gl.baseurl
                url = gl.baseurl + text  # 合成地址
                print url + "kkkkkkkkkkkk"  # 合成地址检测点1
                # 使用curl进行网页下载
                # 如果需要设置了代理取消"代理"行注释，并将"非代理"行注释掉
                os.system("curl -s -o \'" + gl.origindir + "\' \'" + url + "\'")  # 获得网页(非代理)
                # os.system("curl -s -o --socks5-hostname ip:port \'" + gl.origindir +"\' \'" + url+ "\'") #代理     
                # 使用python-requests进行网页下载,在debian中可以正常使用，考虑到其它系统的兼容性，改用curl
                # 如果需要设置了代理取消"代理"行注释，并将"非代理"行注释掉
                # 代理相关参数在gl.py中设置proxyDict变量
                # if gl.proxyDict =={}:
                #    r = requests.get(url)                            #获得网页(非代理)
                # else:
                #    r = requests.get(url, headers={'content-type':'text/plain'}, proxies=gl.proxyDict)  #（代理）
                # f_tar=open(gl.origindir,'w+')             #缓存原始网页
                # print >>f_tar,r.text
                # f_tar.close()
                # os.system("echo \'"+ gl.downloadwait + "\' > cache/result.html")         #清空最终缓冲增强程序稳健性
                
                if(gl.baseurl == gl.baseurlyoudao):
                    fusionyoudao.reconstruct()  # 区分聚合
                if(gl.baseurl == gl.baseurlicb):
                    fusionicb.reconstruct()
                
                
                gl.homeurl = "file://" + gl.resultdir  # 合成最终缓冲访问地址
#                self.window.load(gl.homeurl)  # 加载最终缓冲内容到浏览器
#                self.window.show()  # 显示结果
                self.signal.emit(gl.homeurl)
                gl.lock = 0