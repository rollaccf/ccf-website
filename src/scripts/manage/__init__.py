from google.appengine.api import users
from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.database_models.user_permission import UserPermission, Manage_Restricted_Pages


class Manage_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Manage_BaseHandler, self).__init__(*args, **kwargs)
        self.use_cache = False
        self.restricted = True

    def generate_manage_bar(self):
        if users.is_current_user_admin():
            displayed_pages = Manage_Restricted_Pages.keys()
        else:
            user_permission = UserPermission.get_by_id(self.current_user.email().lower())
            displayed_pages = user_permission.PermittedPageClasses

        pages = {}
        for page in displayed_pages:
            group, link = Manage_Restricted_Pages[page]
            if group in pages:
                pages[group].append(link)
            else:
                pages[group] = [link, ]

        final_pages = []
        for group in sorted(pages.keys()):
            final_group = []
            for link in sorted(pages[group], key=lambda x: x[1]):
                final_group.append(link)
            final_pages.append(final_group)

        self.template_vars['manage_pages'] = final_pages


class ManageHandler(Manage_BaseHandler):
    def get(self):
        self.generate_manage_bar()
        self.render_template("manage/manage.html")


class TestHandler(Manage_BaseHandler):
    def get(self, action):
        if action == "500":
            self.abort(500)
        elif action == "404":
            self.abort(404)
        elif action == "403":
            self.abort(403)
        elif action == "exception":
            raise Exception("Test Exception")


application = webapp.WSGIApplication([
    ('/manage/_test/([^/]+)', TestHandler),
    ('/manage.*', ManageHandler),
    ], debug=Manage_BaseHandler.debug)
