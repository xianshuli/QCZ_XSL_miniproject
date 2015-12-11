__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json

from google.appengine.api import users


class AddPotentialPersons(webapp2.RequestHandler):
    def post(self):
        body = self.request.body

        # parse the json
        j = json.loads(body)
        potentialpersons = j["potentialPerson"]

        for person in potentialpersons:
            print(person)

app = webapp2.WSGIApplication([
    ('/addpotentialpersons', AddPotentialPersons),
], debug=True)
