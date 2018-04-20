# Common useful methods

import os
import sys
import fnmatch

def findFile(filename, pathToSearch):
        for root, directories, files in os.walk(pathToSearch):
                if filename in files:
                        return os.path.join(root, filename)

def findFileAllMatches(fileToFind, pathToSearch):
        results = []
        for root, dirs, files in os.walk(path):
                for name in files:
                        if fnmatch.fnmatch(name, pattern):
                                result.append(os.path.join(root, name))
        return results

