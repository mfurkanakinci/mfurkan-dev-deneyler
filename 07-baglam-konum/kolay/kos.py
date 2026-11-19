#!/usr/bin/env python3
"""Uzun metinde konum, uzunluk ve soru biçimi ölçümü: sade sürüm.

Kendi metinlerinizle çalışır. Bir klasördeki .txt dosyalarını (her dosya bir karar; satırlar paragraf) art arda ekleyip hedef
uzunlukta (o200k_base parçası) belgeler kurar, şablondaki beş cümleyi %0/%25/%50/%75/%100 yuvalarına yerleştirir, her cümleyi iki
biçimde (duz/sade) OpenAI uyumlu bir uca sorar ve cevabı kural tabanlı puanlar (dogru / karistirma / yok_dedi / baska).

Gerekenler: python 3.10+, `pip install tiktoken`.

Örnek:
  export API_KEY=...            # anahtar ortam değişkeninden okunur, hiçbir yere yazılmaz
  python kos.py --metinler ./kararlar --sablonlar sablonlar.json --cikti ./sonuc \
      --uc https://api.openai.com/v1/chat/completions --model gpt-6-luna --uzunluk 16000 --belge 4 --tohum 1

Çıktı: <cikti>/sonuclar.jsonl (öğe başına sınıf) ve ekrana yuva/biçim kırılımında doğruluk.
"""
from __future__ import annotations

import argparse, datetime as dt, json, os, random, re, urllib.request
from pathlib import Path

import tiktoken

ENC = tiktoken.get_encoding("o200k_base")
YUVA = [0, 25, 50, 75, 100]
TALIMAT = ("Aşağıda mahkeme kararları var. Soruyu yalnız bu metne dayanarak cevapla. Cevap olarak yalnız istenen bilgiyi yaz "
           "(tarih, tutar, sayı, dosya numarası ya da il). Bilgi metinde yoksa yalnız 'metinde yok' yaz.")
ILLER = ["Eskişehir", "Kayseri", "Samsun", "Denizli", "Trabzon", "Mersin", "Konya", "Bursa", "Adana", "Gaziantep", "Erzurum", "Balıkesir"]
BITIS = re.compile(r"[.!?:;)\"”’'»]\s*$")


def ntok(s):
    return len(ENC.encode(s))


def tr_lower(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


# ---------------------------------------------------------------- değerler
def deger(tur, rng):
    if tur == "tarih":
        a, b = dt.date(2015, 1, 1).toordinal(), dt.date(2023, 12, 31).toordinal()
        return dt.date.fromordinal(rng.randint(a, b)).strftime("%d.%m.%Y")
    if tur == "tutar":
        return f"{rng.randrange(12000, 950001, 50):,}".replace(",", ".")
    if tur == "gun":
        return str(rng.choice([5, 7, 8, 10, 14, 15, 20, 30, 45, 60]))
    if tur == "yuzde":
        return str(rng.randrange(10, 91, 5))
    if tur == "yil":
        return str(rng.randint(2, 24))
    if tur == "dosya":
        return f"20{rng.randint(15, 23)}/{rng.randint(10000, 99999)}"
    if tur == "il":
        return rng.choice(ILLER)
    raise ValueError(tur)


def metinde_var(tur, v, text):
    low = tr_lower(text)
    if tur == "tarih":
        g, a, y = v.split(".")
        return bool(re.search(rf"(?<!\d)0?{int(g)}[./]0?{int(a)}[./]{y}(?!\d)", text))
    if tur == "tutar":
        return bool(re.search(rf"(?<![\d.,]){re.escape(v)}(?!\d)", text))
    if tur == "gun":
        return bool(re.search(rf"(?<![\d.,]){v}\s*gün", low))
    if tur == "yuzde":
        return bool(re.search(rf"(yüzde\s*{v}|%\s*{v})(?![\d.,])", low))
    if tur == "yil":
        return bool(re.search(rf"(?<![\d.,/]){v}\s*yıl", low))
    if tur == "dosya":
        return v in text
    return bool(re.search(rf"\b{re.escape(tr_lower(v))}(?![a-zçğıöşü])", low))


# ---------------------------------------------------------------- belge
def belge_kur(kararlar, hedef, sab, kokler, rng):
    """kararlar: [[paragraf, ...], ...] (sırayla tüketilir). Döner (metin, {yuva: (kök, değer)}, (kontrol kökü, değeri))."""
    pay = 5 * (ntok(sab["cumle"]) + 1)
    birim, no = [], 0
    while sum(ntok(p) + 1 for _, _, p in birim) < hedef - pay + 3000 and kararlar:
        no += 1
        birim += [(no, -1, f"KARAR {no}")] + [(no, j, p) for j, p in enumerate(kararlar.pop(0))]

    def metin_(bs):
        return "\n".join(x for n, j, p in bs for x in ([""] if j == -1 and n > 1 else []) + [p])
    aday = [i for i, (n, j, p) in enumerate(birim) if j >= 2 and (BITIS.search(p) or i + 1 == len(birim) or birim[i + 1][1] == -1)]
    yak, c = [], 0
    for _, _, p in birim:
        c += ntok(p) + 1; yak.append(c)
    yakin = sorted(aday, key=lambda i: abs(yak[i] - (hedef - pay)))[:6]          # yaklaşık sayımla adaylar, gerçek sayımla seçim
    i = min(yakin, key=lambda i: abs(ntok(metin_(birim[: i + 1])) - (hedef - pay)))
    birim = birim[: i + 1]
    son_no = birim[-1][0]
    sinir, cum = [], 0
    for k, (n, j, p) in enumerate(birim):
        cum += ntok(p) + 1
        if j >= 0 and k + 1 < len(birim) and (BITIS.search(p) or birim[k + 1][1] == -1):
            sinir.append((k, n, cum))
    yer = {0: next(s for s in sinir if s[1] == 1)}
    son = [s for s in sinir if s[1] == son_no and s[0] <= len(birim) - 2]
    yer[100] = son[-1] if son else (len(birim) - 2, son_no, 0)
    kullan = {1, son_no}
    for y in (25, 50, 75):
        h = cum * y / 100
        adaylar = sorted((s for s in sinir if s[0] not in {v[0] for v in yer.values()}), key=lambda s: abs(s[2] - h))
        sec = next((s for s in adaylar if abs(s[2] - h) <= 0.05 * cum and s[1] not in kullan), adaylar[0])
        yer[y] = sec; kullan.add(sec[1])
    govde = metin_(birim)
    ks = rng.sample(kokler, 6)
    vals = []
    while len(vals) < 6:
        v = deger(sab["tur"], rng)
        if v not in vals and not metinde_var(sab["tur"], v, govde):
            vals.append(v)
    sira = list(range(5)); rng.shuffle(sira)
    atama = {y: (ks[sira[i]], vals[sira[i]]) for i, y in enumerate(YUVA)}
    ek = {yer[y][0]: y for y in YUVA}
    satir = []
    for k, (n, j, p) in enumerate(birim):
        if j == -1 and n > 1:
            satir.append("")
        satir.append(p)
        if k in ek:
            kk, v = atama[ek[k]]
            satir.append(sab["cumle"].replace("{KOK}", kk).replace("{DEGER}", v))
    return "\n".join(satir), atama, (ks[5], vals[5])


# ---------------------------------------------------------------- puan
AYLAR = {"ocak": 1, "şubat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8, "eylül": 9,
         "ekim": 10, "kasım": 11, "aralık": 12}
YOK = re.compile(r"metinde\s+yok|yer\s+almıyor|yer\s+almamaktadır|bulunmamaktadır|bulunmuyor|belirtilmemiş")


def adaylar(tur, s):
    v = set()
    if tur == "tarih":
        v |= {f"{int(g):02d}.{int(a):02d}.{y}" for g, a, y in re.findall(r"(?<!\d)(\d{1,2})\s*[./\-]\s*(\d{1,2})\s*[./\-]\s*(\d{4})(?!\d)", s)}
        v |= {f"{int(g):02d}.{AYLAR[a]:02d}.{y}" for g, a, y in re.findall(rf"(?<!\d)(\d{{1,2}})\s+({'|'.join(AYLAR)})\s+(\d{{4}})", s)}
    elif tur == "tutar":
        t = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", ".", s)
        for ana, kurus, b, tl in re.findall(r"(?<![\d.,])(\d{1,3}(?:[.,]\d{3})+|\d+)(?:,(\d{1,2}))?(?!\d)(\s*bin\b)?(\s*(?:tl|lira|₺))?", t):
            n = int(re.sub(r"[.,]", "", ana)) * (1000 if b else 1)
            if n < 1000 and not tl:
                continue                      # "Karar 8" gibi birimsiz küçük sayı tutar adayı değildir
            if kurus and kurus.strip("0"):
                v.add("?"); continue
            v.add(f"{n:,}".replace(",", "."))
        for a_, b_ in re.findall(r"(\d{1,3})\s*bin\s*(\d{1,3})(?!\d)", s):     # "677 bin 300"
            v.discard(f"{int(a_) * 1000:,}".replace(",", "."))
            v.discard(str(int(b_)))
            v.add(f"{int(a_) * 1000 + int(b_):,}".replace(",", "."))
    elif tur in ("gun", "yuzde", "yil"):
        v |= {str(int(x)) for x in re.findall(r"(?<![\d.,/])(\d{1,3})(?![\d]|[.,]\d)", s)}
        if len(v) > 1:                        # birden çok sayı: yalnız birime bitişik olanlar ("30 gün", "%40", "12 yıl")
            birim = {"gun": r"(\d{1,3})\s*(?:\([^)]*\)\s*)?gün", "yil": r"(\d{1,3})\s*(?:\([^)]*\)\s*)?yıl",
                     "yuzde": r"%\s*(\d{1,3})|yüzde\s*(\d{1,3})|(\d{1,3})\s*%"}[tur]
            bv = {str(int(next(g for g in (m if isinstance(m, tuple) else (m,)) if g))) for m in re.findall(birim, s)}
            v = bv or v
    elif tur == "dosya":
        v |= {f"{y}/{int(n)}" for y, n in re.findall(r"(?<!\d)(\d{4})\s*/\s*(\d{1,6})(?!\d)", s)}
    elif tur == "il":
        v |= {tr_lower(il) for il in ILLER if re.search(rf"(?<![a-zçğıöşü]){tr_lower(il)}", s)}
    return v


def norm(tur, d):
    return f"{d.split('/')[0]}/{int(d.split('/')[1])}" if tur == "dosya" else tr_lower(d) if tur == "il" else d


def sinifla(tur, cevap, dogru, obur):
    s = tr_lower(re.sub(r"<think>.*?</think>", " ", cevap or "", flags=re.S).replace("**", " "))
    v = adaylar(tur, s)
    if len(v) == 1:
        x = v.pop()
        if dogru is not None and x == norm(tur, dogru):
            return "dogru"
        return "karistirma" if x in {norm(tur, o) for o in obur} else "baska"
    return "yok_dedi" if not v and YOK.search(s) else "baska"


# ---------------------------------------------------------------- çağrı
def sor(uc, model, istem):
    body = {"model": model, "messages": [{"role": "user", "content": istem}]}
    req = urllib.request.Request(uc, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + os.environ["API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.load(r)
    return d["choices"][0]["message"].get("content"), (d.get("usage") or {}).get("prompt_tokens")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metinler", required=True, help="klasör: her .txt bir karar, satırlar paragraf")
    ap.add_argument("--sablonlar", required=True)
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--uc", required=True, help="OpenAI uyumlu chat/completions adresi")
    ap.add_argument("--model", required=True)
    ap.add_argument("--uzunluk", type=int, default=16000)
    ap.add_argument("--belge", type=int, default=2, help="şablon başına belge")
    ap.add_argument("--sablon", nargs="*", help="yalnız bu şablonlar (ör. s01 s08)")
    ap.add_argument("--soru-basta", action="store_true", help="soruyu belgenin önüne koy")
    ap.add_argument("--tohum", type=int, default=1)
    a = ap.parse_args()
    spec = json.load(open(a.sablonlar, encoding="utf-8"))
    rng = random.Random(a.tohum)
    dosyalar = sorted(Path(a.metinler).glob("*.txt")); rng.shuffle(dosyalar)
    kararlar = [[p.strip() for p in f.read_text(encoding="utf-8").splitlines() if p.strip()] for f in dosyalar]
    kararlar = [k for k in kararlar if len(k) >= 4]
    havuz = tr_lower("\n".join("\n".join(k) for k in kararlar))
    kokler = [k for k in spec["ad_kokleri"] if tr_lower(k) not in havuz]
    out = Path(a.cikti); out.mkdir(parents=True, exist_ok=True)
    sonuc = []
    for sab in spec["sablonlar"]:
        if a.sablon and sab["id"] not in a.sablon:
            continue
        for n in range(a.belge):
            metin, atama, _ = belge_kur(kararlar, a.uzunluk, sab, kokler, rng)
            for y in YUVA:
                for bic in ("duz", "sade"):
                    soru = sab[bic].replace("{KOK}", atama[y][0])
                    istem = f"{TALIMAT}\n\nSoru: {soru}\n\n{metin}" if a.soru_basta else f"{TALIMAT}\n\n{metin}\n\nSoru: {soru}"
                    cevap, pt = sor(a.uc, a.model, istem)
                    s = sinifla(sab["tur"], cevap, atama[y][1], [atama[z][1] for z in YUVA if z != y])
                    sonuc.append({"sablon": sab["id"], "belge": n + 1, "yuva": y, "bicim": bic, "sinif": s,
                                  "o200k": ntok(istem), "bildirilen_parca": pt})
                    print(sab["id"], n + 1, y, bic, s, flush=True)
    with open(out / "sonuclar.jsonl", "w", encoding="utf-8") as fh:
        for r in sonuc:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for y in YUVA:
        rs = [r for r in sonuc if r["yuva"] == y]
        print(f"%{y}: doğruluk {sum(r['sinif'] == 'dogru' for r in rs) / max(len(rs), 1):.3f} (n={len(rs)})")
    for b in ("duz", "sade"):
        rs = [r for r in sonuc if r["bicim"] == b]
        print(f"{b}: doğruluk {sum(r['sinif'] == 'dogru' for r in rs) / max(len(rs), 1):.3f} (n={len(rs)})")


if __name__ == "__main__":
    main()
