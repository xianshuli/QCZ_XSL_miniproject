#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
        curr_usr = users.get_current_user()
        if curr_usr:
            self.redirect("management")
            urltomanage = "management"
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            urltomanage = ""
            url = users.create_login_url("management")
            url_linktext = 'Login'

        template_values = {
            'usr': curr_usr,
            'url': url,
            'url_linktext': url_linktext,
            'url2man': urltomanage,
        }

        template = JINJA_ENVIRONMENT.get_template('/myhtml/index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
