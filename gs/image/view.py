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
        self.__nextImage = None
        self.__prevImage = None
        self.__topicImages = None
        
        self.maxWidth = self.maxHeight = 432 # 24u on OGN

        da = self.context.zsqlalchemy 
        assert da, 'No data-adaptor found'
        self.fileQuery = FileQuery(self.context, da)

    @property
    def scaledImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/resize/500/500/foo.jpg
        retval = self.get_uri_for_scaled(self.imageId, self.maxWidth, 
                                         self.maxHeight, self.filename)
        assert self.imageId in retval
        return retval
    
    def get_uri_for_scaled(self, imageId, maxWidth, maxHeight, filename):
        retval = '%s/files/f/%s/resize/%s/%s/%s' % \
          (self.groupInfo.url, imageId, maxWidth, maxHeight, filename)
        # assert type(retval) == str
        assert retval
        return retval
    
    @property
    def fullImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/foo.jpg
        retval = '%s/files/f/%s/%s' % \
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
            iid = self.imageId
            self.__imageMetadata = self.fileQuery.file_metadata(iid)
        retval = self.__imageMetadata
        return retval

    def images_in_topic(self):
        if self.__topicImages == None:
            topicId = self.imageMetadata['topic']['topic_id']
            files = self.fileQuery.file_metadata_in_topic(topicId)
            self.__topicImages = [f for f in files 
                                  if 'image' in f['mime_type']]
            for f in self.__topicImages:
                iid = f['file_id']
                fn = f['file_name']
                f['icon_uri'] = self.get_uri_for_scaled(iid, 27, 27, fn)

        retval = self.__topicImages
        
        assert type(retval) == list
        assert retval
        return retval
    
    @property
    def prevImage(self):
        if self.__prevImage == None:
            files = self.images_in_topic()
            ids = [f['file_id'] for f in files]
            prevs = files[:ids.index(self.imageMetadata['file_id'])]
            self.__prevImage = prevs and prevs[-1] or None
        retval = self.__prevImage
        return retval

    @property
    def nextImage(self):
        if self.__nextImage == None:
            files = self.images_in_topic()
            ids = [f['file_id'] for f in files]
            nexts = files[ids.index(self.imageMetadata['file_id'])+1:]
            self.__nextImage = nexts and nexts[0] or None
        retval = self.__nextImage
        return retval

