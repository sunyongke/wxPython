import unittest
import wx

import testDialog

"""
This file contains classes and methods for unit testing the API of
wx.FontDialog.

All methods under test.
"""

class FontDialogTest(testDialog.DialogTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(None)
        self.font_data = wx.FontData()
        self.testControl = wx.FontDialog(self.frame, self.font_data)
    
    def testTitle(self):
        """ """
        # wx.FontDialog has different parameter list than wx.TopLevelWindow
        # TODO: assert that calling the constructor with 'title' fails
        pass
    
    def testFontData(self):
        """GetFontData"""
        self.assert_(self.font_data.IsSameAs(self.testControl.GetFontData()))
        
        
if __name__ == '__main__':
    unittest.main()