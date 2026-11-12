# Nasıl ölçüldü

**Karşılaştırılanlar.** (1) Kural tabanlı atıf ayrıştırıcısı: Türk kanun maddesi ve mahkeme kararı atıflarını düzenli ifadelerle
bulan ve kanun numarasına bağlayan bir ayrıştırıcı. (2) İnce ayarlı GLiNER2.5 modeli: aynı atıfları metin aralığı olarak işaretleyen
bir varlık tanıma modeli. Modelin işaretlediği aralıklar, kanun ve madde numarasına aynı kural çözümleyiciyle çevrilir.
Modelin eşikleri önceden, ayrı bir doğrulama bölümünde seçildi (aralık: madde 0,3 ve karar 0,7; anahtar: madde 0,6 ve karar 0,7).
Bu çalışmada hiçbir eşik ya da kural değiştirilmedi, yeni çıkarım yapılmadı. Bütün sayılar mevcut çıktılardan hesaplandı.

**Referans (öğretmen).** Güçlü bir genel dil modelinin her karar için çıkardığı atıf listesi. Madde atıfları `kanun:tür:madde`
anahtarına, karar atıfları (esas, karar) çiftine çevrildi. Liste metindeki yerlere hizalanarak "altın aralıklar" elde edildi.
Öğretmen kusursuz değildir. Yanlış işaret tablolarındaki "öğretmen listesinde olmayan gerçek atıf adayı" satırı bunu gösterir.

**Veri.** Türk mahkeme kararlarından ayrılmış iki bölüm: doğrulama (1.993 karar) ve test (4.033 karar). Çoğu Yargıtay kararıdır.
Danıştay, Anayasa Mahkemesi, bölge adliye ve ilk derece kararları azınlıktadır. Kararlar, en çok atıf alan kararlar ve kurul kararları
ağırlıklı bir kümeden seçildi. Ortalama bir kararın dağılımını temsil etmez.

**Ölçüler.** Aralık ölçüsünde tahmin ile altın aralık bire bir eşleştirilir. Örtüşen iki aralık eşleşmiş sayılır. Anahtar
ölçüsünde karar başına anahtar kümeleri karşılaştırılır. Kesinlik, duyarlılık ve F1 bütün kararlar üzerinden toplanarak
hesaplanır.

**Dört küme.** Her altın aralık için iki sorulur: kural onu buldu mu, model onu buldu mu? Böylece her atıf dört kümeden birine
düşer: ikisi de buldu, yalnız kural buldu, yalnız model buldu, ikisi de kaçırdı. Aynı sınıflama öğretmen anahtarları için de yapıldı.

**Önemli yapısal not.** Altın aralıkların büyük kısmı (A kökeni) tanım gereği kuralın bulduğu aralıklardır. Öğretmen anahtarı
kuralın çözdüğü bir atıfla aynıysa, o atfın aralığı kuralın aralığıdır. Bu yüzden aralık düzeyinde kural yapısal bir avantaja
sahiptir. Modelin bulup kuralın kaçırdığı aralıklar, kuralın kanunu bağlayamadığı (B1) ya da metin aramasıyla bulunan (B3)
aralıklardır. Anahtar düzeyi bu bağdan bağımsızdır. Öğretmenin metinde yerini bulamadığımız anahtarları aralık tablosuna girmez,
anahtar tablosunda yer alır.

**Kategoriler.** Yazım biçimi ve yanlış işaret kategorileri düzenli ifadelerle tanımlandı. Kategoriler yalnız doğrulama bölümünde
geliştirildi. Yeni bir kategori, ancak o kümedeki atıfların en az %3'ünü ya da en az 15 atfı açıklıyorsa eklendi. Liste test
sayımından önce donduruldu. Test bir kez sayıldı. Örnekler doğrulama bölümünden alındı. Örneklere yalnız hukuk sözcüklerinden
ve sayılardan oluşan parçalar girdi. Karar künyelerindeki sayılar biçim yer tutucusuna çevrildi.

**Kırılımlar.** Mahkeme ve karar yılı dilimleri betimseldir. 100'den az kararlı dilimler "az örnek" diye işaretlidir.

**Birleşimler.** Yeni çıkarım yapılmadan üç birleşim kuruldu. (a) İki sistemin aralıklarının birleşimi: örtüşenler tek aralıkta
birleştirildi. (b) Kural öncelikli: kuralın aralıkları, artı hiçbir kural aralığıyla örtüşmeyen model aralıkları. (c) Yalnız
ikisinin de işaretlediği kural aralıkları. Farkların güven aralıkları eşli bootstrap ile hesaplandı (birim karar, 10.000 tekrar).

**Büyüme eğrisi.** Kural ayrıştırıcının dokuz geçmiş sürümü (2026-10-05 ile 2026-11-09 arası) aynı doğrulama kararlarında
çalıştırıldı. Eğri yalnız anahtar duyarlılığını verir, çünkü altın aralıklar bugünkü kurala bağlıdır. Her sürümde kural sayısı
olarak, iki ayrıştırıcı modülünde tanımlı düzenli ifade nesnelerinin sayısı alındı. Ölçüm hattı, testte kullanılan sürümün
çıktısını karar başına birebir yeniden üretti.

**Elle kontrol.** Testten tohumlu rastgele 120 işaret seçildi. Bunların 40'ını yalnız kural, 40'ını yalnız model işaretledi;
kalan 40'ını ikisi de işaretledi ama öğretmen listesinde karşılıkları yok. Kişisel veriler maskelendi, kümeler okuyucudan
gizlendi. Okuyucu her işareti "atıf / atıf değil / emin değilim" diye işaretleyecek. Sonuçlar işaretleme bitince eklenecek.
