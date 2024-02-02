from typing import Iterable


class EnumMetaclass(type):
    __all__: Iterable

    def __contains__(self, item):
        return item in self.__all__
