
import cookielib
import urllib2
from getpass import getpass
from urllib import urlencode

class Youmint:
    def __init__(self):
        self.url = 'http://www.youmint.com/LoginVerification.php?name=shadyabhi&pass=manabhi&agreement=true&checkvalue=false'
        
    def set_credentials(self, username, password):
        self.username = username
        self.password = password
    
    def set_message(self, message):
        self.message = message
        #To convert spaces to + and things like that
        self.message = urlencode({'message':self.message})  
        self.message = self.message[self.message.find("=")+1:]

    def set_number(self, number):
        self.phone_number = number
        
    def send_sms(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        try:
            usock = opener.open(self.url, "")
        except IOError:
            return False

        #Headers added to avoid the Missing data, try again!! error
        opener.addheaders = [('Referer','Referer: http://www.youmint.com/FreeSmsNri.html'),('User-Agent','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.5.3 GTB7.0')]

        url_send = "http://www.youmint.com/SendingSms.php?ToMobileNumber="+self.phone_number+"&Message="+self.message+"&FromMobileNumber=9950677689"
        
        #SMS send POST
        try:
            send = opener.open(url_send,"")
            return True
        except IOError:
            print "Error sending SMS\nExiting now.."
            return False
