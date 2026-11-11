"""Aynı metnin altı tokenizer'da nasıl bölündüğünü yazdırır.

Yazı: https://mfurkan.dev/yazilar/tokenizer-nedir/
Çalıştırma: python 01-tokenizer/ornekler.py
"""

import json
from pathlib import Path

import tiktoken
from transformers import AutoTokenizer

# Sonuçların tekrarlanabilmesi için model depolarının sürümleri sabit.
HF_TOKENIZERLAR = {
    "BERTurk": ("dbmdz/bert-base-turkish-cased", "b6e1de16c983e0f2c70664591ea3f22810072608"),
    "ModernBERT-tr": ("ytu-ce-cosmos/modernbert-tr-base", "d16b9da8f7dc0eadf8946255ee5f38042bdf59c2"),
    "BGE-M3": ("BAAI/bge-m3", "5617a9f61b028005a4858fdac845db406aefb181"),
    "Qwen3": ("Qwen/Qwen3-Embedding-0.6B", "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3"),
}
TIKTOKEN_SOZLUKLERI = ["o200k_base", "cl100k_base"]

METINLER = [
    "hükümsüzlüğünün",
    "hüküm",
    "hükümsüz",
    "hükümsüzlük",
    "invalidity",
    "TBK m. 344/1",
    "E. 2023/125, K. 2024/87",
    "Kiracı, kira bedelinin belirlenmesini isteyebilir.",
]


def hf_bol(tokenizer, metin):
    """Özel token eklemeden böler; her parçayı okunur metne çevirir."""
    kimlikler = tokenizer.encode(metin, add_special_tokens=False)
    return {
        "parcalar": [tokenizer.decode([k]) for k in kimlikler],
        "kimlikler": kimlikler,
        "geri_cevrilen": tokenizer.decode(kimlikler),
    }


def tiktoken_bol(sozluk, metin):
    kimlikler = sozluk.encode(metin)
    return {
        "parcalar": [sozluk.decode_single_token_bytes(k).decode("utf-8", "replace") for k in kimlikler],
        "kimlikler": kimlikler,
        "geri_cevrilen": sozluk.decode(kimlikler),
    }


def main():
    bolucular = {}
    for ad, (depo, surum) in HF_TOKENIZERLAR.items():
        tokenizer = AutoTokenizer.from_pretrained(depo, revision=surum)
        bolucular[ad] = lambda metin, t=tokenizer: hf_bol(t, metin)
    for ad in TIKTOKEN_SOZLUKLERI:
        sozluk = tiktoken.get_encoding(ad)
        bolucular[ad.removesuffix("_base")] = lambda metin, s=sozluk: tiktoken_bol(s, metin)

    sonuc = {}
    for metin in METINLER:
        print(f"\n{metin}")
        sonuc[metin] = {}
        for ad, bol in bolucular.items():
            cikti = bol(metin)
            sonuc[metin][ad] = cikti
            print(f"  {ad:14s} {len(cikti['parcalar']):2d}  {cikti['parcalar']}")

    hedef = Path(__file__).with_name("cikti.json")
    hedef.write_text(json.dumps(sonuc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nYazıldı: {hedef}")


if __name__ == "__main__":
    main()
