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

def find_matches(args):
    search = EnvSearch(args)
    output = []
    for _, _, files in os.walk(args.env_dir):
        for file in files:
            if file.endswith(".al"):
                matches = search.search_file("{}/{}".format(args.env_dir, file), args.search)
                if matches.exact_match:
                    return [matches]
                if len(matches.definitions) > 0:
                    output.append(matches)
    return output


def display_matches(matches, args):
    for file_matches in matches:
        # Only output exact matches when name_only flag is set
        if file_matches.exact_match or not args.name_only:
            out.write_header(
                file_matches.filename,
                file_matches.count()
            )
            for match in file_matches.definitions:
                out.write_match(match, args.search)

if __name__ == "__main__":
    matches = find_matches(args)
    display_matches(matches, args)
