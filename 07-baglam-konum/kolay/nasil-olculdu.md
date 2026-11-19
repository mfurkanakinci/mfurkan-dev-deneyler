# Nasıl ölçüldü

**Soru.** Uzun bir karar metni ya da bir dosya dolusu karar büyük bir dil modeline verildiğinde model metnin her yerini aynı
başarıyla okuyor mu? Üç ayrı ölçüm yapıldı: aranan bilginin metindeki yeri (S1), metnin uzunluğu (S2), sorunun yeri ve dili (S3).

**Belgeler.** Yargıtay hukuk dairelerinin yayımlanmış kararlarından (kaynağında anonim; kalan "Ad Soyad" kalıpları ayrıca baş
harfe indirildi) sabit tohumla rastgele kararlar çekildi ve "KARAR 1", "KARAR 2" başlıklarıyla, bütün olarak art arda eklendi.
Yalnız son karar, hedef uzunluğa en yakın paragraf sınırında kesildi. Uzunluk bütün modeller için tek bir ölçüyle, OpenAI'nin
`o200k_base` parça listesiyle sayıldı. Üç hedef uzunluk:

| hedef | belge | ortalama karar | ortalama karakter | ortalama kelime | yaklaşık sayfa (3.000 karakter) |
|---|---:|---:|---:|---:|---:|
| 4.000 parça | 40 | 4 | 13.200 | 1.650 | 4–5 |
| 16.000 parça | 40 | 17 | 52.700 | 6.600 | 17–18 |
| 64.000 parça | 20 | 62 | 212.900 | 26.700 | 70 |

Türkçe hukuk metninde bir parça ortalama 3,3 karakter, 0,41 kelimedir.

**Eklenen cümleler.** Her belgeye aynı şablondan beş cümle eklendi (ör. "Borçlu Zernova Yapı A.Ş., 14.03.2019 tarihinde temerrüde
düşmüştür."). Beşi aynı kalıptadır, yalnız uydurma şirket adı ve değer farklıdır; böylece öbür dört cümle doğal çeldiricidir.
Cümleler belgenin %0, %25, %50, %75 ve %100 noktalarına en yakın paragraf sınırına, kendi paragrafı olarak kondu. 20 şablon,
30 uydurma ad kökü ve değer kuralları `sablonlar.json`'dadır. Ad köklerinin hiçbiri karar havuzunda geçmiyor; değerler o belgenin
başka bir yerinde aynen geçmeyecek biçimde çekildi.

**Sorular.** Her cümle iki biçimde soruldu: *düz* (cümledeki hukuk terimleriyle: "… hangi tarihte temerrüde düşmüştür?") ve
*sade* (gündelik dille: "… hangi günden itibaren borcunu geç ödemiş sayılmıştır?"). Belge değişmez; yalnız sorulan şirket değişir.
Talimat tektir: "Aşağıda mahkeme kararları var. Soruyu yalnız bu metne dayanarak cevapla. Cevap olarak yalnız istenen bilgiyi yaz
(tarih, tutar, sayı, dosya numarası ya da il). Bilgi metinde yoksa yalnız 'metinde yok' yaz." Her çağrı tek başınadır (geçmiş ve
araç yok). Ana düzende soru metnin sonundadır; bir kolda aynı soru metnin önüne kondu.

**Izgara (model başına 1.360 çağrı).** 4.000 parça: 40 belge × 5 yuva × 2 biçim; 16.000: 40 × 5 × 2; 64.000: 20 × 5 × 2;
soru başta: 16.000'lik 20 belgede 3 yuva (%0, %50, %100) × 2 biçim; metinde yok kontrolü: 16.000'lik 40 belgede eklenmemiş
altıncı bir şirket; kısa taban: karar metni olmadan yalnız beş cümle, her şablonda 5 × 2.

**Modeller.** Altı koşu: `gpt-6-astra` ve `gpt-6.1-terra` (OpenAI, Codex aboneliği üzerinden), `gpt-6-luna` (OpenAI API,
flex), `deepseek-ai/DeepSeek-V4.1-Flash` (DeepInfra), `glm-5.3-flash` (Z.ai coding plan aboneliği; GLM için birincil) ve aynı
GLM modelinin ücretli bir yoldan (Wafer, `GLM-5.3-Flash`) ikincil koşusu. Her model tek ayarla, erişim yolunun varsayılan
düşünme düzeyiyle koştu; sıcaklık ayarlanabilen modellerde 0, OpenAI modellerinde gönderilmedi. Her çağrıda sağlayıcının bildirdiği
giriş parça sayısı kaydedildi ve beklenenle karşılaştırıldı; metin bütün koşularda kesilmeden ulaştı (8.160 çağrının hepsi
normal bitti, kesilmeyi gösterecek düşük sayım yok).

**Koşullar her yolda aynı değil.** Codex aboneliği yolu (`gpt-6-astra`, `gpt-6.1-terra`) istemin önüne her çağrıda aynı olan
yaklaşık 4.500 parçalık, Z.ai yolu 2.000 parçalık bir sistem metni ekliyor; öbür yollar çıplak API'dir. Yani bu iki yoldaki
modeller, bizim talimatımızdan önce yolun kendi talimatını gördü. Bir yol içindeki karşılaştırmalar (konum, uzunluk, soru yeri
ve dili) bundan etkilenmez; modeller arası düzey karşılaştırması bu farkla okunmalıdır. Aynı GLM modeli iki yolda öğelerin
%99,1'inde aynı sonucu verdi, ama ayrışan farkların hepsi düşünmesi açık ve sistem metinli Z.ai yolunda çıktı.

**Bir istisna.** Bir yazılım hatası iki ücretli yolda 55 cevabı kaydedilmeden düşürdü; bu cevaplar hiç görülmeden aynı sorular
yeniden soruldu (iletim hatası gibi). Bunun dışında alınan hiçbir cevap yeniden sorulmadı.

**Puanlama.** Kural tabanlı; hiçbir model hakem değildir. Cevaptan türe göre değer adayları çıkarılır ve normalleştirilir (tarih
biçimleri, ay adları, binlik ayırıcı, "TL", "yüzde", "%", büyük/küçük harf). Sınıflar: *doğru* (yalnız sorulan şirketin değeri),
*karıştırma* (belgedeki öbür dört değerden biri), *metinde yok dedi*, *başka* (başka değer, birden çok aday ya da biçim dışı).
Ana koşudan sonra bir kural düzeltildi (açıklama ekleyen cevaplarda "Karar 8" gibi birimsiz küçük sayılar tutar adayı
sayılmaz; gün/yıl/yüzde türünde birden çok sayı varsa yalnız birime bitişik olan alınır); bütün cevaplar yeniden puanlandı ve
6 cevabın sınıfı değişti (`ozet.json` → `puan_surum`). Ayrıntı `kos.py` → `sinifla`.

**Belirsizlik.** Birim belgedir (uzunluk karşılaştırmasında şablon). Farklar eşli bootstrap ile verildi: 2.000 tekrar, sabit
tohum, yüzdelik %95 aralık. Aralık sıfırı dışlıyorsa fark "ayrışıyor" diye anıldı. Çoklu karşılaştırma düzeltmesi yapılmadı.

**Önceden yazılan beklentiler.** Ortadaki bilgi daha çok kaçar; uzun metinde doğruluk düşer; soru sonda iken sonuç başta
olmasından iyi ya da eşittir; sade soruda doğruluk düşer ve bu fark uzunlukla büyür. Beklentiye uymayan sonuçlar olduğu gibi
verildi.

**Dosyalar.** `ozet.json` (bütün tablolar), `sonuclar.jsonl` (çağrı başına bir satır: model, kol, uzunluk, belge sıra numarası,
şablon, yuva, biçim, düzen, sınıf, bildirilen giriş parça sayısı; metin ve ham cevap yok), `sablonlar.json`, `kos.py` (kendi
metinlerinizle aynı ölçümü kuran, soran ve puanlayan sade betik).
