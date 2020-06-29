#!/usr/bin/env python3
"""
    Search the /env for a certain keyword
"""
import os
import sys
import re
from src.inputs import args
from colorama import Fore, Back, Style


def searchFile(filename, keyword):
    """
    Search the file for the keyword
    if found, return the full alias/function definition(s)
    """
    matches = []
    with open(filename, 'r') as file:
        contents = file.read()
        if keyword.lower() in contents.lower():

            match_lines = []
            in_function = False
            functionNameMatch = False
            match = False
            header = True

            for line in contents.splitlines():
                # Ignore the file headers
                if header and re.match(r'^#',line):
                    continue
                elif header:
                    header = False

                if debug and match: print("MATCHING... ",line)
                match_lines.append(line)

                if match or keyword.lower() in line.lower():
                    match = True
                    if debug: print("KEYWORD MATCH: ",line)
                    # Trivial Case : Alias Match
                    if(re.match(r'^alias\ ', line)):
                        if debug: print("Alias")
                        if(re.match(r'^alias ' + keyword + "=", line)):
                            if nameMatchOnly:
                                printMatch(match_lines,keyword)
                                exit()
                            matches.insert(0,match_lines)
                        else:
                            matches.append(match_lines)
                        match_lines = []
                        match = False

                # Match function definition
                if(re.match(r"^[a-z\_\-]+\(\)\ ?\{",line,re.IGNORECASE)):
                    in_function = True
                    if debug: print("In a Function: ")
                    if(re.match(r"^" + keyword + "\(\)\ ?{",line)):
                        functionNameMatch = True
                elif(in_function and re.match(r'^}$',line)):
                    if debug: print("End of Function ")
                    in_function = False
                    if match:
                        if functionNameMatch:
                            if nameMatchOnly:
                                printMatch(match_lines,keyword)
                                exit()
                            matches.insert(0,match_lines)
                        else:
                            matches.append(match_lines)
                    match_lines = []
                    match = False
                    functionNameMatch = False

                if not in_function and re.match('^$',line):
                    if match:
                        matches.append(match_lines)
                    match_lines = []
                    functionNameMatch = False
    return matches

def printMatch(match_lines, keyword):
    print(Back.BLACK)
    match = ""
    for line in match_lines:
        
        m = re.search(r"" + re.escape(keyword),line,re.IGNORECASE)
        if m:
            match = m.group(0)

        # Output a comment line
        if(re.match(r'^#',line)):
            print(Fore.GREEN + re.sub(re.escape(keyword), Fore.RED + match + Fore.GREEN,line,flags=re.I))
        else:
            print(Fore.BLUE + re.sub(re.escape(keyword),Fore.RED + match + Fore.BLUE,line,flags=re.I))
    print(Style.RESET_ALL)

def printFileHeader(filename, match_count):
    print(Back.WHITE)
    print(Fore.BLACK)
    print(filename + Fore.CYAN  + " [" + str(match_count) + "]")
    print(Style.RESET_ALL)


if __name__ == "__main__":
    env_dir = os.path.expanduser("~") + "/env"
    search_string = args.search 
    nameMatchOnly = args.name_only
    debug = args.debug
    print(Style.RESET_ALL)
    output = []
    for root, dirs, files in os.walk(env_dir):
            for file in files:
                if file.endswith(".al"):
                    matches = searchFile(env_dir + "/" + file, search_string)
                    if len(matches) > 0:
                        output.append({"file": file, "matches": matches})

    if len(output) > 0:
        for fileoutput in output:
            printFileHeader(fileoutput["file"],len(fileoutput["matches"]))
            for match in fileoutput["matches"]:
                printMatch(match,search_string)
