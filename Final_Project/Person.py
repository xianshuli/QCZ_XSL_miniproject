__author__ = 'Qingchuan'

from google.appengine.ext import ndb


class Person(ndb.Model):
    personInfoSet = ndb.BooleanProperty()
    person_name = ndb.StringProperty()
    person_gender = ndb.StringProperty()
    person_age = ndb.IntegerProperty()
    person_school = ndb.StringProperty()
    person_major = ndb.StringProperty()
    person_email = ndb.StringProperty()
    person_phone_number = ndb.StringProperty()

    # person's preference list
    roommate_choice = ndb.IntegerProperty()
    smoking_choice = ndb.IntegerProperty()
    overnight_guest_choice = ndb.IntegerProperty()
    study_habits_choice = ndb.IntegerProperty()
    sleep_habits_choice = ndb.IntegerProperty()
    musictv_choice = ndb.IntegerProperty()
    cleanliness_choice = ndb.IntegerProperty()

    # people match this person's preference
    usr_viewed_updates = ndb.BooleanProperty()

    # people this person matches for


