"""

Job Seeker

Created by: R2D2CST

Created: 29/sep/2026

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
    APP_PATH,
    KEYS_DIRECTORY,
)

from Model.Functions import (
    stringValidation,
    URLValidation,
    extractURLDomain,
)
from Model.Persistor import (
    PersistenceManager,
)


class KeyManagerModelView:

    def __init__(self):

        # Setting app constants
        self.APP_PATH = APP_PATH
        if not Path.exists(KEYS_DIRECTORY):
            os.mkdir(KEYS_DIRECTORY)
        self.KEYS_DIRECTORY = KEYS_DIRECTORY

        # Setting persister object.
        self.persister = PersistenceManager()

        pass

    def buildNewKey(
        self,
        domain: str,
        username: str,
        password: str,
    ) -> None:
        """Builds a new key into the application Key Directory.
        Args:
            domain (str): URL of the job posting site.
            username (str): Site username or acount username.
            password (str): Site password.
        Returns: None
        Raises:
            ValueError: If input validation fails.
            FileNotFoundError: Persistence processing errors occur.
        """
        # Validate target site, username and password are not empty spaces.
        failMessage: List[str] = []
        _, failReasons = URLValidation(urlString=domain)
        failMessage.extend(failReasons)
        _, failReasons = stringValidation(stringInput=username, empty=True)
        failMessage.extend(failReasons)
        _, failReasons = stringValidation(stringInput=password, empty=True)
        failMessage.extend(failReasons)
        if failMessage:
            formattedErrorMessage = "\n".join(f"- {reason}" for reason in failMessage)
            raise ValueError(
                f"Validation failed with the following errors:\n{formattedErrorMessage}"
            )

        # Build keypath.
        urlDomain = extractURLDomain(urlString=domain)
        keyFileName: str = f"{urlDomain}.json"
        keyPath = os.path.join(self.KEYS_DIRECTORY, keyFileName)

        # Build context to write.
        context: Dict[str, str] = {
            "Domain:": domain,
            "Username:": username,
            "Password:": password,
        }

        # Build and write the key.
        if not self.persister.processWrite(filePath=keyPath, dataContent=context):
            raise FileNotFoundError("Persistence processing errors occur.")
        return None

    def modifyExistingKey():
        "Modify existing key."
        pass

    def deleteExistingKey():
        "Delete existing key."
        pass

    pass
