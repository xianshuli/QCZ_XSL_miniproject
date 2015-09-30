__author__ = 'Qingchuan'

import webapp2
import json
import stream_bundle
import management


class MainHandler(webapp2.RequestHandler):
    def post(self):
        body2 = self.request.body
        j = json.loads(body2)
        usr = j["usr"]
        stream_to_sub = j["stream_name"]

        targetStream = stream_bundle.myStream.query(ancestor= management.stream_key(stream_to_sub)).fetch(1)[0]
        subStreamKey = targetStream.key

        streamIOwn_query = stream_bundle.stream_bundles.query(
            ancestor=management.stream_key(usr)).fetch(1)
        stream_bundles_entity = streamIOwn_query[0]
        stream_bundles_entity.stream_isublist.append(subStreamKey)
        stream_bundles_entity.put()

app = webapp2.WSGIApplication([
    ('/subScribeme', MainHandler)
], debug=True)