__author__ = 'Qingchuan'

from google.appengine.ext import ndb

# set up the preference dictionary
preference_dict = dict()
pref_roommate_gender = {
    "1": "Mixed",
    "2": "Male-only",
    "3": "Female-only",
}

pref_smoking = {
    "1": "I am not bothered by a roommate who smokes outside the room",
    "2": "I am allergic to smoke, so No"
}

pref_overnight_guest = {
    "1": "I am open to overnight guests",
    "2": "No overnight guest, PLEASE...."
}

pref_study_habits = {
    "1": "I will study mostly in the room, so be quite",
    "2": "I will study elsewhere"
}

pref_sleep_habits = {
    "1": "I am an EARLY-to-BED, EARLY-to-RISE person",
    "2": "I stay up late and like to sleep in to compensate"
}

pref_cleanliness = {
    "1": "I am a neat freak, so I want someone like me",
    "2": "Not too messy will be OK with me",
    "3": "I am OK with MESSY person"

}

preference_dict["pref1"] = pref_roommate_gender
preference_dict["pref2"] = pref_smoking
preference_dict["pref3"] = pref_overnight_guest
preference_dict["pref4"] = pref_study_habits
preference_dict["pref5"] = pref_sleep_habits
preference_dict["pref6"] = pref_cleanliness


class PersonIChat(ndb.Model):
    # who I chat with and a pointer to the chat history
    person_account = ndb.StringProperty()
    chat_history = ndb.JsonProperty(repeated=True)
    new_message_unread = ndb.BooleanProperty()


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
    roommate_choice = ndb.IntegerProperty()         # no.1 pref
    smoking_choice = ndb.IntegerProperty()          # no.2 pref
    overnight_guest_choice = ndb.IntegerProperty()  # no.3 pref
    study_habits_choice = ndb.IntegerProperty()     # no.4 pref
    sleep_habits_choice = ndb.IntegerProperty()     # no.5 pref
    musictv_choice = ndb.IntegerProperty()          # no.6 pref
    cleanliness_choice = ndb.IntegerProperty()      # no.7 pref

    # number of new notification and if usr has checked it
    usr_notification = ndb.IntegerProperty()
    usr_viewed_updates = ndb.BooleanProperty()

    # person's current match list
    current_matches = ndb.StringProperty(repeated=True)

    # person's potential roommate list
    potential_roommate = ndb.StringProperty(repeated=True)

    # person's chat history
    myChatHistory = ndb.LocalStructuredProperty(PersonIChat, repeated=True)


def preferenceMatchEngine(pref_name, option):
    # get the corresponding dict
    print("pref_name is "+pref_name+" the option is "+option)
    pref_cat = preference_dict[pref_name]
    return pref_cat[option]
