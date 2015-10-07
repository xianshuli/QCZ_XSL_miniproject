__author__ = 'qingchuan'

import webapp2
import jinja2
import os
import stream_bundle
import json

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import search

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def stream_key(usr_name):
    """Constructs a Datastore key for a usr entity.
    """
    return ndb.Key('ConnexUser', str(usr_name))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        curr_usr = self.request.get("usr")
        logout_url = users.create_logout_url('/')
        if not curr_usr:
            curr_usr = users.get_current_user()

        streamIOwn_query = stream_bundle.stream_bundles.query(
            ancestor=stream_key(curr_usr)).fetch(1)

        # create the doc_id counter if not exist
        doc_id = stream_bundle.doc_id.query(ancestor=ndb.Key('Connex','Coonex')).fetch(1)
        if not doc_id:
            doc_id = stream_bundle.doc_id(parent=ndb.Key('Connex','Coonex'))
            doc_id.doc_id = 0
            doc_id.put()

        # create the top3 list if not exist
        top3list = stream_bundle.top3streams.query(ancestor=ndb.Key('Connex','Coonex')).fetch(1)
        if not top3list:
            singleTop3List = stream_bundle.top3streams(parent=ndb.Key('Connex','Coonex'))
            singleTop3List.put()

        # create the rate setting if not exist, the default is no report
        emailrateset = stream_bundle.emailrate.query(ancestor=ndb.Key('Connex','Coonex')).fetch(1)
        if not emailrateset:
            emailrateset = stream_bundle.emailrate(parent=ndb.Key('Connex','Coonex'))
            emailrateset.count = 0
            emailrateset.rate_setting = 0
            emailrateset.put()

        if not streamIOwn_query:
            streamIOwn = stream_bundle.stream_bundles(parent= stream_key(curr_usr))
            streamIOwn.put()
            myStreams = list()
            subStreams = list()
        else:
            myOwnStream = streamIOwn_query[0].stream_iownlist
            mySubStream = streamIOwn_query[0].stream_isublist
            myStreams = list()
            subStreams = list()
            validsubStreams = list()
            for streams in myOwnStream:
                    myStreams.append(streams)
            for streams in mySubStream:
                    # first test existence
                    if streams.get() is not None:
                        validsubStreams.append(streams)
                        subStreams.append(streams)
            streamIOwn_query[0].stream_isublist = validsubStreams
            streamIOwn_query[0].put()

        template = JINJA_ENVIRONMENT.get_template('management.html')


        template_values = {
            'usr': curr_usr,
            'streamIOwn': myStreams,
            'streamIOwnLength': len(myStreams),
            'streamISub': subStreams,
            'streamISubLength': len(subStreams),
            'logout_url': logout_url,
        }

        self.response.write(template.render(template_values))


class DeleteStreamIOwnHandler(webapp2.RequestHandler):
    def post(self):
        body = self.request.body

        # parse the json
        j = json.loads(body)
        deletelist = j["namelist"]

        # get the usr streamIOwn list and delete the selected entities
        usr = users.get_current_user()
        streamIOwn_query = stream_bundle.stream_bundles.query(
            ancestor=stream_key(usr)).fetch(1)
        stream_bundles_entity = streamIOwn_query[0]
        stream_key_list = stream_bundles_entity.stream_iownlist

        tryToDeleteAlreadyDelete = False
        for name in deletelist:
            findamatch = False
            for keytodelete in stream_key_list:
                if(keytodelete.get() is not None and keytodelete.get().streamname == name):
                    findamatch = True
                    # get the blobkey of this stream first and delete the related photos
                    blokkeylist = keytodelete.get().blob_key
                    for blobkey in blokkeylist:
                        blobstore.delete(blobkey)

                    # delete the corresponding document in Search Index
                    index = search.Index(name='ConnexStreamPool', namespace="Connex")
                    index.delete(keytodelete.get().doc_id)
                    keytodelete.delete()
                    break
            if not findamatch:
                tryToDeleteAlreadyDelete = True

        deleteStatus = {"deleteStatus":tryToDeleteAlreadyDelete}
        # update the stream_iownlist
        b = list()
        for i in range(len(stream_key_list)):
            if(stream_key_list[i].get() is not None):
                b.append(stream_key_list[i])
        stream_bundles_entity.stream_iownlist = b
        stream_bundles_entity.put()

        self.response.write(json.dumps(deleteStatus))

# used on management page to unsubscribe streams I sub
class DeleteStreamISubHandler(webapp2.RequestHandler):
    def post(self):
        body = self.request.body

        # parse the json
        j = json.loads(body)
        deletelist = j["indexlist"]

        # get the usr streamISub list and delete the selected entities
        usr = users.get_current_user()
        streamIOwn_query = stream_bundle.stream_bundles.query(
            ancestor=stream_key(usr)).fetch(1)
        stream_bundles_entity = streamIOwn_query[0]
        stream_key_list = stream_bundles_entity.stream_isublist

        # update the stream_isublist
        b = list()
        tryToUnsubAlreadyUnsub = False
        for name in deletelist:
            findname = False
            for key in stream_key_list:
                if not (key.get() is not None and key.get().streamname == name):
                    b.append(key)
                else:
                    findname = True
            if not findname:
                tryToUnsubAlreadyUnsub = True
            stream_key_list = b

        stream_bundles_entity.stream_isublist = stream_key_list
        stream_bundles_entity.put()

        unSubStatus = {"unSubStatus":tryToUnsubAlreadyUnsub}
        self.response.write(json.dumps(unSubStatus))


# use on ViewSingle page to unsubscribe stream
class DeleteStreamIViewISubHandler(webapp2.RequestHandler):
    def post(self):
        body2 = self.request.body
        j = json.loads(body2)
        usr = j["usr"]
        stream_to_del = j["stream_name"]

        streamIOwn_query = stream_bundle.stream_bundles.query(
            ancestor=stream_key(usr)).fetch(1)
        stream_bundles_entity = streamIOwn_query[0]
        # get the list I sub
        listIsub = stream_bundles_entity.stream_isublist
        # remove stream_to_sub from listIsub, since stream name is unique we use remove
        for key in listIsub:
            if(key.get().streamname == stream_to_del):
                listIsub.remove(key)
                break
        stream_bundles_entity.stream_isublist = listIsub
        stream_bundles_entity.put()


app = webapp2.WSGIApplication([
    ('/management.html', MainHandler),
    ('/deleteStreamIOwn', DeleteStreamIOwnHandler),
    ('/deleteStreamISub', DeleteStreamISubHandler),
    ('/deleteTheStreamISub', DeleteStreamIViewISubHandler),
], debug=True)
