"""Qiskit gerektirmeyen bağımsız doğrulama testleri.

Bunlar simülatörün matematiğini dış bir referansa ihtiyaç duymadan doğrular:
üniterlik, kapı özdeşlikleri, normalize korunumu ve sabit tohumlu istatistikler.
"""

import random

import numpy as np

from quantro.core import QuantumCircuit, Qubit, H, X, bell_state, ghz_state


def test_gates_are_unitary():
    from quantro.core import I2, Y, Z

    for gate in (H, X, Y, Z, I2):
        prod = gate.conj().T @ gate
        assert np.allclose(prod, np.eye(2), atol=1e-12)


def test_cnot_operator_is_unitary():
    qc = QuantumCircuit(2)
    perm = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        bits = list(qc._to_bits(i))
        cb, tb = bits[0], bits[1]
        j = qc._from_bits(bits if cb == 0 else qc._flip(bits, 1))
        col = cb * 2 + tb
        row = cb * 2 + (tb ^ cb)
        perm[i, j] = 1.0
    assert np.allclose(perm.conj().T @ perm, np.eye(4), atol=1e-12)


def test_measurement_preserves_norm():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    assert abs(np.sum(qc.probabilities()) - 1.0) < 1e-12


def test_identity_hx_equals_zh():
    # X H = H Z (Pauli özdeşliği): aynı son duruma götürür
    a = QuantumCircuit(2)
    a.h(0)
    a.x(0)
    b = QuantumCircuit(2)
    b.z(0)
    b.h(0)
    assert np.allclose(a.state, b.state, atol=1e-12)


def test_cnot_twice_is_identity():
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.cx(0, 1)
    qc.cx(0, 1)
    assert qc.probabilities()[2] == 1.0


def test_x_on_all_qubits_measures_all_ones():
    qc = QuantumCircuit(4)
    for q in range(4):
        qc.x(q)
    assert qc.probabilities()[15] == 1.0


def test_superposition_statistics_fixed_seed():
    qc = QuantumCircuit(1)
    qc.h(0)
    counts = {0: 0, 1: 0}
    rng = random.Random(7)
    for _ in range(20000):
        counts[qc.measure_all(rng)] += 1
    p1 = counts[1] / 20000
    assert abs(p1 - 0.5) < 0.02


def test_bell_statistics_no_01_or_10():
    qc = QuantumCircuit(2)
    bell_state(qc)
    rng = random.Random(3)
    seen = set()
    for _ in range(5000):
        seen.add(qc.measure_all(rng))
    assert seen == {0, 3}


def test_qubit_apply_reproducible():
    q = Qubit()
    q.apply(H)
    q.apply(X)
    expected = np.array([1.0, 1.0]) / np.sqrt(2)
    assert np.allclose(q.state, expected, atol=1e-12)


def test_ghz_state_norm_and_support():
    qc = QuantumCircuit(5)
    ghz_state(qc, list(range(5)))
    probs = qc.probabilities()
    assert abs(np.sum(probs) - 1.0) < 1e-12
    assert abs(probs[0] - 0.5) < 1e-9
    assert abs(probs[31] - 0.5) < 1e-9
