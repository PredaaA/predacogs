import functools


def rgetattr(obj, attr, *args):
    def _getattr(obj2, attr2):
        return getattr(obj2, attr2, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))
