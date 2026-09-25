"""

Job Seeker

Created by: R2D2CST

Created: 24/sep/2026

"""

# Python Modules.

# Third Party Libraries.
from colorama import (
    Fore,
    Style,
    Back,
)

# Self Built Modules.

# * --- Uniformed Style ---
# Status messages.
SUCCESS = Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTGREEN_EX
ERROR = Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTRED_EX
WARNING = Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTYELLOW_EX

# Headers and banners.
PROMPT = Style.RESET_ALL + Fore.LIGHTCYAN_EX
BANNER: str = Style.RESET_ALL + Back.BLUE + Fore.WHITE + Style.BRIGHT
HEADER_STYLE: str = Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTCYAN_EX
SUB_HEADER_STYLE: str = Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTBLUE_EX

# Content and typography.
BOLD_TEXT: str = Style.RESET_ALL + Style.BRIGHT + Fore.WHITE
TEXT: str = Style.RESET_ALL + Fore.LIGHTWHITE_EX
MUTED_TEXT: str = Style.RESET_ALL + Style.DIM + Fore.WHITE

# Style reset.
STYLE_RESET: str = Style.RESET_ALL
