import datetime
from google.appengine.api import images
from google.appengine.ext import webapp, ndb
from scripts.main import BaseHandler
from scripts.database_models.semester_series import SemesterSeries, SemesterSeries_Form


class Manage_SemesterSeries_Handler(BaseHandler):
    def get(self):
        start = self.request.get('start', None)
        end = self.request.get('end', None)
        retry = self.request.get('retry', None)
        edit_key = self.request.get('edit', None)
        if retry:
            form = SemesterSeries_Form(self.session['semesterSeries_data'])
            if edit_key:
                form.isEdit = True
                self.template_vars['editkey'] = edit_key
            form.validate()  # we need to generate the errors
            self.template_vars['form'] = form
        elif edit_key:
            edit_item = ndb.Key(urlsafe=edit_key).get()
            form = SemesterSeries_Form(obj=edit_item)
            self.template_vars['form'] = form
            self.template_vars['editkey'] = edit_key
        elif start and end:
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

        self.render_template("manage/semester_series/semester_series.html", use_cache=False)

    def post(self):
        edit_key = self.request.get('edit', None)
        edit_item = None
        if edit_key:
            edit_item = ndb.Key(urlsafe=edit_key).get()
        form = SemesterSeries_Form(self.request.POST, obj=edit_item)
        if edit_key:
            form.isEdit = True
        if form.validate():
            form_data = form.data
            if edit_item:
                if not form_data['Image']:
                    del form_data['Image']
                filled_semester_series = edit_item
                filled_semester_series.populate(**form_data)
            else:
                filled_semester_series = SemesterSeries(**form_data)
            filled_semester_series.Image = images.resize(filled_semester_series.Image, 300, 200)
            filled_semester_series.put()
            self.redirect(self.request.path)
        else:
            form_data = self.request.POST
            del form_data["Image"]
            self.session['semesterSeries_data'] = form_data
            if edit_key:
                self.redirect(self.request.path + '?retry=1&edit=' + edit_key)
            else:
                self.redirect(self.request.path + '?retry=1')


class Manage_SemesterSeriesDelete_Handler(BaseHandler):
    def get(self, urlsafe_key):
        ndb.Key(urlsafe=urlsafe_key).delete()
        self.redirect("/manage/semester_series")


application = webapp.WSGIApplication([
    ('/manage/semester_series/delete/([^/]+)', Manage_SemesterSeriesDelete_Handler),
    ('/manage/semester_series.*', Manage_SemesterSeries_Handler),
    ], debug=BaseHandler.debug)
