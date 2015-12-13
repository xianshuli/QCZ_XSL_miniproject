__author__ = 'Qingchuan'

import webapp2
import json

from google.appengine.api import mail


class EmailUsrIssues(webapp2.RequestHandler):
    def post(self):
        usr_issue = self.request.get('usr_issue')
        usr_account = self.request.get('usr_account')
        print(usr_issue)

        mail.send_mail(sender=usr_account, to="<lixianshu1992@gmail.com>", subject="Usr Reported Issue", body=usr_issue)

        self.response.write("Success")

app = webapp2.WSGIApplication([
    ('/send_usr_report_issue', EmailUsrIssues),
], debug=True)
