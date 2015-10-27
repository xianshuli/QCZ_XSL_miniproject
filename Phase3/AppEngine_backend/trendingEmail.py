__author__ = 'Qingchuan'

import webapp2
import json
import stream_bundle

from google.appengine.api import mail

class EmailRateController(webapp2.RequestHandler):
    def get(self):
        # step1 grab count and setting
        emailRateSetting = stream_bundle.emailrate.query().fetch()[0]
        currentCount = emailRateSetting.count
        currentRateSetting = emailRateSetting.rate_setting
        if(currentRateSetting == 0):
            pass
        elif(currentRateSetting == 1):
            currentCount = 0
            self.sendTheMail()
        elif(currentRateSetting == 2):
            if(currentCount == 11):
                currentCount = 0
                self.sendTheMail()
            else:
                currentCount = currentCount+1
        else:
            if(currentCount == 287):
                currentCount = 0
                self.sendTheMail()
            else:
                currentCount = currentCount+1

        emailRateSetting.count = currentCount
        emailRateSetting.put()

    def sendTheMail(self):
        # get the top3 trending stream
        top3list = stream_bundle.top3streams.query().fetch()[0].top3list
        stream_name_list = list()
        stream_url_list = list()
        for stream in top3list:
            if str(stream) is not "":
                stream_name_list.append(str(stream))
                stream_url_list.append("http://connexversion3.appspot.com/viewStream?Stream_id="+str(stream))

        sender_address = "aptminiprojectzqc@gmail.com"
        subject = "Check out Connex new Trending!"
        body = "The top 3 trending so far is(are):\n\n"
        for i in range(len(stream_name_list)):
            body = body + "Stream name: "+stream_name_list[i] + "   Go and see: " + stream_url_list[i]+"\n"

        body = body+"\n\nHave a nice day!\n\nBest, Qingchuan and Xianshu"

        mail.send_mail(sender=sender_address, to="<nima.dini@utexas.edu>", subject=subject, body=body)



class changeEmailRateHandler(webapp2.RequestHandler):
    def post(self):
        body2 = self.request.body
        js_c = json.loads(body2)
        rate = js_c['rateoption']
        # get the rating variable
        rateing = stream_bundle.emailrate.query().fetch()[0]
        if(rate == 'option1'):
            self.response.write('option1')
            rateing.rate_setting = 0
        elif(rate == 'option2'):
            self.response.write('option2')
            rateing.rate_setting = 1
        elif(rate == 'option3'):
            self.response.write('option3')
            rateing.rate_setting = 2
        else:
            self.response.write('option4')
            rateing.rate_setting = 3

        # reset the count
        rateing.put()


class sendBackRateHandler(webapp2.RequestHandler):
    def get(self):
        emailRateSetting = stream_bundle.emailrate.query().fetch()[0]
        currentRateSetting = emailRateSetting.rate_setting
        currentSetting = {"currentSetting": currentRateSetting}
        self.response.write(json.dumps(currentSetting))

app = webapp2.WSGIApplication([
    ('/changeEmailRate', changeEmailRateHandler),
    ('/emailTrendingController', EmailRateController),
    ('/givemeEmailRate', sendBackRateHandler),
], debug=True)