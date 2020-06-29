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
    for line in match_lines:
        
        # Output a comment line
        if(re.match(r'^#',line)):
            fg = Fore.GREEN
        else:
            fg = Fore.BLUE

        print(fg + re.sub(
                        re.escape(keyword),
                        lambda m: Fore.RED + m.group(0) + fg,
                        line,
                        flags=re.I
                    )
        )
    style_reset()