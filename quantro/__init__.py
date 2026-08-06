"""Quantro: Türkiye'nin ilk 7 araçlık kuantum + astrofizik interaktif lab setinin
açık kaynak çekirdeği."""

from .core import (
    QuantumCircuit,
    Qubit,
    bell_state,
    ghz_state,
    sample_distribution,
)

__version__ = "0.1.0"

__all__ = [
    "QuantumCircuit",
    "Qubit",
    "bell_state",
    "ghz_state",
    "sample_distribution",
    "__version__",
]
