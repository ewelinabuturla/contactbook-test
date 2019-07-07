#!/usr/bin/env python3

import functools
import os


class Cacher(object):

    """
    Cashing class to keep backup of database in a file
    """

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def __call__(self, func, *args, **kwargs):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('Caching new object')
            cache_name = func.__name__
            path = os.path.join(self.cache_dir, cache_name)
            results =  str(func(*args, **kwargs))
            if os.path.exists(path):
                with open(path, 'r+') as f:
                    file_res = f.read()
                    if file_res != results:
                        f.seek(0)
                        f.truncate()
                        print('Updating file, difference between results')
                        f.write(results)
                    else:
                        print('No updates, no difference between files')
                        return results
            else:
                with open(path, 'w') as f:
                    print('File not exists, creating')
                    f.write(results)
            return results
        return wrapper
