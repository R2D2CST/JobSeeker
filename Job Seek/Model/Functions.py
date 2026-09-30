"""

Job Seeker

Created by: R2D2CST

Created: 27/sep/2026

"""

# Python Modules.
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
    punctuation,
    whitespace,
)
from urllib.parse import (
    ParseResult,
    urlparse,
    parse_qs,
)
import sys
import os
from typing import (
    Tuple,
    List,
)
import re

# Third Party Libraries.

# Self Built Modules.


def getAppPath() -> str:
    """This function gets the path where the current code (`__main__`) is been executed, this path will be an absolute path to the file in order to get files and saving elements.
    Args:
        None
    Returns:
        scriptDirectory (str): string containing the directory path absolute path.
    Raises:
        None
    """
    # We get the absolute path where the `__main__` program will be executed.
    if getattr(sys, "frozen", False):
        # If the program has been packed for distribution follows this path.
        scriptDirectory = os.path.dirname(sys.executable)
    else:
        # If program is been executed as a python file.
        scriptDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))
        """
        When this is not main:
        scriptDirectory = os.path.dirname(os.path.abspath(sys.argv[0])) 
        When this is main or we desire the module path:
        scriptDirectory = os.path.dirname(os.path.abspath(__file__) 
        """
    # Returns the script directory.
    return scriptDirectory


def stringValidation(
    stringInput: str,
    empty: bool = False,
    minLength: int = 1,
    numbers: bool = False,
    capital: bool = False,
    specialChar: bool = False,
) -> Tuple[bool, List[str]]:
    """Validates if a string meets given conditions.

    - empty: if True, validates that the string is not empty and not just whitespace.
    - minLength: validates that the string length is greater than or equal to minLength.
    - numbers: validates that the string contains at least one digit.
    - capital: validates that the string contains at least one capital letter.
    - specialChar: validates that the string contains at least one punctuation character.

    Args:
        stringInput (str): The string instance to be validated.
        empty (bool, optional): Flag to enforce non-empty check. Defaults to False.
        minLength (int, optional): Minimum required character length. Defaults to 8.
        numbers (bool, optional): Flag to enforce digit presence. Defaults to False.
        capital (bool, optional): Flag to enforce uppercase character presence. Defaults to False.
        specialChar (bool, optional): Flag to enforce punctuation character presence. Defaults to False.

    Returns:
        Tuple[bool, List[str]]: A tuple containing a boolean result (True if all enabled conditions pass)
        and a list of failure reason descriptions.
    """
    failReasons: List[str] = []

    # 1. Empty validation
    if empty:
        if not stringInput or not stringInput.strip():
            failReasons.append(
                "The string must not be empty or consist solely of whitespace characters."
            )

    # 2. Minimum length validation
    if len(stringInput) < minLength:
        failReasons.append(
            f"The string length must be at least {minLength} characters long."
        )

    # 3. Numeric character validation
    if numbers:
        hasDigit = any(char in digits for char in stringInput)
        if not hasDigit:
            failReasons.append("The string must contain at least one numeric digit.")

    # 4. Capital letter validation
    if capital:
        hasCapital = any(char in ascii_uppercase for char in stringInput)
        if not hasCapital:
            failReasons.append("The string must contain at least one uppercase letter.")

    # 5. Special character validation
    if specialChar:
        hasSpecial = any(char in punctuation for char in stringInput)
        if not hasSpecial:
            failReasons.append(
                "The string must contain at least one special/punctuation character."
            )

    isValid = len(failReasons) == 0
    return isValid, failReasons


def URLValidation(urlString: str) -> Tuple[bool, List[str]]:
    """Validates if a given string meets a Uniform Resource Locator (URL) format.

    Args:
        urlString (str): uniform resource locator (URL) valid string.

    Returns:
        Tuple[bool, List[str]]: A tuple containing a boolean result (True if all enabled conditions pass)
        and a list of failure reason descriptions.
    """
    failureReasons: List[str] = []

    if not urlString or not urlString.strip():
        failureReasons.append("The input URL string cannot be empty.")
        return False, failureReasons

    try:
        parsedUrl: ParseResult = urlparse(urlString)

        # 1. Validate Scheme / Protocol
        if not parsedUrl.scheme:
            failureReasons.append("Missing URL scheme (e.g., 'http://' or 'https://').")
        elif parsedUrl.scheme.lower() not in ["http", "https"]:
            failureReasons.append(
                f"Unsupported scheme '{parsedUrl.scheme}'. Only 'http' and 'https' are allowed."
            )

        # 2. Validate Authority / Domain
        if not parsedUrl.netloc:
            failureReasons.append(
                "Missing domain authority or network location (e.g., 'example.com')."
            )

        # Result calculation
        isValid: bool = len(failureReasons) == 0
        return isValid, failureReasons

    except ValueError as error:
        failureReasons.append(f"Malformed URL string: {str(error)}")
        return False, failureReasons


def extractURLDomain(urlString: str) -> str:
    """Extracts the core domain name from a given URL string.
    Args:
        urlString (str): The full URL to parse.
    Returns:
        str: The extracted core domain name or an empty string if invalid.
    """
    # Ensure URL has a scheme for proper parsing
    normalizedUrl = (
        f"http://{urlString}"
        if not re.match(r"^https?://", urlString, re.IGNORECASE)
        else urlString
    )

    try:
        parsedUrl = urlparse(normalizedUrl)
        hostname = parsedUrl.hostname

        if not hostname:
            return ""

        # Remove 'www.' if present
        if hostname.startswith("www."):
            hostname = hostname[4:]

        # Extract the first segment of the domain name
        domainParts = hostname.split(".")
        return domainParts[0] if domainParts else ""

    except Exception:
        return ""
