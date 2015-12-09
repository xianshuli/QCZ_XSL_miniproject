__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json

from google.appengine.api import users


class RetrieveDialogHistory(webapp2.RequestHandler):
    def get(self):
        curr_usr = users.get_current_user()
        target_usr = self.request.get('client_ID')
        print("Retriving "+str(curr_usr)+"'s dialog history with "+target_usr)

        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(str(curr_usr))).fetch(1)[0]
        myChatHistory = usr_personal_info.myChatHistory

        chatHistory = []

        for personIchat in myChatHistory:
            if personIchat.person_account == target_usr:
                # retrive the chat dialog history a JSONproperty Array
                for chatEntry in personIchat.chat_history:
                    chatHistory.append(chatEntry)
                # set the new_message_unread to False
                personIchat.new_message_unread = False
                break

        usr_personal_info.put()

        self.response.write(chatHistory)


class GetUnreadList(webapp2.RequestHandler):
    def get(self):
        curr_usr = users.get_current_user()
        curr_usr = str(curr_usr)

        # retrive his/her chat history
        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(str(curr_usr))).fetch(1)[0]
        myChatHistory = usr_personal_info.myChatHistory

        unreadList = []

        for personIchat in myChatHistory:
            if personIchat.new_message_unread is True:
                unreadList.append(str(personIchat.person_account))

        self.response.write(unreadList)


class SetMyUnreadToFalse(webapp2.RequestHandler):
    def get(self):
        curr_usr = users.get_current_user()
        curr_usr = str(curr_usr)
        target_usr = self.request.get('whoichat')

        # retrive his/her chat history
        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(str(curr_usr))).fetch(1)[0]
        myChatHistory = usr_personal_info.myChatHistory

        for personIchat in myChatHistory:
            if personIchat.person_account == target_usr:
                personIchat.new_message_unread = False
                break

        usr_personal_info.put()


app = webapp2.WSGIApplication([
    ('/retrieve_Dialog_history', RetrieveDialogHistory),
    ('/get_unread_candidates', GetUnreadList),
    ('/setMyUnreadToFalse', SetMyUnreadToFalse),
], debug=True)
