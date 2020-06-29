from colorama import Fore, Back, Style
import re

def style_reset():
    print(Style.RESET_ALL)

def write_header(filename, match_count):
    print(Back.WHITE)
    print(Fore.BLACK)
    print(filename + Fore.CYAN  + " [" + str(match_count) + "]")
    style_reset()

def write_match(match_lines, keyword):
    print(Back.BLACK)
    match = ""
    for line in match_lines:
        
        # Get the exact text for the match in order to preserve casing
        m = re.search(r"" + re.escape(keyword),line,re.IGNORECASE)
        if m:
            match = m.group(0)

        # Output a comment line
        if(re.match(r'^#',line)):
            fg = Fore.GREEN
        else:
            fg = Fore.BLUE

        print(fg + re.sub(
                        re.escape(keyword),
                        Fore.RED + match + fg,
                        line,
                        flags=re.I
                    )
        )
    style_reset()