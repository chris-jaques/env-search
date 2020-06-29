#!/usr/bin/env python3
"""
    Search the /env for a certain keyword
"""
import os
import sys
import re
from src.inputs import args
import src.output as out
from src.search import EnvSearch

if __name__ == "__main__":
    env_dir = os.path.expanduser("~") + "/env"
    search = EnvSearch(args)

    output = []
    for root, dirs, files in os.walk(env_dir):
        for file in files:
            if file.endswith(".al"):
                matches = search.search_file(env_dir + "/" + file, args.search)
                if matches.exact_match:
                    output = [matches]
                    break
                if len(matches.definitions) > 0:
                    output.append(matches)

    if len(output) > 0:
        for fileoutput in output:
            out.write_header(
                fileoutput.filename,
                len(fileoutput.definitions)
            )
            for match in fileoutput.definitions:
                out.write_match(match, args.search)