import unittest
import wx

import testGraphicsObject

"""
This file contains classes and methods for unit testing the API of
wx.GraphicsBrush.

TODO: The docs say the only valid way to make an instance
        is with a CreateBrush call on a renderer or context.
        The constructor works but produces null brushes.
        is this correct?

Methods yet to test:
__del__
"""

class GraphicsBrushTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.brush = wx.Brush(wx.Colour(0,0,0))
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.testControl = self.renderer.CreateBrush(self.brush)
    
    def testConstructor(self):
        """__init__"""
        brush = wx.GraphicsBrush()
        self.assert_(isinstance(brush, wx.GraphicsBrush))
    
    def testGetRenderer(self):
        """GetRenderer"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
        
    def testIsNullTrue(self):
        """IsNull"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.testControl = wx.GraphicsBrush()
        self.assert_(self.testControl.IsNull())
            
            
if __name__ == '__main__':
    unittest.main()