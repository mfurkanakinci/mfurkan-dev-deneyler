# mfurkan.dev deneyleri

[mfurkan.dev](https://mfurkan.dev) yazılarındaki örneklerin ve ölçümlerin kodu.
Her klasör bir yazıya aittir. Yazıdaki her sayı, o klasördeki `cikti.json`
dosyasından okunabilir.

| Klasör | Yazı | Ne yapar |
| --- | --- | --- |
| `01-tokenizer` | [Model harf görmez, tokenizer'ın böldüğünü görür](https://mfurkan.dev/yazilar/tokenizer-nedir/) | Aynı metni altı tokenizer'a verir, parçaları ve sayılarını yazar |
| `02-vektor` | [Vektör nedir? Yakın olan aynı değildir](https://mfurkan.dev/yazilar/vektor-nedir/) | Cümle çiftlerinin BGE-M3 ile kosinüs benzerliğini hesaplar |

## Çalıştırma

Python 3.11 ya da üstü yeterli. GPU gerekmez.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python 01-tokenizer/ornekler.py
python 02-vektor/benzerlik.py
```

İlk betik yalnız küçük tokenizer dosyalarını indirir. İkincisi BGE-M3
ağırlıklarını indirir, yaklaşık 2,3 GB tutar.

## Bunlar örnek, ölçüm değil

Buradaki metinler elle yazılmış birkaç kısa cümledir. Bir tokenizer'ın ya da
modelin genel başarısı hakkında hüküm kurmaya yetmez. Amaç, yazıda anlatılan
davranışı herkesin kendi bilgisayarında görebilmesi.

Model ve kütüphane sürümleri sabittir. Sürüm değişirse sayılar da değişebilir.

## Veri

Bütün örnek cümleler bu depo için yazıldı. Gerçek karar metni ya da kişisel
veri içermez.

## Lisans

[Apache License 2.0](LICENSE). Atıf bilgisi [NOTICE](NOTICE) dosyasındadır.
