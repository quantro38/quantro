# Quantro v1.0.0

İlk kararlı sürüm — Türkiye'nin ilk 7 araçlık kuantum + astrofizik interaktif lab seti.

## Bu sürümde neler var

- **Motor (Python)**: Qubit, QuantumCircuit, H/X/Y/Z/CNOT, Bell/GHZ, ölçüm ve dağılım örnekleme — 23 test geçiyor
- **Motor (JavaScript)**: birebir port, 1–12 kübit, canlı sitede çalışıyor — 17 test geçiyor
- **Web sitesi**: 7 modüllü interaktif lab (https://quantro-1.vercel.app)
- **Gerçek kuantum rastgelelik (M3b)**: ANU QRNG → NIST Beacon → Web Crypto kaynak zinciri, kaynak etiketi ekranda gösteriliyor
- **Doğrulama**: bağımsız testler + Qiskit karşılaştırma betiği (`docs/qiskit_compare.py`)

## Kilometre taşları

| Milestone | Durum |
|---|---|
| M0 Kurulum | tamam |
| M1 Çekirdek | tamam |
| M2 7 Kübit | tamam |
| M3 Doğrulama | kısmen (Qiskit karşılaştırması laptop'ta) |
| M3b Gerçek Rastgelelik | tamam |
| M4 Lansman | bu sürüm |
| M5 Topluluk | planlandı |

## Lisans

Apache License 2.0
