"""Quantro çekirdeği: saf Python + numpy ile kuantum devre simülatörü.

Küçük ve okunaklı olması, eğitim amaçlı kullanılması hedeflenmiştir.
Kübit durumları karmaşık vektörler, kapılar ise matrislerdir.
Uygulamak = matris çarpımı. Ölçüm = olasılığa göre 0/1 örnekleme.

Kübit sıralaması: |q0 q1 ... q_{n-1}>, en soldaki kübit en anlamlı bittir.
"""

from __future__ import annotations

import random
from typing import Sequence

import numpy as np


class Qubit:
    """Tek kübit: |psi> = a|0> + b|1> (normalleştirilmiş)."""

    def __init__(self, a: float | complex = 1.0, b: float | complex = 0.0):
        norm = np.sqrt(abs(a) ** 2 + abs(b) ** 2)
        if norm == 0:
            raise ValueError("Sıfır durumu geçerli bir kübit değildir")
        self.state = np.array([a, b], dtype=complex) / norm

    def apply(self, matrix: np.ndarray) -> "Qubit":
        self.state = matrix @ self.state
        return self

    def prob(self, bit: int) -> float:
        return abs(self.state[bit]) ** 2

    def measure(self, rng: random.Random | None = None) -> int:
        rng = rng or random
        return 0 if rng.random() < self.prob(0) else 1

    def __repr__(self) -> str:
        return f"Qubit(a={self.state[0]:.4f}, b={self.state[1]:.4f})"


H = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2)  # Hadamard
X = np.array([[0.0, 1.0], [1.0, 0.0]])               # Pauli-X (NOT)
Y = np.array([[0.0, -1j], [1j, 0.0]])                # Pauli-Y
Z = np.array([[1.0, 0.0], [0.0, -1.0]])              # Pauli-Z
I2 = np.eye(2, dtype=complex)                        # Birim (boş)

GATES = {"h": H, "x": X, "y": Y, "z": Z, "i": I2}


class QuantumCircuit:
    """n kübitlik devre. Tüm kapılar tam durum vektörü üzerinde uygulanır."""

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("En az 1 kübit gerekli")
        if n > 15:
            raise ValueError("15 kübitten büyük devreler hafıza için fazla büyük")
        self.n = n
        self._size = 2 ** n
        self.state = np.zeros(self._size, dtype=complex)
        self.state[0] = 1.0
        self.operations: list[str] = []

    def apply(self, matrix: np.ndarray, targets: Sequence[int]) -> "QuantumCircuit":
        """targets 1 elemanlıysa tek kübitlik kapı, 2 elemanlıysa iki kübitlik kapı."""
        if len(targets) == 1:
            self._apply_single(matrix, targets[0])
        elif len(targets) == 2:
            self._apply_two(matrix, targets[0], targets[1])
        else:
            raise ValueError("Bu sürüm en fazla 2 kübitlik kapıları destekler")
        return self

    def _apply_single(self, matrix: np.ndarray, q: int) -> None:
        op = np.eye(1, dtype=complex)
        for p in range(self.n):
            op = np.kron(op, matrix if p == q else I2)
        self.state = op @ self.state

    def _apply_two(self, matrix: np.ndarray, c: int, t: int) -> None:
        perm = np.zeros((self._size, self._size), dtype=complex)
        for i in range(self._size):
            bits = list(self._to_bits(i))
            cb, tb = bits[c], bits[t]
            j = self._from_bits(bits if cb == 0 else self._flip(bits, t))
            col = cb * 2 + tb
            row = cb * 2 + (tb ^ cb)
            perm[i, j] = matrix[row, col]
        self.state = perm @ self.state

    def h(self, q: int) -> "QuantumCircuit":
        return self.apply(H, [q])

    def x(self, q: int) -> "QuantumCircuit":
        return self.apply(X, [q])

    def y(self, q: int) -> "QuantumCircuit":
        return self.apply(Y, [q])

    def z(self, q: int) -> "QuantumCircuit":
        return self.apply(Z, [q])

    def cx(self, control: int, target: int) -> "QuantumCircuit":
        """CNOT: kontrol 1 ise hedef kübiti çevir."""
        if control == target:
            raise ValueError("Kontrol ve hedef aynı olamaz")
        gate = np.zeros((4, 4), dtype=complex)
        gate[0, 0] = 1
        gate[1, 1] = 1
        gate[2, 3] = 1
        gate[3, 2] = 1
        return self.apply(gate, [control, target])

    def probabilities(self) -> np.ndarray:
        return abs(self.state) ** 2

    def measure_all(self, rng: random.Random | None = None) -> int:
        """Tüm kübitleri ölç; 0..2^n-1 arası bir bit deseni döndür."""
        rng = rng or random
        probs = self.probabilities()
        r = rng.random()
        acc = 0.0
        for i, p in enumerate(probs):
            acc += p
            if r < acc:
                return i
        return self._size - 1

    def draw(self) -> str:
        lines = []
        for q in range(self.n):
            parts = [f"q{q}: "]
            for op in self.operations:
                if "q0" in op and "q1" not in op:
                    parts.append(f"--{op[0]}--")
                else:
                    parts.append("-----")
            lines.append("".join(parts))
        return "\n".join(lines)

    def _to_bits(self, i: int) -> tuple[int, ...]:
        return tuple((i >> shift) & 1 for shift in range(self.n - 1, -1, -1))

    def _from_bits(self, bits: Sequence[int]) -> int:
        return int("".join(str(b) for b in bits), 2)

    def _flip(self, bits: list[int], q: int) -> list[int]:
        bits[q] = 1 - bits[q]
        return bits


def bell_state(circuit: QuantumCircuit, a: int = 0, b: int = 1) -> QuantumCircuit:
    """|00> + |11> Bell durumu: H(a) ardından CNOT(a, b)."""
    circuit.h(a)
    circuit.cx(a, b)
    return circuit


def ghz_state(circuit: QuantumCircuit, qubits: Sequence[int]) -> QuantumCircuit:
    """GHZ durumu: |00...0> + |11...1> (n kübit dolanıklık)."""
    qs = list(qubits)
    circuit.h(qs[0])
    for q in qs[1:]:
        circuit.cx(qs[0], q)
    return circuit


def sample_distribution(circuit: QuantumCircuit, shots: int = 1024, seed: int | None = None) -> dict[int, int]:
    rng = random.Random(seed)
    counts: dict[int, int] = {}
    for _ in range(shots):
        key = circuit.measure_all(rng)
        counts[key] = counts.get(key, 0) + 1
    return counts
