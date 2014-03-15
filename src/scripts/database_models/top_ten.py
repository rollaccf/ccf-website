from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, NdbUtcDateProperty
from ext.wtforms import validators, fields
from ext.wtforms.form import Form

class TopTenAnswer_Form(Form):
    StudentName = fields.TextField(
        label=u'Student Name',
        validators=[validators.Required()],
    )
    Answer = fields.TextField(
        label=u'Answer',
        validators=[validators.Required()],
    )


class TopTen_Form(Form):
    QuestionDate = fields.DateField(
        label=u"Date of Question (yyyy-mm-dd)",
        validators=[validators.required()],
    )
    Question = fields.TextField(
        label=u'Question',
        validators=[validators.Required()],
    )
    Answers = fields.FieldList(
        fields.FormField(TopTenAnswer_Form),
        validators=[validators.Required()],
        min_entries=10,
        max_entries=10,
    )


class TopTenAnswer(NdbBaseModel):
    StudentName = ndb.StringProperty(
        required=True,
    )
    Answer = ndb.StringProperty(
        required=True,
    )


class TopTen(NdbBaseModel):
    relevant_page_urls = ["/catalyst/top_ten"]

    CreatedBy = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    ModifiedBy = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)

    QuestionDate = NdbUtcDateProperty(
        required=True,
    )
    Question = ndb.StringProperty(
        required=True,
    )
    Answers = ndb.LocalStructuredProperty(
        TopTenAnswer,
        repeated=True,
    )
