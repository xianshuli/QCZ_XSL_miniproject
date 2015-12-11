__author__ = 'Qingchuan'

import webapp2
import Person
import management


class HighLightMatches(webapp2.RequestHandler):
    def get(self):
        cur_usr = self.request.get('client_ID')
        target_usr = self.request.get('target_person')

        match_result = []

        # retrieve cur_usr preference
        cur_usr_info = Person.Person.query(
            ancestor=management.person_key(str(cur_usr))).fetch(1)[0]
        # retrieve target usr preference
        target_usr_info = Person.Person.query(
            ancestor=management.person_key(str(target_usr))).fetch(1)[0]

        if cur_usr_info.roommate_choice == target_usr_info.roommate_choice:
            match_result.append(1)

        if cur_usr_info.smoking_choice == target_usr_info.smoking_choice:
            match_result.append(2)

        if cur_usr_info.overnight_guest_choice == target_usr_info.overnight_guest_choice:
            match_result.append(3)

        if cur_usr_info.study_habits_choice == target_usr_info.study_habits_choice:
            match_result.append(4)

        if cur_usr_info.sleep_habits_choice == target_usr_info.sleep_habits_choice:
            match_result.append(5)

        if cur_usr_info.cleanliness_choice == target_usr_info.cleanliness_choice:
            match_result.append(6)

        self.response.write(match_result)


class ChangeOptionsOnRight(webapp2.RequestHandler):
    def get(self):
        target_usr = self.request.get('target_person')

        # retrieve target usr preference
        target_usr_info = Person.Person.query(
            ancestor=management.person_key(str(target_usr))).fetch(1)[0]

        target_result = []

        pref1_op = str(target_usr_info.roommate_choice)
        pref2_op = str(target_usr_info.smoking_choice)
        pref3_op = str(target_usr_info.overnight_guest_choice)
        pref4_op = str(target_usr_info.study_habits_choice)
        pref5_op = str(target_usr_info.sleep_habits_choice)
        pref6_op = str(target_usr_info.cleanliness_choice)

        target_result.append(Person.preferenceMatchEngine("pref1", pref1_op))
        target_result.append(Person.preferenceMatchEngine("pref2", pref2_op))
        target_result.append(Person.preferenceMatchEngine("pref3", pref3_op))
        target_result.append(Person.preferenceMatchEngine("pref4", pref4_op))
        target_result.append(Person.preferenceMatchEngine("pref5", pref5_op))
        target_result.append(Person.preferenceMatchEngine("pref6", pref6_op))

        self.response.write(target_result)


app = webapp2.WSGIApplication([
    ('/high_light_matches', HighLightMatches),
    ('/changeoptionsonright', ChangeOptionsOnRight),
], debug=True)
