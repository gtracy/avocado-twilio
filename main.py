import os
import logging
from django.utils import simplejson

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import configuration


# Data model to store callers
class User(db.Model):
  phone = db.StringProperty()
  date  = db.DateTimeProperty(auto_now_add=True)
##

class MainHandler(webapp.RequestHandler):
    def post(self):
    
      # who called? and what did they say?
      phone = self.request.get("From")
      msg = self.request.get("Body")
      
      # take a look at the request and see if it is valid
      # if it is, process the request
      if msg.isdigit():
        response = extract_bus_result(msg)
      else:
        response = 'Yah. Nice try. I need a stop ID dude'
        
      # reply back to twilio with twiml        
      self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
      self.response.out.write('<Response><Sms>%s</Sms></Response>' % response)
      return
      

## end MainHandler


application = webapp.WSGIApplication([('/admin/persistcounters', PersistCounterHandler),
                                      ],
                                     debug=True)

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
