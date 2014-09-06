import os
import urllib
from google.appengine.api import images, capabilities
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.homepage_slide import HomepageSlide, HomepageSlide_Form


class Manage_HomePageSlides_BaseHandler(Manage_BaseHandler):
    pass


class Manage_HomePageSlides_Handler(Manage_HomePageSlides_BaseHandler):
    def get(self):
        self.generate_manage_bar()
        # get slides for the tab we are on
        # TODO: add paging
        tab = self.request.get("tab", default_value='onhomepage')
        if tab == "disabled":
            slides = HomepageSlide.gql("WHERE Enabled = False").fetch(50)
        elif tab == "enabled":
            slides = HomepageSlide.gql("WHERE Enabled = True").fetch(50)
            # Only keep slides without DisplayOrder (if they have DisplayOrder, it means they are on the homepage)
            slides = [slide for slide in slides if not slide.DisplayOrder]
        else:
            slides = HomepageSlide.gql("WHERE DisplayOrder > 0").fetch(50)

        self.template_vars['slides'] = slides
        self.template_vars['tab'] = tab

        self.render_template("manage/homepage_slides/homepage_slides.html")


class Manage_HomePageSlides_CreateHandler(Manage_HomePageSlides_BaseHandler):
    def get(self):
        self.generate_manage_bar()
        if not capabilities.CapabilitySet('datastore_v3', ['write']).is_enabled():
            self.abort(500, "The datastore is down")

        self.template_vars['MaxHomepageSlides'] = self.settings.MaxHomepageSlides
        self.template_vars['LinkPrefix'] = '/'.join((os.environ['HTTP_HOST'],))
        self.template_vars['form'] = self.generate_form(HomepageSlide_Form)
        self.template_vars['error_msg'] = self.session.get('new_slide_error')

        self.render_template("manage/homepage_slides/new_slide.html")

    def post(self):
        def pre_formdata_processing(form_data):
            del form_data['onHomepage']

        def post_process_model(filled_homepage_slide):
            if self.request.get("onHomepage") and filled_homepage_slide.Enabled:
                if filled_homepage_slide.DisplayOrder == None:
                    displayOrderObject = HomepageSlide.gql("ORDER BY DisplayOrder DESC").get()
                    if displayOrderObject and displayOrderObject.DisplayOrder:
                        filled_homepage_slide.DisplayOrder = displayOrderObject.DisplayOrder + 1
                    else:
                        filled_homepage_slide.DisplayOrder = 1
            else:
                filled_homepage_slide.DisplayOrder = None

            if filled_homepage_slide.Image:
                    filled_homepage_slide.Image = images.resize(filled_homepage_slide.Image, 600, 450)

        filled_homepage_slide = self.process_form(HomepageSlide_Form, HomepageSlide,
                                         PreProcessing=pre_formdata_processing, PostProcessing=post_process_model)
        if filled_homepage_slide:
            self.redirect("/manage/homepage_slides")
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class Manage_HomePageSlides_OrderHandler(Manage_HomePageSlides_BaseHandler):
    def get(self, direction, displayOrderToMove):
        displayOrderToMove = int(displayOrderToMove)
        # I am assuming displayOrder has no duplicates
        FirstObject = HomepageSlide.gql("WHERE DisplayOrder = :1", displayOrderToMove).get()
        if direction == 'u':
            SecondObject = HomepageSlide.gql("WHERE DisplayOrder < :1 ORDER BY DisplayOrder DESC",
                                             displayOrderToMove).get()
        else:
            SecondObject = HomepageSlide.gql("WHERE DisplayOrder > :1 ORDER BY DisplayOrder ASC",
                                             displayOrderToMove).get()
        FirstObject.DisplayOrder, SecondObject.DisplayOrder = SecondObject.DisplayOrder, FirstObject.DisplayOrder
        FirstObject.put()
        SecondObject.put()
        self.redirect('/manage/homepage_slides')


class Manage_HomePageSlides_DeleteHandler(Manage_HomePageSlides_BaseHandler):
    def get(self, urlsafe_key):
        urlsafe_key = str(urllib.unquote(urlsafe_key))
        key = ndb.Key(urlsafe=urlsafe_key)
        if key.kind() == "HomepageSlide":
            key.delete()
        else:
            self.abort(400, "Can only delete kind 'HomepageSlide'")
        self.redirect('/manage/homepage_slides')


application = webapp.WSGIApplication([
    ('/manage/homepage_slides/order/([ud])/(\d+)', Manage_HomePageSlides_OrderHandler),
    ('/manage/homepage_slides/delete/([^/]+)', Manage_HomePageSlides_DeleteHandler),
    ('/manage/homepage_slides/new_slide.*', Manage_HomePageSlides_CreateHandler),
    ('/manage/homepage_slides.*', Manage_HomePageSlides_Handler),
    ], debug=Manage_BaseHandler.debug)
