import sys
import argparse
import os

def __parse_input():
    parser = argparse.ArgumentParser(
        prog='Env Search Utility',
        description='searches *.al files in ~/env/ for a keyword/phrase')
    # Args
    parser.add_argument('search', type=str, help="the env is searched for an exact match of this text")
    parser.add_argument('-n', '--name-only', action='store_true', help="Only match search text against alias and function names")
    parser.add_argument('-d', '--debug', action='store_true', default=os.getenv('ENV_SEARCH_DEBUG',False), help="Provide extra debug output for development")
    parser.add_argument('--env-dir', default="{}/env".format(os.path.expanduser("~")), help="Directory where the env is located")

    return parser.parse_args()

args = __parse_input()