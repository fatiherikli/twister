import operator

head = operator.itemgetter(0)
tail = lambda l: l[1:]


class enum(dict):
    __getattr__ = dict.get


def inverse(dictionary, item):
    return {v: k for k, v in dictionary.items()}.get(item)
