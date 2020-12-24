def ctim_time_format(time):
    return f'{time.isoformat(timespec="seconds")}Z'


def all_subclasses(cls):
    """
    Retrieve set of class subclasses recursively.

    """
    subclasses = set(cls.__subclasses__())
    return subclasses.union(s for c in subclasses for s in all_subclasses(c))
