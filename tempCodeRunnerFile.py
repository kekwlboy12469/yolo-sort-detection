cdef class Foo(object):
    def __bool__(self):
        return True
    def __nonzero__(self):
        return self.__bool__()