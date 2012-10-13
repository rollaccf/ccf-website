import os
import urllib
from google.appengine.api import images, capabilities
from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from scripts.main import BaseHandler
from scripts.gaesessions import get_current_session
from scripts.gaesettings import gaesettings
from scripts.database_models.homepageslide import HomepageSlide
from wtforms.ext.appengine.db import model_form

class Manage_HomePageSlides_Handler(BaseHandler):
    def get(self):
      # get slides for the tab we are on
      # TODO: add paging
      tab = self.request.get("tab", default_value='onhomepage')
      if tab == "disabled":
        slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = False").fetch(20);
      elif tab == "enabled":
        slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True").fetch(20);
        # Only keep slides without DisplayOrder (if they have DisplayOrder, it means they are on the homepage)
        slides = [slide for slide in slides if not slide.DisplayOrder]
      else:
        slides = GqlQuery("SELECT * FROM HomepageSlide WHERE DisplayOrder > 0").fetch(20);

      self.render_template("manage/homepage_slides/homepage_slides.html",
      {
        'slides':slides,
        'tab':tab,
      },use_cache=False)

class Manage_HomePageSlides_CreateHandler(BaseHandler):
    FormClass = model_form(HomepageSlide)

    def get(self):
      if not capabilities.CapabilitySet('datastore_v3', ['write']).is_enabled():
        self.abort(500, "The datastore is down")

      session = get_current_session()

      if self.request.get('retry'):
        form = self.FormClass(formdata=session.get('new_slide'))
        if session.has_key('new_slide'):
          form.validate()
      elif self.request.get('edit'):
        editKey = self.request.get("edit")
        form = self.FormClass(obj=HomepageSlide.get(editKey))
      else:
        form = self.FormClass()

      self.render_template("manage/homepage_slides/new_slide.html",
      {
        'MaxHomepageSlides':gaesettings.MaxHomepageSlides,
        'LinkPrefix':'/'.join((os.environ['HTTP_HOST'],)),
        'editKey':self.request.get('edit'),
        'form':form,
      },use_cache=False)

    def post(self):
      # TODO: add cgi escape
      # TODO: add error checking
      session = get_current_session()
      form = self.FormClass(self.request.POST)
      editKey = self.request.get("edit")
      if form.validate(): #add validators, aka If url needs page title and html
        if 'new_slide' in session:
          del session['new_slide']
        if editKey:
          filled_homepage_slide = HomepageSlide.get(editKey)
          if filled_homepage_slide == None:
            self.abort(500, "The slide you are trying to edit does not exist")
        else:
          filled_homepage_slide = HomepageSlide()
        filled_homepage_slide.Update(form.data)

        if self.request.get("onHomepage") and filled_homepage_slide.Enabled:
          if filled_homepage_slide.DisplayOrder == None:
            displayOrderObject = GqlQuery("SELECT * FROM HomepageSlide ORDER BY DisplayOrder DESC").get()
            try:
              filled_homepage_slide.DisplayOrder = displayOrderObject.DisplayOrder + 1 if displayOrderObject else 1
            except:
              # if DisplayOrder is None (NoneType + 1 results in a exception)
              filled_homepage_slide.DisplayOrder = 1
        else:
          filled_homepage_slide.DisplayOrder = None

        if filled_homepage_slide.Image:
          filled_homepage_slide.Image=images.resize(filled_homepage_slide.Image, 600, 450)

        filled_homepage_slide.put()
        self.redirect("/manage/homepage_slides")
      else:
        session['new_slide'] = self.request.POST
        self.redirect(self.request.path + '?edit=%s&retry=1' % editKey)

class Manage_HomePageSlides_OrderHandler(BaseHandler):
  def get(self, direction, displayOrderToMove):
    displayOrderToMove = int(displayOrderToMove)
    # I am assuming displayOrder has no duplicates
    FirstObject = HomepageSlide.gql("WHERE DisplayOrder = :1", displayOrderToMove).get()
    if direction == 'u':
      SecondObject = HomepageSlide.gql("WHERE DisplayOrder < :1 ORDER BY DisplayOrder DESC", displayOrderToMove).get()
    else:
      SecondObject = HomepageSlide.gql("WHERE DisplayOrder > :1 ORDER BY DisplayOrder ASC", displayOrderToMove).get()
    FirstObject.DisplayOrder, SecondObject.DisplayOrder = SecondObject.DisplayOrder, FirstObject.DisplayOrder
    FirstObject.put()
    SecondObject.put()
    self.redirect('/manage/homepage_slides')

class Manage_HomePageSlides_DeleteHandler(BaseHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    homepageSlide = HomepageSlide.get(resource)
    homepageSlide.delete()
    self.redirect('/manage/homepage_slides')


application = webapp.WSGIApplication([
  ('/manage/homepage_slides/order/([ud])/(\d+)', Manage_HomePageSlides_OrderHandler),
  ('/manage/homepage_slides/delete/([^/]+)', Manage_HomePageSlides_DeleteHandler),
  ('/manage/homepage_slides/new_slide.*', Manage_HomePageSlides_CreateHandler),
  ('/manage/homepage_slides.*', Manage_HomePageSlides_Handler),
  ], debug=BaseHandler.debug)
