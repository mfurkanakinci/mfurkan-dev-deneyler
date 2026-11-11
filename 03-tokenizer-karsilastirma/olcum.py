"""Tokenizer karşılaştırması: örnekleme + ölçüm + bootstrap (2026-11-11, PLAN.md ön kaydına göre).

Kullanım:
  python olcum.py --asama deneme --girdi DIR --cikti DIR --onbellek DIR
  python olcum.py --asama asil --sinirlar S1,S2 --girdi DIR --cikti DIR --onbellek DIR

--girdi klasörü şunları içerir (JSON Lines, satır başına bir kayıt):
  mevzuat.jsonl      {"id", "law", "kind", "num", "letter", "heading", "text"}   yürürlükteki kanun maddeleri
  karar_aday.jsonl   {"id", "h", "paras": [gerekçe paragrafları], "gaps"}       karar adayları (h = sha256(tohum|id))
  karar_kunye.jsonl  {"id", "kurum", "role", "group"}                          mahkeme türü ve kopya grubu
Bu dosyalar özel bir veritabanından çıkarıldı ve yayımlanmıyor; karar metinleri paylaşılmaz.
Vikipedi dökümü HF'den sabit sürümle iner. Yalnız tokenizer dosyaları indirilir; model ağırlığı indirilmez.
Ekrana metin basılmaz. Deneme aşamasında tokenizer sonuçları dosyaya yazılır, ekrana yalnız uzunluklar ve sınırlar basılır.
"""
import argparse, csv, hashlib, json, os, platform, re, sys, time, unicodedata, warnings
from itertools import combinations

import numpy as np

TOHUM = "tokkiyas-20261111"
BOOT_TOHUM = 20261111
BOOT_N = 10000
ALT_SINIR = 200
KOTALAR = (34, 33, 33)
DENEME_N = 10
SIGMA = (512, 2048, 8192)
TURLER = ("vikipedi", "mevzuat", "karar")
HF_TOK = {
    "BERTurk": ("dbmdz/bert-base-turkish-cased", "b6e1de16c983e0f2c70664591ea3f22810072608"),
    "ModernBERT-tr": ("ytu-ce-cosmos/modernbert-tr-base", "d16b9da8f7dc0eadf8946255ee5f38042bdf59c2"),
    "BGE-M3": ("BAAI/bge-m3", "5617a9f61b028005a4858fdac845db406aefb181"),
    "Qwen3": ("Qwen/Qwen3-Embedding-0.6B", "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3"),
}
TT_TOK = {"cl100k": "cl100k_base", "o200k": "o200k_base"}
TOK_SIRA = ["BERTurk", "ModernBERT-tr", "BGE-M3", "Qwen3", "cl100k", "o200k"]
IZIN = ["tokenizer*", "vocab*", "merges*", "special_tokens_map.json", "tokenizer_config.json", "config.json",
        "*.model", "added_tokens.json"]
YASAK = ["*.safetensors", "*.bin", "*.pt", "*.pth", "*.onnx", "*.gguf", "*.h5", "*.msgpack", "*.ckpt"]
WIKI = ("wikimedia/wikipedia", "b04c8d1ceb2f5cd4588862100d08de323dccfbaa",
        ["20231101.tr/train-00000-of-00002.parquet", "20231101.tr/train-00001-of-00002.parquet"])
KV_KALIP = [re.compile(r"\b\d{11}\b"), re.compile(r"TR\d{2}[ \d]{20,}"), re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
            re.compile(r"0?5\d{2} ?\d{3} ?\d{2} ?\d{2}")]


def ozet(kimlik):
    return hashlib.sha256(f"{TOHUM}|{kimlik}".encode("utf-8")).hexdigest()


def sha_dosya(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nfc(s):
    return unicodedata.normalize("NFC", s).strip()


def tr_kucuk(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


def norm_ozet(s):
    return hashlib.sha256("".join(c for c in tr_kucuk(unicodedata.normalize("NFC", s)) if c.isalnum()).encode()).hexdigest()


# ---------------------------------------------------------------- adaylar
def aday_vikipedi(onbellek):
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq
    yollar, shalar = [], {}
    for fn in WIKI[2]:
        p = hf_hub_download(WIKI[0], fn, repo_type="dataset", revision=WIKI[1], cache_dir=onbellek)
        yollar.append(p); shalar[fn] = sha_dosya(p)
    ids, basliklar, metin_yer = [], [], []
    for fi, p in enumerate(yollar):
        t = pq.read_table(p, columns=["id", "title"])
        for j, (i, b) in enumerate(zip(t.column("id").to_pylist(), t.column("title").to_pylist())):
            ids.append(i); basliklar.append(b); metin_yer.append((fi, j))
    sira = sorted(range(len(ids)), key=lambda k: ozet(ids[k]))
    tablolar = {}

    def metin(k):
        fi, j = metin_yer[k]
        if fi not in tablolar:
            tablolar[fi] = pq.read_table(yollar[fi], columns=["text"]).column("text")
        return tablolar[fi][j].as_py()

    def gen():
        for k in sira:
            b = basliklar[k]
            if "(anlam ayrımı)" in b:
                yield {"durum": "anlam_ayrimi"}; continue
            yield {"id": str(ids[k]), "metin": nfc(metin(k)), "ek": {"sayfa_id": str(ids[k]), "baslik": b}}
    bilgi = {"depo": WIKI[0], "surum": WIKI[1], "yapilandirma": "20231101.tr", "dosya_sha256": shalar,
             "sayfa_sayisi": len(ids), "lisans": "CC BY-SA 4.0 (ve GFDL)"}
    return gen(), bilgi


def aday_mevzuat(girdi):
    rows = [json.loads(l) for l in open(f"{girdi}/mevzuat.jsonl", encoding="utf-8")]
    rows.sort(key=lambda r: ozet(r["id"]))

    def gen():
        for r in rows:
            m = (r["heading"] + "\n" + r["text"]) if r.get("heading") else (r["text"] or "")
            yield {"id": str(r["id"]), "metin": nfc(m),
                   "ek": {"kanun_no": r["law"], "tur": r["kind"], "madde_no": r["num"], "harf": r.get("letter") or ""}}
    return gen(), {"evren": len(rows), "dosya_sha256": sha_dosya(f"{girdi}/mevzuat.jsonl")}


def aday_karar(girdi):
    kunye = {}
    for l in open(f"{girdi}/karar_kunye.jsonl", encoding="utf-8"):
        r = json.loads(l); kunye[r["id"]] = r
    rows = [json.loads(l) for l in open(f"{girdi}/karar_aday.jsonl", encoding="utf-8")]
    rows.sort(key=lambda r: ozet(r["id"]))
    assert all(r["h"] == ozet(r["id"]) for r in rows), "PG özeti ile Python özeti uyuşmuyor"
    gorulen_grup = set()

    def gen():
        for r in rows:
            k = kunye.get(r["id"], {})
            if k.get("role") == "alias":
                yield {"durum": "alias"}; continue
            g = k.get("group")
            if g:
                if g in gorulen_grup:
                    yield {"durum": "ayni_grup"}; continue
                gorulen_grup.add(g)
            m = nfc("\n".join(p or "" for p in (r["paras"] or [])))
            if any(p.search(m) for p in KV_KALIP):
                yield {"durum": "kisisel_veri_kalibi"}; continue
            yield {"id": r["id"], "metin": m, "ek": {"mahkeme_turu": k.get("kurum") or "bilinmiyor",
                                                     "paragraf_bosluk": r.get("gaps")}}
    return gen(), {"aday": len(rows), "dosya_sha256": {n: sha_dosya(f"{girdi}/{n}") for n in ("karar_aday.jsonl", "karar_kunye.jsonl")}}


# ---------------------------------------------------------------- örnekleme
class Secici:
    def __init__(self):
        self.tam, self.norm = set(), set()

    def kopya_mi(self, m):
        a, b = hashlib.sha256(m.encode()).hexdigest(), norm_ozet(m)
        if a in self.tam or b in self.norm:
            return True
        self.tam.add(a); self.norm.add(b)
        return False


def aralik(n, s1, s2):
    return "A" if n < s1 else ("B" if n < s2 else "C")


def _uygun(gen, secici, sayac):
    for d in gen:
        if "durum" in d:
            sayac[d["durum"]] = sayac.get(d["durum"], 0) + 1; continue
        if len(d["metin"]) < ALT_SINIR:
            sayac["kisa"] = sayac.get("kisa", 0) + 1; continue
        if secici.kopya_mi(d["metin"]):
            sayac["kopya"] = sayac.get("kopya", 0) + 1; continue
        yield d


def sec_deneme(uygun):
    """Deneme: özet sırasıyla ilk DENEME_N uygun belge."""
    out = []
    for d in uygun:
        d["rol"] = "deneme"; out.append(d)
        if len(out) == DENEME_N:
            break
    return out


KOMSU = {"A": ("B",), "B": ("A", "C"), "C": ("B",)}


def sec_asil(uygun, sinirlar, evren_tam):
    """Asıl: denemeden sonraki uygun belgeler sırayla; aralık kotası doluysa atlanır."""
    asil, artik = [], []
    dolu = {"A": 0, "B": 0, "C": 0}
    kota = dict(zip("ABC", KOTALAR))
    for d in uygun:
        a = aralik(len(d["metin"]), *sinirlar)
        if dolu[a] < kota[a]:
            d["rol"] = "asil"; d["aralik"] = a; dolu[a] += 1; asil.append(d)
            if sum(dolu.values()) == sum(KOTALAR):
                break
        else:
            artik.append(d)
    eksik = {a: kota[a] - dolu[a] for a in "ABC" if dolu[a] < kota[a]}
    if eksik and not evren_tam:
        print("DERINLIK_YETMEDI", json.dumps(eksik), flush=True)
        sys.exit(3)
    for a, n in eksik.items():  # PLAN: evren bitti; eksik sayı komşu aralıktan özet sırasıyla
        for d in [d for d in artik if aralik(len(d["metin"]), *sinirlar) in KOMSU[a] and "rol" not in d][:n]:
            d["rol"] = "asil"; d["aralik"] = aralik(len(d["metin"]), *sinirlar) + "*"; asil.append(d)
    return asil, {"dolu": dolu, "eksik": eksik}


# ---------------------------------------------------------------- tokenizer'lar
def tokenizerlari_yukle(onbellek):
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer
    from transformers.utils import logging as tl
    tl.set_verbosity_error()
    import tiktoken
    toks, bilgi = {}, {}
    for ad, (depo, surum) in HF_TOK.items():
        yol = snapshot_download(depo, revision=surum, allow_patterns=IZIN, ignore_patterns=YASAK, cache_dir=onbellek)
        dosyalar = sorted(os.path.relpath(os.path.join(r, f), yol) for r, _, fs in os.walk(yol) for f in fs)
        assert not any(re.search(r"\.(safetensors|bin|pt|pth|onnx|gguf|h5|msgpack|ckpt)$", f) for f in dosyalar), dosyalar
        tok = AutoTokenizer.from_pretrained(yol)
        toks[ad] = ("hf", tok)
        bilgi[ad] = {"depo": depo, "surum": surum, "sinif": type(tok).__name__,
                     "dosyalar": {f: sha_dosya(os.path.join(yol, f)) for f in dosyalar},
                     "sozluk": len(tok), "unk_token": tok.unk_token, "unk_token_id": tok.unk_token_id,
                     "clean_up_tokenization_spaces_varsayilan": getattr(tok, "clean_up_tokenization_spaces", None),
                     "kullanilan_decode": "skip_special_tokens=False, clean_up_tokenization_spaces=False"}
    for ad, kod in TT_TOK.items():
        enc = tiktoken.get_encoding(kod)
        toks[ad] = ("tt", enc)
        cdir = os.environ["TIKTOKEN_CACHE_DIR"]
        bilgi[ad] = {"kodlama": kod, "sozluk": enc.n_vocab, "unk_token": None,
                     "onbellek_dosyalari_sha256": {f: sha_dosya(os.path.join(cdir, f)) for f in sorted(os.listdir(cdir))},
                     "kullanilan_encode": "encode(x, disallowed_special=())"}
    return toks, bilgi


def kodla(tur_tok, x):
    tur, t = tur_tok
    if tur == "hf":
        ids = t(x, add_special_tokens=False, truncation=False)["input_ids"]
        geri = t.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
        unk = sum(1 for i in ids if t.unk_token_id is not None and i == t.unk_token_id)
        unk_s = t.unk_token
    else:
        ids = t.encode(x, disallowed_special=())
        geri = t.decode(ids)
        unk, unk_s = 0, None
    return ids, geri, unk, unk_s


def bosluksuz(s):
    return "".join(s.split())


def fark_turu(x, geri, unk_s):
    if geri == x:
        return ""
    if bosluksuz(geri) == bosluksuz(x):
        return "bosluk"
    if (unk_s and unk_s in geri) or "\ufffd" in geri:
        return "taninmayan"
    return "harf"


def parcalar(tur_tok, ids):
    tur, t = tur_tok
    if tur == "hf":
        return t.convert_ids_to_tokens(ids)
    out = []
    for i in ids:
        b = t.decode_single_token_bytes(i)
        try:
            out.append(b.decode("utf-8"))
        except UnicodeDecodeError:
            out.append("".join(f"<0x{c:02X}>" for c in b))
    return out


def olc(belgeler, toks):
    for d in belgeler:
        x = d["metin"]
        d["karakter"] = len(x); d["birim"] = len(x.split())
        d["olcu"] = {}
        for ad in TOK_SIRA:
            ids, geri, unk, unk_s = kodla(toks[ad], x)
            d["olcu"][ad] = {"parca": len(ids), "unk": unk, "geri": geri == x, "fark": fark_turu(x, geri, unk_s)}


# ---------------------------------------------------------------- özet ve bootstrap
def dizi(belgeler, ad, olcu):
    if olcu == "p1k":
        return np.array([d["olcu"][ad]["parca"] / d["karakter"] * 1000 for d in belgeler])
    if olcu == "pbirim":
        return np.array([d["olcu"][ad]["parca"] / max(d["birim"], 1) for d in belgeler])
    if olcu == "geri":
        return np.array([1.0 if d["olcu"][ad]["geri"] else 0.0 for d in belgeler])
    if olcu.startswith("asim"):
        s = int(olcu[4:])
        return np.array([1.0 if d["olcu"][ad]["parca"] > s else 0.0 for d in belgeler])
    raise ValueError(olcu)


def betimle(belgeler):
    out = {"n": len(belgeler), "karakter_toplam": int(sum(d["karakter"] for d in belgeler)),
           "birim_toplam": int(sum(d["birim"] for d in belgeler)),
           "karakter_ortanca": float(np.median([d["karakter"] for d in belgeler])), "tokenizer": {}}
    for ad in TOK_SIRA:
        p1k, pb = dizi(belgeler, ad, "p1k"), dizi(belgeler, ad, "pbirim")
        top = sum(d["olcu"][ad]["parca"] for d in belgeler)
        farklar = {}
        for d in belgeler:
            f = d["olcu"][ad]["fark"]
            if f:
                farklar[f] = farklar.get(f, 0) + 1
        out["tokenizer"][ad] = {
            "parca_toplam": int(top),
            "p1k": {"ortalama": float(p1k.mean()), "ortanca": float(np.median(p1k)), "y95": float(np.percentile(p1k, 95)),
                    "toplam_oran": top / out["karakter_toplam"] * 1000},
            "parca_birim": {"ortalama": float(pb.mean()), "ortanca": float(np.median(pb)), "y95": float(np.percentile(pb, 95)),
                            "toplam_oran": top / out["birim_toplam"]},
            "sadakat": {"birebir_oran": float(dizi(belgeler, ad, "geri").mean()), "fark_turu": farklar,
                        "unk_toplam": int(sum(d["olcu"][ad]["unk"] for d in belgeler)),
                        "unk_belge": int(sum(1 for d in belgeler if d["olcu"][ad]["unk"] > 0))},
            "sigma": {f"asan_{s}": float(dizi(belgeler, ad, f"asim{s}").mean()) for s in SIGMA},
        }
    return out


def bootstrap(gruplar):
    """gruplar: {tür: belgeler}. Eşli, belge düzeyinde; toplam türler içinde katmanlı."""
    rng = np.random.default_rng(BOOT_TOHUM)
    idx = {t: rng.integers(0, len(gruplar[t]), size=(BOOT_N, len(gruplar[t]))) for t in TURLER}
    olculer = ["p1k", "geri", "asim512"]
    sonuc = {}
    for g in list(TURLER) + ["toplam"]:
        tg = TURLER if g == "toplam" else (g,)
        dag = {}
        for ad in TOK_SIRA:
            for o in olculer:
                parts = []
                for t in tg:
                    v = dizi(gruplar[t], ad, o)
                    parts.append(v[idx[t]])  # BOOT_N x n_t
                m = np.concatenate(parts, axis=1).mean(axis=1)
                nokta = float(np.concatenate([dizi(gruplar[t], ad, o) for t in tg]).mean())
                dag[(ad, o)] = (nokta, m)
        tek = {ad: {o: {"deger": dag[(ad, o)][0], "a95": [float(np.percentile(dag[(ad, o)][1], 2.5)),
                                                          float(np.percentile(dag[(ad, o)][1], 97.5))]} for o in olculer}
               for ad in TOK_SIRA}
        cift = []
        for a, b in combinations(TOK_SIRA, 2):
            r = {"a": a, "b": b}
            for o in olculer:
                f = dag[(a, o)][1] - dag[(b, o)][1]
                lo, hi = float(np.percentile(f, 2.5)), float(np.percentile(f, 97.5))
                r[o] = {"fark": dag[(a, o)][0] - dag[(b, o)][0], "a95": [lo, hi], "sifir_icinde": bool(lo <= 0 <= hi)}
            cift.append(r)
        sonuc[g] = {"tek": tek, "cift": cift}
    return {"tekrar": BOOT_N, "tohum": BOOT_TOHUM, "yontem": "eşli belge düzeyi, yüzdelik %95; toplam tür içinde katmanlı",
            "olculer": {"p1k": "ortalama parça/1.000 karakter", "geri": "birebir geri verme oranı",
                        "asim512": "512 parçayı aşan belge oranı"}, "gruplar": sonuc}


def kontrol(toks, kpath):
    k = json.load(open(kpath, encoding="utf-8"))
    out = []
    for o in k["ogeler"]:
        x = unicodedata.normalize("NFC", o["metin"])
        r = {"id": o["id"], "grup": o["grup"], "metin": x, "tokenizer": {}}
        for ad in TOK_SIRA:
            ids, geri, unk, unk_s = kodla(toks[ad], x)
            r["tokenizer"][ad] = {"parca_sayisi": len(ids), "parcalar": parcalar(toks[ad], ids), "geri": geri,
                                  "birebir": geri == x, "fark": fark_turu(x, geri, unk_s), "unk": unk}
        out.append(r)
    return out


def kontrol_md(kc):
    esc = lambda s: s.replace("|", "\\|").replace("\n", "⏎").replace("\t", "⇥")
    L = ["# Kontrol kümesi çıktısı", "", "Elle yazılmış kısa öğeler. Hücre: parça sayısı; ✓ birebir geri verdi, ✗ vermedi (fark türü).", "",
         "| öğe | metin | " + " | ".join(TOK_SIRA) + " |", "|---|---|" + "---|" * len(TOK_SIRA)]
    for r in kc:
        hs = []
        for ad in TOK_SIRA:
            t = r["tokenizer"][ad]
            hs.append(f"{t['parca_sayisi']} " + ("✓" if t["birebir"] else f"✗ ({t['fark']})"))
        L.append(f"| {r['id']} | {esc(r['metin'])} | " + " | ".join(hs) + " |")
    L += ["", "## Parçalar ve geri çözülen metin", ""]
    for r in kc:
        L.append(f"### {r['id']} ({r['grup']}): `{esc(r['metin'])}`"); L.append("")
        L.append("| tokenizer | parçalar | geri çözülen |"); L.append("|---|---|---|")
        for ad in TOK_SIRA:
            t = r["tokenizer"][ad]
            L.append(f"| {ad} | {esc(' · '.join(t['parcalar']))} | {esc(t['geri'])} |")
        L.append("")
    return "\n".join(L) + "\n"


def surumler():
    import importlib.metadata as md
    v = {"python": sys.version.split()[0], "platform": platform.platform(), "islemci": platform.processor() or platform.machine(),
         "cpu_sayisi": os.cpu_count()}
    for p in ("transformers", "tokenizers", "tiktoken", "huggingface_hub", "numpy", "pyarrow", "sentencepiece", "protobuf"):
        try:
            v[p] = md.version(p)
        except Exception:
            v[p] = None
    return v


def yaz_csv(path, belgeler, ic_kimlik=True):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        bas = ["belge_kimligi", "tur", "rol", "aralik", "karakter", "birim"]
        for ad in TOK_SIRA:
            bas += [f"parca_{ad}", f"birebir_{ad}", f"fark_{ad}", f"unk_{ad}"]
        w.writerow(bas)
        for d in belgeler:
            row = [d["id"], d["tur"], d["rol"], d.get("aralik", ""), d["karakter"], d["birim"]]
            for ad in TOK_SIRA:
                o = d["olcu"][ad]
                row += [o["parca"], int(o["geri"]), o["fark"], o["unk"]]
            w.writerow(row)


def yaz_belge_listesi(path, belgeler):
    """Yayın listesi: metin yok; karar için yalnız sıra, mahkeme türü, karakter."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sira", "tur", "aralik", "karakter", "vikipedi_sayfa_id", "vikipedi_baslik", "kanun_no", "madde_turu",
                    "madde_no", "madde_harf", "mahkeme_turu"])
        for i, d in enumerate(belgeler, 1):
            e = d["ek"]
            if d["tur"] == "vikipedi":
                w.writerow([i, d["tur"], d.get("aralik", ""), d["karakter"], e["sayfa_id"], e["baslik"], "", "", "", "", ""])
            elif d["tur"] == "mevzuat":
                w.writerow([i, d["tur"], d.get("aralik", ""), d["karakter"], "", "", e["kanun_no"], e["tur"], e["madde_no"], e["harf"], ""])
            else:
                w.writerow([i, d["tur"], "", d["karakter"], "", "", "", "", "", "", e["mahkeme_turu"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asama", choices=["deneme", "asil"], required=True)
    ap.add_argument("--sinirlar", default=None)
    ap.add_argument("--girdi", required=True)
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--onbellek", required=True)
    ap.add_argument("--kontrol", default=None)
    a = ap.parse_args()
    warnings.filterwarnings("ignore")
    os.makedirs(a.cikti, exist_ok=True)
    os.environ.setdefault("TIKTOKEN_CACHE_DIR", os.path.join(a.onbellek, "tiktoken"))
    os.makedirs(os.environ["TIKTOKEN_CACHE_DIR"], exist_ok=True)
    t0 = time.time()
    sinirlar = tuple(int(x) for x in a.sinirlar.split(",")) if a.asama == "asil" else None
    secici = Secici()
    gens = {}
    kaynak = {}
    gens["vikipedi"], kaynak["vikipedi"] = aday_vikipedi(a.onbellek)
    gens["mevzuat"], kaynak["mevzuat"] = aday_mevzuat(a.girdi)
    gens["karar"], kaynak["karar"] = aday_karar(a.girdi)
    deneme, asil, secim, uygun, sayac = {}, {}, {}, {}, {}
    for t in TURLER:  # önce bütün türlerin denemesi, sonra asıl örneklem (kopya denetimi türler arası)
        sayac[t] = {}
        uygun[t] = _uygun(gens[t], secici, sayac[t])
        deneme[t] = sec_deneme(uygun[t])
        for d in deneme[t]:
            d["tur"] = t
    for t in TURLER:
        bilgi = {}
        if sinirlar is not None:
            asil[t], bilgi = sec_asil(uygun[t], sinirlar, evren_tam=(t != "karar"))
            for d in asil[t]:
                d["tur"] = t
        secim[t] = {"atlanan": sayac[t], **bilgi, "deneme": len(deneme[t]), "asil": len(asil.get(t, []))}
    uz = {t: [len(d["metin"]) for d in deneme[t]] for t in TURLER}
    hepsi = sorted(sum(uz.values(), []))
    q = np.quantile(np.array(hepsi), [1 / 3, 2 / 3], method="linear")
    oneri = [int(round(v / 100.0)) * 100 for v in q]
    toks, tbilgi = tokenizerlari_yukle(a.onbellek)
    bel_d = sum((deneme[t] for t in TURLER), [])
    olc(bel_d, toks)
    yaz_csv(f"{a.cikti}/deneme_belgeler.csv", bel_d)
    bosluk = [d["ek"].get("paragraf_bosluk") for d in deneme["karar"]]
    json.dump({"deneme_uzunluklari": uz, "quantile_1_3_2_3": [float(v) for v in q], "sinir_onerisi": oneri,
               "karar_paragraf_bosluklari": bosluk, "secim": secim},
              open(f"{a.cikti}/deneme.json", "w"), ensure_ascii=False, indent=1)
    print("DENEME_UZUNLUK", json.dumps(uz), "SINIR", oneri, flush=True)
    if a.asama == "deneme":
        print("DENEME_BITTI", round(time.time() - t0, 1), "sn", flush=True)
        return
    bel = sum((asil[t] for t in TURLER), [])
    olc(bel, toks)
    gruplar = {t: asil[t] for t in TURLER}
    betim = {g: betimle(gruplar[g]) for g in TURLER}
    betim["toplam"] = betimle(bel)
    boot = bootstrap(gruplar)
    kc = kontrol(toks, a.kontrol) if a.kontrol else None
    aralik_say = {t: {k: sum(1 for d in asil[t] if d["aralik"] == k) for k in sorted({d["aralik"] for d in asil[t]})} for t in TURLER}
    ozet_json = {
        "deney": "2026-11-11-tokenizer-kiyas", "yazi": "https://mfurkan.dev/yazilar/tokenizer-karsilastirma/",
        "tarih": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "surumler": surumler(), "tokenizerlar": tbilgi,
        "ornekleme": {"tohum": TOHUM, "alt_sinir_karakter": ALT_SINIR, "sinirlar": list(sinirlar), "kotalar": list(KOTALAR),
                      "deneme_n": DENEME_N, "aralik_sayilari": aralik_say, "secim": secim, "kaynaklar": kaynak},
        "betimleyici": betim, "bootstrap": boot,
        "notlar": ["Metin NFC, baş/son boşluk atıldı; büyük/küçük harfe dokunulmadı.",
                   "HF: add_special_tokens=False, truncation=False; decode skip_special_tokens=False, clean_up_tokenization_spaces=False.",
                   "tiktoken: encode(x, disallowed_special=()); bayt düzeyi, unk yok (0 yapı gereği)."],
        "sure_sn": round(time.time() - t0, 1),
    }
    json.dump(ozet_json, open(f"{a.cikti}/ozet.json", "w"), ensure_ascii=False, indent=1)
    yaz_csv(f"{a.cikti}/belgeler.csv", bel)
    yaz_belge_listesi(f"{a.cikti}/belge_listesi.csv", bel)
    with open(f"{a.cikti}/secilen_kimlikler.json", "w") as f:
        json.dump({"karar": [d["id"] for d in asil["karar"] + deneme["karar"]],
                   "mevzuat_article_pk": [d["id"] for d in asil["mevzuat"] + deneme["mevzuat"]]}, f)
    if kc:
        json.dump(kc, open(f"{a.cikti}/kontrol_cikti.json", "w"), ensure_ascii=False, indent=1)
        open(f"{a.cikti}/kontrol_cikti.md", "w", encoding="utf-8").write(kontrol_md(kc))
    print("ASIL_BITTI", round(time.time() - t0, 1), "sn", "aralik", json.dumps(aralik_say), flush=True)


if __name__ == "__main__":
    main()
