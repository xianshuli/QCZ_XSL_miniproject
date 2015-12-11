__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json

from google.appengine.api import users


class AddPotentialPersons(webapp2.RequestHandler):
    def post(self):
        body = self.request.body

        cur_usr = users.get_current_user();
        cur_usr = str(cur_usr)

        # parse the json
        j = json.loads(body)
        potentialpersons = j["potentialPerson"]

        # get the handler of the current usr
        current_usr_info = Person.Person.query(ancestor= management.person_key(str(cur_usr))).fetch(1)[0]
        usr_current_potential_roommate_list = current_usr_info.potential_roommate
        my_potential_roommate = list()

        for person in potentialpersons:
            if person not in usr_current_potential_roommate_list:
                print(person)
                my_potential_roommate.append(person)

        current_usr_info.potential_roommate = usr_current_potential_roommate_list + my_potential_roommate

        current_usr_info.put()

app = webapp2.WSGIApplication([
    ('/addpotentialpersons', AddPotentialPersons),
], debug=True)
