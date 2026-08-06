# Katkı Rehberi (CONTRIBUTING)

Quantro'ya katkı yaptığın için teşekkürler! Bu rehber, herkesin (özellikle öğrencilerin) kolayca katkı verebilmesi için sade tutuldu.

## Kimlik

- **Dil:** Türkçe (kod, commit ve dokümantasyon)
- **Lisans:** Apache 2.0 — katkıların aynı lisans altında yayınlanır
- **Motor:** Python (`quantro/core.py`) ve JavaScript (`web/quantro.js`) — ikisi de aynı matematiği kullanır

## Hata Bildirme (Bug)

- [Yeni issue](https://github.com/quantro38/quantro/issues/new) aç.
- Şablonu doldur: ne yaptın, ne bekledin, ne gördün.
- Mümkünse tarayıcı adı/sürümünü ve hata mesajını ekle.

## Özellik Önerme

- [Yeni issue](https://github.com/quantro38/quantro/issues/new) aç.
- Ne istediğini, neden istediğini ve nasıl çalışacağını kısaca yaz.

## Kod Katkısı

1. Repo'yu fork et ve klonla.
2. Yeni bir dal aç: `git checkout -b ozellik-adi`
3. Değişikliği yap ve testleri çalıştır:
   - Python: `python -m pytest tests/`
   - JS: `node tests/test_web.js`
4. Değişikliğe yeni test ekle (yeni davranış için).
5. Commit et: `git commit -m "kisa ve aciklayici mesaj"`
6. Pull request aç ve değişikliği özetle.

## Kod Kuralları

- `quantro/core.py` ile `web/quantro.js` aynı sonucu üretmelidir (tutarlılık testi).
- 1–12 kübit arası tüm devreler çalışmalıdır.
- Kullanıcı arayüzü değişiklikleri canlı sitede (Vercel) test edilmelidir.
- Yorum satırı eklemekten kaçın; kod kendini açıklasın.

## İletişim

Soruların için GitHub Discussions veya issue'lardan yazabilirsin.
