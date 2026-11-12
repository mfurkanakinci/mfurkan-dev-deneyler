"""Eğitilmiş atıf modelini elle yazılmış 24 cümlede dener ve çıktıyı cikti.json dosyasına yazar.

Bu bir ölçüm değildir. Modelin hangi yazımları yakalayıp hangilerini kaçırdığını göstermek içindir.
Cümlelerin hepsi bu deneme için yazıldı, künyeler uydurmadır.
"""
import json

from gliner2 import AutoExtractor

MODEL = "mfurkanakinci/gliner-tr-legal-extraction"

CUMLELER = [
    "6098 sayılı Türk Borçlar Kanunu'nun 49. maddesi uygulanır.",
    "Davalının sorumluluğu 6098 sayılı Türk Borçlar Kanunu'nun 49. maddesi uyarınca değerlendirilmiştir.",
    "Hukuk Genel Kurulunun 12.03.2019 tarihli ve E. 2017/1234, K. 2019/567 sayılı kararında da aynı sonuca varılmıştır.",
    "Sanık hakkında TCK'nin 150/2. maddesinin uygulanması gerekirken bu hususun gözetilmemesi hukuka aykırıdır.",
    "3713 sayılı Yasanın 13 . maddesine göre işlem yapılmıştır.",
    "6100 sayılı Yasanın 120.maddesine göre gider avansının yatırılması gerekir.",
    "Anayasa Mahkemesinin 21/04/2022 tarih ve E:2021/42, K:2022/45 sayılı kararı ile hüküm iptal edilmiştir.",
    "Anayasa Mahkemesinin benzer bir başvuruda verdiği kararda (B. No: 2014/2293, 1/12/2016, § 55) aynı ilke benimsenmiştir.",
    "Yargıtay Ceza Genel Kurulunun 11.11.1991 tarih, Esas 9-242, Karar 305 sayılı kararı da bu yöndedir.",
    "Duruşma 12.03.2019 tarihinde saat 10.30'da yapılmış, dosya 2019/45 sıra numarasıyla kaydedilmiştir.",
    "Miktarın kesinlik sınırının altında kalması halinde anılan Kanun'un 366. maddesi uyarınca karar kesindir.",
    "Görev, aynı yasanın 5. maddesi uyarınca idare mahkemesine aittir.",
    "3402 sayılı Yasaya eklenen Ek 4. madde uyarınca kullanım kadastrosu yapılmıştır.",
    "2942 sayılı Kanun'un geçici 6. maddesinin uygulanma koşulları oluşmamıştır.",
    "Devir, İİK'nun 44.madde koşullarına uygun yapılmamıştır.",
    "TTK.`nun 708. maddesinde açıklandığı üzere keşide yeri zorunlu unsurdur.",
    "Avrupa İnsan Hakları Mahkemesi de aynı görüştedir (Niemietz/Almanya, B. No: 13710/88, 16/12/1992, § 29).",
    "Yargıtay Ceza Genel Kurulunun 26.09.2017 tarih, 2017/16-956 Esas ve 2017/370 sayılı Kararı ile hüküm onanmıştır.",
    "Mahkemenin 24.4.1985 gün, esas 1984/337, karar 1985/190 sayılı görevsizlik kararı kesinleşmiştir.",
    "Yargıtay 9. Hukuk Dairesinin 2019/1234 Esas, 2020/567 Karar sayılı ilamı emsal niteliğindedir.",
    "Taraflar arasındaki sözleşmenin 6. maddesinde teslim süresi otuz gün olarak belirlenmiştir.",
    "Yönetmeliğin 12. maddesi uyarınca başvuru süresi on beş gündür.",
    "Sözleşme'nin 10. maddesinin ikinci fıkrasında sınırlama sebepleri sayılmıştır.",
    "Davacı 15.06.2021 tarihinde 2021/3456 sayılı fatura ile ödeme yapmıştır."
]


def main():
    model = AutoExtractor.from_pretrained(MODEL)
    model.eval()
    sema = (
        model.create_schema()
        .entities({
            "kanun maddesi atfı": "kanun maddesi numarası atfı (yalnız madde kısmı, kanun adı hariç)",
            "kanun anışı": "kanun adı, numarası ya da kısaltması anışı",
            "mahkeme kararı atfı": "esas/karar numaralı mahkeme kararı atfı",
        })
        .relations(["madde_kanunu"])
    )
    ciktilar = model.batch_extract(
        CUMLELER, sema, batch_size=4, threshold=0.2,
        include_confidence=True, include_spans=True,
    )
    sonuc = [{"metin": m, "cikti": c} for m, c in zip(CUMLELER, ciktilar)]
    with open("06-kural-model/cikti.json", "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    for satir in sonuc:
        print("•", satir["metin"])
        for etiket, parcalar in (satir["cikti"].get("entities") or {}).items():
            for p in parcalar:
                print(f"    {etiket}: {p['text']} ({p['confidence']:.2f})")


if __name__ == "__main__":
    main()
