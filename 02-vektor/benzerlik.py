"""Cümle çiftlerinin BGE-M3 ile kosinüs benzerliğini hesaplar.

Yazı: https://mfurkan.dev/yazilar/vektor-nedir/
Çalıştırma: python 02-vektor/benzerlik.py
Model ağırlıkları yaklaşık 2,3 GB tutar; GPU gerekmez.
"""

import argparse
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

MODEL = "BAAI/bge-m3"
SURUM = "5617a9f61b028005a4858fdac845db406aefb181"

CUMLELER = [
    "Ev sahibim kirayı artırmak istiyor.",
    "Kiraya veren, kira bedelinin yeniden belirlenmesini talep etmektedir.",
    "Sözleşme geçerlidir.",
    "Sözleşme geçersizdir.",
    "Sözleşme hükümsüzdür.",
    "Davalı, davacıya ait markayı izinsiz kullanmıştır.",
    "Boğaz'da bugün hava çok güzel.",
    "Mahkeme davanın kabulüne karar vermiştir.",
    "Mahkeme davanın reddine karar vermiştir.",
    "Kiracı kirayı ödemedi.",
    "Kiracı kirayı ödedi.",
]


def main():
    secenekler = argparse.ArgumentParser()
    secenekler.add_argument("--model-yolu", help="Model yerelde duruyorsa klasörü")
    yol = secenekler.parse_args().model_yolu

    model = SentenceTransformer(yol) if yol else SentenceTransformer(MODEL, revision=SURUM)
    vektorler = model.encode(CUMLELER, normalize_embeddings=True)
    benzerlik = vektorler @ vektorler.T

    ciftler = []
    for i in range(len(CUMLELER)):
        for j in range(i + 1, len(CUMLELER)):
            ciftler.append({"a": CUMLELER[i], "b": CUMLELER[j], "benzerlik": round(float(benzerlik[i, j]), 3)})
    ciftler.sort(key=lambda c: -c["benzerlik"])

    for c in ciftler:
        print(f"{c['benzerlik']:.3f}  {c['a']}  |  {c['b']}")

    sonuc = {
        "model": MODEL,
        "surum": SURUM,
        "boyut": int(vektorler.shape[1]),
        "ilk_alti_sayi": {"cumle": CUMLELER[2], "degerler": [round(float(x), 3) for x in vektorler[2][:6]]},
        "ciftler": ciftler,
    }
    hedef = Path(__file__).with_name("cikti.json")
    hedef.write_text(json.dumps(sonuc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nYazıldı: {hedef}")


if __name__ == "__main__":
    main()
