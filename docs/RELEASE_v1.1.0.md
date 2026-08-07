# Quantro v1.1.0

Kuantum araç seti genişletme sürümü — 8. araç eklendi, gerçek rastgelelik güçlendirildi.

## Bu sürümde neler var

- **8. Araç — Kuantum Işınlanma**: qubit 0'ın durumu (ψ) Bell çifti üzerinden qubit 2'ye ışınlanır; koşullu düzeltmelerle marjinal olasılık korunur (P(|1⟩)=0.30, 20.000 atışta doğrulandı)
- **ANU proxy (`/api/anu`)**: Vercel serverless önbellek katmanı — ANU'nun 1 istek/dakika sınırını 45 sn'lik dönen blokla çözer; CORS `*`, gerekli uzunlukta gerçek kuantum baytı döner
- **Ki-kare rastgelelik testi (T1)**: canlı ANU verisi üzerinde χ² (16 kova, 1024 bayt) — test sırasında gerçek veri geçerli: χ²=21.44 < 24.996 ✓
- **TR/EN dil desteği**: sayfanın tamamı tek tıkla Türkçe/İngilizce arasında geçiş yapar (34 çevrilebilir öğe)
- **PWA**: manifest + service worker — site kurulabilir ve çevrimdışı çalışır (API uçları çevrimdışında atlanır)
- **Motor: RY + CZ kapıları**: hem Python (`quantro/core.py`) hem JS (`quantro.js`) — döndürme ve kontrollü-Z kapıları, ışınlanmanın temeli
- **Testler**: JS motoru 17 → 20 teste yükseltildi (RY, CZ, ışınlanma); Python tarafına eşdeğer 3 test eklendi

## Doğrulama

- `tests/test_web.js`: **20 pass, 0 fail**
- Canlı deploy: https://quantro-1.vercel.app — proxy, ki-kare, ışınlanma, i18n, PWA doğrulandı
- `quantro.js` MD5 birebir (kaynak = canlı)

## Lisans

Apache License 2.0
