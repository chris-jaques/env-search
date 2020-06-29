#!/usr/bin/env python3
"""
    Search the /env for a certain keyword
"""
import os
import sys
import re
from src.inputs import args
import src.output as out


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
                if header and line.startswith('#'):
                    continue
                elif header:
                    header = False

                if debug and match: print("MATCHING... ",line)
                match_lines.append(line)

                if match or keyword.lower() in line.lower():
                    match = True
                    if debug: print("KEYWORD MATCH: ",line)
                    # Trivial Case : Alias Match
                    if line.startswith('alias '):
                        if debug: print("Alias")
                        if line.startswith('alias {}='.format(keyword)):
                            if nameMatchOnly:
                                out.write_match(match_lines,keyword)
                                exit()
                            matches.insert(0,match_lines)
                        else:
                            matches.append(match_lines)
                        match_lines = []
                        match = False

                # Match function definition
                if re.match(r"^[a-z\_\-]+\(\)\ ?\{", line, re.IGNORECASE):
                    in_function = True
                    if debug: print("In a Function: ")
                    if(re.match(r"^" + keyword + r"\(\)\ ?{",line)):
                        functionNameMatch = True
                elif(in_function and re.match(r'^}$',line)):
                    if debug: print("End of Function ")
                    in_function = False
                    if match:
                        if functionNameMatch:
                            if nameMatchOnly:
                                out.write_match(match_lines,keyword)
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


if __name__ == "__main__":
    env_dir = os.path.expanduser("~") + "/env"
    search_string = args.search 
    nameMatchOnly = args.name_only
    debug = args.debug

    output = []
    for root, dirs, files in os.walk(env_dir):
            for file in files:
                if file.endswith(".al"):
                    matches = searchFile(env_dir + "/" + file, search_string)
                    if len(matches) > 0:
                        output.append({"file": file, "matches": matches})

    if len(output) > 0:
        for fileoutput in output:
            out.write_header(
                fileoutput['file'],
                len(fileoutput['matches'])
            )
            for match in fileoutput["matches"]:
                out.write_match(match,search_string)
