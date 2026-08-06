"""Qiskit ile karşılaştırma testleri (M3).

Qiskit kurulu olmayan ortamlarda otomatik atlanır (pytest.importorskip).
Bilgisayarda `pip install qiskit` sonrası bu testler gerçek dış referans
doğrulaması yapar: aynı devrelerin durum vektörlerini Qiskit'in Statevector
simülasyonuyla karşılaştırırız.

Kübit sıralaması farkı: Quantro'da kübit 0 en anlamlı bit (solda), Qiskit'te
ise kübit 0 en az anlamlı bittir. Bu yüzden indeksleri bit düzeyinde çeviririz.
"""

import numpy as np
import pytest

qiskit = pytest.importorskip("qiskit")

from qiskit import QuantumCircuit as QCircuit
from qiskit.quantum_info import Statevector

from quantro.core import QuantumCircuit, bell_state, ghz_state


def _qiskit_state(circuits_desc, n):
    qc = QCircuit(n)
    for op, qubits in circuits_desc:
        if op == "h":
            qc.h(*qubits)
        elif op == "x":
            qc.x(*qubits)
        elif op == "z":
            qc.z(*qubits)
        elif op == "cx":
            qc.cx(*qubits)
        else:
            raise ValueError(op)
    return np.asarray(Statevector(qc).data)


def _reverse_index(i, n):
    return int(f"{i:0{n}b}"[::-1], 2)


def _assert_matches(ours, qiskit_sv, atol=1e-9):
    n = ours.size.bit_length() - 1
    mapped = np.zeros(2**n, dtype=complex)
    for i, amp in enumerate(ours):
        mapped[_reverse_index(i, n)] = amp
    if np.vdot(mapped, qiskit_sv) < 0:
        mapped = -mapped
    assert np.allclose(mapped, qiskit_sv, atol=atol)


def test_single_h_matches_qiskit():
    qc = QuantumCircuit(1)
    qc.h(0)
    _assert_matches(qc.state, _qiskit_state([("h", (0,))], 1))


def test_bell_matches_qiskit():
    qc = QuantumCircuit(2)
    bell_state(qc)
    desc = [("h", (0,)), ("cx", (0, 1))]
    _assert_matches(qc.state, _qiskit_state(desc, 2))


def test_ghz_7_matches_qiskit():
    n = 7
    qc = QuantumCircuit(n)
    ghz_state(qc, list(range(n)))
    desc = [("h", (0,))] + [("cx", (0, q)) for q in range(1, n)]
    _assert_matches(qc.state, _qiskit_state(desc, n))


def test_cnot_then_h_matches_qiskit():
    qc = QuantumCircuit(3)
    qc.h(2)
    qc.cx(2, 1)
    qc.z(0)
    desc = [("h", (2,)), ("cx", (2, 1)), ("z", (0,))]
    _assert_matches(qc.state, _qiskit_state(desc, 3))
