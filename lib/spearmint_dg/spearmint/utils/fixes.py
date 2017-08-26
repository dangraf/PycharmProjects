import sys

def items(x):
    if sys.version < '3':
        return x.iteritems()
    return x.items()

def xrange(*args):
    if sys.version < '3':
        return __builtins__['xrange'](*args)  # seems a bit fishy, in my console __builtins__.xrange() works
    return range(*args)
