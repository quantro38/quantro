"""Quantro CLI: örnek devreleri çalıştırıp dağılımı yazdırır.

Kullanım:
    python3 -m quantro single     # tek kübit: H sonrası %50-50
    python3 -m quantro bell       # Bell durumu: |00> + |11>
    python3 -m quantro ghz 7      # 7 kübit GHZ durumu
"""

from __future__ import annotations

import sys

from .core import QuantumCircuit, bell_state, ghz_state, sample_distribution


def _fmt(counts: dict[int, int], n: int, shots: int) -> str:
    width = max(len(f"{s:0{n}b}") for s in counts) or 1
    out = []
    for key in sorted(counts):
        bits = f"{key:0{n}b}"
        out.append(f"  |{bits}> : %5.1f%%  ({counts[key]}/{shots})" % (100 * counts[key] / shots))
    return "\n".join(out)


def demo_single(shots: int = 1024) -> None:
    qc = QuantumCircuit(1)
    qc.h(0)
    counts = sample_distribution(qc, shots=shots, seed=42)
    print("Tek kübit: H |0> -> ölçüm dağılımı")
    print(_fmt(counts, 1, shots))


def demo_bell(shots: int = 1024) -> None:
    qc = QuantumCircuit(2)
    bell_state(qc)
    counts = sample_distribution(qc, shots=shots, seed=42)
    print("Bell durumu: |00> + |11> -> ölçüm dağılımı (dolanıklık!)")
    print(_fmt(counts, 2, shots))


def demo_ghz(n: int = 3, shots: int = 1024) -> None:
    qc = QuantumCircuit(n)
    ghz_state(qc, list(range(n)))
    counts = sample_distribution(qc, shots=shots, seed=42)
    print(f"{n} kübit GHZ durumu: |0...0> + |1...1>")
    print(_fmt(counts, n, shots))


def main() -> None:
    args = sys.argv[1:]
    demo = args[0] if args else "single"
    if demo == "single":
        demo_single()
    elif demo == "bell":
        demo_bell()
    elif demo == "ghz":
        n = int(args[1]) if len(args) > 1 else 3
        demo_ghz(n)
    else:
        print(f"Bilinmeyen demo: {demo}")
        sys.exit(1)


if __name__ == "__main__":
    main()
