import os
from google.appengine.ext import webapp
from scripts.globals import TEMPLATE_PATH
from django.template.loader import get_template
from django.template.context import Context

class BaseHandler(webapp.RequestHandler):
  def render_template(self, filename, template_args):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    path = os.path.join(TEMPLATE_PATH, filename)
    templ = get_template(path)
    self.response.out.write(templ.render(Context(template_args)))

#TODO: move this into its own file (with the event link handler)
from google.appengine.api import memcache
from google.appengine.ext.db import GqlQuery, to_dict
from scripts.database_models import HomepageSlide
from scripts.gaesettings import gaesettings
class HomePageHandler(BaseHandler):
  def get(self):
    slideDicts = memcache.get('homepageSlides')
    if slideDicts == None:
      slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True ORDER BY DisplayOrder ASC").fetch(gaesettings.MaxHomepageSlides);
      if slides != []:
        slideDicts = []
        for slide in slides:
          d = to_dict(slide)
          d['key'] = slide.key()
          slideDicts.append(d)
        memcache.set('homepageSlides', slideDicts)

    self.render_template("index.html",
      { 'title':"Christian Campus Fellowship, Rolla Missouri",
        'headerText':"Christian Campus Fellowship",
        'slides':slideDicts,
        'HomepageSlideRotationDelay':gaesettings.HomepageSlideRotationDelay,
    })


application = webapp.WSGIApplication([('/', HomePageHandler)], debug=True)

