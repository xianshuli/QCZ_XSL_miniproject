__author__ = 'Qingchuan'

from google.appengine.ext import ndb


class myStream(ndb.Model):
    streamname = ndb.StringProperty()
    streamOwner = ndb.UserProperty()
    doc_id = ndb.StringProperty()
    lastNewPicture = ndb.DateProperty(required=False)
    createTime = ndb.DateProperty()
    urltoCoverPhoto = ndb.StringProperty()
    numOfPictures = ndb.IntegerProperty()
    numOfViews = ndb.IntegerProperty()
    viewTimeQueue = ndb.DateTimeProperty(repeated=True)
    blob_key = ndb.BlobKeyProperty(repeated=True)
    photoComments = ndb.StringProperty(repeated=True)


class stream_bundles(ndb.Model):
    stream_iownlist = ndb.KeyProperty(repeated=True)
    stream_isublist = ndb.KeyProperty(repeated=True)


class top3streams(ndb.Model):
    top3list = ndb.StringProperty(repeated=True)


class emailrate(ndb.Model):
    rate_setting = ndb.IntegerProperty() # 0: no email 1: 5 min 2: 1 hr 3: 1day
    count = ndb.IntegerProperty()


class doc_id(ndb.Model):
    doc_id = ndb.IntegerProperty()