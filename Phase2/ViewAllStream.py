__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import stream_bundle
from google.appengine.api import images
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class streamToShow:
    def __init__(self, stream_name, coverurl, i_stream_blobKey, hasCover):
        self.urlToStream = "/viewStream?Stream_id="+stream_name
        if(hasCover):
            self.coverPhotoURL = coverurl
        else:
            self.coverPhotoURL = images.get_serving_url(i_stream_blobKey)
        self.streamName = stream_name

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('myhtml/View.html')
        # retrieve all the streams
        streamlist = stream_bundle.myStream.query().order(-stream_bundle.myStream.lastNewPicture).fetch()
        curr_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')
        streams_to_show = list()

        for stream in streamlist:
            if stream.numOfPictures > 0:
                l_stream_name = stream.streamname
                i_stream_coverurl = stream.urltoCoverPhoto
                hasCover = True
                i_stream_blobKey = ""
                if(i_stream_coverurl == ""):
                    hasCover = False
                    i_stream_blobKey = stream.blob_key[0]
                i_stream = streamToShow(l_stream_name, i_stream_coverurl, i_stream_blobKey, hasCover)
                streams_to_show.append(i_stream)

        template_values = {
            'usr': curr_usr,
            'streams_to_show': streams_to_show,
            'logout_url': logout_url,
        }

        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/myhtml/View.html', MainHandler),
], debug=True)
