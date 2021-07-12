from config import Config
from analz.geo_main import GeoTest, Mapp, MapsDB

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from config import Config

class CreateMapForm(FlaskForm):

    """The geocode() method supports finding the following types of locations:

            Street addresses
                27488 Stanford Ave, Bowden, North Dakota
                380 New York St, Redlands, CA 92373
        `
            Points of interest (POI) by name and type
                Disneyland
                banks in Paris
                los angeles starbucks
                mount everest

            Administrative place names such as city, county, state, province, or country names

                Seattle, Washington
                State of Mahārāshtra
                Liechtenstein
                mount everest
            Postal codes
                92591
                TW9 1DN
            """

    data_dir = Config.data_dir
    templates_dir = Config.templates_dir

    mapname = StringField('Map Name', validators=[DataRequired()])
    address  = StringField('Address', validators=[DataRequired(), Length(min=5, max=60)])
    submit = SubmitField('create map')

    def validate_mapname(self, mapname):
        keys  = MapsDB().mdic.keys()
        if mapname in keys:
            raise ValidationError('Map Name alread exists. Please use a different map name.')

    def validate_address(self, address):
            loc, lstr  = GeoTest.get_single_location(addr=address)
            if loc is None:
                raise ValidationError('address not found via Google geo Locator.')




