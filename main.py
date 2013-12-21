import cgi
import datetime
import urllib
import urllib2
import wsgiref.handlers
import os
import logging

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from xml.dom.minidom import parse, parseString

class MainPage(webapp.RequestHandler):
    def get(self):
      
      template_values = {
        }
      
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))

class ContentPage(webapp.RequestHandler):
    def get(self):
      file = urllib2.urlopen('http://www.mta.info/status/serviceStatus.txt')
      data = file.read()
      file.close()
      dom = parseString(data)
      
      subways = []

      for x in range(0, 9):
          line = dom.getElementsByTagName('name')[x].toxml()
          status = dom.getElementsByTagName('status')[x].toxml()
          line = line.replace('<name>','').replace('</name>','')
          status = status.replace('<status>','').replace('</status>','')
          subways.append({'status': status, 'line': line})
      
      template_values = {
        'subways': subways
        }
      
      path = os.path.join(os.path.dirname(__file__), 'content.html')
      self.response.out.write(template.render(path, template_values))


def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', MainPage),
                                      ('/content', ContentPage)], debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()