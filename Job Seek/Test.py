"""

Job Seeker

Created by: R2D2CST

Created: 25/sep/2026

"""

# Python Modules.

# Third Party Libraries.

# Self Built Modules.
from View.CLI import runAllCliTests

from Model.Persistor import runPersistenceTestSuite

if __name__ == "__main__":
    runAllCliTests()

    runPersistenceTestSuite()

    pass
