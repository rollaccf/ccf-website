from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from scripts import BaseHandler
from scripts.gaesettings import gaesettings


class HomePageHandler(BaseHandler):
    def get_slides(self):
        slides_query = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True ORDER BY DisplayOrder ASC")
        self.template_vars['slides'] = slides_query.fetch(gaesettings.MaxHomepageSlides)

    def get_HomepageSlideRotationDelay(self):
        self.template_vars['HomepageSlideRotationDelay'] = gaesettings.HomepageSlideRotationDelay

    def get(self):
        self.register_var_function(self.get_slides)
        self.register_var_function(self.get_HomepageSlideRotationDelay)
        self.render_template("index.html")


class SlideHandler(BaseHandler):
    def get(self):
        dbSlide = GqlQuery("SELECT * FROM HomepageSlide WHERE CompleteURL = :1", self.request.path).get()
        if dbSlide and dbSlide.Enabled == True:
            self.template_vars['title'] = dbSlide.Title
            self.template_vars['slide'] = dbSlide
            self.render_template("slide.html", use_cache=False)
        else:
            self.abort(404, "Page Does Not Exist")


application = webapp.WSGIApplication([
    ('/', HomePageHandler),
    ('.*', SlideHandler),
    ], debug=BaseHandler.debug)

