import SimpleHTTPServer
import SocketServer
import os
import urllib
import urllib2
import unittest
import proxy_server
from geopy.geocoders.base import Geocoder

### UNIT TEST(S) to test Proxy in Geocoder base class ###
###
### Solution requires that proxy_server.py is run to start simple proxy
### daemon proxy PID is located in /var/run/proxy_server.pid and can be 
### stoped using the command `kill -9 $(cat /var/run/proxy_server.pid)`


class ProxyTestCase(unittest.TestCase):
    def setUp(self):
       
        # Backup environ settings
        self.orig_http_proxy = os.environ['http_proxy'] if os.environ.has_key('http_proxy') else None
        
        # Get HTTP for comparison before proxy test
        base_http = urllib2.urlopen('http://www.blankwebsite.com/')
        base_html = base_http.read()
        self.noproxy_data = base_html if base_html else None

        # Create the proxy instance
        self.proxyd = proxy_server.ProxyServer()
        # Set the http_proxy environment variable with Proxy_server default value
        os.environ['http_proxy'] = self.proxyd.get_proxy_url()

    def teardown(self):
        if self.orig_http_proxy:
            os.environ['http_proxy'] = self.orig_http_proxy
        else:
            del os.environ['http_proxy']


    def test_proxy(self):
        ''' Test of OTB Geocoder Proxy functionality works'''
        class DummyGeocoder(Geocoder):
            def geocode(self, location):
                geo_request = urllib2.urlopen(location)
                geo_html = geo_request.read()
                return geo_html if geo_html else None

        '''Testcase to test that proxy standup code works'''
        geocoder_dummy = DummyGeocoder()
        self.assertTrue(self.noproxy_data, geocoder_dummy.geocode('http://www.blankwebsite.com/'))

if __name__ == '__main__':
    unittest.main()