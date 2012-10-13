import os
import logging
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import webapp
from webapp2_extras import jinja2

class BaseHandler(webapp.RequestHandler):
  debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

  @webapp.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def handle_exception(self, exception, debug_mode):
    # https://webapp-improved.appspot.com/guide/exceptions.html
    if debug_mode:
        raise

    logging.exception(exception)
    if isinstance(exception, webapp2.HTTPException):
        self.response.set_status(exception.code)
    else:
        self.response.set_status(500)

    if exception.code and exception.code == 404:
        page_displayed_code = 404
    else:
        page_displayed_code = 500

    self.response.clear()
    template_file = "%s.html" % unicode(page_displayed_code)
    template_vars = {}
    template_vars['title'] = "%s!" % unicode(page_displayed_code)
    template_vars['errorCode'] = page_displayed_code
    template_vars['errorMessage'] = exception.message
    template_vars['requestURL'] = self.request.url

    self.render_template(template_file, template_vars, use_cache=False)

  def render_template(self, filename, template_args, use_cache=True):
    if use_cache and not self.debug:
      version_id = os.environ['CURRENT_VERSION_ID']
      rendered_html = memcache.get(version_id + filename) or self.jinja2.render_template(filename, **template_args)
      memcache.add(version_id + filename, rendered_html, time=60*60)
    else:
      rendered_html = self.jinja2.render_template(filename, **template_args)
    self.response.out.write(rendered_html)
