import os
from google.appengine.ext import webapp
from webapp2_extras import jinja2

class Http404(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    self.code = 404

class Http500(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    self.code = 500

class BaseHandler(webapp.RequestHandler):
  debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

  @webapp.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def handle_exception(self, exception, debug_mode):
    if debug_mode:
      webapp.RequestHandler.handle_exception(self, exception, debug_mode)
    else:
      self.response.clear()
      self.response.set_status(exception.code)
      self.render_template(unicode(exception.code)+".html",
        { 'title': unicode(exception.code) + "!",
          'errorCode':exception.code,
          'errorMessage':exception.message,
          'requestURL':self.request.url,
        })

  def render_template(self, filename, template_args):
    self.response.out.write(self.jinja2.render_template(filename, **template_args))


#TODO: move this into its own file (with the event link handler)
from google.appengine.api import memcache
from google.appengine.ext.db import GqlQuery
from scripts.database_models.homepageslide import HomepageSlide
from scripts.gaesettings import gaesettings
class HomePageHandler(BaseHandler):
  def get(self):
    slides = memcache.get('homepageSlides')
    if slides == None:
      slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True ORDER BY DisplayOrder ASC").fetch(gaesettings.MaxHomepageSlides);
      if slides != []:
        memcache.set('homepageSlides', slides)

    self.render_template("index.html",
    { 'title':"Christian Campus Fellowship, Rolla Missouri",
      'slides':slides,
      'HomepageSlideRotationDelay':gaesettings.HomepageSlideRotationDelay,
    })


class SlideHandler(BaseHandler):
    def get(self):
      dbSlide = GqlQuery("SELECT * FROM HomepageSlide WHERE CompleteURL = :1", self.request.path).get()
      if dbSlide and dbSlide.Enabled == True:
        self.render_template("slide.html",
          { 'title':dbSlide.Title,
            'slide':dbSlide,
          })
      else:
        raise Http404("Page Does Not Exist")

application = webapp.WSGIApplication([
  ('/', HomePageHandler),
  ('.*', SlideHandler),
  ], debug=BaseHandler.debug)

