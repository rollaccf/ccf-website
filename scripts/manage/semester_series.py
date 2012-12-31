import datetime
from google.appengine.api import images
from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.gaesessions import get_current_session
from scripts.database_models.semester_series import * 
from wtforms.fields import FormField
from scripts.gaesessions import get_current_session

class Manage_SemesterSeries_Handler(BaseHandler):
    def get(self):
        session = get_current_session()
        start = self.request.get('start', None)
        end = self.request.get('end', None)
        retry = self.request.get('retry', None)
        if retry:
            form = SemesterSeries_Form(session['semesterSeries_data'])
            form.validate() # we need to generate the errors
            self.template_vars['form'] = form
        elif start and end:
            form = SemesterSeries_Form()

            # http://stackoverflow.com/questions/5891555/display-the-date-like-may-5th-using-pythons-strftime
            def suffix(d):
                return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

            def custom_strftime(format, t):
                return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

            start_date = datetime.datetime.strptime(start, "%B %d %Y")
            end_date = datetime.datetime.strptime(end, "%B %d %Y")
            delta = datetime.timedelta(days=7)
            while start_date <= end_date:
                form.Weeks.append_entry({'Date':custom_strftime("%B {S}", start_date)})
                start_date += delta
            self.template_vars['form'] = form
        else:
            query = SemesterSeries.query()
            self.template_vars['Semesters'] = query

        self.render_template("manage/semester_series/semester_series.html", use_cache=False)
    def post(self):
       #print self.request.POST["Image"].value
        session = get_current_session()
        form = SemesterSeries_Form(self.request.POST)
        if form.validate():
            form_data = form.data
            form_data['Image'] = form_data['Image'].value 
            filled_semester_series = SemesterSeries(**form_data)
            filled_semester_series.Image = images.resize(filled_semester_series.Image, 300, 200)
            filled_semester_series.put()
            self.redirect(self.request.path)
        else:
           #from cgi import FieldStorage
           #print "Content-Type: text/plain\n\n"
           #print "data", form.Image.data
           #field = form.Image
           #if not field.data or isinstance(field.data, string_types) and not field.data.strip():
           #    print "failed DataRequired"
           #if not field.raw_data[0]:# or not field.raw_data[0]:
           #    print "failed InputRequired"
           #if field.raw_data:
           #    print "found raw"
           #if not isinstance(field.data, FieldStorage):# .raw_data[0]:
           #    print "is instance"
           #print "raw", type(field.raw_data)
           #print "raw[0]", type(field.raw_data[0])
           #print "<br /> form not valid <br />", form.Image.errors
           #for e in form.errors:
           #    print "||" + e + "||<br />" 
            form_data = self.request.POST
            del form_data["Image"]
            session['semesterSeries_data'] = form_data
            self.redirect(self.request.path + '?retry=1')
       #print(form.Weeks.entries)


application = webapp.WSGIApplication([
 #('/manage/housing_applications/view/([^/]+)', Manage_HousingApplication_ViewHandler),
 #('/manage/housing_applications/(archive|unarchive)/([^/]+)', Manage_HousingApplication_ArchiveHandler),
  ('/manage/semester_series.*', Manage_SemesterSeries_Handler),
  ], debug=BaseHandler.debug)
