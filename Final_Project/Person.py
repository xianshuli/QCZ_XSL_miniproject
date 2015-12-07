__author__ = 'Qingchuan'

from google.appengine.ext import ndb


class Person(ndb.Model):
    # person's personal information
    person_account = ndb.StringProperty()
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

    # number of new notification and if usr has checked it
    usr_notification = ndb.IntegerProperty()
    usr_viewed_updates = ndb.BooleanProperty()

    # person's current match list
    current_matches = ndb.StringProperty(repeated=True)


