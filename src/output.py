"""
    Output related helper functions
"""
import re
from colorama import Fore, Back, Style

def style_reset():
    """Resets all font colors"""
    print(Style.RESET_ALL)

def write_header(filename, match_count):
    """Outputs the filename and number of matches"""
    print(Back.WHITE)
    print(Fore.BLACK)
    print(filename + Fore.CYAN  + " [" + str(match_count) + "]")
    style_reset()

def write_match(match_lines, keyword):
    """Outputs a color-coded function definition
        with the keyword highlighted
    """
    print(Back.BLACK)
    for line in match_lines:

        # Output a comment line
        if re.match(r'^#', line):
            fore_color = Fore.GREEN
        else:
            fore_color = Fore.BLUE

        print(
            "{}{}".format(
                fore_color,
                re.sub(
                    re.escape(keyword),
                    lambda m, fg=fore_color: Fore.RED + m.group(0) + fg,
                    line,
                    flags=re.I
                )
            )
        )
    style_reset()
