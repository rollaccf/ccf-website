from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, GaeFileField
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class HomepageSlide_Form(Form):
    Enabled = fields.BooleanField(u'Enabled')
    onHomepage = fields.BooleanField(u'onHomepage')

    Image = GaeFileField(u'Carousel Image', validators=[validators.data_required()])
    Link = fields.TextField(u'URL')
    Title = fields.TextField(u'Page Title')
    Html = fields.TextAreaField(u'Page Content')


class HomepageSlide(NdbBaseModel):
    relevant_page_urls = ["/"]

    Enabled = ndb.BooleanProperty()
    DisplayOrder = ndb.IntegerProperty()

    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    Modifiedby = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)

    Image = ndb.BlobProperty(
        verbose_name="Carousel Image",
    )
    Link = ndb.StringProperty(
        verbose_name="URL",
    )
    Title = ndb.StringProperty(
        verbose_name="Page Title",
    )
    Html = ndb.TextProperty(
        verbose_name="Page Content",
    )


    @ndb.ComputedProperty
    def onHomepage(self):
        return self.DisplayOrder is not None


    @ndb.ComputedProperty
    def CompleteURL(self):
        return '/' + self.Link

    def _post_put_hook(self, future):
        super(HomepageSlide, self)._post_put_hook(future)
        self._clear_relevant_memcache([self.CompleteURL, ])

    @classmethod
    def _pre_delete_hook(cls, key):
        cls._clear_relevant_memcache([key.get().CompleteURL, ])
