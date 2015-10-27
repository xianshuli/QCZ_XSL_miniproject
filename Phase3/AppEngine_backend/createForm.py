__author__ = 'Qingchuan'

import webapp2
import json
import datetime
import unicodedata
import stream_bundle
from management import stream_key

from google.appengine.api import users
from google.appengine.api import search
from google.appengine.api import mail
from google.appengine.ext import ndb
import management

class MainHandler(webapp2.RequestHandler):
    def post(self):
        body2 = self.request.body
        j = json.loads(body2)
        streamName = j["name"]
        streamTag = j["tag"]
        urltocover = j["urltocover"]
        invitelist = j["emaillist"]
        add_msg = j['add_msg']
        createDate = datetime.datetime.now()
        usr = users.get_current_user()

        # check if the stream is already created

        query_string = "stream_name: "+streamName
        query = search.Query(query_string=query_string)



        index = search.Index(name='ConnexStreamPool', namespace="Connex")
        result = index.search(query)
        for doc in result.results:
            singleStream = stream_bundle.myStream.query(ancestor= management.stream_key(str(doc.fields[0].value))).fetch()
            if(len(singleStream)>0 ):
                if(singleStream[0].streamname == streamName):
                    Duplicate = {
                        'duplicate': "dup",
                        'aha': singleStream[0].streamname
                    }
                    self.response.write(json.dumps(Duplicate))
                    return





        # add the stream_name to our search database for later search operation
        # step1 create the document
        # get doc_id
        doc_id = stream_bundle.doc_id.query(ancestor=ndb.Key('Connex','Coonex')).fetch(1)[0]
        mydoc_id = doc_id.doc_id
        doc_id.doc_id = mydoc_id+1
        doc_id.put()
        stream_document = search.Document(
            doc_id=str(mydoc_id),
            fields=[
                search.TextField(name='stream_name', value=streamName)
            ]
        )
        # step2 retrieve the index if not exit create one, index name is ConnexStreamPool
        myIndex = search.Index(name='ConnexStreamPool', namespace="Connex")

        # step3 put the document into the index


        myNewStream = stream_bundle.myStream(parent=stream_key(usr_name=streamName),
                                             streamOwner=usr,
                                             streamname=streamName,
                                             urltoCoverPhoto=urltocover,
                                             doc_id=stream_document.doc_id,
                                             lastNewPicture=None,
                                             createTime=createDate.date(),
                                             numOfPictures=0,
                                             numOfViews=0,
                                             )

        myIndex.put(stream_document)
        newStreamKey = myNewStream.put()

        # get the stream_bundles
        streamIOwn_query = stream_bundle.stream_bundles.query(
            ancestor=stream_key(usr)).fetch(1)
        stream_bundles_entity = streamIOwn_query[0]
        stream_bundles_entity.stream_iownlist.append(newStreamKey)
        stream_bundles_entity.put()

        # at last we send out invite email
        if len(invitelist) > 0:
            self.inviteEmail(invitelist, add_msg)

    def inviteEmail(self, emaillist, add_msg):
        inviteList = list()
        # pre-processing the email receiver list
        step1_list = emaillist.split(',')
        for entry in step1_list:
            entry = entry.strip()
            inviteList.append(entry)

        sender_address = "aptminiprojectzqc@gmail.com"
        subject = "Connex inviatation!"
        body = "Join us at http://connexversion3.appspot.com!\n\n\n"+add_msg
        body = body+"\n\nHave a nice day!\n\nBest, Qingchuan and Xianshu"

        for receiver in inviteList:
            self.response.write(receiver)
            mail.send_mail(sender=sender_address, to="<"+receiver+">", subject=subject, body=body)



app = webapp2.WSGIApplication([
    ('/createForm', MainHandler),
], debug=True)
