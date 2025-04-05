# distutils: language = c++

cimport cython
from libc.stdint cimport int32_t, uint32_t

from .src._hpf cimport *

ctypedef int32_t CapInt32
ctypedef float CapFloat32

# <template>
cdef class Hpf<ClassNameExt>:
    cdef Hpf[<CapType>, <LabelOrder>, <RootOrder>]* c_hpf

    def __cinit__(self, size_t expected_nodes=0, size_t expected_arcs=0):
        self.c_hpf = new Hpf[<CapType>, <LabelOrder>, <RootOrder>](expected_nodes, expected_arcs)

    def __dealloc__(self):
        del self.c_hpf

    def reserve_nodes(self, size_t num):
        self.c_hpf.reserve_nodes(num)

    def reserve_edges(self, size_t num):
        self.c_hpf.reserve_edges(num)

    def add_node(self, size_t num):
        return self.c_hpf.add_node(num)

    def add_edge(self, uint32_t i, uint32_t j, <CapType> capacity):
        self.c_hpf.add_edge(i, j, capacity)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def add_edges(self,  uint32_t[::1] i, uint32_t[::1] j, <CapType>[::1] capacity):
        cdef Py_ssize_t length = i.shape[0]

        assert i.shape[0] == j.shape[0] == capacity.shape[0]

        for n in range(length):
            self.c_hpf.add_edge(i[n], j[n], capacity[n])

    def mincut(self):
        self.c_hpf.mincut()

    def what_label(self, uint32_t node):
        return self.c_hpf.what_label(node)

    def compute_maxflow(self):
        return self.c_hpf.compute_maxflow()

    def recover_flow(self):
        self.c_hpf.recover_flow()

    def set_source(self, uint32_t s):
        self.c_hpf.set_source(s)

    def set_sink(self, uint32_t t):
        self.c_hpf.set_sink(t)

# </template>