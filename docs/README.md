# Quantro Dokümantasyonu

## Kübitler nasıl çalışır?

Bir kübit bir vektördür: `|0> = [1, 0]`, `|1> = [0, 1]`.
Süperpozisyon `a|0> + b|1>` iki vektörün karışımıdır.
Kapılar 2x2 matristir; bir kapıyı uygulamak = matrisi vektörle çarpmak.
Ölçüm, `|a|^2` olasılığıyla 0 veya 1 verir.

7 kübit = 2^7 = 128 boyutlu vektör (tensör çarpımı ile).

## Kapılar

| Kapı | Matris | Ne yapar? |
|---|---|---|
| X | [[0,1],[1,0]] | 0<->1 (klasik NOT) |
| H | (1/√2)[[1,1],[1,-1]] | |0> -> süperpozisyon |
| Z | [[1,0],[0,-1]] | |1>'nin işaretini çevirir |
| CNOT | 4x4 | Kontrol 1 ise hedefi çevirir (dolanıklık kurar) |

## Sonraki adımlar

- Qiskit-Aer ile karşılaştırma testleri (M3)
- Bloch küresi görselleştirme
- ANU QRNG ile gerçek kuantum rastgelelik (M3b)
