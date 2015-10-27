__author__ = 'Qingchuan'
import webapp2
import jinja2
import os
import stream_bundle
import datetime
import management
import json

from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import urlfetch
from google.appengine.api import images

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        stream_key = self.request.get("Stream_id")
        usr = users.get_current_user()
        logout_url = users.create_logout_url('/')

        myStream_qurey = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)
        if len(myStream_qurey) == 0:
            self.redirect("/myhtml/Errorpage.html?Error_code=404")
            return
        myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)[0]
        owner = myStream.streamOwner
        # increase the view by 1 if not view by owner
        if owner != usr:
            myStream.numOfViews = myStream.numOfViews +1
            # get the view Time queue
            viewTimeQueue = myStream.viewTimeQueue
            currentTime = datetime.datetime.now()
            while len(viewTimeQueue)> 0 and (currentTime - viewTimeQueue[0]).seconds > 3600:
                del viewTimeQueue[0]
            viewTimeQueue.append(datetime.datetime.now())
            myStream.viewTimeQueue = viewTimeQueue
            myStream.put()

        # test to see if this is the stream usr sub
        streamIOwn_query = stream_bundle.stream_bundles.query(ancestor=management.stream_key(usr)).fetch(1)
        stream_bundles_entity = streamIOwn_query[0]
        # get the list I sub
        listIsub = stream_bundles_entity.stream_isublist
        IsubthisStream = False
        for key in listIsub:
            if(key.get() is not None and key.get().streamname == stream_key):
                IsubthisStream = True
                break

        template = JINJA_ENVIRONMENT.get_template('myhtml/viewSingleStream.html')

        # step1 Create an upload URL if user want to upload pages
        upload_url = blobstore.create_upload_url('/viewSingleAfterUpload')

        # get image if any
        if(len(myStream.blob_key) > 0):
            image_bolb_key_list = myStream.blob_key
            image_url = [""]*3
            counter = 0
            for bbkey in image_bolb_key_list:
                image_url[counter]= images.get_serving_url(bbkey)
                counter = counter +1
                if(counter == 3):
                    break
            weHaveImage = True
        else:
            weHaveImage = False
            image_url = [""]*3

        template_values = {
            'owner': str(owner),
            'usr': str(usr),
            'blobstore_url': upload_url,
            'stream_key': stream_key,
            'haveImage': weHaveImage,
            'imageUrl': image_url,
            'IsubThisStream': IsubthisStream,
            'logout_url': logout_url,
        }

        self.response.write(template.render(template_values))

    def post(self):
        self.response.write("upload seems successful")


class AfterUpload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            stream_key = self.request.get("stream_key")
            usrcomments = self.request.get("usrcomments")
            self.response.write(stream_key)
            myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)[0]

            #myStream.blob_key.append(upload.key())
            myStream.photoComments = [usrcomments] + myStream.photoComments
            myStream.blob_key = [upload.key()] + myStream.blob_key
            myStream.lastNewPicture = datetime.datetime.now()
            myStream.pic_lat = ["None"] + myStream.pic_lat
            myStream.pic_long = ["None"] + myStream.pic_long
            myStream.numOfPictures = myStream.numOfPictures+1
            myStream.put()
            self.redirect("/viewStream?Stream_id="+stream_key)
        except:
            self.error(500)


class viewSingleMoble(webapp2.RequestHandler):
    def get(self):
        stream_key = self.request.get("Stream_id")
        usr_launch_search = self.request.get('usr_launch_search')

        myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)[0]

        # increment the view number if usr other than owner view the stream
        l_stream_owner = str(myStream.streamOwner)
        if l_stream_owner.find("@") < 0:
            l_stream_owner = l_stream_owner+"@gmail.com"
        if(usr_launch_search != l_stream_owner):
            num_of_view = myStream.numOfViews
            myStream.numOfViews = num_of_view + 1;
            # get the view Time queue
            viewTimeQueue = myStream.viewTimeQueue
            currentTime = datetime.datetime.now()
            while len(viewTimeQueue)> 0 and (currentTime - viewTimeQueue[0]).seconds > 3600:
                del viewTimeQueue[0]
            viewTimeQueue.append(datetime.datetime.now())
            myStream.viewTimeQueue = viewTimeQueue
            myStream.put()

        # get image if any
        if(len(myStream.blob_key) > 0):
            image_bolb_key_list = myStream.blob_key
            image_url = list()
            for bbkey in image_bolb_key_list:
                image_url.append(images.get_serving_url(bbkey))
            weHaveImage = True
        else:
            weHaveImage = False
            image_url = list()

        dictPassed = {
            'displayImages_name': stream_key,
            'wehaveimage': weHaveImage,
            'image_url': image_url,
        }
        jsonObj = json.dumps(dictPassed, sort_keys=True)
        self.response.write(jsonObj)


class mobileGetUploadURL(webapp2.RequestHandler):
        def get(self):
            upload_url = blobstore.create_upload_url('/mobileUploadHandler')
            upload_url = str(upload_url)
            dictPassed = {'upload_url':upload_url}
            jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
            self.response.write(jsonObj)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]

        stream_key = self.request.params['stream_id']
        pic_lat = self.request.params['pic_lat']
        pic_long = self.request.params['pic_long']


        myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)[0]

        myStream.blob_key = [upload.key()] + myStream.blob_key
        myStream.lastNewPicture = datetime.datetime.now()
        myStream.numOfPictures = myStream.numOfPictures+1
        myStream.pic_lat = [pic_lat] + myStream.pic_lat
        myStream.pic_long = [pic_long] + myStream.pic_long
        myStream.put()

        # some debug info
        dictPassed = {'pic_lat': pic_lat,'pic_long':pic_long,'stream_id':stream_key}
        jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)




app = webapp2.WSGIApplication([
    ('/viewStream', MainHandler),
    ('/viewSingleAfterUpload', AfterUpload),
    ('/mobileViewSingleStream', viewSingleMoble),
    ('/mobileGetUploadUrl', mobileGetUploadURL),
    ('/mobileUploadHandler', UploadHandler),
], debug=True)
