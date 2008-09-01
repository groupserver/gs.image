# coding=utf-8

from Products.Five import BrowserView
from OFS.Image import Image
from zope.component import createObject, getMultiAdapter
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implements

from interfaces import *
from queries import FileQuery

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
        
        assert hasattr(self.groupInfo.groupObj, 'files'), \
          'No "files" in %s (%s)' % (self.groupInfo.name, self.groupInfo.id)
        fileLibrary = self.groupInfo.groupObj.files
        files = fileLibrary.find_files({'id': self.imageId})
        assert len(files) == 1, \
          'Wrong number of files returned: %s' % len(files)
        self.file = files[0].getObject()
        assert self.file
        self.fullImage = Image(self.imageId, self.imageId, self.file.data)
        
        self.__imageMetadata = None
        self.__authorInfo = None
        
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
    def fullImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/foo.jpg
        retval = '%s/files/f/%s/resize/%s' % \
          (self.groupInfo.url, self.imageId, self.filename)
        assert self.imageId in retval
        return retval        

    @property
    def filename(self):
        # Inspried by the get_file method of the virtual file library.
        title  =  self.file.getProperty('title', '')
        retval =  self.file.getProperty('filename', title).strip()
        return retval

    @property
    def topic(self):
        retval = self.imageMetadata['topic']
        assert type(retval) == dict
        assert retval
        return retval

    @property
    def post(self):
        retval = self.imageMetadata['post']
        assert type(retval) == dict
        assert retval
        return retval
        
    @property
    def authorInfo(self):
        if self.__authorInfo == None:
            authorId = self.post['author_id']
            self.__authorInfo = createObject('groupserver.UserFromId', 
                                             self.context, authorId)
        retval = self.__authorInfo
        return retval
        
    @property
    def imageMetadata(self):
        if self.__imageMetadata == None:
            da = self.context.zsqlalchemy 
            assert da, 'No data-adaptor found'
            fileQuery = FileQuery(self.context, da)
            self.__imageMetadata = fileQuery.file_metadata(self.imageId)
        retval = self.__imageMetadata
        return retval

