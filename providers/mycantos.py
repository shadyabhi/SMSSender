
import cookielib
import urllib2
from getpass import getpass

import logging, sys

logger= logging.getLogger(__file__)
logging.basicConfig( stream=sys.stdout, level=logging.DEBUG, format='%(filename)s:%(lineno)s %(levelname)s:%(message)s')

class MyCantos:
    def __init__(self):
        self.url = 'http://www.mycantos.com/'
        
    def set_credentials(self, username, password):
        self.username = username
        self.password = password
    
    def set_message(self, message):
        self.message = message
        
    def set_number(self, number):
        self.phone_number = number
        
    def send_sms(self):
        data = 'username='+self.username+'&password='+self.password+'&checklogin=1'
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        try:
            logger.debug("Sending request for login...")
            print "Sending request for login..."
            usock = opener.open(self.url, data)
            logger.debug("We are logged in to the site")
        except IOError:
            print "Error fetching page www.mycantos.com\nExiting now.."
            return False

        #Headers added to avoid the Missing data, try again!! error
        opener.addheaders = [('Referer','http://www.mycantos.com/sendSMS.php'),('User-Agent','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.5.3 GTB7.0')]
        data_to_send = 'checkSMS=1&SMSnumber='+self.phone_number+'&SMSmessage='+self.message
        url_send = "http://www.mycantos.com/sendSMStoanyone.php"

        #SMS send POST
        try:
            logger.debug("Sending SMS...")
            send = opener.open(url_send,data_to_send)
            logger.debug("SMS sent")
            return True
        except IOError:
            logger.debug("Could not connect to remote server")
            return False
