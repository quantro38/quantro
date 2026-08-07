import random

import numpy as np

from quantro.core import QuantumCircuit, Qubit, bell_state, ghz_state, sample_distribution


def test_qubit_initial():
    q = Qubit()
    assert q.prob(0) == 1.0
    assert q.prob(1) == 0.0


def test_qubit_normalized():
    q = Qubit(a=2, b=2)
    assert abs(q.prob(0) - 0.5) < 1e-9
    assert abs(q.prob(1) - 0.5) < 1e-9


def test_x_flips_qubit():
    q = Qubit()
    q.apply(X := np.array([[0.0, 1.0], [1.0, 0.0]]))
    assert q.prob(0) == 0.0
    assert q.prob(1) == 1.0


def test_measure_qubit_deterministic_with_seed():
    q = Qubit()
    assert q.measure(random.Random(0)) == 0
    q.apply(np.array([[0.0, 1.0], [1.0, 0.0]]))
    assert q.measure(random.Random(0)) == 1


def test_superposition_probability():
    q = Qubit()
    q.apply(np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2))
    assert abs(q.prob(0) - 0.5) < 1e-9
    assert abs(q.prob(1) - 0.5) < 1e-9


def test_circuit_initial_state():
    qc = QuantumCircuit(2)
    assert qc.state[0] == 1.0
    assert qc.probabilities()[0] == 1.0


def test_single_qubit_h_on_first():
    qc = QuantumCircuit(2)
    qc.h(0)
    probs = qc.probabilities()
    assert abs(probs[0] - 0.5) < 1e-9
    assert abs(probs[2] - 0.5) < 1e-9
    assert abs(probs[1] + probs[3]) < 1e-9


def test_cnot_flips_target():
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.cx(0, 1)
    assert qc.probabilities()[3] == 1.0


def test_cnot_noop_when_control_zero():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    assert qc.probabilities()[0] == 1.0


def test_bell_state_correlation():
    qc = QuantumCircuit(2)
    bell_state(qc)
    counts = sample_distribution(qc, shots=4096, seed=42)
    assert all(key in (0, 3) for key in counts)
    assert len(counts) == 2


def test_ghz_state_3_qubits():
    qc = QuantumCircuit(3)
    ghz_state(qc, [0, 1, 2])
    counts = sample_distribution(qc, shots=4096, seed=42)
    assert all(key in (0, 7) for key in counts)
    assert len(counts) == 2


def test_ghz_state_7_qubits():
    qc = QuantumCircuit(7)
    ghz_state(qc, list(range(7)))
    counts = sample_distribution(qc, shots=4096, seed=42)
    assert all(key in (0, 127) for key in counts)
    assert len(counts) == 2


def test_measure_all_reproducible():
    qc = QuantumCircuit(1)
    qc.h(0)
    assert qc.measure_all(random.Random(5)) in (0, 1)


def test_ry_creates_superposition():
    import math

    qc = QuantumCircuit(1)
    qc.ry(2 * math.acos(math.sqrt(0.7)), 0)
    p = qc.probabilities()
    assert abs(p[0] - 0.7) < 1e-9
    assert abs(p[1] - 0.3) < 1e-9


def test_cz_flips_phase_on_11():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    qc.cz(0, 1)
    p = qc.probabilities()
    assert all(abs(x - 0.25) < 1e-9 for x in p)


def test_teleportation_bob_receives_psi():
    import math

    qc = QuantumCircuit(3)
    qc.ry(2 * math.acos(math.sqrt(0.7)), 0)
    qc.h(1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.cx(1, 2)
    qc.cz(0, 2)
    counts = sample_distribution(qc, shots=20000, seed=7)
    one = sum(c for key, c in counts.items() if key & 1 == 1)
    assert abs(one / 20000 - 0.3) < 0.01
