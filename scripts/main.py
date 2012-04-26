from google.appengine.ext import webapp
from webapp2_extras import jinja2

class BaseHandler(webapp.RequestHandler):
  @webapp.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def fatal_error(self, errorTitle, ErrorText):
    #TODO: make this a nice looking page
    self.response.out.write("<p>%s</p><p>%s</p>" % (errorTitle, ErrorText))

  def render_template(self, filename, template_args):
    self.response.out.write(self.jinja2.render_template(filename, **template_args))


#TODO: move this into its own file (with the event link handler)
from google.appengine.api import memcache
from google.appengine.ext.db import GqlQuery
from scripts.database_models import HomepageSlide
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
        self.fatal_error("404", "Page Not Found")

application = webapp.WSGIApplication([
  ('/', HomePageHandler),
  ('.*', SlideHandler),
  ], debug=True)

