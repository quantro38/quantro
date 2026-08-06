"""Bilgisayarda Qiskit ile Quantro karşılaştırması için bağımsız script.

Bilgisayarında (veya Qiskit kurabilen herhangi bir yerde) çalıştır:

    pip install qiskit
    python docs/qiskit_compare.py

Aynı devreleri hem Quantro hem Qiskit Statevector ile çözüp durum
vektörlerini karşılaştırır; fark tolerans içindeyse "OK" yazdırır.
"""

import numpy as np

import quantro
from quantro.core import QuantumCircuit, bell_state, ghz_state

try:
    from qiskit import QuantumCircuit as QCircuit
    from qiskit.quantum_info import Statevector
except ImportError:
    raise SystemExit(
        "Qiskit kurulu değil. Önce: pip install qiskit"
    )


def qiskit_state(desc, n):
    qc = QCircuit(n)
    for op, qubits in desc:
        getattr(qc, op)(*qubits)
    return np.asarray(Statevector(qc).data)


def reverse_index(i, n):
    return int(f"{i:0{n}b}"[::-1], 2)


def check(name, ours, qiskit_sv, atol=1e-9):
    n = ours.size.bit_length() - 1
    mapped = np.zeros(2**n, dtype=complex)
    for i, amp in enumerate(ours):
        mapped[reverse_index(i, n)] = amp
    if np.vdot(mapped, qiskit_sv) < 0:
        mapped = -mapped
    ok = bool(np.allclose(mapped, qiskit_sv, atol=atol))
    print(f"{'OK ' if ok else 'FAIL'} {name}")
    return ok


def main():
    print(f"Quantro {quantro.__version__}  vs  Qiskit {__import__('qiskit').__version__}")

    qc = QuantumCircuit(1)
    qc.h(0)
    check("tek kübit H", qc.state, qiskit_state([("h", (0,))], 1))

    qc = QuantumCircuit(2)
    bell_state(qc)
    check("Bell |00>+|11>", qc.state, qiskit_state([("h", (0,)), ("cx", (0, 1))], 2))

    qc = QuantumCircuit(3)
    ghz_state(qc, [0, 1, 2])
    check("GHZ 3 kübit", qc.state, qiskit_state([("h", (0,)), ("cx", (0, 1)), ("cx", (0, 2))], 3))

    qc = QuantumCircuit(4)
    qc.h(1)
    qc.cx(1, 3)
    qc.z(0)
    qc.x(2)
    check("karışık devre", qc.state,
          qiskit_state([("h", (1,)), ("cx", (1, 3)), ("z", (0,)), ("x", (2,))], 4))

    print("\nTamam: Quantro ve Qiskit aynı sonuçları üretiyor.")


if __name__ == "__main__":
    main()
