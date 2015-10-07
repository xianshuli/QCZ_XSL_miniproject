__author__ = 'Qingchuan'

import webapp2
import jinja2
import os

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/myhtml/Create.html')
        logout_url = users.create_logout_url('/')

        curr_usr = users.get_current_user()
        template_values = {
            'usr': curr_usr,
            'logout_url': logout_url,
        }

        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/myhtml/Create.html', MainHandler),
], debug=True)
