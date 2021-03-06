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

import wx.media

sys.modules['wxPython.wx'] = _wx
del sys, _wx


# Now assign all the reverse-renamed names:
wxMEDIASTATE_STOPPED = wx.media.MEDIASTATE_STOPPED
wxMEDIASTATE_PAUSED = wx.media.MEDIASTATE_PAUSED
wxMEDIASTATE_PLAYING = wx.media.MEDIASTATE_PLAYING
wxMEDIACTRLPLAYERCONTROLS_NONE = wx.media.MEDIACTRLPLAYERCONTROLS_NONE
wxMEDIACTRLPLAYERCONTROLS_STEP = wx.media.MEDIACTRLPLAYERCONTROLS_STEP
wxMEDIACTRLPLAYERCONTROLS_VOLUME = wx.media.MEDIACTRLPLAYERCONTROLS_VOLUME
wxMEDIACTRLPLAYERCONTROLS_DEFAULT = wx.media.MEDIACTRLPLAYERCONTROLS_DEFAULT
wxMEDIABACKEND_DIRECTSHOW = wx.media.MEDIABACKEND_DIRECTSHOW
wxMEDIABACKEND_MCI = wx.media.MEDIABACKEND_MCI
wxMEDIABACKEND_QUICKTIME = wx.media.MEDIABACKEND_QUICKTIME
wxMEDIABACKEND_GSTREAMER = wx.media.MEDIABACKEND_GSTREAMER
wxMediaEvent = wx.media.MediaEvent
wxMediaEventPtr = wx.media.MediaEventPtr
wxMediaCtrlNameStr = wx.media.MediaCtrlNameStr
wxMediaCtrl = wx.media.MediaCtrl
wxMediaCtrlPtr = wx.media.MediaCtrlPtr
wxPreMediaCtrl = wx.media.PreMediaCtrl
wxEVT_MEDIA_FINISHED = wx.media.wxEVT_MEDIA_FINISHED
wxEVT_MEDIA_STOP = wx.media.wxEVT_MEDIA_STOP
wxEVT_MEDIA_LOADED = wx.media.wxEVT_MEDIA_LOADED


