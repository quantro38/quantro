# Quantro

Türkiye'nin ilk **7 araçlık kuantum + astrofizik interaktif lab seti** projesinin
açık kaynak çekirdeği. Bu depo, [quantro-1.vercel.app](https://quantro-1.vercel.app)
adresindeki Lab'ın kuantum devre simülatörü kodunu barındırır.

> Konumlandırma notu: Tek tek araçların (devre simülatörü, BB84, kozmolojik
> hesaplayıcılar vb.) çok sayıda muadili vardır. Quantro'yu özgün yapan,
> bu 7 aracı **tek pakette, Türkçe ve interaktif** sunmasıdır. "İlk" iddiası
> yalnızca bu kombinasyon için geçerlidir.

## Özellikler (bu sürümde)

- `Qubit` sınıfı: `a|0> + b|1>` durum vektörü, kapı uygulama, olasılık, ölçüm
- Kapılar: H (Hadamard), X, Y, Z, CNOT
- `QuantumCircuit`: n kübitlik devre, tensör çarpımı ile tam uzayda işlem
- Bell (`|00> + |11>`) ve GHZ (`|0...0> + |1...1>`) dolanıklık durumları
- `sample_distribution`: topluluk ölçümü (shots) ile olasılık dağılımı

## Kurulum

```bash
python3 -m pip install numpy pytest
git clone https://github.com/quantro38/quantro.git
cd quantro
```

## Kullanım

```bash
python3 -m quantro single   # H |0> -> %50-50
python3 -m quantro bell     # dolanıklık: yalnızca |00> veya |11>
python3 -m quantro ghz 7    # 7 kübit GHZ
```

## Test

```bash
python3 -m pytest tests/ -q
```

## Basit örnek

```python
from quantro import QuantumCircuit, bell_state, sample_distribution

qc = QuantumCircuit(2)
bell_state(qc)
print(sample_distribution(qc, shots=4096, seed=42))
# {0: ~2048, 3: ~2048} -> sadece |00> ve |11>!
```

## Yol haritası

| Kilometre taşı | Durum | İçerik |
|---|---|---|
| M0 - Kurulum | tamam | Repo, Apache 2.0 lisans, README |
| M1 - Çekirdek | tamam | Qubit, H/X/Z, CNOT, ölçüm, Bell/GHZ |
| M2 - 7 Kübit | tamam | n kübit destekli devre + dağılım örnekleme |
| M3 - Doğrulama | sıradaki | Qiskit-Aer ile karşılaştırma testleri, Bloch küresi |
| M3b - Gerçek Rastgelelik | - | ANU QRNG entegrasyonu (Lab rastgelelik motoru) |
| M4 - Lansman | - | v1.0, dokümantasyon, duyuru |
| M5 - Topluluk | - | Katkı rehberi, geri bildirim, TÜBİTAK 2204 |

## Lisans

Apache License 2.0 (bkz. `LICENSE`).
