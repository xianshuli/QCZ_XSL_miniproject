__author__ = 'Qingchuan'
import webapp2
import jinja2
import os
import stream_bundle
import datetime
import time
import calendar
import management
import json
import copy
import random

from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import urlfetch
from google.appengine.api import images
from stream_bundle import Location

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
            myStream.numOfPictures = myStream.numOfPictures+1
            myStream.put()
            self.redirect("/viewStream?Stream_id="+stream_key)
        except:
            self.error(500)


class MultipleFilesAfterUpload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            stream_key = self.request.get("stream_key")
            #usrcomments = self.request.get("usrcomments")
            self.response.write(stream_key)
            myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)[0]

            #myStream.blob_key.append(upload.key())
            #myStream.photoComments = [usrcomments] + myStream.photoComments
            for blob_info in self.get_uploads():
                myStream.blob_key = [blob_info.key()] + myStream.blob_key
                myStream.imageCreateDateList = [time.mktime(time.gmtime()) * 1000] + myStream.imageCreateDateList
                myStream.imageLocation = [Location(longitude = random.uniform(-170, 170),
                                                   latitude = random.uniform(-50, 50))] + myStream.imageLocation
            print(len(myStream.blob_key))
            print(type(time.mktime(time.gmtime()) * 1000))
            myStream.lastNewPicture = datetime.datetime.now()
            # modified the following code
            # print(self.get_uploads().__len__())
            # print(myStream.numOfPictures)
            myStream.numOfPictures = myStream.numOfPictures+len(self.get_uploads())
            # print(myStream.numOfPictures)
            myStream.put()
            self.redirect("/viewStream?Stream_id="+stream_key)
        except:
            self.error(500)

class UploadURLGenerator(webapp2.RedirectHandler):
    def post(self):
        try:
            upload_url = blobstore.create_upload_url('/viewSingleAfterUpload')
            self.response.headers['Content-Type'] = 'application/json'
            upload_url = json.dumps(upload_url)
            self.response.out.write(upload_url)
        except:
            self.error(500)


class image:
    def __init__(self):
        url = ""
        created = 0
        lat = 0
        lng = 0



class GeoViewHandler(webapp2.RequestHandler):

    def get(self):
        stream_key = self.request.get("Stream_id")

        template = JINJA_ENVIRONMENT.get_template('myhtml/GeoViewPage.html')

        template_values = {
            'stream_key': stream_key,
        }
        self.response.write(template.render(template_values))

    def post(self):
        stream_key = self.request.get("Stream_id")
        myStream_qurey = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)
        if len(myStream_qurey) == 0:
            self.redirect("/myhtml/Errorpage.html?Error_code=404")
            return
        myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_key))).fetch(1)[0]

        imagesToJquery = []
        pic = image()
        # get image if any
        if(len(myStream.blob_key) > 0):
            image_blob_key_list = myStream.blob_key
            image_created_time_list = myStream.imageCreateDateList
            image_location_list = myStream.imageLocation
            for bbkey in image_blob_key_list:
                pic.url = images.get_serving_url(bbkey)
                imagesToJquery.append(copy.deepcopy(pic))
            for i in range(len(image_created_time_list)):
                imagesToJquery[i].created = image_created_time_list[i]
            for i in range(len(image_location_list)):
                imagesToJquery[i].lat = image_location_list[i].latitude
                imagesToJquery[i].lng = image_location_list[i].longitude

        # for i in range(len(imagesToJquery)):
        #     print(i)
        #     print(imagesToJquery[i].url)
        #     print(imagesToJquery[i].created)
        #     print(imagesToJquery[i].lat)
        #     print(imagesToJquery[i].lng)
        #     # print(vars(imagesToJquery[i]))
        #     print(imagesToJquery[i].__dict__)
        json_string = json.dumps([img.__dict__ for img in imagesToJquery])
        print(json_string)
        # output = json.dumps(imagesToJquery)
        # obj_list = json.loads(json_string)
        # for obj in obj_list:
        #     print("#")
        #     print(obj['url'])
        #     print(obj['created'])
        #     print(obj['lat'])
        #     print(obj['lng'])
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(json_string)
app = webapp2.WSGIApplication([
    ('/viewStream', MainHandler),
    ('/viewSingleAfterUpload', MultipleFilesAfterUpload),
    ('/geoViewRequest', GeoViewHandler),
    ('/getUploadUrl', UploadURLGenerator)
], debug=True)
