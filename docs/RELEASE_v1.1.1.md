# Quantro v1.1.1

Bloch Küresi — 9. araç eklendi.

## Bu sürümde neler var

- **9. Araç — Bloch Küresi**: bir kübitin durumu birim küre üzerinde canlandırılır; θ/φ kaydırıcıları ve |0⟩, |1⟩, |+⟩, |−⟩, |+i⟩, |−i⟩ ön ayar butonlarıyla durum değiştirilebilir
- Küre sürüklenerek görünüm döndürülebilir; amplitüd (|α|², |β|²) ve Bloch vektörü (x, y, z) anlık okunur
- **Bağımsız Canvas 2D** ile çizildi (harici CDN bağımlılığı yok) — service worker önbelleğinde çevrimdışı da çalışır
- İki dilli (TR/EN); araç sayısı metinleri 9'a güncellendi
- Service worker önbelleği `v1.1.1`'e taşındı (yeni içerik otomatik yüklenir)

## Doğrulama

- Canlı: https://quantro-1.vercel.app — sayfa MD5 birebir, T9 modülü canlıda doğrulandı
- Projeksiyon matematiği birim vektör uzunluğu ve durum ayrımıyla test edildi
- `tests/test_web.js`: 20 pass, 0 fail (değişmedi)

## Lisans

Apache License 2.0
