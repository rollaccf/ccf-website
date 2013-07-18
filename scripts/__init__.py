import os
import logging
import webapp2
from google.appengine.api import memcache, users
from google.appengine.ext import webapp
from webapp2_extras import jinja2
from scripts.gaesessions import get_current_session
from scripts.database_models.gae_setting import BaseSetting

class GAESettingDoesNotExist(Exception):
    pass


# http://stackoverflow.com/questions/3012421/python-lazy-property-decorator
def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazy_property

class global_settings(object):
    def __getattr__(self, name):
        dbValue = BaseSetting.get_by_id(name)
        if dbValue == None:
            raise GAESettingDoesNotExist("'" + name + "' does not exist in the default values or in the datastore")
        return dbValue.Value

class BaseHandler(webapp.RequestHandler):
    debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.settings = global_settings()
        self.template_vars = {}
        self.use_cache = True

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

        self.render_template(template_file)


    def dispatch(self):
        if self.use_cache and self.request.method == "GET" and not self.debug:
            memcache_key = os.environ['CURRENT_VERSION_ID'] + self.request.path
            response_values = memcache.get(memcache_key)

            if response_values:
                logging.info("Cache entry found")
                self.response.headerlist = response_values[0]
                self.response.body = response_values[1]
            else:
                logging.info("Cache entry not found")
                super(BaseHandler, self).dispatch()
                # extract response body and headers and save them for the future
                response_values = (self.response.headerlist, self.response.body)
                memcache.add(memcache_key, response_values)
        else:
            logging.info("Skipping cache")
            super(BaseHandler, self).dispatch()


    def render_template(self, filename):
        rendered_html = self.jinja2.render_template(filename, **self.template_vars)
        return self.response.out.write(rendered_html)
