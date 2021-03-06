import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import wx
import floatcanvas2 as fc

# FlowerBed example
#
# situation: We are a company producing plastic flowers.
#            Our designers want a tool to visualize and design the flowers
#            and place them on a flower bed for illustrative purposed.
#            In the end our database should hold the necessary production
#            parameters needed to produce the flowers.
#            The visualization consists of two layers. The front one shows all
#            the labels with flower names, the back one is the actual flower
#            layer. For the sake of using a lot of features in this example
#            it will be drawn to a bitmap.
#
# not covered:
#
# - view serialization
# - single object on multiple canvasses
# - svg
# - bitmaps
# - animation
# - groups (although a layer can be conceived a group)
#

class FlowerBedModel(fc.models.DefaultModelEventSender):
    #implements(fc.models.IRectangle)
    def __init__(self, name):
        self.name = name
        self.color = 'brown'
        self.flowers = []
        self.size = (100, 100)


class FlowerModel(fc.models.DefaultModelEventSender):
    def __init__(self, name, no_blades = 5, blade_colour = 'red', size = 10):
        self.name = name
        self.no_blades = no_blades
        self.blade_colour = blade_colour
        self.size = size


class SimpleFlowerView(object):
    # can_view( FlowerModel )
    def Render(self, renderer, model):
        no_blades = model.no_blades
        size = model.size
        
        # draw the center part and dynamically generate and apply the look
        look = fc.look.DefaultLook( line_colour = 'black', fill_colour = model.blade_colour )
        look.Apply( renderer )
        renderer.DrawCircle( (0,0), size )
        # draw a line per blade
        for blade in range(no_blades):
            x, y = sin(no_blades / blade * 2 * PI) * size, cos(no_blades / blade * 2 * PI) * size
            renderer.DrawLine( (0,0), (x,y) )

    def GetBoundingBox(self, model):
        return (model.size, model.size)


def loadFlowerbedModel():
    ''' stub for a flowerbed loading function. should really get data from
         a database '''
    bed = FlowerBedModel( 'Example bed' )

    # add some flowers
    flowers = [ FlowerModel( 'Tulip', 3 ),
                FlowerModel( 'Rose', 4, size = 20 ),
                FlowerModel( 'Sunflower', 10, 'yellow' ),
                FlowerModel( 'BoringDefault' )
              ]
    bed.flowers = flowers

    return bed

def createViewFromModel(flowerBed, canvas):
    flowerLayer = fc.node.Node()              # this draws all its children into a bitmap, caches it and uses it for subsequent drawing, not sure if it should really be a node
    labelLayer = fc.node.Node()

    canvas.addChild( flowerLayer, where = 0 )
    canvas.addChild( labelLayer, where = 'front' )
    
    genericFlowerRenderer = SimpleFlowerView()
    #labelRenderer = fc.defaultRenderers.ScaledTextRenderer()
    #labelLook = fc.TextLook( base_size = 10, fill_colour = 'black' )

    # create flowers and their labels and a row
    for i, flowerData in enumerate(flowerBed.flowers):
        pos_x, pos_y = i % 5, i // 5    # put 5 flowers in a row
        pos_x *= 25
        pos_y *= 25
        
        flowerNode = fc.RenderableNode( flowerData, genericFlowerRenderer, fc.NoLook )          # use fc.NoLook since the flower renderer sets its own one
        flowerNode.transformer.translation = (pos_x, pos_y)                                     # the default transformer simply applies a 3x2 matrix
        labelLayer.addChild(flowerNode)

        labelNode = fc.RenderableNode( flowerData.name, labelRenderer, labelLook )
        labelNode.transformer.translation = (pos_x, pos_y + 15)                                   # put label a bit below the flower
        flowerLayer.addChild( labelNode )

    bed = fc.Rectangle( flowerBed )
    bed.enable = True       # just show the attribute, not strictly needed here
    flowerLayer.addChild( bed, where = fc.BACK )

    
    def customTransformer(node, coordinates):
        ''' square the coordinates for lack of imagniation of something more sensible '''
        return coordinates.x ** 2, coordinates.y ** 2
        
    bed.transformer = customTransformer

    def onClickFlower1(node, evt):
        node.data.size *= 2                                                   # change the data which will in turn change the view

    flower1 = flowerLayer.getChildren()[0]
    flower1.events.Bind( fc.events.LEFT_CLICK )                               # is flower1.Bind better here instead

    return flower1



def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        
    renderer = fc.gcrenderer.GCRenderer( window = frame )
    canvas = fc.canvas.SimpleCanvas()

    flowerBed = loadFlowerbedModel()
    flower1 = createViewFromModel( flowerBed, canvas )

    # the default cam, looking at 500, 500
    canvas.camera.target = target
    canvas.camerta.zoom = (1.0, 1.0)

    def doUpdates():
        # now change the model a bit and see if the view catches it :-)
        flowerBed.flowers[0].size *= 2

        # move one of the objects, this should cause the object to send a fc.events.viewChanged message. This can then be caught by some controller to change the model.
        flower1.transformer.Rotate( PI/4 )

    wx.CallAfter( doUpdates )

    app.MainLoop()



if __name__ == '__main__':
    start()
