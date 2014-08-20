import yaml
from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, GaeFileField
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


def validate_int(min, max):
    def func(prop, value):
        if value < min or value > max:
            raise ValueError("Value out of range")
    return func


class RaPiConfig_Form(Form):
    # TODO: create form
    pass


class RaPiConfig(NdbBaseModel):
    CreatedBy = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    ModifiedBy = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)

    Interval = ndb.IntegerProperty(
        verbose_name="Interval in Seconds",
        required=True,
    )
    UploadLocation = ndb.StringProperty(
        required=True,
    )

    encoding = ndb.StringProperty(
        required=True,
        choices=['jpg', 'bmp', 'gif', 'png'],
        default='jpg',
    )
    width = ndb.IntegerProperty(
        verbose_name="Set image width",
    )
    height = ndb.IntegerProperty(
        verbose_name="Set image height",
    )

    quality = ndb.IntegerProperty(
        verbose_name="Set jpeg quality (0 to 100)",
        validator=validate_int(0, 100),
    )
    sharpness = ndb.IntegerProperty(
        verbose_name="Set image sharpness (-100 to 100)",
        validator=validate_int(-100, 100),
    )
    contrast = ndb.IntegerProperty(
        verbose_name="Set image contrast (-100 to 100)",
        validator=validate_int(-100, 100),
    )
    brightness = ndb.IntegerProperty(
        verbose_name="Set image brightness (0 to 100)",
        validator=validate_int(0, 100),
    )
    saturation = ndb.IntegerProperty(
        verbose_name="Set image saturation (-100 to 100)",
        validator=validate_int(-100, 100),
    )
    ISO = ndb.IntegerProperty(
        verbose_name="Set capture ISO",
        validator=validate_int(100, 800),
    )
    vstab = ndb.BooleanProperty(
        verbose_name="Turn on video stabilisation",
    )
    ev = ndb.IntegerProperty(
        verbose_name="Set EV compensation",
        validator=validate_int(-10, 10)
    )
    exposure = ndb.StringProperty(
        verbose_name="Set exposure mode",
        choices=['auto', 'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach',
                 'verylong', 'fixedfps', 'antishake', 'fireworks',
        ],
    )
    awb = ndb.StringProperty(
        verbose_name="Set AWB mode",
        choices=['off', 'auto', 'sun', 'cloud', 'shade', 'tungsten', 'fluorescent', 'incandescent',
                 'flash', 'horizon',
        ],
    )
    imxfx = ndb.StringProperty(
        verbose_name="Set image effect",
        choices=['none', 'negative', 'solarise', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
                 'pastel', 'watercolour', 'film', 'blur', 'saturation', 'colourswap', 'washedout', 'posterise',
                 'colourpoint', 'colourbalance', 'cartoon',
        ],
    )
    colfx = ndb.IntegerProperty(
        verbose_name="Set colour effect (U:V)",
        repeated=True,
        validator=validate_int(0, 255),
    )
    metering = ndb.StringProperty(
        verbose_name="Set metering mode",
        choices=['average', 'spot', 'backlit', 'matrix'],
    )
    rotation = ndb.IntegerProperty(
        verbose_name="Set image rotation (0-359)",
        validator=validate_int(0, 359),
    )
    hflip = ndb.BooleanProperty(
        verbose_name="Set horizontal flip",
    )
    vflip = ndb.BooleanProperty(
        verbose_name="Set vertical flip",
    )
    roi = ndb.FloatProperty(
        verbose_name="Set region of interest (x,y,w,d as normalised coordinates [0.0-1.0])",
        repeated=True,
    )
    shutter = ndb.IntegerProperty(
        verbose_name="Set shutter speed in microseconds",
    )

    def to_yaml(self):
        d = self.to_dict()
        del d['CreatedBy']
        del d['CreationDateTime']
        del d['ModifiedDateTime']
        del d['ModifiedBy']
        for k, v in d.items():
            if isinstance(v, unicode):
                d[k] = str(v)
        out = {}
        out['Interval'] = d['Interval']
        del d['Interval']
        out['UploadLocation'] = d['UploadLocation']
        del d['UploadLocation']
        out['raspistill'] = d

        return yaml.dump(out,  default_flow_style=False)
