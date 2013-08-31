﻿# Copyright (c) 2013, Matthew Sitton. 
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import imp
import importlib
import fnmatch
import time
try:  # Python 3
    from importlib.machinery import SourceFileLoader
except ImportError:  # Python 2
    from imp import load_source

# These are functions to help with file related tasks


def get_path():
    ''' get the current path '''

    fullPath = os.path.realpath(sys.path[0])

    if 'py' in fullPath.split('.'):
        fullPath = os.sep.join(fullPath.split(os.sep)[-1])

    return fullPath


def get_filename(filePath):
    ''' Return a file from a path without the extension '''
    return os.path.basename(filePath).split('.')[0]


def load_source_file(pathName, name):
    ''' Load source file from the specified file
        Returns module, and puts it as specified alias in sys.module.
    '''
    # In python 3 parts of imp needed are deprecated, we use importlib instead.
    try: # Python 3
        SourceFileLoader(name, pathName).load_module(name)
    except NameError: # Python 2
        load_source(name, pathName)

    return sys.modules[name]


def file_listener(path, queue):
    ''' check the filesystem if any times in the current path have changed.
        Must use either multiprocessing or threading
    '''
    running = True
    filesInfo = []
    oldFilesInfo = None
    while running:
        time.sleep(0.05) # To reduce 

        del oldFilesInfo
        oldFilesInfo = filesInfo
        filesInfo = []
        for root, dirname, filenames in os.walk(path):
            for fileName in fnmatch.filter(filenames, '*.py'):
                filePath = os.sep.join((root, fileName))
                filesInfo.append((filePath, os.path.getmtime(filePath)))
        data = tuple(set(filesInfo) - set(oldFilesInfo))
        if data and oldFilesInfo:
            data = tuple(item[0] for item in data)
            queue.put(data)
        else:
            del data