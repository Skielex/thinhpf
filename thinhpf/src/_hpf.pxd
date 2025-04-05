# _hpf.pxd
# distutils: language = c++

from libc.stdint cimport uint32_t


cdef extern from "core/hpf.h":
    ctypedef enum class LabelOrder:
        pass
        
    ctypedef enum class RootOrder:
        pass

    ctypedef enum class TermType(uint32_t):
        pass

    ### Hacky way to pass enums to template.
    cdef cppclass HF "LabelOrder::HIGHEST_FIRST":
        pass

    cdef cppclass LF "LabelOrder::LOWEST_FIRST":
        pass

    cdef cppclass FIFO "RootOrder::FIFO":
        pass

    cdef cppclass LIFO "RootOrder::LIFO":
        pass
    ###

    cdef cppclass Hpf[Cap, LabelOrder, RootOrder]:
        Hpf(size_t expectedNodes, size_t expectedArcs)
        void reserve_nodes(size_t num)
        void reserve_edges(size_t num)
        uint32_t add_node(uint32_t num)
        void add_edge(uint32_t i, uint32_t j, Cap capacity)
        void mincut()
        TermType what_label(uint32_t node) const
        Cap compute_maxflow() const
        void recover_flow()
        void set_source(uint32_t s)
        void set_sink(uint32_t t)