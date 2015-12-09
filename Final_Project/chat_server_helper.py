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
                break

        self.response.write(chatHistory)


app = webapp2.WSGIApplication([
    ('/retrieve_Dialog_history', RetrieveDialogHistory),
], debug=True)
