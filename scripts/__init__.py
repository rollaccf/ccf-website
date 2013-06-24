import os
import logging
import webapp2
from google.appengine.api import memcache, users
from google.appengine.ext import webapp
from webapp2_extras import jinja2
from scripts.gaesessions import get_current_session

# http://stackoverflow.com/questions/3012421/python-lazy-property-decorator
def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazy_property


class BaseHandler(webapp.RequestHandler):
    debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.template_vars = {}
        self.template_vars_functions = []

    # I should move to webapp2 sessions
    # http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
    @lazy_property
    def session(self):
        return get_current_session()

    @lazy_property
    def current_user(self):
        return users.get_current_user()

    @webapp.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def handle_exception(self, exception, debug_mode):
        # https://webapp-improved.appspot.com/guide/exceptions.html
        if debug_mode:
            raise

        if isinstance(exception, webapp2.HTTPException):
            # just a simple http exception
            self.response.set_status(exception.code)
            if exception.code == 404:
                page_displayed_code = 404
            else:
                page_displayed_code = 500
        else:
            # some unknown bad exception
            logging.exception(exception)
            self.response.set_status(500)
            page_displayed_code = 500

        self.response.clear()
        template_file = "%s.html" % unicode(page_displayed_code)
        self.template_vars['title'] = "%s!" % unicode(page_displayed_code)
        self.template_vars['errorCode'] = page_displayed_code
        self.template_vars['errorMessage'] = exception.message
        self.template_vars['requestURL'] = self.request.url

        self.render_template(template_file, use_cache=False)

    def register_var_function(self, function):
        self.template_vars_functions.append(function)

    def populate_template_vars(self):
        for function in self.template_vars_functions:
            function()

    def __render_template(self, filename):
        self.populate_template_vars()
        return self.jinja2.render_template(filename, **self.template_vars)

    def render_template(self, filename, use_cache=True):
        if use_cache and not self.debug:
            version_id = os.environ['CURRENT_VERSION_ID']
            rendered_html = memcache.get(version_id + filename) or self.__render_template(filename)
            memcache.add(version_id + filename, rendered_html, time=60 * 60)
        else:
            rendered_html = self.__render_template(filename)
        self.response.out.write(rendered_html)
