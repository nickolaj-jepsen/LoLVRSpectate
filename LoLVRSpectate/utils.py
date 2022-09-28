import time
import os
import logging
import platform
import sys


# From https://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/
from LoLVRSpectate.VorpX import is_excluded


class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {
                key: self._caches[func][key]
                for key in self._caches[func]
                if (time.time() - self._caches[func][key][1])
                < self._timeouts[func]
            }

            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                v = self.cache[key] = f(*args, **kwargs), time.time()
            return v[0]
        func.func_name = f.__name__

        return func


def setup_logging(debug=False, os_info=True):
    if os.environ.get("LOLVRSPECTATE_DEBUG") == "1":
        debug = True

    if not debug:
        format_ = '%(asctime)-15s || %(message)s'
        logging.basicConfig(filename="LoLVRSpectate.log", format=format_, level=logging.INFO, filemode="w")
        logging.getLogger().addHandler(logging.StreamHandler())  # Log both to file and console
    else:
        logging.basicConfig(level=logging.DEBUG)

    if os_info:
        logging.info(f"Win platform = {platform.platform()}")
        if 'PROGRAMFILES(X86)' in os.environ:
            logging.info('System Arch = 64 bit')
        else:
            logging.info('System Arch = 32 bit')
        logging.info(f"Python version = {sys.version}")
        logging.info(f"VorpX exclusion = {is_excluded()}")
