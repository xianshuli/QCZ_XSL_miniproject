__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import json
import stream_bundle
import management
from google.appengine.api import images
from google.appengine.api import users

class mobileViewSubscribe(webapp2.RequestHandler):
    def get(self):
        curr_usr = self.request.params['usr_email']

        if curr_usr.find("@gmail.com") > 0:
            curr_usr = curr_usr.split('@')[0]

        streamIRelated_query = stream_bundle.stream_bundles.query(
            ancestor=management.stream_key(curr_usr)).fetch(1)
        mySubStream = streamIRelated_query[0].stream_isublist

        if len(mySubStream) == 0:
            hasSubStream = False;
        else:
            hasSubStream = True

        image_url = list()
        stream_name = list()
        stream_owner = list()

        for key in mySubStream:
            tempStream = key.get()
            stream_name.append(tempStream.streamname)
            l_stream_owner = str(tempStream.streamOwner)
            if l_stream_owner.find("@") < 0:
                l_stream_owner = l_stream_owner+"@gmail.com"
            stream_owner.append(l_stream_owner)

            hasCover = True
            i_stream_coverurl = tempStream.urltoCoverPhoto
            i_stream_blobKey = ""
            if(i_stream_coverurl == ""):
                hasCover = False
                i_stream_blobKey = tempStream.blob_key[0]
            if(hasCover):
                image_url.append(i_stream_coverurl)
            else:
                image_url.append(images.get_serving_url(i_stream_blobKey))


        dictPassed = {
            'cover_url': image_url,
            'stream_names': stream_name,
            'stream_owners': stream_owner,
            'hasSubStream': hasSubStream,
        }
        jsonObj = json.dumps(dictPassed, sort_keys=True)
        self.response.write(jsonObj)


app = webapp2.WSGIApplication([
    ('/mobileViewSubscribe', mobileViewSubscribe),
], debug=True)
