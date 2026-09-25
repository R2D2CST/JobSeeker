"""

Job Seeker

Created by: R2D2CST

Created: 24/sep/2026

"""

# Python Modules.

# Third Party Libraries.
from colorama import init

# Self Built Modules.
from View.AppStyle import (
    SUCCESS,
    ERROR,
    WARNING,
    PROMPT,
    BANNER,
    HEADER_STYLE,
    SUB_HEADER_STYLE,
    BOLD_TEXT,
    TEXT,
    MUTED_TEXT,
    STYLE_RESET,
)

MAIN_MENU_OPTIONS: list[str] = [
    "Exit.",
]


class MainLoop:

    def __init__(self):
        # Starts colorama color and style modifier.
        init()

        print(f"{SUCCESS}Success")
        print(f"{ERROR}Error")
        print(f"{WARNING}Warning")
        print(f"{PROMPT}Prompt")
        print(f"{BANNER}Banner{STYLE_RESET}")
        print(f"{HEADER_STYLE}Header Style")
        print(f"{SUB_HEADER_STYLE}Sub Header Style")
        print(f"{BOLD_TEXT}Bold Text")
        print(f"{TEXT}Text")
        print(f"{MUTED_TEXT}Muted Text")

        pass

    pass
