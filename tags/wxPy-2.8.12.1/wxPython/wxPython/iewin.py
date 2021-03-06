## This file reverse renames symbols in the wx package to give
## them their wx prefix again, for backwards compatibility.
##
## Generated by BuildRenamers in config.py

# This silly stuff here is so the wxPython.wx module doesn't conflict
# with the wx package.  We need to import modules from the wx package
# here, then we'll put the wxPython.wx entry back in sys.modules.
import sys
_wx = None
if sys.modules.has_key('wxPython.wx'):
    _wx = sys.modules['wxPython.wx']
    del sys.modules['wxPython.wx']

import wx.iewin

sys.modules['wxPython.wx'] = _wx
del sys, _wx


# Now assign all the reverse-renamed names:
wxMSHTMLEvent = wx.iewin.MSHTMLEvent
wxMSHTMLEventPtr = wx.iewin.MSHTMLEventPtr
wxEVT_COMMAND_MSHTML_BEFORENAVIGATE2 = wx.iewin.wxEVT_COMMAND_MSHTML_BEFORENAVIGATE2
wxEVT_COMMAND_MSHTML_NEWWINDOW2 = wx.iewin.wxEVT_COMMAND_MSHTML_NEWWINDOW2
wxEVT_COMMAND_MSHTML_DOCUMENTCOMPLETE = wx.iewin.wxEVT_COMMAND_MSHTML_DOCUMENTCOMPLETE
wxEVT_COMMAND_MSHTML_PROGRESSCHANGE = wx.iewin.wxEVT_COMMAND_MSHTML_PROGRESSCHANGE
wxEVT_COMMAND_MSHTML_STATUSTEXTCHANGE = wx.iewin.wxEVT_COMMAND_MSHTML_STATUSTEXTCHANGE
wxEVT_COMMAND_MSHTML_TITLECHANGE = wx.iewin.wxEVT_COMMAND_MSHTML_TITLECHANGE
wxIEHTML_REFRESH_NORMAL = wx.iewin.IEHTML_REFRESH_NORMAL
wxIEHTML_REFRESH_IFEXPIRED = wx.iewin.IEHTML_REFRESH_IFEXPIRED
wxIEHTML_REFRESH_CONTINUE = wx.iewin.IEHTML_REFRESH_CONTINUE
wxIEHTML_REFRESH_COMPLETELY = wx.iewin.IEHTML_REFRESH_COMPLETELY
wxIEHtmlWin = wx.iewin.IEHtmlWin
wxIEHtmlWinPtr = wx.iewin.IEHtmlWinPtr


d = globals()
for k, v in wx.iewin.__dict__.iteritems():
    if k.startswith('EVT'):
        d[k] = v
del d, k, v



