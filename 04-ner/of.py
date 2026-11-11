"""Aynı yazılışa sahip adların cümleye göre nasıl etiketlendiğini gösterir.

Yazı: https://mfurkan.dev/yazilar/ner-bert/
Çalıştırma: python 04-ner/of.py
"""

import argparse
import json
from pathlib import Path

from transformers import pipeline

MODEL = "akdeniz27/bert-base-turkish-cased-ner"

CUMLELER = [
    "Sanık Deniz Yıldız, Siirt Ağır Ceza Mahkemesinde yargılanmıştır.",
    "Davacı, Trabzon ili Of ilçesinde ikamet etmektedir.",
    "Of Asliye Hukuk Mahkemesinin kararı temyiz edilmiştir.",
    "Davalı Bank of America ile kredi sözleşmesi imzalamıştır.",
    "Of, yine mi erteleme!",
    "Davacı Batman'da ikamet etmekte, davalı ise Ordu'da çalışmaktadır.",
    "Müşteki Savaş Barış, Tokat'ta bir tokat yediğini beyan etmiştir.",
    "Davacı vekili Av. Çiçek Gül, Gül Sokak'taki işyerinin tahliyesini istemiştir.",
]

TURLER = {"PER": "kişi", "LOC": "yer", "ORG": "kurum"}


def main():
    secenekler = argparse.ArgumentParser()
    secenekler.add_argument("--model-yolu", help="Model yerelde duruyorsa klasörü")
    yol = secenekler.parse_args().model_yolu

    bul = pipeline("token-classification", model=yol or MODEL, aggregation_strategy="simple")
    sonuc = []
    for cumle in CUMLELER:
        varliklar = [
            {"metin": v["word"], "tur": TURLER.get(v["entity_group"], v["entity_group"]), "guven": round(float(v["score"]), 2)}
            for v in bul(cumle)
        ]
        sonuc.append({"cumle": cumle, "varliklar": varliklar})
        print(cumle)
        print("   ", [(v["metin"], v["tur"], v["guven"]) for v in varliklar])

    hedef = Path(__file__).with_name("cikti.json")
    hedef.write_text(json.dumps({"model": MODEL, "sonuc": sonuc}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nYazıldı: {hedef}")


if __name__ == "__main__":
    main()
