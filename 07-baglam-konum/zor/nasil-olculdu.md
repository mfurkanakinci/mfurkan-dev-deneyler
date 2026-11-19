# Nasıl ölçüldü (zor sürüm)

**Soru.** Uzun bir karar metni ya da bir dosya dolusu karar büyük bir dil modeline verildiğinde model metnin her yerini aynı
başarıyla okuyor mu? Üç ölçüm yapıldı: aranan bilginin metindeki yeri (S1), metnin uzunluğu (S2), sorunun yeri ve dili (S3).
İlk sürümde görev kolay kaldı (güçlü modeller her hücrede %98–100); bu sürüm aynı soruları daha zor bir kurulumda ölçer.

**Neden daha zor.** İlk sürümde aranan cümle sorunun sözcüklerini aynen taşıyordu ("… ödeme emrini … tarihinde tebellüğ etmiştir"),
şirketin adı da aynı cümlede geçiyordu; model yalnız adı ve fiili eşleştirerek bulabiliyordu. Bu sürümde:
1. **Sözcük örtüşmesi yok.** Değeri taşıyan cümle sorunun ayırt edici sözcüklerini kullanmaz. Soru "ödeme emrini hangi tarihte
   tebellüğ etmiştir?" iken metindeki cümle "İcra müdürlüğünce gönderilen ödeme emri, 12.03.2019 itibarıyla davalı şirkete usulüne
   uygun olarak ulaşmıştır." biçimindedir. 20 şablonun yeniden yazımı `sablonlar.json` → `hedef_v3`.
2. **Dolaylı gönderme.** Şirketin tam adı yalnız bir tanıtım cümlesinde geçer ("Zernova Lojistik A.Ş., yargılamada davalı sıfatıyla
   yer almaktadır."). Değer cümlesi aynı kararda 3–6 paragraf sonra gelir ve şirketi yalnız rolüyle anar ("davalı şirket"). Aynı
   kararda birden çok şirket tanıtılmışsa roller sıra sayısıyla ayrılır ("birinci davalı şirket", "ikinci davalı şirket").
3. **Yakın çeldiriciler.** Her aranan şirket için beş çeldirici birim eklendi, hepsi aynı yapıda (tanıtım + rol adıyla değer):
   iki **yakın ad** (aynı kök, başka sektör: "Zernova Nakliyat A.Ş."; bunların değer cümlesi sorunun sözcüklerini aynen taşır),
   iki **aynı şirketin başka bir olayı** (ör. ödeme emrine itiraz tarihi) ve bir **doğrulanmamış iddia** ("… tebellüğ ettiğini ileri
   sürmüş ise de bu iddia dosya kapsamıyla doğrulanmamıştır."). Çeldiricilerin ikisi aranan şirketin kararına, üçü başka kararlara
   kondu. Bir belgede 5 aranan şirket ve 25 çeldirici, yani 30 birim (60 cümle) vardır; değerlerin hepsi farklıdır.

**Belgeler.** Yargıtay hukuk dairelerinin yayımlanmış kararlarından (kaynağında anonim; kalan "Ad Soyad" kalıpları baş harfe
indirildi) sabit tohumla kararlar çekildi, "KARAR 1", "KARAR 2" başlıklarıyla art arda eklendi; eklenen cümlelerin payı düşülerek
hedef uzunlukta paragraf sınırından kesildi. Uzunluk OpenAI'nin `o200k_base` parça listesiyle sayıldı: 4.000, 16.000 ve 64.000
parça (ortalama 3.985 / 15.986 / 63.917; yaklaşık 4, 18 ve 71 sayfa, sayfa 3.000 karakter). 4.000 parçalık belgelerde eklenen
cümleler metnin yaklaşık üçte biridir.

**Yuvalar ve sorular.** Aranan değer cümleleri belgenin %0, %25, %50, %75 ve %100 noktalarına en yakın paragraf sınırına kondu.
Her biri iki biçimde soruldu: *düz* (hukuk terimleriyle) ve *sade* (gündelik dille). Talimat tektir: "Aşağıda mahkeme kararları var.
Soruyu yalnız bu metne dayanarak cevapla. Cevap olarak yalnız istenen bilgiyi yaz (tarih, tutar, sayı, dosya numarası ya da il).
Bilgi metinde yoksa yalnız 'metinde yok' yaz." Üç düzen: soru metnin sonunda, başında, hem başında hem sonunda. Her çağrı tek başınadır.

**Izgara (model başına 2.240 çağrı).** Soru sonda: 4.000 parçada 40, 16.000'de 40, 64.000'de 20 belge × 5 yuva × 2 biçim.
Soru başta ve başta+sonda: 20 / 20 / 10 belge × 5 × 2 (aynı belgeler). Metinde yok kontrolü: 16.000'lik 40 belgede hiç geçmeyen bir
şirket. Kısa taban: karar metni olmadan yalnız eklenen 60 cümle (karar başlıklarıyla), 20 şablonda 5 × 2.

**Ön deneme.** Ana ölçümden önce 16.000 parçalık 8 ayrı belgede model başına 40 soruluk denemeler yapıldı (ana ölçüme girmedi).
Yalnız çeldirici sayısını artırmak (5'ten 8'e) güçlü modelleri etkilemedi (40/40). Örtüşmesiz cümle ve dolaylı göndermeyle güçlü
modeller %92,5–95'e indi; kısa tabanda %100 bildikleri için soruların tek doğru cevabı olduğu görüldü. Hedeflenen %70–90 bandı en
güçlü modelde biraz aşıldı; ana ölçüme bu kurulumla geçildi.

**Modeller.** `gpt-6-astra` ve `gpt-6.1-terra` (OpenAI, Codex aboneliği üzerinden), `gpt-6-luna` (OpenAI API, flex),
`deepseek-ai/DeepSeek-V4.1-Flash` (DeepInfra), `glm-5.3-flash` (Z.ai coding plan aboneliği; GLM için birincil) ve aynı GLM modelinin
ücretli bir yoldan (Wafer, `GLM-5.3-Flash`) ikincil koşusu. Her model tek ayarla, yolun varsayılan düşünme düzeyiyle; sıcaklık
ayarlanabilen modellerde 0. Codex yolu istemin önüne her çağrıda aynı ~4.500 parçalık, Z.ai yolu 2.000 parçalık bir sistem metni
ekler; öbürleri çıplak API'dir. Bir yol içindeki karşılaştırmalar bundan etkilenmez; modeller arası düzey bu farkla okunmalıdır.

**Sonradan eklenen modeller.** Aynı belgeler, sorular, talimat ve puanlamayla beş model daha ölçüldü (yalnız bu sürümde; ilk sürümde
yoklar): `gemini-4-hydrogen` ve `gemini-4-carbon` (Google Antigravity, Ultra aboneliği üzerinden, "medium" düşünme düzeyi; yol istemin
önüne her çağrıda aynı ~2.200 parçalık bir sistem metni ekler), `claude-haiku-5-5` (Anthropic API, istem önbelleği açık; sistem metni
yok), `claude-opus-5-5` (Google Antigravity, Ultra aboneliği, "medium"; ~2.000 parçalık sabit önek) ve `claude-sonnet-5-5` (Claude
aboneliği, `claude -p`: araçsız, eklentisiz, boş bir dizinde, "You are a helpful assistant." sistem istemiyle; ~360 parçalık sabit
önek; efor medium, uyarlamalı düşünme). Bu modellere sıcaklık gönderilmedi: Claude Haiku 5.5 sıcaklık parametresini reddediyor
(HTTP 400); öbürleri akıl yürüten modeller olduğu için, ilk sürümdeki OpenAI modelleri gibi, yolun ya da modelin varsayılanıyla
bırakıldı (`claude -p`'de bu ayar yok). Düşünme düzeyi yolun ya da modelin varsayılanı. Claude modellerinde bildirilen parça sayısı Claude'un kendi parçalayıcısıyladır (aynı metin
`o200k_base`'in yaklaşık 1,76 katı); `sonuclar.jsonl`'daki `giris_parca` bu yüzden model aileleri arasında karşılaştırılamaz.

**Kapsam.** Abonelik kotaları ve bedel yüzünden yeni modellerin bir kısmı ızgaranın tamamını koşmadı. Claude Haiku 5.5, Opus 5.5 ve
Sonnet 5.5'te 64.000 parçada soru başta ve başta+sonda kolları 10 yerine 5 belgeyle planlandı (önceden yazılmış küçültme); Sonnet'te
64.000 parça hiç koşulmadı. 14.11 itibarıyla Opus'ta yalnız 4.000 parça (üç düzen) ve kısa taban, Sonnet'te yalnız kısa taban tamam;
öbür hücreleri sonradan eklenecek. Tablolar hücre düzeyindedir: bir model bir hücrede (düzen × uzunluk) planındaki bütün soruları
cevapladıysa o hücrede gösterilir, yarım hücreler hiçbir tabloya ve `sonuclar.jsonl`'a girmez; hangi modelin hangi hücrede olduğu
`ozet.json` → `kapsam` alanında. Karşılaştırmalar her model içinde, yalnız ortak sorularla yapılır.

**Puanlama.** Kural tabanlı; hiçbir model hakem değildir. Cevaptan türe göre değer adayları çıkarılır ve normalleştirilir (tarih
biçimleri, ay adları, binlik ayırıcı, "TL", "yüzde", "%", büyük/küçük harf). Sınıflar: *doğru* (yalnız sorulan şirketin değeri),
*karıştırma* (belgedeki başka bir değer; alt türü: yakın ad, aynı şirketin başka olayı, iddia, başka bir aranan şirketin değeri ya
da onun çeldiricisi), *metinde yok dedi*, *başka* (başka değer, birden çok aday ya da biçim dışı; doğru değeri bir çeldiriciyle
birlikte veren cevap da buraya düşer). Ayrıntı `kos.py` → `sinifla`. Bu kural bir modeli belirgin biçimde etkiler: Claude Opus 5.5 hatalarının
çoğunda doğru değeri, iddia edilen ya da başka bir olaya ait değerle birlikte verdi; bu cevaplar kurala göre yanlış sayıldı.

**Belirsizlik.** Birim belgedir (uzunluk karşılaştırmasında şablon). Farklar eşli bootstrap ile verildi: 2.000 tekrar, sabit tohum,
yüzdelik %95 aralık. Aralık sıfırı dışlıyorsa "ayrışıyor" denir. İlk sürümle karşılaştırmada belgeler farklı olduğu için iki örneklemli
bootstrap kullanıldı. Çoklu karşılaştırma düzeltmesi yapılmadı.

**Önceden yazılan beklentiler.** Ortadaki bilgi daha çok kaçar; uzun metinde doğruluk düşer; soru sonda iken (ve başta+sonda iken)
sonuç başta olmasından iyi ya da eşittir; sade soruda doğruluk düşer ve bu fark uzunlukla büyür.

**Dosyalar.** `ozet.json` (bütün tablolar), `sonuclar.jsonl` (çağrı başına bir satır: model, kol, uzunluk, belge sıra numarası,
şablon, yuva, biçim, düzen, sınıf, karıştırma alt türü, çeldiricinin yeri, bildirilen giriş parça sayısı; metin ve ham cevap yok),
`sablonlar.json` (şablonlar, çeldirici kalıpları, örtüşmesiz hedef kalıpları), `kos.py` (kendi metinlerinizle aynı ölçümü kuran,
soran ve puanlayan sade betik).
