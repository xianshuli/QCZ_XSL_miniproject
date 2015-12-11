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
            info_dict['ID'] = match_usr_info.person_account
            info_dict['Name'] = match_usr_info.person_name
            info_dict['Gender'] = match_usr_info.person_gender
            info_dict['Age'] = match_usr_info.person_age
            info_dict['School'] = match_usr_info.person_school

            current_matches.append(info_dict)

        # get the 1st match person's information, that is used as the default to show on match page
        first_person = current_matches_names[0]
        first_person_info = Person.Person.query(ancestor= management.person_key(str(first_person))).fetch(1)[0]

        # save first person info in a dict
        first_p_setting = dict()

        first_p_setting['roommategender'] = Person.preferenceMatchEngine("pref1", str(first_person_info.roommate_choice))
        first_p_setting['smoking_choice'] = Person.preferenceMatchEngine("pref2", str(first_person_info.smoking_choice))
        first_p_setting['overnight_guest_choice'] = Person.preferenceMatchEngine("pref3", str(first_person_info.overnight_guest_choice))
        first_p_setting['study_habits_choice'] = Person.preferenceMatchEngine("pref4", str(first_person_info.study_habits_choice))
        first_p_setting['sleep_habits_choice'] = Person.preferenceMatchEngine("pref5", str(first_person_info.sleep_habits_choice))
        first_p_setting['cleanliness_choice'] = Person.preferenceMatchEngine("pref6", str(first_person_info.cleanliness_choice))

        template_values = {
            'usr': curr_usr,
            'logout_url': logout_url,
            'current_matches': current_matches,
            'first_person_setting': first_p_setting,
            'first_person_id': current_matches_names[0],
        }

        template = JINJA_ENVIRONMENT.get_template('/myhtml/match_list.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/matchmanagement', MainHandler)
], debug=True)
