import unittest

from thinhpf import hpf, types


class TestGraph(unittest.TestCase):
    @staticmethod
    def create_hpf_type(cap_type, label_order, root_order):
        return lambda *args: hpf(
            *args,
            capacity_type=cap_type,
            label_order=label_order,
            root_order=root_order
        )

    def setUp(self):

        self.hpf_types = []

        for cap_type in types.capacity_types_lookup:
            for label_order in types.label_order_lookup:
                for root_order in types.root_order_lookup:
                    self.hpf_types.append(
                        self.create_hpf_type(cap_type, label_order, root_order)
                    )

    def test_create_hpf(self):
        """Test HPF constructors."""
        hpf()
        for hpf_type in self.hpf_types:
            hpf_type()
        for hpf_type in self.hpf_types:
            hpf_type(100, 100)

    def test_add_node(self):
        """Test add_node function."""
        for hpf_type in self.hpf_types:

            hpf = hpf_type()

            node_id = hpf.add_node(1)
            self.assertEqual(node_id, 1)

            node_id = hpf.add_node(100)
            self.assertEqual(node_id, 101)

    def test_add_pairwise_term(self):
        """Test add_edge function."""
        for hpf_type in self.hpf_types:

            hpf = hpf_type()

            node_id = hpf.add_node(2)
            self.assertEqual(node_id, 2)

            hpf.add_edge(0, 1, 1)

    def test_example(self):
        """Test maxflow function."""
        for hpf_type in self.hpf_types:

            hpf = hpf_type()

            # Add s and t.
            next_node_id = hpf.add_node(2)
            self.assertEqual(next_node_id, 2)

            def offset(n):
                return 2 + n

            s = 0
            t = 1

            hpf.set_source(0)
            hpf.set_sink(1)

            # Number of nodes to add.
            nodes_to_add = 2

            # Add two nodes.
            next_node_id = hpf.add_node(nodes_to_add)
            self.assertEqual(next_node_id, offset(nodes_to_add))

            # Add edges.
            hpf.add_edge(s, offset(0), 5)  # s     --5->   n(0)
            hpf.add_edge(offset(0), t, 1)  # n(0)  --1->   t
            hpf.add_edge(offset(1), t, 3)  # n(1)  --3->   t
            hpf.add_edge(offset(0), offset(1), 2)  # n(0)  --2->   n(1)
            hpf.add_edge(offset(1), offset(0), 1)  # n(1)  --1->   n(0)
            # Find maxflow/cut hpf.
            hpf.mincut()
            flow = hpf.compute_maxflow()

            for n in range(nodes_to_add):
                segment = hpf.what_label(n)
                self.assertEqual(n, segment)
            # Node 0 has label 0.
            # Node 1 has label 1.

            self.assertEqual(flow, 3)
            # Maximum flow: 3


if __name__ == "__main__":
    unittest.main()
