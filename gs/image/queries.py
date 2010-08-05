# coding=utf-8
from Products.XWFMailingListManager.queries import MessageQuery

class FileQuery(MessageQuery):

    def file_metadata(self, fileId):
        ft = self.fileTable
        
        statement = ft.select()
        statement.append_whereclause(ft.c.file_id == fileId)
        
        r = statement.execute()
        x = r.fetchone()
        retval = {'file_id':   x['file_id'],
                  'mime_type': x['mime_type'],
                  'file_name': x['file_name'],
                  'file_size': x['file_size'],
                  'date':      x['date'],
                  'post':      self.post(x['post_id']),
                  'topic':     self.topic(x['topic_id'])}
        return retval

    def file_metadata_in_topic(self, topicId):
        assert type(topicId) == str,\
          'topicId is a %s not a string' % type(topicId)
        ft = self.fileTable
        
        statement = ft.select()
        statement.append_whereclause(ft.c.topic_id == topicId)
        statement.order_by(ft.c.date)
        
        r = statement.execute()
        retval = [{'file_id':   x['file_id'],
                  'mime_type': x['mime_type'],
                  'file_name': x['file_name'],
                  'file_size': x['file_size'],
                  'date':      x['date'],
                  'post':      self.post(x['post_id'])} for x in r]

        assert type(retval) == list
        assert retval
        return retval

