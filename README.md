# Thin wrapper for HPF
Thin Python wrapper for the non-parametric Hochbaum Pseudoflow (HPF) min-cut/max-flow algorithm. The original source code by Bala Chandran and Dorit S. Hochbaum is availbable [here](https://riot.ieor.berkeley.edu/Applications/Pseudoflow/maxflow.html). The C++ code used in this wrapper has been refractored by Patrick M. Jensen and published [here](https://github.com/patmjen/maxflow_algorithms).

## Installation
```
pip install thinhpf
```
## Tiny example
```python
import thinhpf

hpf = thinhpf.hpf()

# Add s and t.
next_node_id = hpf.add_node(2)

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
    print('Node %d has label %d.' % (n, segment))
# Node 0 has label 0.
# Node 1 has label 1.

print('Flow: %s' % flow)
# Maximum flow: 3
```

## Related repositories
- [Hochbaum Group](https://github.com/hochbaumGroup) on GitHub
- [Original source](https://riot.ieor.berkeley.edu/Applications/Pseudoflow/maxflow.html) website
- [slgbuilder](https://github.com/Skielex/slgbuilder) Python package (CVPR 2020)
- [shrdr](https://github.com/Skielex/shrdr) Python package (ICCV 2021)
- [thinqpbo](https://github.com/Skielex/thinqpbo) Python package
- [thinmaxflow](https://github.com/Skielex/thinmaxflow) Python package
- [C++ implementations](https://github.com/patmjen/maxflow_algorithms) of max-flow/min-cut algorithms

## License
The original C code by Bala Chandran and Dorit S. Hochbaum and thereby the content of `hpf.h` (previously `pseudo.c`) is published under an academic license (see LICENSE file). More information on the [original website](https://riot.ieor.berkeley.edu/Applications/Pseudoflow/maxflow.html).