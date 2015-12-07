__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json
import time

from google.appengine.api import channel


def notifiyclient(clientID, num_of_matches):
        j_num_matches = {"num_of_matches": num_of_matches}
        message = json.dumps(j_num_matches)
        channel.send_message(clientID, message)


class TokenGenerator(webapp2.RequestHandler):
    def get(self):
        usr_name = self.request.get('client_ID')

        print("Client ID = " +usr_name)

        # TODO
        # go to database and see if usr has

        # create a channel token
        token = channel.create_channel(usr_name)
        self.response.write(token)


class OpenedPage(webapp2.RequestHandler):
    def post(self):
        usr_name = self.request.get('client_ID')
        source = self.request.get('source')
        client_ID = usr_name+source

        # fetch usr info
        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(usr_name)).fetch(1)

        if usr_personal_info:
            usr_personal_info_data = usr_personal_info[0]
            num_notification = usr_personal_info_data.usr_notification
            usr_checked_notification = usr_personal_info_data.usr_viewed_updates

            if num_notification > 0 and (not usr_checked_notification):
                print("Send "+client_ID + " "+ str(num_notification) + "notifications\n")
                notifiyclient(client_ID, num_notification)
            else:
                print("No notification unread")

        i = 7
        while i < 4:
            notifiyclient(usr_name, i)
            i = i+1
            time.sleep(5)


app = webapp2.WSGIApplication([
    ('/get_channel_token', TokenGenerator),
    ('/opened', OpenedPage,)
], debug=True)
