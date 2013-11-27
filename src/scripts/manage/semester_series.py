import datetime
from google.appengine.api import images
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.semester_series import SemesterSeries, SemesterSeries_Form


class Manage_SemesterSeries_Handler(Manage_BaseHandler):
    def get(self):
        start = self.request.get('start', None)
        end = self.request.get('end', None)
        retry = self.request.get('retry', None)
        edit_key = self.request.get('edit', None)
        if retry or edit_key:
            self.template_vars['form'] = self.generate_form(SemesterSeries_Form)
        if start and end:
            form = SemesterSeries_Form()

            # http://stackoverflow.com/questions/5891555/display-the-date-like-may-5th-using-pythons-strftime
            def suffix(d):
                return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

            def custom_strftime(format_string, t):
                return t.strftime(format_string).replace('{S}', str(t.day) + suffix(t.day))

            start_date = datetime.datetime.strptime(start, "%B %d %Y")
            end_date = datetime.datetime.strptime(end, "%B %d %Y")
            delta = datetime.timedelta(days=7)
            while start_date <= end_date:
                form.Weeks.append_entry({'Date': custom_strftime("%B {S}", start_date)})
                start_date += delta
            self.template_vars['form'] = form
        else:
            query = SemesterSeries.query().order(-SemesterSeries.CreationDateTime)
            self.template_vars['Semesters'] = query

        self.render_template("manage/semester_series/semester_series.html")


    def post(self):
        def post_process_model(filled_semester_series):
            filled_semester_series.Image = images.resize(filled_semester_series.Image, 300, 200)

        filled_semester_series = self.process_form(SemesterSeries_Form, SemesterSeries,
                                                   PostProcessing=post_process_model)
        if filled_semester_series:
            self.redirect(self.request.path)
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class Manage_SemesterSeriesDelete_Handler(Manage_BaseHandler):
    def get(self, urlsafe_key):
        ndb.Key(urlsafe=urlsafe_key).delete()
        self.redirect("/manage/semester_series")


application = webapp.WSGIApplication([
    ('/manage/semester_series/delete/([^/]+)', Manage_SemesterSeriesDelete_Handler),
    ('/manage/semester_series.*', Manage_SemesterSeries_Handler),
    ], debug=Manage_BaseHandler.debug)
