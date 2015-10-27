__author__ = 'Qingchuan'

import webapp2
import json
import stream_bundle
import math
from google.appengine.api import images


def distance_on_unit_sphere(lat1, long1, lat2, long2):

        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi/180.0

        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians

        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians

        # Compute spherical distance from spherical coordinates.

        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta', phi')
        # cosine( arc length ) =
        #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length

        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
               math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.
        return arc * 6.371 * 1000000

class MainHandler(webapp2.RequestHandler):
    def get(self):
        device_lat = str(self.request.params['device_lat'])
        device_long = str(self.request.params['device_long'])
        #distance_on_unit_sphere(float("12.456"),float("-23.45"),float(device_lat),float(device_long))

        # retrieve all streams, outer loop: iterate through streams, inner loop: iterate through pics lat and long
        streamlist = stream_bundle.myStream.query().order(-stream_bundle.myStream.lastNewPicture).fetch()

        pic_url = list()
        stream_name = list()
        stream_owner = list()
        dist_dev2pic = list()

        for stream in streamlist:
            if stream.numOfPictures > 0:
                l_stream_name = stream.streamname
                l_stream_owner = str(stream.streamOwner)
                if l_stream_owner.find("@") < 0:
                    l_stream_owner = l_stream_owner+"@gmail.com"
                blob_key_list = stream.blob_key
                pic_lat_list = stream.pic_lat
                pic_long_list = stream.pic_long
                for i in range(len(pic_lat_list)):
                    pic_lat = pic_lat_list[i]
                    pic_long = pic_long_list[i]
                    pic_blob_key = blob_key_list[i]
                    if pic_lat != "None":
                        dist_pic2dev = distance_on_unit_sphere(float(pic_lat),float(pic_long),
                                                               float(device_lat),float(device_long))

                        # update the three list
                        pic_url.append(images.get_serving_url(pic_blob_key))
                        dist_dev2pic.append(int(dist_pic2dev))
                        stream_name.append(l_stream_name)
                        stream_owner.append(l_stream_owner)


        dictPassed = {'pic_url':pic_url, 'stream_names':stream_name, 'dist_dev2pic':dist_dev2pic,
                      'stream_owner': stream_owner}
        jsonObj = json.dumps(dictPassed, sort_keys=True, indent=4, separators=(',', ': '))
        self.response.write(jsonObj)



app = webapp2.WSGIApplication([
    ('/viewNearby', MainHandler),
], debug=True)
