__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json
import time

from google.appengine.api import users
from google.appengine.api import channel


def notifiyclient(clientID, num_of_matches):
        j_num_matches = {"num_of_matches": num_of_matches}
        message = json.dumps(j_num_matches)
        channel.send_message(clientID, message)


class TokenGenerator(webapp2.RequestHandler):
    def get(self):
        usr_name = self.request.get('client_ID')

        # TODO
        # go to database and see if usr has

        # create a channel token
        token = channel.create_channel(usr_name)
        self.response.write(token)


class OpenedPage(webapp2.RequestHandler):
    def post(self):
        usr_name = self.request.get('client_ID')
        i = 0
        while i < 4:
            notifiyclient(usr_name, i)
            i = i+1
            time.sleep(5)



app = webapp2.WSGIApplication([
    ('/get_channel_token', TokenGenerator),
    ('/opened', OpenedPage,)
], debug=True)
