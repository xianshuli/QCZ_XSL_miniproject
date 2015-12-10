__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import Person
import management

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # get the current usr
        curr_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')

        # get the current match list
        usr_ndb_info = Person.Person.query(ancestor= management.person_key(str(curr_usr))).fetch(1)[0]
        current_matches_names = usr_ndb_info.current_matches

        current_matches = []

        for match_usr in current_matches_names:
            # retrive the usr info
            match_usr_info = Person.Person.query(ancestor= management.person_key(str(match_usr))).fetch(1)[0]
            # construct a dict
            info_dict = dict()
            info_dict['Name'] = match_usr_info.person_name
            info_dict['Gender'] = match_usr_info.person_gender
            info_dict['Age'] = match_usr_info.person_age
            info_dict['School'] = match_usr_info.person_school

            current_matches.append(info_dict)

        template_values = {
            'usr': curr_usr,
            'logout_url': logout_url,
            'current_matches': current_matches,
        }

        template = JINJA_ENVIRONMENT.get_template('/myhtml/match_list.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/matchmanagement', MainHandler)
], debug=True)
