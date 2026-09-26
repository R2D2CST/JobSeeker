"""

Job Seeker

Created by: R2D2CST

Created: 25/sep/2026

"""

# Python Modules.
import os
import shutil
import tempfile
import unittest
from abc import (
    ABC,
    abstractmethod,
)
import csv
import json
from typing import Any, List, Union

# Third Party Libraries.

# Self Built Modules.


class BasePersister(ABC):
    """Abstract Base Class defining the contract for data persistence across formats.

    All subclasses must implement readData and writeData methods following camelCase naming conventions.
    """

    @abstractmethod
    def readData(self, filePath: str) -> Any:
        """Reads data from the specified file path.

        Args:
            filePath (str): The absolute or relative path to the source file.

        Returns:
            Any: The parsed content of the file.
        """
        pass

    @abstractmethod
    def writeData(self, filePath: str, dataContent: Any) -> bool:
        """Writes data content to the specified file path.

        Args:
            filePath (str): The destination path for the file.
            dataContent (Any): The payload to be persisted.

        Returns:
            bool: True if the write operation succeeded, False otherwise.
        """
        pass


class JsonPersister(BasePersister):

    def readData(self, filePath: str) -> Any:
        try:
            with open(filePath, "r", encoding="utf-8") as fileStream:
                return json.load(fileStream)
        except Exception as executionError:
            print(f"Error reading JSON from {filePath}: {executionError}")
            return None

    def writeData(self, filePath: str, dataContent: Any) -> bool:
        try:
            with open(filePath, "w", encoding="utf-8") as fileStream:
                json.dump(dataContent, fileStream, indent=4, ensure_ascii=False)
            return True
        except Exception as executionError:
            print(f"Error writing JSON to {filePath}: {executionError}")
            return False

    pass


class TextPersister(BasePersister):

    def readData(self, filePath: str) -> str:
        try:
            with open(filePath, "r", encoding="utf-8") as fileStream:
                return fileStream.read()
        except Exception as executionError:
            print(f"Error reading text from {filePath}: {executionError}")
            return ""

    def writeData(self, filePath: str, dataContent: str) -> bool:
        try:
            with open(filePath, "w", encoding="utf-8") as fileStream:
                fileStream.write(str(dataContent))
            return True
        except Exception as executionError:
            print(f"Error writing text to {filePath}: {executionError}")
            return False

    pass


class CsvPersister(BasePersister):

    def readData(self, filePath: str) -> List[List[str]]:
        try:
            with open(filePath, "r", encoding="utf-8", newline="") as fileStream:
                csvReader = csv.reader(fileStream)
                return list(csvReader)
        except Exception as executionError:
            print(f"Error reading CSV from {filePath}: {executionError}")
            return []

    def writeData(self, filePath: str, dataContent: List[List[Any]]) -> bool:
        try:
            with open(filePath, "w", encoding="utf-8", newline="") as fileStream:
                csvWriter = csv.writer(fileStream)
                csvWriter.writerows(dataContent)
            return True
        except Exception as executionError:
            print(f"Error writing CSV to {filePath}: {executionError}")
            return False

    pass


class LogPersister(TextPersister):

    def readLogLines(self, filePath: str) -> List[str]:
        """Reads all entries from the log file as a list of strings without trailing newlines."""
        try:
            with open(filePath, "r", encoding="utf-8") as fileStream:
                return [line.rstrip("\r\n") for line in fileStream.readlines()]
        except Exception as executionError:
            print(f"Error reading log lines from {filePath}: {executionError}")
            return []

    def appendLogEntry(self, filePath: str, logMessage: str) -> bool:
        """Appends a new log entry to the end of the specified log file."""
        try:
            with open(filePath, "a", encoding="utf-8") as fileStream:
                fileStream.write(f"{logMessage}\n")
            return True
        except Exception as executionError:
            print(f"Error appending to log {filePath}: {executionError}")
            return False

    pass


class MarkdownPersister(TextPersister):
    """Handles Markdown document reading and writing by leveraging text stream operations."""

    pass


# * --- Persistence Manager (Model View intended object to use and call.) ---


class PersistenceManager:
    """Facade Manager Class providing unified access to all persister instances."""

    def __init__(self) -> None:
        self.jsonPersister = JsonPersister()
        self.textPersister = TextPersister()
        self.csvPersister = CsvPersister()
        self.logPersister = LogPersister()
        self.markdownPersister = MarkdownPersister()

    def processWrite(self, formatType: str, filePath: str, dataContent: Any) -> bool:
        """Dispatches write operations based on format selection."""
        formatMap = {
            "json": self.jsonPersister,
            "txt": self.textPersister,
            "csv": self.csvPersister,
            "log": self.logPersister,
            "md": self.markdownPersister,
        }
        persister = formatMap.get(formatType.lower())
        if not persister:
            raise ValueError(f"Unsupported format type: {formatType}")
        return persister.writeData(filePath, dataContent)

    def processRead(self, formatType: str, filePath: str) -> Any:
        """Dispatches read operations based on format selection."""
        formatMap = {
            "json": self.jsonPersister,
            "txt": self.textPersister,
            "csv": self.csvPersister,
            "log": self.logPersister,
            "md": self.markdownPersister,
        }
        persister = formatMap.get(formatType.lower())
        if not persister:
            raise ValueError(f"Unsupported format type: {formatType}")
        return persister.readData(filePath)

    pass


# ! Unit tests.

class TestPersistenceLayer(unittest.TestCase):

    def setUp(self) -> None:
        """Creates a isolated temporary directory for test file generation."""
        self.testDirectory = tempfile.mkdtemp()
        self.manager = PersistenceManager()

    def tearDown(self) -> None:
        """Cleans up temporary directory after test execution."""
        shutil.rmtree(self.testDirectory)

    def testJsonPersister(self) -> None:
        persister = JsonPersister()
        filePath = os.path.join(self.testDirectory, "test.json")
        payload = {"projectName": "Job Seeker", "version": 1.0, "status": "Active"}

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testTextPersister(self) -> None:
        persister = TextPersister()
        filePath = os.path.join(self.testDirectory, "test.txt")
        payload = "Hello World\nPersistence Test"

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testCsvPersister(self) -> None:
        persister = CsvPersister()
        filePath = os.path.join(self.testDirectory, "test.csv")
        payload = [["ID", "Name", "Role"], ["1", "Alice", "Developer"], ["2", "Bob", "Tester"]]

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testLogPersister(self) -> None:
        persister = LogPersister()
        filePath = os.path.join(self.testDirectory, "test.log")
        initialContent = "2026-09-25 10:00:00 [INFO] System Initialized"
        appendContent = "2026-09-25 10:05:00 [ERROR] Connection Timeout"

        self.assertTrue(persister.writeData(filePath, initialContent))
        self.assertTrue(persister.appendLogEntry(filePath, appendContent))

        fullLogText = persister.readData(filePath)
        self.assertIn(initialContent, fullLogText)
        self.assertIn(appendContent, fullLogText)

        lines = persister.readLogLines(filePath)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], initialContent)
        self.assertEqual(lines[1], appendContent)

    def testMarkdownPersister(self) -> None:
        persister = MarkdownPersister()
        filePath = os.path.join(self.testDirectory, "test.md")
        payload = "# Header\n\n- Item 1\n- Item 2"

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testPersistenceManagerIntegrator(self) -> None:
        filePath = os.path.join(self.testDirectory, "integrator.json")
        payload = {"key": "value"}

        self.assertTrue(self.manager.processWrite("json", filePath, payload))
        readPayload = self.manager.processRead("json", filePath)
        self.assertEqual(readPayload, payload)

        with self.assertRaises(ValueError):
            self.manager.processRead("xml", filePath)


def runPersistenceTestSuite() -> None:
    """Integrator function to execute the full unit test suite and return results."""
    testLoader = unittest.TestLoader()
    testSuite = testLoader.loadTestsFromTestCase(TestPersistenceLayer)
    testRunner = unittest.TextTestRunner(verbosity=2)
    testRunner.run(testSuite)


if __name__ == "__main__":
    runPersistenceTestSuite()