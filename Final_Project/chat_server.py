__author__ = 'Qingchuan'

import webapp2
import Person
import management
import json

from google.appengine.api import channel


def notifiyclient(clientID, caller, chatcontent, messageType):
        # set caller's new message unread to True
        usr_i_info = Person.Person.query(
                    ancestor=management.person_key(clientID)).fetch(1)[0]

        if messageType == "chatroom":
            j_messagefrom = {"message_type": "chatroom",
                             "new_message_from": caller,
                             "chatcontent": chatcontent}
            message = json.dumps(j_messagefrom)

            possible_client1 = clientID+"management_page"
            possible_client2 = clientID+"chatroom"
            print("start to send messages from chat server to "+possible_client1)
            channel.send_message(possible_client1, message)
            channel.send_message(possible_client2, message)

        if messageType == "newmatchnotification":
            num_of_matches = usr_i_info.usr_notification
            j_num_matches = {"message_type": "newmatchnotification",
                            "num_of_matches": num_of_matches}
            message = json.dumps(j_num_matches)
            possible_client1 = clientID+"management_page"
            possible_client2 = clientID+"preferencepage"
            print("start to send messages to "+possible_client1+" and "+possible_client2)
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
                notifiyclient(usr_name, "", "", "newmatchnotification")
            else:
                print("No notification unread")


class NewMessageHandler(webapp2.RequestHandler):
    def post(self):
        caller = self.request.get('client_ID')
        chatcontent = self.request.get('chatcontent')
        receiver = self.request.get('receiverID')
        print(caller + " is sending following message to " + receiver)
        print(chatcontent)

        # =========================================================================================
        # update the backend server

        #                 PART 1 update caller database

        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(caller)).fetch(1)[0]
        chat_history = usr_personal_info.myChatHistory
        # go over the chat history to find the receiver if any
        new_receiver = True
        j_new_message = {"myMessage": True,
                        "content": chatcontent}
        message = json.dumps(j_new_message)
        for chat_record in chat_history:
            chat_person = chat_record.person_account
            # not a new receiver
            if chat_person == receiver:
                new_receiver = False
                chat_record.new_message_unread = True
                # append the message
                print("add to a existing chat record")
                if chat_record.chat_history:
                    chat_record.chat_history.append(message)
                else:
                    chat_record.chat_history = [message]
                break

        if new_receiver:
            # create a new chat record
            print("add a new chat record")
            new_chat_record = Person.PersonIChat()
            new_chat_record.person_account = receiver
            new_chat_record.new_message_unread = True
            new_chat_record.chat_history = [message]
            # add this record
            if usr_personal_info.myChatHistory:
                usr_personal_info.myChatHistory.append(new_chat_record)
            else:
                usr_personal_info.myChatHistory = [new_chat_record]

        usr_personal_info.put()

        #                 PART 2 update receiver database

        usr_personal_info = Person.Person.query(
            ancestor=management.person_key(receiver)).fetch(1)[0]
        chat_history = usr_personal_info.myChatHistory
        # go over the chat history to find the caller if any
        new_caller = True
        j_new_message = {"myMessage": False,
                        "content": chatcontent}
        message = json.dumps(j_new_message)
        for chat_record in chat_history:
            chat_person = chat_record.person_account
            # not a new caller
            if chat_person == caller:
                new_caller = False
                chat_record.new_message_unread = True
                # append the message
                print("add to a existing chat record")
                chat_record.chat_history.append(message)
                break

        # a new caller
        if new_caller:
            # create a new chat record
            print("add a new chat record")
            new_chat_record = Person.PersonIChat()
            new_chat_record.person_account = caller
            new_chat_record.new_message_unread = True
            new_chat_record.chat_history = [message]
            # add this record
            if usr_personal_info.myChatHistory:
                usr_personal_info.myChatHistory.append(new_chat_record)
            else:
                usr_personal_info.myChatHistory = [new_chat_record]

        usr_personal_info.put()

        # end of backend server update
        # =======================================================================================================

        # send notification to the receiver
        # Note: for now the receiver should in management page to get this notice
        notifiyclient(receiver, caller, chatcontent, "chatroom")



app = webapp2.WSGIApplication([
    ('/get_chat_channel_token', TokenGenerator),
    ('/newMessage', NewMessageHandler),
    ('/opened_from_management', OpenedPage,)
], debug=True)
