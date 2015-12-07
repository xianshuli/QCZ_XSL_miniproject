__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json
import update_match_engine

from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def post(self):
        # get the usr email info
        usr_login = users.get_current_user()

        body = self.request.body

        # parse the json
        j = json.loads(body)
        roommate_choice = str(j["roommate_choice"])
        smoking_choice = str(j["smoking_choice"])
        overnight_guest_choice = str(j["overnight_guest_choice"])
        study_habits_choice = str(j["study_habits_choice"])
        sleep_habits_choice = str(j["sleep_habits_choice"])
        musictv_choice = str(j["musictv_choice"])
        cleanliness_choice = str(j["cleanliness_choice"])

        # Option string to integer map
        optionMap = {
            "Option1": 1,
            "Option2": 2,
            "Option3": 3,
        }

        # print out for testing
        print(roommate_choice)
        print(smoking_choice)
        print(overnight_guest_choice)
        print(study_habits_choice)
        print(sleep_habits_choice)
        print(musictv_choice)
        print(cleanliness_choice)

        # update the datebase
        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(usr_login)).fetch(1)[0]

        usr_personal_info.roommate_choice = optionMap[roommate_choice]
        usr_personal_info.smoking_choice = optionMap[smoking_choice]
        usr_personal_info.overnight_guest_choice = optionMap[overnight_guest_choice]
        usr_personal_info.study_habits_choice = optionMap[study_habits_choice]
        usr_personal_info.sleep_habits_choice = optionMap[sleep_habits_choice]
        usr_personal_info.musictv_choice = optionMap[musictv_choice]
        usr_personal_info.cleanliness_choice = optionMap[cleanliness_choice]

        usr_personal_info.put()

        # call match engine to compute number of match
        update_match_engine.update_match(str(usr_login))




app = webapp2.WSGIApplication([
    ('/personal_preference_handler', MainHandler)
], debug=True)
