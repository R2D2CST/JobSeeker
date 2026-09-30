"""

Job Seeker

Created by: R2D2CST

Created: 25/sep/2026

"""

# Python Modules.
import os

# Third Party Libraries.

# Self Built Modules.
from Model.Functions import getAppPath

# * --- App constants. ---

APP_NAME: str = "JOB SEEKER"
# Realease Version. Mayor Updates / Fixes. Development Changes (Stable Commits).
APP_VERSION: str = "0.0.6"
APP_PATH: str = getAppPath()
KEYS_DIRECTORY: str = os.path.join(APP_PATH, "Keys")
