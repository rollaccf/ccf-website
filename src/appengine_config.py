
def webapp_add_wsgi_middleware(app):
    # appstats https://developers.google.com/appengine/docs/python/tools/appstats
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)

    # gaesessions https://github.com/dound/gae-sessions
    from ext.gaesessions import SessionMiddleware
    app = SessionMiddleware(app, cookie_key="fm19dewrg49san}[HAN73(lrwimQ23lnhfgking")
    return app

