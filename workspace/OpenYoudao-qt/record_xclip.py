#!/usr/bin/python
# -*- coding: utf-8 -*-
# Simple demo for the RECORD extension
# Not very much unlike the xmacrorec2 program in the xmacro package


import sys
import os
import gl
# Change path so we find Xlib
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

record_dpy = display.Display()
pre_text = ""

def record_callback(reply):
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        print "* received swapped protocol data, cowardly ignored"
        return
    if not len(reply.data) or ord(reply.data[0]) < 2:
        # not an event
        return
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)

        # deal with the event type
        if event.type == X.ButtonRelease:
            # get text
            pipe = os.popen("xclip -o")
            text = pipe.readline()
            pipe.readlines()  # 清空管道剩余部分
            pipe.close()
            print "您抹黑的是: ", text
        
            text = text.strip('\r\n\x00')
            global pre_text
            if(pre_text != text):
                pre_text = text
                os.system("/bin/echo -e  \'" + text + "\' >> \'" + gl.historydir + "\'")    
            else:
                print "我不翻译"
            
                
# Check if the extension is present
if not record_dpy.has_extension("RECORD"):
    print "RECORD extension not found"
    sys.exit(1)
    r = record_dpy.record_get_version(0, 0)
    print "RECORD extension version %d.%d" % (r.major_version, r.minor_version)
    
# Create a recording context; we only want key and mouse events
ctx = record_dpy.record_create_context(
       0,
       [record.AllClients],
       [{
         'core_requests': (0, 0),
         'core_replies': (0, 0),
         'ext_requests': (0, 0, 0, 0),
         'ext_replies': (0, 0, 0, 0),
         'delivered_events': (0, 0),
         'device_events': (X.KeyPress, X.MotionNotify),
         'errors': (0, 0),
         'client_started': False,
         'client_died': False,
         }])

