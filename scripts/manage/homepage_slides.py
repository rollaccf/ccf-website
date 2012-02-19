import os
from os.path import join
from google.appengine.api import images, memcache
from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery, to_dict
from scripts.main import BaseHandler
from scripts.gaesettings import gaesettings
from scripts.database_models import HomepageSlide

class ManageHomePageSlidesHandler(BaseHandler):
    def get(self):
      # TODO: add paging
      tab = self.request.get("tab", default_value='onhomepage')
      if tab == "disabled":
        slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = False").fetch(20);
      elif tab == "enabled":
        slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True").fetch(20);
        for slide in slides:
          if slide.DisplayOrder: # it's on the Homepage
            slides.remove(slide)
      else:
        slides = GqlQuery("SELECT * FROM HomepageSlide WHERE DisplayOrder > 0").fetch(20);

      slideDicts = []
      for slide in slides:
        d = to_dict(slide)
        d['key'] = slide.key()
        slideDicts.append(d)

      self.render_template(join("manage", "homepage_slides", "homepage_slides.html"),
        { 'title':"Homepage Slides",
          'slides':slideDicts,
          'tab':tab,
      })

class ManageNewSlideHandler(BaseHandler):
    def get(self):
      # TODO: add Capabilities API to check that the datastore is up
      # TODO: add image handling for editing
      editKey = self.request.get("edit")
      slideValues = None
      if editKey != '':
        editDbSlide = HomepageSlide.get(editKey)
        if editDbSlide != None:
          slideValues = to_dict(editDbSlide)
          slideValues['key'] = editDbSlide.key()

      self.render_template(join("manage", "homepage_slides", "new_slide.html"),
        { 'title':"New Homepage Slide",
          'MaxHomepageSlides':gaesettings.MaxHomepageSlides,
          'LinkPrefix':'/'.join((os.environ['HTTP_HOST'], gaesettings.HomepageLinkPrefix)),
          'slideValues':slideValues,
      })
    def post(self):
      # TODO: add cgi escape
      # TODO: add error checking and fatel errors
      enabled = bool(self.request.get("enabled"))
      slideImage = images.resize(self.request.get("image"), 600, 450)
      link = self.request.get("link")
      title = self.request.get("title")
      html = self.request.get("slideHtml")
      onHomepage = self.request.get("onHomepage")

      newSlide = None
      editKey = self.request.get("edit")
      if editKey != '':
        editDbSlide = HomepageSlide.get(editKey)
        if editDbSlide != None:
          newSlide = editDbSlide
      if newSlide == None:
        newSlide = HomepageSlide()

      newSlide.Enabled=enabled
      if onHomepage and enabled:
        displayOrderObject = GqlQuery("SELECT * FROM HomepageSlide ORDER BY DisplayOrder DESC").get()
        newSlide.DisplayOrder = displayOrderObject.DisplayOrder + 1 if displayOrderObject else 1
      else:
        newSlide.DisplayOrder = None
      newSlide.Link=link
      newSlide.Image=slideImage
      newSlide.Title=title
      newSlide.Html=html
      newSlide.put()

      memcache.delete("homepageSlides")
      self.redirect(self.request.path)

application = webapp.WSGIApplication([
  ('/manage/homepage_slides/new_slide.*', ManageNewSlideHandler),
  ('/manage/homepage_slides.*', ManageHomePageSlidesHandler),
  ], debug=True)
