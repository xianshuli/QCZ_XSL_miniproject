__author__ = 'Qingchuan'

import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/myhtml/popup_about.html')
        self.response.write(template.render())


class HelpHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/myhtml/popup_help.html')
        self.response.write(template.render())


class ReportIssueHandler(webapp2.RequestHandler):
    def get(self):
        usr = self.request.get('usr')
        #print(usr+" wants to report an issue")

        template_values = {
            'usr': usr,
        }
        template = JINJA_ENVIRONMENT.get_template('/myhtml/popup_report_issue.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/popup_about', AboutHandler),
    ('/popup_help', HelpHandler),
    ('/popup_report_issue', ReportIssueHandler),
], debug=True)
