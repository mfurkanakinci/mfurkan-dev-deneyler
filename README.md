# mfurkan.dev deneyleri

[mfurkan.dev](https://mfurkan.dev) yazılarındaki örneklerin ve ölçümlerin kodu.
Her klasör bir yazıya aittir. Yazıdaki her sayı, o klasördeki `cikti.json`
dosyasından okunabilir.

| Klasör | Yazı | Ne yapar |
| --- | --- | --- |
| `01-tokenizer` | [Model harf görmez, tokenizer'ın böldüğünü görür](https://mfurkan.dev/yazilar/tokenizer-nedir/) | Aynı metni altı tokenizer'a verir, parçaları ve sayılarını yazar |
| `02-vektor` | [Vektör nedir? Yakın olan aynı değildir](https://mfurkan.dev/yazilar/vektor-nedir/) | Cümle çiftlerinin BGE-M3 ile kosinüs benzerliğini hesaplar |
| `03-tokenizer-karsilastirma` | [Tokenizer'ları nasıl karşılaştırdım?](https://mfurkan.dev/yazilar/tokenizer-karsilastirma/) | Altı tokenizer'ı 300 belgede uzunluk, sadakat ve sığma bakımından ölçer |
| `04-ner` | [NER'den BERT'e](https://mfurkan.dev/yazilar/ner-bert/) | Aynı yazılışa sahip adların cümleye göre nasıl etiketlendiğini gösterir |

## Çalıştırma

Python 3.11 ya da üstü yeterli. GPU gerekmez.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python 01-tokenizer/ornekler.py
python 02-vektor/benzerlik.py
python 04-ner/of.py
```

İlk betik yalnız küçük tokenizer dosyalarını indirir. İkincisi BGE-M3
ağırlıklarını indirir, yaklaşık 2,3 GB tutar.

## Örnek ile ölçümü ayırın

`01`, `02` ve `04` klasörlerindeki metinler elle yazılmış birkaç kısa cümledir. Bir tokenizer'ın ya da modelin
genel başarısı hakkında hüküm kurmaya yetmez. Amaç, yazıda anlatılan davranışı kendi bilgisayarınızda görebilmeniz.

`03` klasörü bir ölçümdür. Plan sonuçlardan önce yazıldı, 300 belge önceden belirlenmiş bir kuralla seçildi ve
farklar belirsizlik aralıklarıyla birlikte verildi.

Model ve kütüphane sürümleri sabittir. Sürüm değişirse sayılar da değişebilir.

## Veri

İlk iki klasör ile dördüncü klasördeki örnek cümleler bu depo için yazıldı. Gerçek karar metni ya da kişisel
veri içermez.

`03-tokenizer-karsilastirma` gerçek belgelerle ölçüldü. Vikipedi sayfaları ve kanun maddeleri `belge_listesi.csv`
dosyasında kimlikleriyle duruyor, isteyen aynı metinleri bulup ölçümü tekrarlayabilir. Mahkeme kararlarının metni
ve numarası paylaşılmıyor. Listede yalnız mahkeme türü ve karakter sayısı var, o kısım için yalnız toplu sonuç
veriliyor.

## Lisans

[Apache License 2.0](LICENSE). Atıf bilgisi [NOTICE](NOTICE) dosyasındadır.
