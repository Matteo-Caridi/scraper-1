"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

db.define_table(
    'siti_importati',
    Field('website_url'),
)

db.define_table(
    'files_excel',
    Field('reference_file', 'reference siti_importati'),
    Field('file'),
)

db.commit()