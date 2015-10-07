__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import stream_bundle
import management

from google.appengine.api import images
from google.appengine.api import users

class streamToShow:
    def __init__(self, stream_name, blobKey, views):
        self.urlToStream = "/viewStream?Stream_id="+stream_name
        self.coverPhotoURL = images.get_serving_url(blobKey)
        self.streamName = stream_name
        self.numOfViews = views

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('myhtml/Trending.html')
        # get the top3 guys with stream names
        top3list = stream_bundle.top3streams.query().fetch()[0].top3list
        # fetch the streams
        stream_list = list()

        for stream in top3list:
            if str(stream) is not "":
                myStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(stream))).fetch(1)[0]
                l_stream_name = myStream.streamname
                i_stream_blobkey = myStream.blob_key[0]
                i_stream_views = len(myStream.viewTimeQueue)
                i_stream = streamToShow(l_stream_name, i_stream_blobkey, i_stream_views)
                stream_list.append(i_stream)

        curr_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')
        template_values = {
            'usr': curr_usr,
            'streams_to_show': stream_list,
            'logout_url': logout_url,
        }

        self.response.write(template.render(template_values))


class pollNumOfViewHandler(webapp2.RequestHandler):
    def get(self):
        streamlist = stream_bundle.myStream.query().fetch()
        top4 = [0 ,0, 0, 0]
        top4stream = ["", "", "", ""]
        for stream in streamlist:
            numOfView= len(stream.viewTimeQueue)
            top4[3] = numOfView
            top4stream[3] = stream.streamname
            for i in [2, 1, 0]:
                if(top4[i] < top4[i+1]):
                    temp = top4[i]
                    top4[i] = top4[i+1]
                    top4[i+1] = temp
                    tempstr = top4stream[i]
                    top4stream[i] = top4stream[i+1]
                    top4stream[i+1] = tempstr

        # fetch the top3 list
        top3list = stream_bundle.top3streams.query().fetch()[0]
        top3list.top3list = top4stream[0:3]
        top3list.put()

        self.response.write(top3list.top3list[0])
        self.response.write(top3list.top3list[1])
        self.response.write(top3list.top3list[2])


app = webapp2.WSGIApplication([
    ('/myhtml/Trending.html', MainHandler),
    ('/pollTheNumOfViews', pollNumOfViewHandler),
], debug=True)
