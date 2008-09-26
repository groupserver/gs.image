# coding=utf-8
from Products.XWFCore.XWFUtils import locateDataDirectory
from zope.app.file.image import Image
from zope.interface import implements
from interfaces import IGSImage
from PIL import Image as PILImage
from StringIO import StringIO
import md5, os, logging
log = logging.getLogger('GSImage') #@UndefinedVariable

class GSImage(object):
    implements(IGSImage)
    
    method=PILImage.BICUBIC
    
    def __init__(self, image):
        self.image = image
        self.data_dir = locateDataDirectory("groupserver.GSImage.cache")    
        self.md5sum = md5.new(StringIO(image.data).read()).hexdigest()
        self.base_path = os.path.join(self.data_dir, self.md5sum)
        
    def _pilImage(self):
        data_reader = StringIO(self.image.data)
        img = PILImage.open(data_reader)
        return img
        
    def get_resized(self, x, y, maintain_aspect=True, only_smaller=True):
        """ Resize an image, and return an Image instance of the resized image.
        
        This does not change the GSImage instance, since we may want to
        resize a number of times.
        
        Optionally we can also force the aspect ratio to be maintained, and
        only shrink the size.
        
        """
        cache_name = self.base_path+'%sx%sx%s' % (x,y,maintain_aspect)
        
        if os.path.isfile(cache_name):
            img = Image(file(cache_name))
            # backwards compatibility with Zope2
            img.width, img.height = img.getImageSize()
            img.fromCache = True
            
            return img
        
        # check to see that we're not already smaller than x,y
        if only_smaller:
            width, height = self.image.getImageSize()
            if height <= y and width <= x:
                self.image.width, self.image.height = width, height
                return self.image
        
        image = self._pilImage()
        origFormat = image.format # We will lose track of the format below
        if (image.mode not in ('RGB', 'RGBA', 'RGBX', 'CMYK')):
            try: # Try and convert the image to RGBA before scaling it
                image = image.convert('RGBA')
            except:
              log.warning('Could not convert image to RGBA')
              image = self._pilImage()

        if maintain_aspect:
            #
            # With thanks to kevin@cazabon.com:
            # http://mail.python.org/pipermail/image-sig/2006-January/003724.html
            #
            imAspect = float(image.size[0])/float(image.size[1])
            outAspect = float(x)/float(y)
            if imAspect >= outAspect:
                #set to maxWidth x maxWidth/imAspect
                img = image.resize((x,
                                    int((float(x)/imAspect) + 0.5)),
                                    self.method)
            else:
                #set to maxHeight*imAspect x maxHeight
                img = image.resize((int((float(y)*imAspect) + 0.5), y),
                                    self.method)
        else:
            img = image.resize((x,y), self.method)

        if img.mode != image.mode:
            # Change the image back to the original mode before saving
            img = img.convert(image.mode)
        img.save(cache_name, origFormat)
        
        img = Image(file(cache_name))
        # backwards compatibility with Zope2
        img.width, img.height = img.getImageSize()
        img.fromCache = False
        return img 
    
    def _clean_cache(self):
        """ Tidy up files that have been saved in association with this 
        image."""
        for fname in os.listdir(self.data_dir):
            if fname.find(self.md5sum) == 0:
                os.remove(os.path.join(self.data_dir, fname))

