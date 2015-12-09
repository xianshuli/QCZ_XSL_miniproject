__author__ = 'Qingchuan'

import Person
import management

from google.appengine.api import users


def updateMutualMatches(curr_usr, potential_target):

    # retrive the current chat history list
    usr_ndb_info = Person.Person.query(ancestor= management.person_key(curr_usr)).fetch(1)[0]
    myChatHistory = usr_ndb_info.myChatHistory

    newTarget = True

    for addedtarget in myChatHistory:
        addedtarget_account = addedtarget.person_account
        if addedtarget_account == potential_target:
            newTarget = False
            break

    if newTarget:
        # create a new PersonIChat
        new_chat_person = Person.PersonIChat()
        new_chat_person.person_account = potential_target
        new_chat_person.new_message_unread = False
        new_chat_person.chat_history = []

        # add this PersonIChat to the usr
        myChatHistory.append(new_chat_person)
        usr_ndb_info.myChatHistory = myChatHistory

    usr_ndb_info.put()
