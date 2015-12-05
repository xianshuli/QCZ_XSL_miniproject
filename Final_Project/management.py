__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import Person

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def person_key(usr_name):
    """Constructs a Datastore key for a usr entity."""
    return ndb.Key('PerfectRoommate', str(usr_name))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # get the current usr
        curr_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')

        # try to get the usr's personal info if any
        usr_personal_info = Person.Person.query(
            ancestor=person_key(curr_usr)).fetch(1)

        usr_has_info = False
        usr_name = ""
        usr_gender = ""
        usr_age = 0
        usr_school = ""
        usr_major = ""
        usr_email = ""
        usr_phone = ""

        if usr_personal_info and usr_personal_info[0].personInfoSet != False:
            # get the fields of personal info in case the usr wants to modify them
            usr_name = usr_personal_info[0].person_name
            usr_gender = usr_personal_info[0].person_gender
            usr_age = usr_personal_info[0].person_age
            usr_school = usr_personal_info[0].person_school
            usr_major = usr_personal_info[0].person_major
            usr_email = usr_personal_info[0].person_email
            usr_phone = usr_personal_info[0].person_phone_number
            usr_has_info = True

        template_values = {
            'usr': curr_usr,
            'logout_url': logout_url,
            'usr_has_info': usr_has_info,
            'usr_name': usr_name,
            'usr_gender': usr_gender,
            'usr_age': usr_age,
            'usr_school': usr_school,
            'usr_major': usr_major,
            'usr_email': usr_email,
            'usr_phone_area': usr_phone[0:3],
            'usr_phone_notarea': usr_phone[3:],
        }

        template = JINJA_ENVIRONMENT.get_template('/myhtml/management.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/management', MainHandler)
], debug=True)
