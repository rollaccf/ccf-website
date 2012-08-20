import os
import logging
from google.appengine.api import memcache
from google.appengine.ext import webapp
from webapp2_extras import jinja2

class Http404(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    self.code = 404

class Http500(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    self.code = 500

class BaseHandler(webapp.RequestHandler):
  debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

  @webapp.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def handle_exception(self, exception, debug_mode):
    # https://webapp-improved.appspot.com/guide/exceptions.html
    if debug_mode:
      raise #webapp.RequestHandler.handle_exception(self, exception, debug_mode)
    else:
      if hasattr(exception, 'code'):
        code = exception.code
      else:
        code = 500
      if code != 404:
        logging.exception(exception)
      self.response.clear()
      self.response.set_status(code)
      self.render_template(unicode(code)+".html",
        { 'title': unicode(code) + "!",
          'errorCode':code,
          'errorMessage':exception.message,
          'requestURL':self.request.url,
        },use_cache=False)

  def render_template(self, filename, template_args, use_cache=True):
    if use_cache and not self.debug:
      version_id = os.environ['CURRENT_VERSION_ID']
      rendered_html = memcache.get(version_id + filename) or self.jinja2.render_template(filename, **template_args)
      memcache.add(version_id + filename, rendered_html, time=60*60)
    else:
      rendered_html = self.jinja2.render_template(filename, **template_args)
    self.response.out.write(rendered_html)
