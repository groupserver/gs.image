from zope.interface import Interface
from zope.schema import *

class IGSImageView(Interface):
    width = Int(title=u'Width',
        description=u'The width of the image',
        default=432)

    height = Int(title=u'Height',
        description=u'The height of the image',
        default=432)

class IGSImage(Interface):
    def get_resized(x, y, maintain_aspect=True): #@NoSelf
        """ resize an image, maintaining the optionally maintaining
        the aspect ratio.
        
        """
        pass

