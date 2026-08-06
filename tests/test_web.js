/* Quantro JS motoru testleri — Python tarafındaki testlerin birebir karşılığı.
   Çalıştırma:  node --test web/   (kök dizinde)  veya  node tests/test_web.js */

const { test } = require("node:test");
const assert = require("node:assert");

const Quantro = require("../web/quantro.js");
const { QuantumCircuit, Qubit, H, X, Y, Z, I2, bellState, ghzState, sampleDistribution, mulberry32, c } = Quantro;

function allclose(a, b, tol) {
  tol = tol || 1e-9;
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) {
    const da = a[i].re - b[i].re;
    const db = a[i].im - b[i].im;
    if (Math.sqrt(da * da + db * db) > tol) return false;
  }
  return true;
}

function matMul(A, B) {
  const m = A.length, n = B[0].length, k = B.length;
  const R = Array.from({ length: m }, () => Array.from({ length: n }, () => c(0)));
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) {
      let acc = c(0);
      for (let l = 0; l < k; l++) {
        acc = Quantro.c(acc.re, acc.im);
        const mul = Quantro.c(A[i][l].re * B[l][j].re - A[i][l].im * B[l][j].im,
                             A[i][l].re * B[l][j].im + A[i][l].im * B[l][j].re);
        acc.re += mul.re; acc.im += mul.im;
      }
      R[i][j] = acc;
    }
  return R;
}

function conjTranspose(M) {
  return M[0].map((_, j) => M.map(row => c(row[j].re, -row[j].im)));
}

function isUnitary(M) {
  const id = matMul(M, conjTranspose(M));
  for (let i = 0; i < id.length; i++)
    for (let j = 0; j < id.length; j++) {
      const expect = i === j ? 1 : 0;
      if (Math.abs(id[i][j].re - expect) > 1e-9 || Math.abs(id[i][j].im) > 1e-9) return false;
    }
  return true;
}

test("qubit ilk durum |0>", () => {
  const q = new Qubit();
  assert.ok(Math.abs(q.prob(0) - 1) < 1e-9);
  assert.ok(q.prob(1) < 1e-9);
});

test("qubit normalleştirme", () => {
  const q = new Qubit(c(2), c(2));
  assert.ok(Math.abs(q.prob(0) - 0.5) < 1e-9);
  assert.ok(Math.abs(q.prob(1) - 0.5) < 1e-9);
});

test("X kapısı 0<->1 çevirir", () => {
  const q = new Qubit();
  q.apply(X);
  assert.ok(q.prob(0) < 1e-9);
  assert.ok(Math.abs(q.prob(1) - 1) < 1e-9);
});

test("H süperpozisyon %50-50", () => {
  const q = new Qubit();
  q.apply(H);
  assert.ok(Math.abs(q.prob(0) - 0.5) < 1e-9);
  assert.ok(Math.abs(q.prob(1) - 0.5) < 1e-9);
});

test("kapılar üniterdir", () => {
  for (const g of [H, X, Y, Z, I2]) assert.ok(isUnitary(g), "kapı üniter olmalı");
});

test("devre ilk durum", () => {
  const qc = new QuantumCircuit(2);
  assert.ok(Math.abs(qc.probabilities()[0] - 1) < 1e-9);
});

test("tek kübit H ilk sırada", () => {
  const qc = new QuantumCircuit(2);
  qc.h(0);
  const p = qc.probabilities();
  assert.ok(Math.abs(p[0] - 0.5) < 1e-9);
  assert.ok(Math.abs(p[2] - 0.5) < 1e-9);
  assert.ok(p[1] + p[3] < 1e-9);
});

test("CNOT kontrol=1 ise hedefi çevirir", () => {
  const qc = new QuantumCircuit(2);
  qc.x(0);
  qc.cx(0, 1);
  assert.ok(Math.abs(qc.probabilities()[3] - 1) < 1e-9);
});

test("CNOT kontrol=0 ise değişmez", () => {
  const qc = new QuantumCircuit(2);
  qc.cx(0, 1);
  assert.ok(Math.abs(qc.probabilities()[0] - 1) < 1e-9);
});

test("CNOT iki kez = kimlik", () => {
  const qc = new QuantumCircuit(2);
  qc.x(0);
  qc.cx(0, 1);
  qc.cx(0, 1);
  assert.ok(Math.abs(qc.probabilities()[2] - 1) < 1e-9);
});

test("XH = HZ özdeşliği", () => {
  const a = new QuantumCircuit(2); a.h(0); a.x(0);
  const b = new QuantumCircuit(2); b.z(0); b.h(0);
  assert.ok(allclose(a.state, b.state));
});

test("Bell: yalnızca |00> ve |11>", () => {
  const qc = new QuantumCircuit(2);
  bellState(qc);
  const counts = sampleDistribution(qc, 4096, 42);
  const keys = Object.keys(counts).map(Number);
  assert.deepStrictEqual(keys.sort(), [0, 3]);
});

test("GHZ 3 kübit: yalnızca |000> ve |111>", () => {
  const qc = new QuantumCircuit(3);
  ghzState(qc, [0, 1, 2]);
  const counts = sampleDistribution(qc, 4096, 42);
  assert.deepStrictEqual(Object.keys(counts).map(Number).sort(), [0, 7]);
});

test("GHZ 7 kübit: yalnızca |0...0> ve |1...1>", () => {
  const qc = new QuantumCircuit(7);
  ghzState(qc, [0, 1, 2, 3, 4, 5, 6]);
  const counts = sampleDistribution(qc, 4096, 42);
  assert.deepStrictEqual(Object.keys(counts).map(Number).sort(), [0, 127]);
});

test("tohumlanmış ölçüm tekrarlanabilir", () => {
  const qc = new QuantumCircuit(1);
  qc.h(0);
  const r1 = sampleDistribution(qc, 100, 7);
  const r2 = sampleDistribution(qc, 100, 7);
  assert.deepStrictEqual(r1, r2);
});

test("50/50 dağılım istatistiksel olarak doğru", () => {
  const qc = new QuantumCircuit(1);
  qc.h(0);
  const counts = sampleDistribution(qc, 20000, 42);
  const p1 = (counts[1] || 0) / 20000;
  assert.ok(Math.abs(p1 - 0.5) < 0.02);
});

test("mulberry32 deterministik", () => {
  const a = mulberry32(5);
  const b = mulberry32(5);
  for (let i = 0; i < 10; i++) assert.strictEqual(a(), b());
});
