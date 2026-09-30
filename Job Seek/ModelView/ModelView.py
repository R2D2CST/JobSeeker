"""

Job Seeker

Created by: R2D2CST

Created: 25/sep/2026

"""

# Python Modules.
from pathlib import Path
import os
from typing import (
    List,
    Dict,
)

# Third Party Libraries.

# Self Built Modules.
from Model.Constants import (
    APP_NAME,
    APP_VERSION,
    APP_PATH,
)

from Model.Persistor import (
    PersistenceManager,
)


class ModelView:

    def __init__(self):

        # Setting app constants
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION
        self.APP_PATH = APP_PATH

        # Setting persister object.
        self.persister = PersistenceManager()

        pass

    pass
