__author__ = 'Qingchuan'
import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        Error_code = self.request.get("Error_code")
        error_msg = ""
        if(Error_code == "404"):
            error_msg = "Stream Not Found"
        elif(Error_code == "406"):
            error_msg = "The stream you want to delete is not exist"
        template_values = {
            "error_msg": error_msg,
        }
        template = JINJA_ENVIRONMENT.get_template('myhtml/Errorpage.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/myhtml/Errorpage.html', MainHandler),
], debug=True)
