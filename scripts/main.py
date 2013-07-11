from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.homepageslide import HomepageSlide
from scripts.gaesettings import gaesettings


class HomePageHandler(BaseHandler):
    def get(self):
        slides_query = HomepageSlide.gql("WHERE Enabled = True ORDER BY DisplayOrder ASC")
        self.template_vars['slides'] = slides_query.fetch(gaesettings.MaxHomepageSlides)
        self.template_vars['HomepageSlideRotationDelay'] = gaesettings.HomepageSlideRotationDelay
        self.render_template("index.html")


class SlideHandler(BaseHandler):
    def get(self):
        dbSlide = HomepageSlide.gql("WHERE CompleteURL = :1", self.request.path).get()
        if dbSlide and dbSlide.Enabled == True:
            self.template_vars['title'] = dbSlide.Title
            self.template_vars['slide'] = dbSlide
            self.render_template("slide.html")
        else:
            self.abort(404, "Page Does Not Exist")


application = webapp.WSGIApplication([
    ('/', HomePageHandler),
    ('.*', SlideHandler),
    ], debug=BaseHandler.debug)

