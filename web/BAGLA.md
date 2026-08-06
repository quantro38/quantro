# quantro.js — SITEYE BAĞLAMA KILAVUZU

Bu dosya, `quantro-1.vercel.app`'deki **Kuantum Devre Simülatörü** modülünün
şu anki sahte 2 kübitlik hesabının yerine geçen, doğrulanmış durum vektörü
motorudur (`quantro/core.py`'nin JavaScript çevirisi). Tarayıcıda, sunucusuz
çalışır.

## Ne işe yarar

| Şu anki site | quantro.js |
|---|---|
| 2 kübit, kodlanmış H/X/Z | 1-12 kübit, gerçek matematik |
| CNOT sahte (`[.5,0,0,.5]`) | Gerçek CNOT (dolanıklık doğru) |
| Sadece elle `|00>`..`|11>` | Her boyutta histogram |
| — | Bell ve GHZ hazır fonksiyonlar |

## Bağlama (2 adım)

Bilgisayarında site kaynağının olduğu klasörde `quantro-lab.html` dosyasını aç:

**1. Adım — motoru ekle.** Dosyanın en altındaki `</body>` etiketinden hemen
önce (mevcut `<script>` etiketlerinin yanına) şunu ekle:

```html
<script src="quantro.js"></script>
```

ve `quantro.js` dosyasını aynı klasöre kopyala.

**2. Adım — ölçüm fonksiyonunu değiştir.** Sitedeki `mc()` fonksiyonunun
gövdesini aşağıdakiyle değiştir (mevcut UI aynen kalır):

```js
function mc(){
  const qc = new Quantro.QuantumCircuit(2);
  for (const g of circ[0]) {
    if (g.g === 'H') qc.h(0);
    else if (g.g === 'X') qc.x(0);
    else if (g.g === 'Z') qc.z(0);
    else if (g.g === 'CNOT') qc.cx(0, 1);
  }
  for (const g of circ[1]) {
    if (g.g === 'H') qc.h(1);
    else if (g.g === 'X') qc.x(1);
    else if (g.g === 'Z') qc.z(1);
  }
  const counts = Quantro.sampleDistribution(qc, 1024, Date.now() >>> 0);
  const slots = [0, 0, 0, 0];
  for (const k in counts) slots[k] = counts[k];
  const mx = Math.max(...slots);
  document.getElementById('crb').innerHTML =
    ['|00⟩','|01⟩','|10⟩','|11⟩'].map((l, i) =>
      `<div class="crb-w"><div class="crb-val">${slots[i]}</div>` +
      `<div class="crb ${slots[i]===mx&&slots[i]>0?'active':''}" style="height:${mx>0?Math.round(slots[i]/mx*60):3}px"></div>` +
      `<div class="crb-lbl">${l}</div></div>`).join('');
  document.getElementById('cr').style.display = 'block';
}
```

> Not: Sitedeki `circ` yapısı düz string tutuyorsa (`['H','X',...]`) üstteki
> `g.g` yerine `g` kullan; `simulator-demo.html`'deki `applyCircuit()` örneğine bak.

## N kübite çıkarmak istersen

`simulator-demo.html` 1-7 kübiti destekler. Onu örnek al: her kübit için bir
satır (`clane`) ekle, `ag()` çağrılarına kübit numarasını geç, `mc()` içinde
`QuantumCircuit(n)` kur. Üstteki örnek 2 kübit için yazılmıştır.

## Doğrulama

- Motor: `node --test tests/test_web.js` → **17 test geçer** (durum vektörü,
  CNOT, Bell/GHZ, istatistik).
- Python ikizi: `python3 -m pytest tests/ -q` → **24 test geçer**.
- Qiskit ile (bilgisayarında): `pip install qiskit && python docs/qiskit_compare.py`.

## Hızlı test

`simulator-demo.html`'yi tarayıcıda aç (çift tık). "Bell |00>+|11>" ve "GHZ
(tümü)" butonları çalışmalı — yalnızca |00>/|11> ve |0..0>/|1..1> çıkmalı.
