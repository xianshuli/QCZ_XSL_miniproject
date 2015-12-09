__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json
import time

from google.appengine.api import channel


def notifiyclient(clientID):
        # get num of notifications
        usr_i_info = Person.Person.query(
                    ancestor=management.person_key(clientID)).fetch(1)[0]
        num_of_matches = usr_i_info.usr_notification
        j_num_matches = {"num_of_matches": num_of_matches}
        message = json.dumps(j_num_matches)
        possible_client1 = clientID+"management_page"
        possible_client2 = clientID+"preferencepage"
        print("start to send messages")
        channel.send_message(possible_client1, message)
        channel.send_message(possible_client2, message)


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

        # fetch usr info
        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(usr_name)).fetch(1)

        if usr_personal_info:
            usr_personal_info_data = usr_personal_info[0]
            num_notification = usr_personal_info_data.usr_notification
            usr_checked_notification = usr_personal_info_data.usr_viewed_updates

            if num_notification > 0 and (not usr_checked_notification):
                print("Send "+usr_name + " "+ str(num_notification) + "notifications\n")
                notifiyclient(usr_name)
            else:
                print("No notification unread")


app = webapp2.WSGIApplication([
    ('/get_channel_token', TokenGenerator),
    ('/opened', OpenedPage,)
], debug=True)
