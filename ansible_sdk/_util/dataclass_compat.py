# make everything from the real module available here
from dataclasses import *

# this can be removed once we no longer support Python 3.9
if 'KW_ONLY' not in globals():
    _dataclass_real = dataclass

    def dataclass(cls=None, *args, **kwargs):
        """a rudimentary polyfill for `kw_only` support on Python 3.9"""

        def wrap(cls):
            kwo = kwargs.pop('kw_only', None)
            dc = _dataclass_real(cls, *args, **kwargs)

            if kwo:
                realinit = dc.__init__

                def initwrapper(self, *args, **kwargs):
                    if args:
                        raise TypeError(f'{self.__class__.__name__} only supports construction with keyword arguments')
                    return realinit(self, *args, **kwargs)

                dc.__init__ = initwrapper
            return dc

        # decorator applied as a function call (eg @dataclass(...)); capture the args and return a closure to build the class later
        if not cls:
            return wrap

        # decorator applied as a type (eg @dataclass); build the class now
        return wrap(cls)

