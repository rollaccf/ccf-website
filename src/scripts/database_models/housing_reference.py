from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class HousingReference_Form(Form):
    YearsKnown = fields.IntegerField(
        label="How many years have you known ...?",
        validators=[validators.data_required()],
    )
    Relation = fields.StringField(
        label="What is your relation to ...?",
        validators=[validators.data_required()],
    )
    HonestResponsible = fields.SelectField(
        label="Is ... honest and responsible?",
        choices=[("Yes", "Yes"), ("No", "No")],
        validators=[validators.data_required()],
    )
    Strengths = fields.TextAreaField(
        label="In your opinion, what are ... strengths?",
        validators=[validators.data_required()],
    )
    Weaknesses = fields.TextAreaField(
        label="In your opinion, what are ... weaknesses?",
        validators=[validators.data_required()],
    )
    SocialSkills = fields.TextAreaField(
        label="Do you believe ... will get along and be a positive influence on roommates and housemates?",
        validators=[validators.data_required()],
    )
    Interests = fields.TextAreaField(
        label="Do you believe ... will explore interests outside the campus house?",
        validators=[validators.data_required()],
    )
    Trustworthy = fields.TextAreaField(
        label="Is ... honest with where he/she stands with others?",
        validators=[validators.data_required()],
    )
    Morals = fields.TextAreaField(
        label="Do you believe ... to have solid moral and spiritual convictions?",
        validators=[validators.data_required()],
    )
    Growth = fields.TextAreaField(
        label="Do you believe ... to have a desire to grow and be used by God?",
        validators=[validators.data_required()],
    )
    Reservations = fields.TextAreaField(
        label="Do you have any reservations about recommending ... for residency?",
        validators=[validators.data_required()],
    )
    Comments =fields.TextAreaField(
        label="Additional Comments",
        validators=[validators.data_required()],
    )



class HousingReference(NdbBaseModel):
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)

    YearsKnown = ndb.IntegerProperty(
        required=True,
    )
    Relation = ndb.StringProperty(
        required=True,
    )
    Strengths = ndb.TextProperty(
        required=True,
    )
    Weaknesses = ndb.TextProperty(
        required=True,
    )
    HonestResponsible = ndb.StringProperty(
        required=True,
        choices=["Yes", "No"],
    )
    SocialSkills = ndb.TextProperty(
        required=True,
    )
    Interests = ndb.TextProperty(
        required=True,
    )
    Trustworthy = ndb.TextProperty(
        required=True,
    )
    Morals = ndb.TextProperty(
        required=True,
    )
    Growth = ndb.TextProperty(
        required=True,
    )
    Reservations = ndb.TextProperty(
        required=True,
    )
    Comments =ndb.TextProperty(
        required=True,
    )

