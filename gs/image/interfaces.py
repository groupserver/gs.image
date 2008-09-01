from zope.interface import Interface
from zope.schema import *

# marker interface for regular old image
class IImage(Interface):
    pass

class IGSImageView(Interface):
    width = Int(title=u'Width',
        description=u'The width of the image',
        default=432)

    height = Int(title=u'Height',
        description=u'The height of the image',
        default=432)

class IGSImage(Interface):
    def resize(x, y, maintain_aspect=True): #@NoSelf
        """ resize an image, maintaining the optionally maintaining
        the aspect ratio.
        
        """
        pass

