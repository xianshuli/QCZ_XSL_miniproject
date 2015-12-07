__author__ = 'Qingchuan'

import webapp2
import Person
import management
import update_match_engine

from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def post(self):
        # get the usr email info
        usr_login = users.get_current_user()

        print("Update "+str(usr_login)+" 's personal information\n")
        
        # The validility of these input fields are checked by JavaScript in the front end
        usr_account = str(usr_login)
        usr_name = self.request.get('name_input')
        usr_gender = self.request.get('gender_input')
        usr_age = int(self.request.get('age_input'))
        usr_school = self.request.get('school_input')
        usr_major = self.request.get('major_input')
        usr_email = self.request.get('email_input')
        usr_phone_area = self.request.get('phone_area_input')
        usr_phone_notarea = self.request.get('phone_notarea_input')

        # following print are used for testing parameter passing
        print(usr_account)
        print(usr_name)
        print(usr_gender)
        print(usr_age)
        print(usr_school)
        print(usr_major)
        print(usr_email)
        print(usr_phone_area + usr_phone_notarea)
        
        # store what is submitted into NDB store
           # step 1: get the handle
        usr_ndb_info = Person.Person.query(ancestor= management.person_key(str(usr_login))).fetch(1)
           # set the fields
        if usr_ndb_info: # update current usr infp
            usr_ndb_info[0].person_name = usr_name
            usr_ndb_info[0].person_gender = usr_gender
            usr_ndb_info[0].person_age = usr_age
            usr_ndb_info[0].person_school = usr_school
            usr_ndb_info[0].person_major = usr_major
            usr_ndb_info[0].person_email = usr_email
            usr_ndb_info[0].person_phone_number = usr_phone_area + usr_phone_notarea         
            usr_ndb_info[0].personInfoSet = True
            usr_ndb_info[0].usr_viewed_updates = False
            usr_ndb_info[0].put()
        else:
            #create a ndb entry
            new_usr_info = Person.Person(parent= management.person_key(str(usr_login)))
            new_usr_info.person_account = usr_account
            new_usr_info.person_name = usr_name
            new_usr_info.person_gender = usr_gender
            new_usr_info.person_age = usr_age
            new_usr_info.person_school = usr_school
            new_usr_info.person_major = usr_major
            new_usr_info.person_email = usr_email
            new_usr_info.person_phone_number = usr_phone_area + usr_phone_notarea         
            new_usr_info.personInfoSet = True
            new_usr_info.usr_viewed_updates = False
            new_usr_info.usr_notification = 0
            new_usr_info.put()

        # call match engine to compute number of match
        update_match_engine.update_match(str(usr_login))

app = webapp2.WSGIApplication([
    ('/personal_info_handler', MainHandler)
], debug=True)
