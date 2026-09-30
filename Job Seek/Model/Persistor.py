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
from typing import (
    Any,
    List,
    Union,
    Dict,
)

# Third Party Libraries.

# Self Built Modules.

# * --- Abstract and Child Clases ---


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

    pass


class JsonPersister(BasePersister):

    def readData(self, filePath: str) -> Dict[str:Any]:
        """
        Receives a JSON file path and returns the content in the given file path.
        Args:
            filePath (str): JSON valid file path.
        Returns:
            content (Dict[str:Any]): valid JSON dictionary content format.
        """
        try:
            with open(filePath, "r", encoding="utf-8") as fileStream:
                return json.load(fileStream)
        except Exception as executionError:
            print(f"Error reading JSON from {filePath}: {executionError}")
            return None

    def writeData(self, filePath: str, dataContent: Any | Dict[str:Any]) -> bool:
        """
        Receives a dictionary and writes it's content into a JSON valid format.
        Args:
            filePath (str): a valid JSON file path.
            dataContent (Any | Dict [str:Any]): valid JSON content format.

        Returns:
            bool: True, in case of success. False, in case of failure while writing.
        """
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
        """
        Receives a text (TXT) file path and returns the content in the given file path.
        Args:
            filePath (str): TXT valid file path.
        Returns:
            content (str): valid TXT string content format.
        """
        try:
            with open(filePath, "r", encoding="utf-8") as fileStream:
                return fileStream.read()
        except Exception as executionError:
            print(f"Error reading text from {filePath}: {executionError}")
            return ""

    def writeData(self, filePath: str, dataContent: str) -> bool:
        """
        Receives a string and writes it's content into a TEXT valid format.
        Args:
            filePath (str): a valid TXT file path.
            dataContent (str): valid TXT content format.

        Returns:
            bool: True, in case of success. False, in case of failure while writing.
        """
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
        """
        Receives a comma separate value (CSV) file path and returns the content in the given file path.
        Args:
            filePath (str): CSV valid file path.
        Returns:
            content (List[List[str]]): valid CSV nested lists content format.
        """
        try:
            with open(filePath, "r", encoding="utf-8", newline="") as fileStream:
                csvReader = csv.reader(fileStream)
                return list(csvReader)
        except Exception as executionError:
            print(f"Error reading CSV from {filePath}: {executionError}")
            return []

    def writeData(self, filePath: str, dataContent: List[List[Any]]) -> bool:
        """
        Receives a nested lists data format and writes it's content into a CSV valid format.
        Args:
            filePath (str): a valid TXT file path.
            dataContent (List[List[Any]]): valid CSV nested list content format.

        Returns:
            bool: True, in case of success. False, in case of failure while writing.
        """
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
        """
        Receives a Log (LOG) file path and returns the content in the given file path as a list of strings without trailing end lines (\\n)
        Args:
            filePath (str): LOG valid file path.
        Returns:
            content (List[str]): valid list of string content for the LOG format.
        """
        try:
            with open(filePath, "r", encoding="utf-8") as fileStream:
                return [line.rstrip("\r\n") for line in fileStream.readlines()]
        except Exception as executionError:
            print(f"Error reading log lines from {filePath}: {executionError}")
            return []

    def appendLogEntry(self, filePath: str, logMessage: str) -> bool:
        """
        Receives a string and appends it's content into a list of strings (LOG) valid format.
        Args:
            filePath (str): a valid TXT file path.
            dataContent (str): valid TXT content format.

        Returns:
            bool: True, in case of success. False, in case of failure while writing.
        """
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
        """Class initializer, first initializes the persister objects and latter build the class maps for the persister objects and valid data structure.
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        # * Object initializations.
        self.jsonPersister = JsonPersister()
        self.textPersister = TextPersister()
        self.csvPersister = CsvPersister()
        self.logPersister = LogPersister()
        self.markdownPersister = MarkdownPersister()

        # * Persistent object mapping.
        self.formatMap: Dict[str, BasePersister] = {
            ".json": self.jsonPersister,
            ".txt": self.textPersister,
            ".csv": self.csvPersister,
            ".log": self.logPersister,
            ".md": self.markdownPersister,
        }

        # * Valid persistent formats mapping.
        self.dataStructuresMap: Dict[str, str] = {
            ".json": "Dict[str:Any]",
            ".txt": "str",
            ".csv": "List[List[Any]]",
            ".log": "str",
            ".md": "str",
        }
        return None

    def __extractExtension(self, filePath: str) -> str:
        """Extracts and normalizes the file extension from a file path.
        Args:
            filePath (str): The target file path.
        Returns:
            str: The lowercased extension including the dot (e.g., '.json').
        """
        _, fileExtension = os.path.splitext(filePath)
        return fileExtension.lower()

    def __validateDataStructure(
        self,
        fileExtension: str,
        dataContent: Any,
    ) -> bool:
        """Validates if the content matches the required data structure for the inferred format.
        Args:
            fileExtension (str): The normalized file extension (e.g., '.json').
            dataContent (Any): The payload to be verified.
        Returns:
            bool: True if dataContent matches the expected structure, False otherwise.
        """
        targetStructure = self.dataStructuresMap.get(fileExtension)

        if not targetStructure:
            return False

        if targetStructure == "str":
            return isinstance(dataContent, str)  # Returns True if str.

        if targetStructure == "Dict[str:Any]":
            if not isinstance(dataContent, dict):
                return False
            # Returns True all keys are str.
            return all(isinstance(key, str) for key in dataContent.keys())

        if targetStructure == "List[List[Any]]":
            if not isinstance(dataContent, list):
                return False
            # Returns True if all elements with in the list are nested lists.
            return all(isinstance(row, list) for row in dataContent)

        return False

    def processWrite(self, filePath: str, dataContent: Any) -> bool:
        """Dispatches write operations based on the file extension after validating data structure.

        Args:
            filePath (str): The destination file path including filename and extension.
            dataContent (Any): The payload content to write.

        Returns:
            bool: True if the write operation succeeded.

        Raises:
            ValueError: If the file extension is unsupported or if dataContent fails structure validation.
        """
        fileExtension = self.__extractExtension(filePath)
        persister = self.formatMap.get(fileExtension)

        if not persister:
            raise ValueError(
                f"Unsupported file extension '{fileExtension}' for path: {filePath}"
            )

        if not self.__validateDataStructure(fileExtension, dataContent):
            expectedType = self.dataStructuresMap.get(fileExtension)
            receivedType = type(dataContent).__name__
            raise TypeError(
                f"Data structure mismatch for '{fileExtension}'. Expected: {expectedType}, Received: {receivedType}"
            )

        return persister.writeData(filePath, dataContent)

    def processRead(self, filePath: str) -> Any:
        """Dispatches read operations based on the file extension.

        Args:
            filePath (str): The source file path to read data from.

        Returns:
            Any: The parsed content of the file.

        Raises:
            ValueError: If the file extension is unsupported.
        """
        fileExtension = self.__extractExtension(filePath)
        persister = self.formatMap.get(fileExtension)

        if not persister:
            raise ValueError(
                f"Unsupported file extension '{fileExtension}' for path: {filePath}"
            )

        return persister.readData(filePath)

    pass


# ! Unit tests.


class TestPersistenceLayer(unittest.TestCase):

    def setUp(self) -> None:
        """Creates an isolated temporary directory for test file generation."""
        self.testDirectory = tempfile.mkdtemp()
        self.manager = PersistenceManager()

    def tearDown(self) -> None:
        """Cleans up temporary directory after test execution."""
        shutil.rmtree(self.testDirectory)

    def testJsonPersisterDirectly(self) -> None:
        """Tests JsonPersister direct read and write operations."""
        persister = JsonPersister()
        filePath = os.path.join(self.testDirectory, "directTest.json")
        payload = {"projectName": "Job Seeker", "version": 1.0, "status": "Active"}

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testTextPersisterDirectly(self) -> None:
        """Tests TextPersister direct read and write operations."""
        persister = TextPersister()
        filePath = os.path.join(self.testDirectory, "directTest.txt")
        payload = "Hello World\nPersistence Test"

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testCsvPersisterDirectly(self) -> None:
        """Tests CsvPersister direct read and write operations."""
        persister = CsvPersister()
        filePath = os.path.join(self.testDirectory, "directTest.csv")
        payload = [
            ["ID", "Name", "Role"],
            ["1", "Alice", "Developer"],
            ["2", "Bob", "Tester"],
        ]

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testLogPersisterDirectly(self) -> None:
        """Tests LogPersister read, write, append, and line extraction operations."""
        persister = LogPersister()
        filePath = os.path.join(self.testDirectory, "directTest.log")
        initialContent = "2026-09-27 10:00:00 [INFO] System Initialized"
        appendContent = "2026-09-27 10:05:00 [ERROR] Connection Timeout"

        self.assertTrue(persister.writeData(filePath, initialContent))
        self.assertTrue(persister.appendLogEntry(filePath, appendContent))

        fullLogText = persister.readData(filePath)
        self.assertIn(initialContent, fullLogText)
        self.assertIn(appendContent, fullLogText)

        lines = persister.readLogLines(filePath)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], initialContent)
        self.assertEqual(lines[1], appendContent)

    def testMarkdownPersisterDirectly(self) -> None:
        """Tests MarkdownPersister direct read and write operations."""
        persister = MarkdownPersister()
        filePath = os.path.join(self.testDirectory, "directTest.md")
        payload = "# Header\n\n- Item 1\n- Item 2"

        self.assertTrue(persister.writeData(filePath, payload))
        readPayload = persister.readData(filePath)
        self.assertEqual(readPayload, payload)

    def testPersistenceManagerSuccessCases(self) -> None:
        """Challenges PersistenceManager with valid payloads across all supported file extensions."""
        testCases: Dict[str, Any] = {
            "testFile.json": {"app": "JobSeeker", "modulesCount": 5},
            "testFile.txt": "Line 1 content\nLine 2 content",
            "testFile.csv": [["Col1", "Col2"], ["Val1", "Val2"]],
            "testFile.log": "2026-09-27 [DEBUG] Executing manager test",
            "testFile.md": "## Title\n\n> [!info] Reference Block",
        }

        for fileName, payload in testCases.items():
            filePath = os.path.join(self.testDirectory, fileName)
            with self.subTest(fileName=fileName):
                self.assertTrue(self.manager.processWrite(filePath, payload))
                readContent = self.manager.processRead(filePath)
                self.assertEqual(readContent, payload)

    def testPersistenceManagerDataStructureMismatch(self) -> None:
        """Challenges PersistenceManager by passing invalid data structures for specific extensions."""
        mismatchCases: Dict[str, Any] = {
            "invalidJson.json": ["Not", "A", "Dict"],
            "invalidCsv.csv": {"key": "Not a List of Lists"},
            "invalidTxt.txt": 123456,
            "invalidLog.log": ["Not", "A", "String"],
            "invalidMd.md": {"not": "string"},
        }

        for fileName, payload in mismatchCases.items():
            filePath = os.path.join(self.testDirectory, fileName)
            with self.subTest(fileName=fileName):
                with self.assertRaises(TypeError):
                    self.manager.processWrite(filePath, payload)

    def testPersistenceManagerUnsupportedExtensions(self) -> None:
        """Tests handling of unsupported file extensions in read and write operations."""
        invalidPaths = [
            os.path.join(self.testDirectory, "file.xml"),
            os.path.join(self.testDirectory, "file.yaml"),
            os.path.join(self.testDirectory, "fileNoExtension"),
        ]

        for filePath in invalidPaths:
            with self.subTest(filePath=filePath):
                with self.assertRaises(ValueError):
                    self.manager.processWrite(filePath, "sample data")

                with self.assertRaises(ValueError):
                    self.manager.processRead(filePath)


def runPersistenceTestSuite() -> None:
    """Integrator function to execute the full unit test suite and return results."""
    testLoader = unittest.TestLoader()
    testSuite = testLoader.loadTestsFromTestCase(TestPersistenceLayer)
    testRunner = unittest.TextTestRunner(verbosity=2)
    testRunner.run(testSuite)


if __name__ == "__main__":
    runPersistenceTestSuite()
