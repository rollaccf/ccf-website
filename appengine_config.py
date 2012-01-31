from scripts.gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
  return SessionMiddleware(app, cookie_key="fm19dewrg49san}[HAN73(lrwimQ23lnhfgking")

