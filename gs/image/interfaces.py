from zope.interface import Interface

# marker interface for regular old image
class IImage(Interface):
    pass

class IGSImageView(Interface):
    pass

class IGSImage(Interface):
    def resize(x, y, maintain_aspect=True): #@NoSelf
        """ resize an image, maintaining the optionally maintaining
        the aspect ratio.
        
        """
        pass
