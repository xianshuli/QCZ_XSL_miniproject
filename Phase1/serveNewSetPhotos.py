__author__ = 'Qingchuan'

import webapp2
import json
import stream_bundle
import management
import re

from google.appengine.api import images

class MainHandler(webapp2.RequestHandler):
    def post(self):
        body2 = self.request.body
        js_c = json.loads(body2)
        stream_id = js_c["stream_id"]
        numOfPage = js_c["page"]

        # fetch the urls
        myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream_id))).fetch(1)[0]
        blob_key_list = myStream.blob_key
        image_url = list()
        for bbkey in blob_key_list:
            image_url.append(images.get_serving_url(bbkey))

        # self.response.write(image_url)

        i = (numOfPage-1)*3
        j = i+3

        # check boundarys
        endIndex = len(image_url)-1
        if(i>endIndex):
            url_for_return = list()   # empty list
        elif (j > endIndex):
            url_for_return = image_url[i:(endIndex+1)]
        else:
            url_for_return = image_url[i:j]

        a = [""]*3
        s = list()
        for url in url_for_return:
            s.append(str(url))
        a[0:len(s)] = s

        myUrls = {
            'urls': s
        }
        self.response.write(json.dumps(myUrls))

app = webapp2.WSGIApplication([
    ('/fetchAnotherSetOfPhotos', MainHandler),
], debug=True)
