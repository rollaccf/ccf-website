from google.appengine.ext import db, blobstore
from scripts.gaesettings import gaesettings

class BaseModel(db.Model):

  def Update(self, data):
    """Updates each field in the model with the corresponding value in the UnicodeMultiDict data"""
    properties = self.properties()
    for prop in properties:
      if prop in data and data[prop]:
        if type(properties[prop]).__name__ == "BlobProperty":
          setattr(self, prop, db.Blob(data[prop].value))
        else:
          setattr(self, prop, data[prop])

  def PrintEscapedParagraph(self, property):
    from cgi import escape
    """This is probably a bad way to do this, but I cannot think of any other"""
    return escape(getattr(self, property)).replace('\n', '<br />')

class HomepageSlide(BaseModel):
  Enabled = db.BooleanProperty()
  DisplayOrder = db.IntegerProperty()

  Createdby = db.UserProperty(auto_current_user_add=True)
  CreationDateTime = db.DateTimeProperty(auto_now_add=True)
  Modifiedby = db.UserProperty(auto_current_user=True)
  ModifiedDateTime = db.DateTimeProperty(auto_now=True)

  Image = db.BlobProperty(
    verbose_name="Carousel Image",
  )
  Link = db.StringProperty(
    verbose_name="URL",
  )
  Title = db.StringProperty(
    verbose_name="Page Title",
  )
  Html = db.TextProperty(
    verbose_name="Page Content",
  )

  @db.ComputedProperty
  def CompleteURL(self):
    return '/' + self.Link

class HousingApplication(BaseModel):
  TimeSubmitted = db.DateTimeProperty(
    verbose_name="Time Submitted",
    auto_now_add=True,
  )

  FullName = db.StringProperty(
    verbose_name="Full Name",
    required=True,
  )
  EmailAddress = db.EmailProperty(
    verbose_name="Email Address",
    required=True,
  )
  PhoneNumber = db.PhoneNumberProperty(
    verbose_name="Phone Number",
    required=True,
  )
  DateOfBirth = db.DateProperty(
    verbose_name="Date of Birth (yyyy-mm-dd)",
    required=True,
  )
  HomeAddress = db.PostalAddressProperty(
    verbose_name="Home Address",
    required=True,
  )
  CurrentGradeLevel = db.StringProperty(
    verbose_name="Current Grade Level",
    required=True,
    choices=[
      "High School Junior",
      "High School Senior",
      "College Freshman",
      "College Sophmore",
      "College Junior",
      "College Senior",
      "Graduate Student",
    ]
  )
  ProposedDegree = db.StringProperty(
    verbose_name="Proposed Degree",
    required=True,
    choices=[
      "Aerospace Engineering",
      "Applied Mathematics",
      "Architectural Engineering",
      "Biological Sciences",
      "Business & Management Systems",
      "Ceramic Engineering",
      "Chemical Engineering",
      "Chemistry",
      "Civil Engineering",
      "Computer Engineering",
      "Computer Science",
      "Economics",
      "Electrical Engineering",
      "Engineering Management",
      "English",
      "Environmental Engineering",
      "Geological Engineering",
      "Geology & Geophysics",
      "History",
      "Information Science & Technology",
      "Mechanical Engineering",
      "Metallurgical Engineering",
      "Mining Engineering",
      "Nuclear Engineering",
      "Petroleum Engineering",
      "Philosophy",
      "Physics",
      "Pre-Law",
      "Pre-Med",
      "Pre-Nursing",
      "Pre-Veterinary",
      "Psychology",
      "Teacher Certifications",
      "Technical Communication",
      "Undecided Engineering",
      "Undecided",
      "Other",
    ]
  )
  House = db.StringProperty(
    verbose_name="House",
    required=True,
    choices=[
      "Men's Christian Campus House",
      "Women's Christian Campus House",
    ]
  )
  SemesterToBegin = db.StringProperty(
    verbose_name="Semester for which you seek to begin residence",
    required=True,
  )

  HowAndWhy = db.TextProperty(
    verbose_name="Briefly state how you found out about the Campus House and why you are seeking housing with us?",
    required=True,
  )
  LeadershipRoles = db.TextProperty(
    verbose_name="List any leadership roles in which you have served.",
    required=True,
  )
  TalentsAndInterests = db.TextProperty(
    verbose_name="What talents and interests do you have that you desire to explore while you are a resident?",
    required=True,
  )

  ParentNames = db.StringProperty(
    verbose_name="Your Parents' Names",
    required=True,
  )
  ParentPhoneNumber = db.PhoneNumberProperty(
    verbose_name="Phone Number",
    required=True,
  )
  ParentEmail = db.StringProperty(
    verbose_name="Email",
  )

  HomeChurchName = db.StringProperty(
    verbose_name="Name of your home church",
    required=True,
  )
  HomeChurchMinisterName = db.StringProperty(
    verbose_name="Name of the staff member",
    required=True,
  )
  HomeChurchPhoneNumber = db.PhoneNumberProperty(
    verbose_name="Phone Number",
    required=True,
  )
  HomeChurchEmail = db.StringProperty(
    verbose_name="Email",
  )

  OtherReferenceRelation = db.StringProperty(
    verbose_name="Relation to you (e.g. teacher, coach, employer)",
    required=True,
  )
  OtherReferenceName = db.StringProperty(
    verbose_name="Name",
    required=True,
  )
  OtherReferencePhoneNumber = db.PhoneNumberProperty(
    verbose_name="Phone Number",
    required=True,
  )
  OtherReferenceEmail = db.StringProperty(
    verbose_name="Email",
  )

  CriminalActivity = db.TextProperty(
    verbose_name="Have you ever been convicted of a crime? If yes, please explain.",
    required=True,
  )

  MedicalAllergies = db.TextProperty(
    verbose_name="List any medical conditions or allergies.",
  )
  Medications = db.TextProperty(
    verbose_name="List any medications you take on a regular basis.",
  )

  @db.ComputedProperty
  def PrintFormatedDateTime(self):
    #TODO: make a real timezone thingy (pytz); this code will no longer work March 10, 2013
    import datetime
    if (datetime.datetime.now() < datetime.datetime(2012, 11, 4)):
      return (self.TimeSubmitted + datetime.timedelta(hours=-5)).strftime('%a %b %d, %Y at %I:%M %p %z %Z')
    else:
      return (self.TimeSubmitted + datetime.timedelta(hours=-6)).strftime('%a %b %d, %Y at %I:%M %p %z %Z')

  def generateHtmlMailMessageBody(self):
    url = "www.rollaccf.org/manage/housing_applications/view_housing_application?key=%s" % self.key()
    return """<p>A new application has been submitted to %s.</p>
              <p><a href="%s">%s</a></p>""" % (self.House, url, url)

  def generatePlainTextMailMessageBody(self):
    url = "www.rollaccf.org/manage/housing_applications/view_housing_application?key=%s" % self.key()
    return """A new application has been submitted to %s.\n
              %s""" % (self.House, url)

class HousingApplicationNote(BaseModel):
  Createdby = db.UserProperty(auto_current_user_add=True)
  CreationDateTime = db.DateTimeProperty(auto_now_add=True)

  Content = db.TextProperty(
    required=True,
  )
  Application = db.ReferenceProperty(
    reference_class=HousingApplication,
    collection_name='notes',
  )

  @db.ComputedProperty
  def PrintFormatedDateTime(self):
    #TODO: make a real timezone thingy (pytz); this code will no longer work March 10, 2013
    import datetime
    if (datetime.datetime.now() < datetime.datetime(2012, 11, 4)):
      return (self.CreationDateTime + datetime.timedelta(hours=-5)).strftime('%a %b %d, %Y at %I:%M %p %z %Z')
    else:
      return (self.CreationDateTime + datetime.timedelta(hours=-6)).strftime('%a %b %d, %Y at %I:%M %p %z %Z')

class Newsletter(BaseModel):
  Createdby = db.UserProperty(auto_current_user_add=True)
  CreationDateTime = db.DateTimeProperty(auto_now_add=True)
  DisplayOrder = db.IntegerProperty()

  Title = db.StringProperty(
    verbose_name="Title",
    required=True,
  )
  NewsletterBlob = blobstore.BlobReferenceProperty(
    verbose_name="Newsletter",
    required=True,
  )
