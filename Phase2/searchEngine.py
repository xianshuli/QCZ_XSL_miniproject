__author__ = 'Qingchuan'

import webapp2
import jinja2
import os
import json
import stream_bundle
import management
from ViewAllStream import streamToShow
from google.appengine.api import search
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('myhtml/SearchHome.html')

        curr_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')

        template_values = {
            'usr': curr_usr,
            'logout_url': logout_url,
            'hasResult': True,
        }

        self.response.write(template.render(template_values))

    def post(self):
        # A query string
        keyword = self.request.get('SearchInput')

        # Build the QueryOptions
        # Create a FieldExpression
        query_options = search.QueryOptions(
            limit=5,
        )

        # Build the Query and run the search
        query = search.Query(query_string=keyword, options=query_options)

        index = search.Index(name='ConnexStreamPool', namespace="Connex")
        result = index.search(query)
        streamlist = list()

        for doc in result.results:
            singleStream = \
            stream_bundle.myStream.query(ancestor=management.stream_key(str(doc.fields[0].value))).fetch()[0]
            streamlist.append(singleStream)

        streams_to_show = list()

        for stream in streamlist:
            if stream.numOfPictures > 0:
                l_stream_name = stream.streamname
                i_stream_coverurl = stream.urltoCoverPhoto
                hasCover = True
                i_stream_blobKey = ""
                if (i_stream_coverurl == ""):
                    hasCover = False
                    i_stream_blobKey = stream.blob_key[0]
                i_stream = streamToShow(l_stream_name, i_stream_coverurl, i_stream_blobKey, hasCover)
                streams_to_show.append(i_stream)

        curr_usr = users.get_current_user()
        logout_url = users.create_logout_url('/')
        if len(streams_to_show) > 0:
            hasResult = True
        else:
            hasResult = False

        template_values = {
            'usr': curr_usr,
            'streams_to_show': streams_to_show,
            'logout_url': logout_url,
            'hasResult': hasResult,
        }
        template = JINJA_ENVIRONMENT.get_template('myhtml/SearchHome.html')
        self.response.write(template.render(template_values))


class KeyStoreHandler(webapp2.RequestHandler):
    def get(self):
        inputText = self.request.get("query")
        print(inputText)
        print(type(inputText))
        # A query string
        keyword = ".*"
        # print(keyword)
        # Build the Query and run the search
        query = search.Query(query_string=keyword)
        index = search.Index(name='ConnexStreamPool', namespace="Connex")
        result = index.search(query)
        streamlist = list()

        for doc in result.results:
            singleStream = \
                stream_bundle.myStream.query(ancestor=management.stream_key(str(doc.fields[0].value))).fetch()[0]
            streamlist.append(singleStream.streamname)

        # for doc in result.results:
        #     streamlist.append(str(doc.fields[0].value))
        print(streamlist)
        output = [];
        for streamName in streamlist:
            if inputText in streamName:
                output.append(streamName)
        print(output)
        output = json.dumps(output)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(output)




app = webapp2.WSGIApplication([
    ('/myhtml/SearchHome.html', MainHandler),
    ('/searchEngine', MainHandler),
    ('/keyStore', KeyStoreHandler)
], debug=True)
