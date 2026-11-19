#!/usr/bin/env python3
"""Uzun metinde konum, uzunluk ve soru biçimi ölçümü, zor sürüm: sade betik.

Kendi metinlerinizle çalışır. Bir klasördeki .txt dosyalarını (her dosya bir karar; satırlar paragraf) art arda ekleyip hedef
uzunlukta (o200k_base) belgeler kurar. Her belgeye bir şablondan 5 hedef şirket ve her hedef için 5 yakın çeldirici (2 yakın ad,
2 aynı şirketin başka olayı, 1 doğrulanmamış iddia) eklenir. Her birim iki cümledir: şirketin tam adını ve rolünü veren tanıtım
ve aynı kararda 3–6 paragraf sonra değeri veren, şirketi yalnız rol adıyla ("davalı şirket"; aynı kararda birden çok şirket varsa
"birinci davalı şirket", "ikinci davalı şirket" …) anan cümle. Hedef değer cümlesi sorunun sözcüklerini paylaşmaz (hedef_v3).
Hedefler %0/%25/%50/%75/%100 yuvalarındadır. Her hedef iki biçimde (duz/sade) ve seçilen düzende (sonda / basta / ikisi) OpenAI
uyumlu bir uca sorulur; cevap kural tabanlı puanlanır (dogru / karistirma[alt tür] / yok_dedi / baska).

Gerekenler: python 3.10+, `pip install tiktoken`.
  export API_KEY=...            # anahtar ortam değişkeninden okunur, hiçbir yere yazılmaz
  python kos.py --metinler ./kararlar --sablonlar sablonlar.json --cikti ./sonuc \
      --uc https://api.openai.com/v1/chat/completions --model gpt-6-luna --uzunluk 16000 --belge 2 --duzen sonda --tohum 1
"""
from __future__ import annotations

import argparse, collections, datetime as dt, json, os, random, re, statistics as st, urllib.request
from pathlib import Path

import tiktoken

ENC = tiktoken.get_encoding("o200k_base")
YUVA = [0, 25, 50, 75, 100]
TALIMAT = ("Aşağıda mahkeme kararları var. Soruyu yalnız bu metne dayanarak cevapla. Cevap olarak yalnız istenen bilgiyi yaz "
           "(tarih, tutar, sayı, dosya numarası ya da il). Bilgi metinde yoksa yalnız 'metinde yok' yaz.")
ILLER = ["Eskişehir", "Kayseri", "Samsun", "Denizli", "Trabzon", "Mersin", "Konya", "Bursa", "Adana", "Gaziantep", "Erzurum", "Balıkesir"]
IL_GENIS = ILLER + """Adıyaman Afyonkarahisar Aksaray Amasya Ankara Antalya Ardahan Artvin Aydın Bartın Bayburt Bilecik Bingöl Bitlis Bolu Burdur
Çanakkale Çankırı Çorum Diyarbakır Düzce Edirne Elazığ Erzincan Giresun Gümüşhane Hakkari Hatay Iğdır Isparta İstanbul İzmir Kahramanmaraş
Karabük Karaman Kars Kastamonu Kırıkkale Kırklareli Kırşehir Kocaeli Kütahya Malatya Manisa Mardin Muğla Nevşehir Niğde Rize Sakarya Siirt
Sinop Sivas Şanlıurfa Şırnak Tekirdağ Tunceli Uşak Yalova Yozgat Zonguldak""".split()
BITIS = re.compile(r"[.!?:;)\"”’'»]\s*$")
SIRA = ["birinci", "ikinci", "üçüncü", "dördüncü", "beşinci", "altıncı", "yedinci", "sekizinci", "dokuzuncu", "onuncu"]
SIRA += ["on " + x for x in SIRA[:9]] + ["yirminci"] + ["yirmi " + x for x in SIRA[:9]] + ["otuzuncu"]
ROLKELIME = r"(?:Davalı|Davacı|Borçlu|Alacaklı|Kiracı|İşveren|Alıcı|Lehtar|davalı|davacı|borçlu|alacaklı|kiracı|işveren|alıcı)"
EK = {"'ye": "şirkete", "'ne": "şirkete", "'nin": "şirketin", "'den": "şirketten", "": "şirket"}
DUZELT = {"{R} şirket lehine düzenlenen bono {DEGER} tarihinde düzenlenmiştir.": "{R} şirket lehine bono {DEGER} tarihinde keşide edilmiştir.",
          "{R} şirketin şirket paylarının yüzde {DEGER} oranındaki kısmı davalıya devredilmiştir.": "{R} şirketin paylarının yüzde {DEGER} oranındaki kısmı davalıya devredilmiştir.",
          "{R} şirket, davalı sigorta şirketine {DEGER} TL prim ödemiştir.": "{R} şirket, sigortacısına {DEGER} TL prim ödemiştir."}


def ntok(s):
    return len(ENC.encode(s))


def tr_lower(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


def buyut(s):
    return s[0].replace("i", "İ").replace("ı", "I").upper() + s[1:]


def rolle(p, ad):
    """Kalıptaki şirket adını rol yer tutucusuna çevirir ({R} şirket / şirkete / şirketin …)."""
    a = re.escape(ad)
    p = re.sub(rf"[Ll]ehtarı {a} olan bono", "{R} şirket lehine düzenlenen bono", p)
    p = re.sub(rf"Davacının {a} işyerindeki", "Davacının {R} şirketteki", p)
    p = re.sub(rf"Davacı, {a} işyerindeki", "Davacı, {R} şirketteki", p)
    p = re.sub(rf"(?:{ROLKELIME}\s+)?{a}('ye|'ne|'nin|'den)?", lambda m: "{R} " + EK[m.group(1) or ""], p)
    return DUZELT.get(p, p)


# ---------------------------------------------------------------- değerler
def deger(tur, rng, genis=False):
    if tur == "tarih":
        a, b = dt.date(2015, 1, 1).toordinal(), dt.date(2023, 12, 31).toordinal()
        return dt.date.fromordinal(rng.randint(a, b)).strftime("%d.%m.%Y")
    if tur == "tutar":
        return f"{rng.randrange(12000, 950001, 50):,}".replace(",", ".")
    if tur == "gun":
        return str(rng.randint(3, 90) if genis else rng.choice([5, 7, 8, 10, 14, 15, 20, 30, 45, 60]))
    if tur == "yuzde":
        return str(rng.randint(5, 95) if genis else rng.randrange(10, 91, 5))
    if tur == "yil":
        return str(rng.randint(1, 45) if genis else rng.randint(2, 24))
    if tur == "dosya":
        return f"20{rng.randint(15, 23)}/{rng.randint(10000, 99999)}"
    if tur == "il":
        return rng.choice(IL_GENIS if genis else ILLER)
    raise ValueError(tur)


# ---------------------------------------------------------------- belge
def govde(kararlar, hedef):
    """Kararları art arda ekler, hedefe en yakın paragraf sınırında keser. Döner [(karar_no, satır)] (başlık satırı: KARAR n)."""
    birim, no = [], 0
    while sum(ntok(p) + 1 for _, p in birim) < hedef + 2000 and kararlar:
        no += 1
        birim += [(no, f"KARAR {no}")] + [(no, p) for p in kararlar.pop(0)]
    c, kes = 0, len(birim)
    for i, (n, p) in enumerate(birim):
        c += ntok(p) + 1
        if c >= hedef and (BITIS.search(p) or i + 1 == len(birim) or birim[i + 1][1].startswith("KARAR ")):
            kes = i + 1; break
    return birim[:kes]


def belge_kur(kararlar, hedef, sab, cel, h3, kokler, rng, tanitimlar):
    """Döner (metin, hedefler {yuva: (kök, değer)}, etiket {değer: (yuva, tür)})."""
    pay = 1450                                                    # eklenen 60 cümlenin yaklaşık o200k payı
    bs = govde(kararlar, hedef - pay)
    karar = [n for n, _ in bs]
    psinir = collections.defaultdict(list); hsinir = {}
    for i, (n, p) in enumerate(bs[:-1]):
        if p.startswith("KARAR "):
            hsinir[n] = i
        elif BITIS.search(p) or bs[i + 1][1].startswith("KARAR "):
            psinir[n].append(i)
    hepsi = [i for n in psinir for i in psinir[n]]; tum = len(hepsi)
    yuva_at = {0: psinir[1][0], 100: psinir[karar[-1]][-1]}
    for y in (25, 50, 75):
        yuva_at[y] = sorted(hepsi)[min(tum - 1, round(tum * y / 100))]

    def oncesi(n, at, g):
        sl = ([hsinir[n]] if n in hsinir else []) + psinir[n]
        i = sl.index(at)
        return sl[max(0, i - g)] if i > 0 else at
    ks = rng.sample(kokler, 6); kullanilan = set(); vals = []
    while len(vals) < 5:
        v = deger(sab["tur"], rng)
        if v not in kullanilan:
            kullanilan.add(v); vals.append(v)
    tanit, birimler, yuk = {}, [], collections.Counter()
    for k, y in enumerate(YUVA):
        ad = cel["ad"].replace("{KOK}", ks[k]); at = yuva_at[y]; n = karar[at]
        tanit[(n, ad)] = oncesi(n, at, rng.choice([3, 4, 5, 6]))
        birimler.append((n, ad, at, h3["hedef"], vals[k], y, "hedef")); yuk[n] += 1
    for k, y in enumerate(YUVA):
        ad = cel["ad"].replace("{KOK}", ks[k]); hk = karar[yuva_at[y]]
        turler = ["yakin_ad", "yakin_ad", "baska_olay", "baska_olay", "iddia"]
        yerler = ["ayni_karar"] * 2 + ["uzak"] * 3; rng.shuffle(yerler)
        ya = rng.sample(cel["yakin_ad"], 2); bo = rng.sample(cel["baska_olay"], 2); idd = rng.sample(cel["iddia"], 1)
        for tur, yer in zip(turler, yerler):
            v = deger(sab["tur"], rng, genis=True)
            while v in kullanilan:
                v = deger(sab["tur"], rng, genis=True)
            kullanilan.add(v)
            if tur == "yakin_ad":
                ad2, kal = ya.pop().replace("{KOK}", ks[k]), rolle(sab["cumle"], cel["ad"])
            else:
                ad2, kal = ad, rolle((bo if tur == "baska_olay" else idd).pop(), cel["ad"])
            if yer == "ayni_karar":
                n = hk
            else:
                ad_ = [m for m in psinir if m != hk] or [hk]
                n = min(ad_, key=lambda m: (yuk[m], rng.random()))
            if (n, ad2) in tanit:
                at = rng.choice([i for i in psinir[n] if i > tanit[(n, ad2)]] or [tanit[(n, ad2)]])
            else:
                at = rng.choice(psinir[n]); tanit[(n, ad2)] = oncesi(n, at, rng.choice([3, 4, 5, 6]))
            yuk[n] += 1
            birimler.append((n, ad2, at, kal, v, y, tur))
    rol = {}
    for n in {m for m, _ in tanit}:
        sir = sorted((t, a) for (m, a), t in tanit.items() if m == n)
        for j, (_, a) in enumerate(sir):
            rol[(n, a)] = (SIRA[j] + " " + h3["rol"]) if len(sir) > 1 else h3["rol"]
    ek = collections.defaultdict(list); yaz = set()
    for n, ad2, at, kal, v, y, tur in birimler:
        r = rol[(n, ad2)]
        if (n, ad2) not in yaz:
            ek[tanit[(n, ad2)]].append((0, buyut(rng.choice(tanitimlar).replace("{AD}", ad2).replace("{ROL}", r)))); yaz.add((n, ad2))
        ek[at].append((1, buyut(kal.replace("{R}", r).replace("{DEGER}", v))))
    satir = []
    for i, (n, p) in enumerate(bs):
        if p.startswith("KARAR ") and n > 1:
            satir.append("")
        satir.append(p)
        satir += [c for _, c in sorted(ek.get(i, []), key=lambda x: x[0])]
    hedefler = {y: (ks[k], vals[k]) for k, y in enumerate(YUVA)}
    etiket = {v: (y, tur) for _, _, _, _, v, y, tur in birimler}
    return "\n".join(satir), hedefler, etiket


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
                continue
            if kurus and kurus.strip("0"):
                v.add("?"); continue
            v.add(f"{n:,}".replace(",", "."))
    elif tur in ("gun", "yuzde", "yil"):
        v |= {str(int(x)) for x in re.findall(r"(?<![\d.,/])(\d{1,3})(?![\d]|[.,]\d)", s)}
        if len(v) > 1:
            birim = {"gun": r"(\d{1,3})\s*(?:\([^)]*\)\s*)?gün", "yil": r"(\d{1,3})\s*(?:\([^)]*\)\s*)?(?:yıl|sene)",
                     "yuzde": r"%\s*(\d{1,3})|yüzde\s*(\d{1,3})|(\d{1,3})\s*%"}[tur]
            bv = {str(int(next(g for g in (m if isinstance(m, tuple) else (m,)) if g))) for m in re.findall(birim, s)}
            v = bv or v
    elif tur == "dosya":
        v |= {f"{y}/{int(n)}" for y, n in re.findall(r"(?<!\d)(\d{4})\s*/\s*(\d{1,6})(?!\d)", s)}
    elif tur == "il":
        v |= {tr_lower(il) for il in IL_GENIS if re.search(rf"(?<![a-zçğıöşü]){tr_lower(il)}", s)}
    return v


def norm(tur, d):
    return f"{d.split('/')[0]}/{int(d.split('/')[1])}" if tur == "dosya" else tr_lower(d) if tur == "il" else str(int(d)) if tur in ("gun", "yuzde", "yil") else d


def sinifla(tur, cevap, dogru, etiket, y):
    """→ (sınıf, karıştırma alt türü)."""
    s = tr_lower(re.sub(r"<think>.*?</think>", " ", cevap or "", flags=re.S).replace("**", " "))
    v = adaylar(tur, s)
    if len(v) == 1:
        x = v.pop()
        if x == norm(tur, dogru):
            return "dogru", None
        rol = {norm(tur, k): yt for k, yt in etiket.items()}.get(x)
        if rol is None:
            return "baska", None
        yy, t = rol
        return "karistirma", (t if yy == y and t != "hedef" else ("diger_hedef" if t == "hedef" else "diger_celdirici"))
    return ("yok_dedi" if not v and YOK.search(s) else "baska"), None


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
    ap.add_argument("--sablonlar", required=True, help="yayındaki sablonlar.json")
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--uc", required=True, help="OpenAI uyumlu chat/completions adresi")
    ap.add_argument("--model", required=True)
    ap.add_argument("--uzunluk", type=int, default=16000)
    ap.add_argument("--belge", type=int, default=1, help="şablon başına belge")
    ap.add_argument("--sablon", nargs="*", help="yalnız bu şablonlar (ör. s01 s08)")
    ap.add_argument("--duzen", choices=["sonda", "basta", "ikisi"], default="sonda")
    ap.add_argument("--tohum", type=int, default=1)
    a = ap.parse_args()
    spec = json.load(open(a.sablonlar, encoding="utf-8"))
    cel, h3 = spec["celdiriciler"]["sablonlar"], spec["hedef_v3"]
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
            metin, hedefler, etiket = belge_kur(kararlar, a.uzunluk, sab, cel[sab["id"]], h3["sablonlar"][sab["id"]], kokler, rng, h3["tanitim"])
            for y in YUVA:
                for bic in ("duz", "sade"):
                    soru = sab[bic].replace("{KOK}", hedefler[y][0])
                    istem = {"sonda": f"{TALIMAT}\n\n{metin}\n\nSoru: {soru}", "basta": f"{TALIMAT}\n\nSoru: {soru}\n\n{metin}",
                             "ikisi": f"{TALIMAT}\n\nSoru: {soru}\n\n{metin}\n\nSoru: {soru}"}[a.duzen]
                    cevap, pt = sor(a.uc, a.model, istem)
                    s, alt = sinifla(sab["tur"], cevap, hedefler[y][1], etiket, y)
                    sonuc.append({"sablon": sab["id"], "belge": n + 1, "yuva": y, "bicim": bic, "duzen": a.duzen, "sinif": s,
                                  "karistirma_alt": alt, "o200k": ntok(istem), "bildirilen_parca": pt})
                    print(sab["id"], n + 1, y, bic, s, alt or "", flush=True)
    with open(out / "sonuclar.jsonl", "w", encoding="utf-8") as fh:
        for r in sonuc:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for y in YUVA:
        rs = [r for r in sonuc if r["yuva"] == y]
        print(f"%{y}: doğruluk {sum(r['sinif'] == 'dogru' for r in rs) / max(len(rs), 1):.3f} (n={len(rs)})")
    print("sınıflar", dict(collections.Counter(r["sinif"] for r in sonuc)), "alt türler", dict(collections.Counter(r["karistirma_alt"] for r in sonuc if r["karistirma_alt"])))


if __name__ == "__main__":
    main()
