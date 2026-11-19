# 07 Bağlam ve konum

[Prompt, bağlam ve dikkat eksikliği](https://mfurkan.dev/yazilar/prompt-baglam-dikkat/) yazısının verisi.

Uzun bir belgeye eklenen cümlelerin yeri, belgenin uzunluğu ve sorunun yeri ile dili değiştirildiğinde
modellerin aranan bilgiyi ne kadar bulduğu ölçüldü. İki ölçüm var.

| Klasör | Ölçüm |
| --- | --- |
| `kolay` | Aranan cümle sorunun kelimelerini ve şirket adını taşır. Beş model. |
| `zor` | Aranan cümle sorunun kelimelerini taşımaz, şirket yalnız rolüyle anılır, 25 yanıltıcı kayıt vardır. |

Her klasörde aynı dosyalar bulunur.

| Dosya | İçerik |
| --- | --- |
| `nasil-olculdu.md` | Yöntem |
| `ozet.json` | Bütün tablolar ve belirsizlik aralıkları |
| `sonuclar.jsonl` | Her soru için bir satır. Metin ve model cevabı yoktur. |
| `sablonlar.json` | Eklenen cümlelerin ve soruların kalıpları |
| `kos.py` | Belgeyi kuran, soruyu soran ve puanlayan betik |

## Puanlama farkı

Bu klasördeki dosyalar ilk puanlama kuralıyla üretildi. O kuralda doğru değerin yanına ikinci bir değer
yazan cevap yanlış sayılıyordu. Yazıdaki ana doğruluk tablosunda bu cevaplar doğru sayıldı. Fark en çok
GLM-5.3 Flash satırında görülür (3 ile 5 puan). Yazıdaki konum grafiği ve sorunun yeri tablosu ilk
kuralla verilmiştir.

Karar metinleri paylaşılmıyor. Şirket adları uydurmadır.
