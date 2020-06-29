import re
from os.path import basename

class EnvSearch():

    def __init__(self, options):
        self.debug = options.debug or False
        self.name_only = options.name_only or False

    def search_file(self, filename: str, keyword: str):
        """
        Search the file for the keyword
        if found, return the full alias/function definition(s)
        """
        matches = Matches(filename)
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

                    if self.debug and match: print("MATCHING... ",line)
                    match_lines.append(line)

                    if match or keyword.lower() in line.lower():
                        match = True
                        if self.debug: print("KEYWORD MATCH: ",line)
                        # Trivial Case : Alias Match
                        if line.startswith('alias '):
                            if self.debug: print("Alias")
                            if line.startswith('alias {}='.format(keyword)):
                                if self.name_only:
                                    return Matches.exact(filename, match_lines)
                                matches.insert(match_lines)
                            else:
                                matches.append(match_lines)
                            match_lines = []
                            match = False

                    # Match function definition
                    if re.match(r"^[a-z\_\-]+\(\)\ ?\{", line, re.IGNORECASE):
                        in_function = True
                        if self.debug: print("In a Function: ")
                        if(re.match(r"^" + keyword + r"\(\)\ ?{",line)):
                            functionNameMatch = True
                    elif(in_function and re.match(r'^}$',line)):
                        if self.debug: print("End of Function ")
                        in_function = False
                        if match:
                            if functionNameMatch:
                                if self.name_only:
                                    return Matches.exact(filename, match_lines)
                                matches.insert(match_lines)
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

class Matches():
    def __init__(self, filename:str, definitions = None, exact_match=False):
        self.filename = basename(filename)
        self.exact_match = exact_match
        self.definitions = definitions or []

    @classmethod
    def exact(cls, filename:str, definition: list):
        return cls(filename, [definition], True)

    def insert(self, definition):
        self.definitions.insert(0, definition)

    def append(self, definition):
        self.definitions.append(definition)

    def count(self) -> int:
        return len(self.definitions)