# coding=utf-8

from Products.Five import BrowserView
from zope.component import createObject, getMultiAdapter
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implements

from interfaces import *

import logging
log = logging.getLogger('GSImageView')

class GSImageTraversal(BrowserView):
    implements(IPublishTraverse)
    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.imageId = None
                
    def publishTraverse(self, request, name):
        if self.imageId == None:
            self.imageId = name
            
        return self
    
    def __call__(self):
      return getMultiAdapter((self.context, self.request), 
                             name="gsimage")()

class GSImageView(BrowserView):
    implements(IGSImageView)
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.groupInfo = createObject('groupserver.GroupInfo', context)

        self.imageId = context.imageId
        print 'Image ID %s' % self.imageId
        
        assert hasattr(self.groupInfo.groupObj, 'files'), \
          'No "files" in %s (%s)' % (self.groupInfo.name, self.groupInfo.id)
        fileLibrary = self.groupInfo.groupObj.files
        files = fileLibrary.find_files({'id': self.imageId})
        assert len(files) == 1, \
          'Wrong number of files returned: %s' % len(files)
        self.image = files[0].getObject()
        assert self.image

        self.width = self.height = 500

    @property
    def scaledImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/resize/500/500/foo.jpg
        retval = '%s/files/f/%s/resize/%s/%s/%s' % \
          (self.groupInfo.url, self.imageId, self.width, self.height, 
           self.filename)
        assert self.imageId in retval
        return retval        

    @property
    def filename(self):
        title  =  self.image.getProperty('title', '')
        print title
        retval =  self.image.getProperty('filename', title).strip()
        print 'filename %s' % retval
        return retval

