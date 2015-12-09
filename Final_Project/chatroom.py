__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import Person
import management

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')

        print(str(current_usr) + "is in chat room now")

        # get the chat list
        usr_ndb_info = Person.Person.query(ancestor= management.person_key(str(current_usr))).fetch(1)[0]
        chat_list = usr_ndb_info.myChatHistory

        template_values = {
            'logout_url': logout_url,
            'usr': current_usr,
            'chat_list': chat_list,

        }

        template = JINJA_ENVIRONMENT.get_template('/myhtml/chatroom.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/chatroom', MainHandler)
], debug=True)
