"""Module containing functions for creating solvers."""

import numpy as np

from . import _hpf
from .types import capacity_types_lookup, label_order_lookup, root_order_lookup


def _create_class_name(base_name, capacity_type, label_order, root_order):

    try:
        capacity_type = np.dtype(capacity_type).name
    except:
        raise ValueError(
            f"Invalid capacity type '{capacity_type}'. Must be a valid NumPy dtype."
        )

    if capacity_type not in capacity_types_lookup:
        raise ValueError(
            f"Unsupported capacity type '{capacity_type}'. Supported types are: {', '.join(capacity_types_lookup)}"
        )

    if label_order not in label_order_lookup:
        raise ValueError(
            f"Unsupported label order '{label_order}'. Supported types are: {', '.join(label_order_lookup)}"
        )

    if root_order not in root_order_lookup:
        raise ValueError(
            f"Unsupported root order '{root_order}'. Supported types are: {', '.join(root_order_lookup)}"
        )

    return (
        base_name
        + capacity_types_lookup[capacity_type]
        + label_order_lookup[label_order]
        + root_order_lookup[root_order]
    )


def hpf(
    expected_nodes=0,
    expected_arcs=0,
    capacity_type="int32",
    label_order="hf",
    root_order="lifo",
):
    """Returns a new Hpf class instance of the specified type."""
    class_name = _create_class_name("Hpf", capacity_type, label_order, root_order)
    class_ctor = getattr(_hpf, class_name)
    return class_ctor(expected_nodes, expected_arcs)
