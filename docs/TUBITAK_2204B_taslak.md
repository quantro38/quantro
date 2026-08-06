# TÜBİTAK 2204-B — Başvuru Taslağı

> **Not:** Bu dosya bir **başlangıç iskeletidir**. Resmî başvuru, TÜBİTAK 2204-B yarışması portalındaki güncel forma göre doldurulmalıdır (her yıl form şablonu değişebilir). Başvuru dönemini ve alan kodlarını kontrol et.

## Proje Künyesi

- **Proje adı:** Quantro — Kuantum Fiziği ve Astrofiziği İnteraktif Araçlarla Öğrenme (Lab Seti)
- **Proje alanı:** Fizik (uygun alan kodu kontrol edilecek)
- **Hazırlayan:** [Ad Soyad] — 9. sınıf öğrencisi
- **Danışman öğretmen:** [Ad Soyad, okul]

## Özet

Kuantum fiziği ve astrofizik, soyut kavramlar içerdiği için öğrencilerde sezgisel anlama zordur. Quantro; tarayıcıdan ücretsiz çalışan, 7 interaktif araçtan oluşan bir lab setidir. Süperpozisyon, Bell/GHZ dolaşıklığı, BB84 şifreleme, kara delik fiziği ve evren yaşı gibi konuları deneyerek öğretmeyi amaçlar. Rastgelelik motoru, gerçek kuantum kaynağına (ANU vakum dalgalanması) bağlanabilmektedir.

## Amaç / Araştırma Sorusu

- Kuantum fiziği ve astrofizik kavramlarını interaktif araçlarla öğretmek, soyut konulara karşı ilgiyi artırmak mümkün müdür?
- Hedef: Ortaokul/lise öğrencilerinin kendi başına deneyebileceği ücretsiz bir lab seti geliştirmek ve etkililiğini ölçmek.

## Yöntem

- **Araçlar:** Python + JavaScript ile geliştirilen matematiksel motor (Qubit, H/X/Y/Z/CNOT, tensör ürünü, ölçüm, örnekleme)
- **Doğrulama:** 40'a yakın otomatik test; Qiskit-Statevector karşılaştırması
- **Veri:** Gerçek kuantum rastgelelik (ANU QRNG) ile üretilen sayıların istatistiksel testi (ör. tekrarlama, aralık dağılımı)
- **Etki ölçümü:** Sınıf arkadaşlarına ön test/son test uygulanması

## Bulgular

- [Test sonuçları, rastgelelik analizi, kullanıcı deneyimi geri bildirimleri buraya]

## Sonuç ve Tartışma

- [Neler başarıldı, sınırlar, gelecek çalışma]

## Özgünlük

- Kuantum fiziği ve astrofiziği **tek çatıda** toplayan 7 araçlı ilk Türkçe interaktif lab seti olması; gerçek kuantum verisi kullanabilmesi.

## Yaygın Etki

- Ücretsiz ve tarayıcıdan çalıştığı için her okuldan erişilebilir
- Türkçe içerik eksikliğini gidermeye katkı
- Açık kaynak (Apache 2.0) — başka öğretmenler de kullanabilir

## Kaynakça

- ANU Quantum Random Numbers (vakum dalgalanması)
- Nielsen & Chuang, Quantum Computation and Quantum Information
- Qiskit dokümantasyonu
