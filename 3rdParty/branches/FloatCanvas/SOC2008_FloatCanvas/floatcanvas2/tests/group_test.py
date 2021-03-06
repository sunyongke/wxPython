''' Tests 'Group' nodes. '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc


def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.FloatCanvas( window = frame,  backgroundColor = 'white' )
    #canvas.dirty = False

    parent = canvas.create( 'Group', name = 'group node', pos = (100, 0) )
    # create 1000 rectangles
    for i in range(0, 100):
        r = canvas.create( 'Rectangle',
                           (100, 100),
                           parent = parent,
                           name = 'r%d' % i,
                           pos = (i * 50, 0),
                           look = fc.SolidColourLook( line_colour = 'blue',
                                                      fill_colour = 'red' )
                           )
        #r._debugDrawBoundingBoxes = True

    # the default cam, looking at 0, 0
    canvas.camera.position = (0, 0)
    canvas.camera.zoom = (1.0, 1.0)
    
    def print_culled_nodes():
        try:
            print 'rendered %d nodes' % ( len(canvas.renderPolicy.renderedNodes), )
            #print r.boundingBox
            #for node in canvas.renderPolicy.renderedNodes:
            #    print node.name
        except AttributeError:
            pass
    
    rotate = True
    if rotate:
        import time
        for i in range(0, 361):
            parent.rotation = i
            canvas.Render()
            wx.Yield()
            print_culled_nodes()
            #time.sleep(0.01)
        
    wx.CallLater( 1000, print_culled_nodes )
    
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
