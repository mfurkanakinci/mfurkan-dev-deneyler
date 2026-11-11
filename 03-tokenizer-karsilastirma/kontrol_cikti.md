# Kontrol kümesi çıktısı

Elle yazılmış kısa öğeler. Hücre: parça sayısı; ✓ birebir geri verdi, ✗ vermedi (fark türü).

| öğe | metin | BERTurk | ModernBERT-tr | BGE-M3 | Qwen3 | cl100k | o200k |
|---|---|---|---|---|---|---|---|
| k01 | çğıöşü ÇĞİÖŞÜ | 10 ✓ | 10 ✓ | 10 ✓ | 11 ✓ | 13 ✓ | 11 ✓ |
| k02 | I İ ı i | 4 ✓ | 4 ✓ | 5 ✓ | 5 ✓ | 5 ✓ | 5 ✓ |
| k03 | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul | 10 ✓ | 7 ✓ | 14 ✓ | 19 ✓ | 20 ✓ | 19 ✓ |
| k04 | KIRIK kırık KİRİŞ kiriş | 8 ✓ | 7 ✓ | 9 ✓ | 11 ✓ | 15 ✓ | 11 ✓ |
| k05 | Hâkim hakim; kâr kar; Kur'ân-ı Kerîm | 14 ✗ (bosluk) | 12 ✗ (bosluk) | 16 ✓ | 19 ✓ | 19 ✓ | 16 ✓ |
| k06 | TBK m. 344/1 | 8 ✗ (bosluk) | 8 ✗ (bosluk) | 7 ✓ | 10 ✓ | 8 ✓ | 8 ✓ |
| k07 | 6098 sayılı Türk Borçlar Kanunu'nun 344'üncü maddesinin birinci fıkrası | 16 ✗ (bosluk) | 15 ✗ (bosluk) | 20 ✓ | 28 ✓ | 29 ✓ | 25 ✓ |
| k08 | Geçici Madde 2 | 3 ✓ | 3 ✓ | 4 ✓ | 7 ✓ | 7 ✓ | 7 ✓ |
| k09 | HMK m. 107/1-a ve TMK md. 4 | 16 ✗ (bosluk) | 15 ✗ (bosluk) | 15 ✓ | 18 ✓ | 16 ✓ | 16 ✓ |
| k10 | 5237 s. TCK'nın 53/1-b maddesi | 13 ✗ (bosluk) | 13 ✗ (bosluk) | 13 ✓ | 19 ✓ | 16 ✓ | 14 ✓ |
| k11 | Ek Madde 3 – (Ek: 1/1/2020-7200/5 md.) | 20 ✗ (bosluk) | 20 ✗ (bosluk) | 17 ✓ | 27 ✓ | 23 ✓ | 23 ✓ |
| k12 | E. 2023/125, K. 2024/87 | 12 ✗ (bosluk) | 11 ✗ (bosluk) | 12 ✓ | 22 ✓ | 15 ✓ | 15 ✓ |
| k13 | Yargıtay 3. HD, 12.03.2024, E. 2023/1250 K. 2024/870 | 25 ✗ (bosluk) | 23 ✗ (bosluk) | 21 ✓ | 44 ✓ | 33 ✓ | 32 ✓ |
| k14 | AYM, B. No: 2019/12345, 15/6/2022 | 18 ✗ (bosluk) | 16 ✗ (bosluk) | 15 ✓ | 29 ✓ | 21 ✓ | 21 ✓ |
| k15 | 12.03.2024 tarihinde | 7 ✗ (bosluk) | 6 ✗ (bosluk) | 4 ✓ | 13 ✓ | 9 ✓ | 7 ✓ |
| k16 | 1 Ocak 2025 ile 31/12/2025 arası | 12 ✗ (bosluk) | 10 ✗ (bosluk) | 8 ✓ | 22 ✓ | 16 ✓ | 16 ✓ |
| k17 | %25 oranında, yüzde 12,5 faiz | 9 ✗ (bosluk) | 9 ✗ (bosluk) | 7 ✓ | 14 ✓ | 15 ✓ | 11 ✓ |
| k18 | 1.250.000,00 TL | 8 ✗ (bosluk) | 8 ✗ (bosluk) | 4 ✓ | 13 ✓ | 8 ✓ | 8 ✓ |
| k19 | ₺3.500,75 ve 2.000 USD | 11 ✗ (bosluk) | 11 ✗ (bosluk) | 10 ✓ | 17 ✓ | 13 ✓ | 13 ✓ |
| k20 | hükümsüzlüğünün | 3 ✓ | 3 ✓ | 4 ✓ | 8 ✓ | 10 ✓ | 7 ✓ |
| k21 | değerlendirilemeyeceğinden | 5 ✓ | 5 ✓ | 4 ✓ | 9 ✓ | 10 ✓ | 9 ✓ |
| k22 | sorumluluklarından kurtulamayacaklarını | 5 ✓ | 4 ✓ | 7 ✓ | 13 ✓ | 16 ✓ | 10 ✓ |
| k23 | Çekoslovakyalılaştıramadıklarımızdan mısınız | 9 ✓ | 8 ✓ | 13 ✓ | 18 ✓ | 20 ✓ | 18 ✓ |
| k24 | kiralayanın tahliye edilmesine karar verilmesine | 6 ✓ | 6 ✓ | 10 ✓ | 17 ✓ | 17 ✓ | 11 ✓ |
| k25 | Birinci satır.⏎⏎  İkinci satır⇥sekmeli. | 8 ✗ (bosluk) | 8 ✗ (bosluk) | 10 ✗ (bosluk) | 16 ✓ | 16 ✓ | 15 ✓ |
| k26 | “Tırnaklı” — uzun tire – kısa tire … üç nokta | 16 ✗ (bosluk) | 15 ✗ (bosluk) | 15 ✗ (harf) | 17 ✓ | 20 ✓ | 15 ✓ |

## Parçalar ve geri çözülen metin

### k01 (harf): `çğıöşü ÇĞİÖŞÜ`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | ç · ##ğı · ##ö · ##ş · ##ü · Ç · ##Ğİ · ##Ö · ##Ş · ##Ü | çğıöşü ÇĞİÖŞÜ |
| ModernBERT-tr | ç · ##ğı · ##ö · ##ş · ##ü · Ç · ##Ğİ · ##Ö · ##Ş · ##Ü | çğıöşü ÇĞİÖŞÜ |
| BGE-M3 | ▁ç · ğı · ö · şü · ▁Ç · Ğ · İ · Ö · Ş · Ü | çğıöşü ÇĞİÖŞÜ |
| Qwen3 | Ã§ · ÄŁÄ± · Ã¶ · ÅŁ · Ã¼ · ĠÃĩ · Äŀ · Ä° · Ãĸ · Åŀ · Ãľ | çğıöşü ÇĞİÖŞÜ |
| cl100k | ç · ğı · ö · ş · ü ·  Ç · <0xC4> · <0x9E> · İ · Ö · <0xC5> · <0x9E> · Ü | çğıöşü ÇĞİÖŞÜ |
| o200k | ç · ğı · ö · ş · ü ·  Ç · Ğ · İ · Ö · Ş · Ü | çğıöşü ÇĞİÖŞÜ |

### k02 (harf): `I İ ı i`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | I · İ · ı · i | I İ ı i |
| ModernBERT-tr | I · İ · ı · i | I İ ı i |
| BGE-M3 | ▁I · ▁İ · ▁ · ı · ▁i | I İ ı i |
| Qwen3 | I · ĠÄ° · Ġ · Ä± · Ġi | I İ ı i |
| cl100k | I ·  İ ·   · ı ·  i | I İ ı i |
| o200k | I ·  İ ·   · ı ·  i | I İ ı i |

### k03 (harf): `ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | IS · ##PA · ##R · ##TA · Isparta · ıspan · ##ak · İSTANBUL · İstanbul · istanbul | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul |
| ModernBERT-tr | ISP · ##ARTA · Isparta · ıspanak · İSTANBUL · İstanbul · istanbul | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul |
| BGE-M3 | ▁I · SP · ARTA · ▁Is · parta · ▁ · ı · span · ak · ▁İSTANBUL · ▁İstanbul · ▁ist · an · bul | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul |
| Qwen3 | IS · PART · A · ĠI · sp · arta · Ġ · Ä± · span · ak · ĠÄ° · ST · AN · B · UL · ĠÄ°stanbul · Ġist · an · bul | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul |
| cl100k | IS · PART · A ·  I · sp · arta ·   · ı · span · ak ·  İ · ST · AN · B · UL ·  İ · stanbul ·  ist · an · bul | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul |
| o200k | IS · PART · A ·  I · sp · arta ·   · ı · span · ak ·  İ · ST · AN · B · UL ·  İstanbul ·  ist · an · bul | ISPARTA Isparta ıspanak İSTANBUL İstanbul istanbul |

### k04 (harf): `KIRIK kırık KİRİŞ kiriş`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | KIR · ##IK · kırık · K · ##İR · ##İŞ · kir · ##iş | KIRIK kırık KİRİŞ kiriş |
| ModernBERT-tr | KIR · ##IK · kırık · KİR · ##İŞ · kir · ##iş | KIRIK kırık KİRİŞ kiriş |
| BGE-M3 | ▁KI · RIK · ▁kır · ık · ▁K · İR · İŞ · ▁kir · iş | KIRIK kırık KİRİŞ kiriş |
| Qwen3 | K · IR · IK · Ġk · Ä±r · Ä±k · ĠK · Ä°R · Ä°Åŀ · Ġk · iriÅŁ | KIRIK kırık KİRİŞ kiriş |
| cl100k | K · IR · IK ·  k · ır · ık ·  K · İ · R · İ · <0xC5> · <0x9E> ·  k · iri · ş | KIRIK kırık KİRİŞ kiriş |
| o200k | K · IR · IK ·  kır · ık ·  K · İR · İ · Ş ·  k · iriş | KIRIK kırık KİRİŞ kiriş |

### k05 (harf): `Hâkim hakim; kâr kar; Kur'ân-ı Kerîm`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | Hâ · ##kim · hakim · ; · kâr · kar · ; · Kur · ' · ân · - · ı · Ker · ##îm | Hâkim hakim ; kâr kar ; Kur ' ân - ı Kerîm |
| ModernBERT-tr | Hâkim · hakim · ; · kâr · kar · ; · Kur · ' · ân · - · ı · Kerîm | Hâkim hakim ; kâr kar ; Kur ' ân - ı Kerîm |
| BGE-M3 | ▁H · â · kim · ▁hakim · ; · ▁ · kâr · ▁kar · ; · ▁Kur · ' · ân · - · ı · ▁Ker · îm | Hâkim hakim; kâr kar; Kur'ân-ı Kerîm |
| Qwen3 | H · Ã¢ · kim · Ġhak · im · ; · Ġk · Ã¢ · r · Ġkar · ; · ĠKur · ' · Ã¢n · - · Ä± · ĠKer · Ã® · m | Hâkim hakim; kâr kar; Kur'ân-ı Kerîm |
| cl100k | H · â · kim ·  hak · im · ; ·  k · â · r ·  kar · ; ·  Kur · ' · ân · - · ı ·  Ker · î · m | Hâkim hakim; kâr kar; Kur'ân-ı Kerîm |
| o200k | H · â · kim ·  hakim · ; ·  k · âr ·  kar · ; ·  Kur · ' · ân · - · ı ·  Ker · îm | Hâkim hakim; kâr kar; Kur'ân-ı Kerîm |

### k06 (atif): `TBK m. 344/1`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | TB · ##K · m · . · 34 · ##4 · / · 1 | TBK m. 344 / 1 |
| ModernBERT-tr | TB · ##K · m · . · 34 · ##4 · / · 1 | TBK m. 344 / 1 |
| BGE-M3 | ▁T · BK · ▁m · . · ▁ · 344 · /1 | TBK m. 344/1 |
| Qwen3 | TB · K · Ġm · . · Ġ · 3 · 4 · 4 · / · 1 | TBK m. 344/1 |
| cl100k | TB · K ·  m · . ·   · 344 · / · 1 | TBK m. 344/1 |
| o200k | TB · K ·  m · . ·   · 344 · / · 1 | TBK m. 344/1 |

### k07 (atif): `6098 sayılı Türk Borçlar Kanunu'nun 344'üncü maddesinin birinci fıkrası`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | 60 · ##98 · sayılı · Türk · Borç · ##lar · Kanunu · ' · nun · 34 · ##4 · ' · üncü · maddesinin · birinci · fıkrası | 6098 sayılı Türk Borçlar Kanunu ' nun 344 ' üncü maddesinin birinci fıkrası |
| ModernBERT-tr | 60 · ##98 · sayılı · Türk · Borçlar · Kanunu · ' · nun · 34 · ##4 · ' · üncü · maddesinin · birinci · fıkrası | 6098 sayılı Türk Borçlar Kanunu ' nun 344 ' üncü maddesinin birinci fıkrası |
| BGE-M3 | ▁60 · 98 · ▁sayılı · ▁Türk · ▁Bor · ç · lar · ▁Kanunu · ' · nun · ▁ · 344 · ' · üncü · ▁maddesi · nin · ▁birinci · ▁fı · k · rası | 6098 sayılı Türk Borçlar Kanunu'nun 344'üncü maddesinin birinci fıkrası |
| Qwen3 | 6 · 0 · 9 · 8 · ĠsayÄ±lÄ± · ĠTÃ¼rk · ĠBor · Ã§ · lar · ĠKan · unu · 'n · un · Ġ · 3 · 4 · 4 · ' · Ã¼ncÃ¼ · Ġm · add · es · inin · Ġbir · inci · ĠfÄ± · kr · asÄ± | 6098 sayılı Türk Borçlar Kanunu'nun 344'üncü maddesinin birinci fıkrası |
| cl100k | 609 · 8 ·  say · ılı ·  Tür · k ·  Bor · ç · lar ·  Kan · unu · 'n · un ·   · 344 · ' · ü · nc · ü ·  m · add · es · inin ·  bir · inci ·  f · ı · kr · ası | 6098 sayılı Türk Borçlar Kanunu'nun 344'üncü maddesinin birinci fıkrası |
| o200k | 609 · 8 ·  say · ılı ·  Türk ·  Bor · ç · lar ·  Kan · unu · 'n · un ·   · 344 · ' · ün · cü ·  madd · es · inin ·  bir · inci ·  f · ık · rası | 6098 sayılı Türk Borçlar Kanunu'nun 344'üncü maddesinin birinci fıkrası |

### k08 (atif): `Geçici Madde 2`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | Geçici · Madde · 2 | Geçici Madde 2 |
| ModernBERT-tr | Geçici · Madde · 2 | Geçici Madde 2 |
| BGE-M3 | ▁Geç · ici · ▁Madde · ▁2 | Geçici Madde 2 |
| Qwen3 | Ge · Ã§ · ici · ĠMad · de · Ġ · 2 | Geçici Madde 2 |
| cl100k | Ge · ç · ici ·  Mad · de ·   · 2 | Geçici Madde 2 |
| o200k | Ge · ç · ici ·  Mad · de ·   · 2 | Geçici Madde 2 |

### k09 (atif): `HMK m. 107/1-a ve TMK md. 4`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | H · ##M · ##K · m · . · 107 · / · 1 · - · a · ve · TM · ##K · md · . · 4 | HMK m. 107 / 1 - a ve TMK md. 4 |
| ModernBERT-tr | HM · ##K · m · . · 107 · / · 1 · - · a · ve · TM · ##K · md · . · 4 | HMK m. 107 / 1 - a ve TMK md. 4 |
| BGE-M3 | ▁H · MK · ▁m · . · ▁107 · /1 · - · a · ▁ve · ▁T · MK · ▁m · d · . · ▁4 | HMK m. 107/1-a ve TMK md. 4 |
| Qwen3 | H · MK · Ġm · . · Ġ · 1 · 0 · 7 · / · 1 · -a · Ġve · ĠTM · K · Ġmd · . · Ġ · 4 | HMK m. 107/1-a ve TMK md. 4 |
| cl100k | H · MK ·  m · . ·   · 107 · / · 1 · -a ·  ve ·  TM · K ·  md · . ·   · 4 | HMK m. 107/1-a ve TMK md. 4 |
| o200k | HM · K ·  m · . ·   · 107 · / · 1 · -a ·  ve ·  TM · K ·  md · . ·   · 4 | HMK m. 107/1-a ve TMK md. 4 |

### k10 (atif): `5237 s. TCK'nın 53/1-b maddesi`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | 52 · ##37 · s · . · TCK · ' · nın · 53 · / · 1 · - · b · maddesi | 5237 s. TCK ' nın 53 / 1 - b maddesi |
| ModernBERT-tr | 52 · ##37 · s · . · TCK · ' · nın · 53 · / · 1 · - · b · maddesi | 5237 s. TCK ' nın 53 / 1 - b maddesi |
| BGE-M3 | ▁52 · 37 · ▁s · . · ▁T · CK · ' · nın · ▁53 · /1 · - · b · ▁maddesi | 5237 s. TCK'nın 53/1-b maddesi |
| Qwen3 | 5 · 2 · 3 · 7 · Ġs · . · ĠT · CK · 'n · Ä±n · Ġ · 5 · 3 · / · 1 · -b · Ġm · add · esi | 5237 s. TCK'nın 53/1-b maddesi |
| cl100k | 523 · 7 ·  s · . ·  T · CK · 'n · ın ·   · 53 · / · 1 · -b ·  m · add · esi | 5237 s. TCK'nın 53/1-b maddesi |
| o200k | 523 · 7 ·  s · . ·  T · CK · 'nın ·   · 53 · / · 1 · -b ·  madd · esi | 5237 s. TCK'nın 53/1-b maddesi |

### k11 (atif): `Ek Madde 3 – (Ek: 1/1/2020-7200/5 md.)`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | Ek · Madde · 3 · – · ( · Ek · : · 1 · / · 1 · / · 2020 · - · 720 · ##0 · / · 5 · md · . · ) | Ek Madde 3 – ( Ek : 1 / 1 / 2020 - 7200 / 5 md. ) |
| ModernBERT-tr | Ek · Madde · 3 · – · ( · Ek · : · 1 · / · 1 · / · 2020 · - · 720 · ##0 · / · 5 · md · . · ) | Ek Madde 3 – ( Ek : 1 / 1 / 2020 - 7200 / 5 md. ) |
| BGE-M3 | ▁Ek · ▁Madde · ▁3 · ▁– · ▁( · Ek · : · ▁1/1 · / · 2020 · -7 · 200 · /5 · ▁m · d · . · ) | Ek Madde 3 – (Ek: 1/1/2020-7200/5 md.) |
| Qwen3 | Ek · ĠMad · de · Ġ · 3 · ĠâĢĵ · Ġ( · Ek · : · Ġ · 1 · / · 1 · / · 2 · 0 · 2 · 0 · - · 7 · 2 · 0 · 0 · / · 5 · Ġmd · .) | Ek Madde 3 – (Ek: 1/1/2020-7200/5 md.) |
| cl100k | Ek ·  Mad · de ·   · 3 ·  – ·  ( · Ek · : ·   · 1 · / · 1 · / · 202 · 0 · - · 720 · 0 · / · 5 ·  md · .) | Ek Madde 3 – (Ek: 1/1/2020-7200/5 md.) |
| o200k | Ek ·  Mad · de ·   · 3 ·  – ·  ( · Ek · : ·   · 1 · / · 1 · / · 202 · 0 · - · 720 · 0 · / · 5 ·  md · .) | Ek Madde 3 – (Ek: 1/1/2020-7200/5 md.) |

### k12 (kunye): `E. 2023/125, K. 2024/87`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | E · . · 2023 · / · 125 · , · K · . · 20 · ##24 · / · 87 | E. 2023 / 125, K. 2024 / 87 |
| ModernBERT-tr | E · . · 2023 · / · 125 · , · K · . · 2024 · / · 87 | E. 2023 / 125, K. 2024 / 87 |
| BGE-M3 | ▁E · . · ▁2023 · / · 125 · , · ▁K · . · ▁20 · 24 · / · 87 | E. 2023/125, K. 2024/87 |
| Qwen3 | E · . · Ġ · 2 · 0 · 2 · 3 · / · 1 · 2 · 5 · , · ĠK · . · Ġ · 2 · 0 · 2 · 4 · / · 8 · 7 | E. 2023/125, K. 2024/87 |
| cl100k | E · . ·   · 202 · 3 · / · 125 · , ·  K · . ·   · 202 · 4 · / · 87 | E. 2023/125, K. 2024/87 |
| o200k | E · . ·   · 202 · 3 · / · 125 · , ·  K · . ·   · 202 · 4 · / · 87 | E. 2023/125, K. 2024/87 |

### k13 (kunye): `Yargıtay 3. HD, 12.03.2024, E. 2023/1250 K. 2024/870`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | Yargıtay · 3 · . · HD · , · 12 · . · 03 · . · 20 · ##24 · , · E · . · 2023 · / · 125 · ##0 · K · . · 20 · ##24 · / · 87 · ##0 | Yargıtay 3. HD, 12. 03. 2024, E. 2023 / 1250 K. 2024 / 870 |
| ModernBERT-tr | Yargıtay · 3 · . · HD · , · 12 · . · 03 · . · 2024 · , · E · . · 2023 · / · 125 · ##0 · K · . · 2024 · / · 87 · ##0 | Yargıtay 3. HD, 12. 03. 2024, E. 2023 / 1250 K. 2024 / 870 |
| BGE-M3 | ▁Yar · gı · tay · ▁3. · ▁HD · , · ▁12. · 03.20 · 24 · , · ▁E · . · ▁2023 · /12 · 50 · ▁K · . · ▁20 · 24 · / · 870 | Yargıtay 3. HD, 12.03.2024, E. 2023/1250 K. 2024/870 |
| Qwen3 | Y · arg · Ä±t · ay · Ġ · 3 · . · ĠHD · , · Ġ · 1 · 2 · . · 0 · 3 · . · 2 · 0 · 2 · 4 · , · ĠE · . · Ġ · 2 · 0 · 2 · 3 · / · 1 · 2 · 5 · 0 · ĠK · . · Ġ · 2 · 0 · 2 · 4 · / · 8 · 7 · 0 | Yargıtay 3. HD, 12.03.2024, E. 2023/1250 K. 2024/870 |
| cl100k | Y · arg · ı · t · ay ·   · 3 · . ·  HD · , ·   · 12 · . · 03 · . · 202 · 4 · , ·  E · . ·   · 202 · 3 · / · 125 · 0 ·  K · . ·   · 202 · 4 · / · 870 | Yargıtay 3. HD, 12.03.2024, E. 2023/1250 K. 2024/870 |
| o200k | Y · arg · ıt · ay ·   · 3 · . ·  HD · , ·   · 12 · . · 03 · . · 202 · 4 · , ·  E · . ·   · 202 · 3 · / · 125 · 0 ·  K · . ·   · 202 · 4 · / · 870 | Yargıtay 3. HD, 12.03.2024, E. 2023/1250 K. 2024/870 |

### k14 (kunye): `AYM, B. No: 2019/12345, 15/6/2022`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | AY · ##M · , · B · . · No · : · 2019 · / · 123 · ##45 · , · 15 · / · 6 · / · 20 · ##22 | AYM, B. No : 2019 / 12345, 15 / 6 / 2022 |
| ModernBERT-tr | AYM · , · B · . · No · : · 2019 · / · 123 · ##45 · , · 15 · / · 6 · / · 2022 | AYM, B. No : 2019 / 12345, 15 / 6 / 2022 |
| BGE-M3 | ▁A · YM · , · ▁B · . · ▁No · : · ▁2019 · /12 · 345 · , · ▁15 · /6 · / · 2022 | AYM, B. No: 2019/12345, 15/6/2022 |
| Qwen3 | AY · M · , · ĠB · . · ĠNo · : · Ġ · 2 · 0 · 1 · 9 · / · 1 · 2 · 3 · 4 · 5 · , · Ġ · 1 · 5 · / · 6 · / · 2 · 0 · 2 · 2 | AYM, B. No: 2019/12345, 15/6/2022 |
| cl100k | AY · M · , ·  B · . ·  No · : ·   · 201 · 9 · / · 123 · 45 · , ·   · 15 · / · 6 · / · 202 · 2 | AYM, B. No: 2019/12345, 15/6/2022 |
| o200k | AY · M · , ·  B · . ·  No · : ·   · 201 · 9 · / · 123 · 45 · , ·   · 15 · / · 6 · / · 202 · 2 | AYM, B. No: 2019/12345, 15/6/2022 |

### k15 (tarih_sayi): `12.03.2024 tarihinde`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | 12 · . · 03 · . · 20 · ##24 · tarihinde | 12. 03. 2024 tarihinde |
| ModernBERT-tr | 12 · . · 03 · . · 2024 · tarihinde | 12. 03. 2024 tarihinde |
| BGE-M3 | ▁12. · 03.20 · 24 · ▁tarihinde | 12.03.2024 tarihinde |
| Qwen3 | 1 · 2 · . · 0 · 3 · . · 2 · 0 · 2 · 4 · Ġt · arih · inde | 12.03.2024 tarihinde |
| cl100k | 12 · . · 03 · . · 202 · 4 ·  t · arih · inde | 12.03.2024 tarihinde |
| o200k | 12 · . · 03 · . · 202 · 4 ·  tarihinde | 12.03.2024 tarihinde |

### k16 (tarih_sayi): `1 Ocak 2025 ile 31/12/2025 arası`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | 1 · Ocak · 20 · ##25 · ile · 31 · / · 12 · / · 20 · ##25 · arası | 1 Ocak 2025 ile 31 / 12 / 2025 arası |
| ModernBERT-tr | 1 · Ocak · 2025 · ile · 31 · / · 12 · / · 2025 · arası | 1 Ocak 2025 ile 31 / 12 / 2025 arası |
| BGE-M3 | ▁1 · ▁Ocak · ▁2025 · ▁ile · ▁31 · /12/ · 2025 · ▁arası | 1 Ocak 2025 ile 31/12/2025 arası |
| Qwen3 | 1 · ĠOc · ak · Ġ · 2 · 0 · 2 · 5 · Ġile · Ġ · 3 · 1 · / · 1 · 2 · / · 2 · 0 · 2 · 5 · Ġar · asÄ± | 1 Ocak 2025 ile 31/12/2025 arası |
| cl100k | 1 ·  Oc · ak ·   · 202 · 5 ·  ile ·   · 31 · / · 12 · / · 202 · 5 ·  ar · ası | 1 Ocak 2025 ile 31/12/2025 arası |
| o200k | 1 ·  Oc · ak ·   · 202 · 5 ·  ile ·   · 31 · / · 12 · / · 202 · 5 ·  ar · ası | 1 Ocak 2025 ile 31/12/2025 arası |

### k17 (tarih_sayi): `%25 oranında, yüzde 12,5 faiz`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | % · 25 · oranında · , · yüzde · 12 · , · 5 · faiz | % 25 oranında, yüzde 12, 5 faiz |
| ModernBERT-tr | % · 25 · oranında · , · yüzde · 12 · , · 5 · faiz | % 25 oranında, yüzde 12, 5 faiz |
| BGE-M3 | ▁% · 25 · ▁oranında · , · ▁yüzde · ▁12,5 · ▁faiz | %25 oranında, yüzde 12,5 faiz |
| Qwen3 | % · 2 · 5 · Ġoran · Ä±nda · , · ĠyÃ¼zde · Ġ · 1 · 2 · , · 5 · Ġfa · iz | %25 oranında, yüzde 12,5 faiz |
| cl100k | % · 25 ·  or · an · ında · , ·  y · üz · de ·   · 12 · , · 5 ·  fa · iz | %25 oranında, yüzde 12,5 faiz |
| o200k | % · 25 ·  oran · ında · , ·  yüzde ·   · 12 · , · 5 ·  faiz | %25 oranında, yüzde 12,5 faiz |

### k18 (tarih_sayi): `1.250.000,00 TL`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | 1 · . · 250 · . · 000 · , · 00 · TL | 1. 250. 000, 00 TL |
| ModernBERT-tr | 1 · . · 250 · . · 000 · , · 00 · TL | 1. 250. 000, 00 TL |
| BGE-M3 | ▁1. · 25 · 0.000,00 · ▁TL | 1.250.000,00 TL |
| Qwen3 | 1 · . · 2 · 5 · 0 · . · 0 · 0 · 0 · , · 0 · 0 · ĠTL | 1.250.000,00 TL |
| cl100k | 1 · . · 250 · . · 000 · , · 00 ·  TL | 1.250.000,00 TL |
| o200k | 1 · . · 250 · . · 000 · , · 00 ·  TL | 1.250.000,00 TL |

### k19 (tarih_sayi): `₺3.500,75 ve 2.000 USD`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | ₺ · ##3 · . · 500 · , · 75 · ve · 2 · . · 000 · USD | ₺3. 500, 75 ve 2. 000 USD |
| ModernBERT-tr | ₺ · ##3 · . · 500 · , · 75 · ve · 2 · . · 000 · USD | ₺3. 500, 75 ve 2. 000 USD |
| BGE-M3 | ▁ · ₺ · 3 · . · 500 · , · 75 · ▁ve · ▁2.000 · ▁USD | ₺3.500,75 ve 2.000 USD |
| Qwen3 | âĤº · 3 · . · 5 · 0 · 0 · , · 7 · 5 · Ġve · Ġ · 2 · . · 0 · 0 · 0 · ĠUSD | ₺3.500,75 ve 2.000 USD |
| cl100k | <0xE2><0x82> · <0xBA> · 3 · . · 500 · , · 75 ·  ve ·   · 2 · . · 000 ·  USD | ₺3.500,75 ve 2.000 USD |
| o200k | <0xE2><0x82> · <0xBA> · 3 · . · 500 · , · 75 ·  ve ·   · 2 · . · 000 ·  USD | ₺3.500,75 ve 2.000 USD |

### k20 (uzun_ek): `hükümsüzlüğünün`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | hüküm · ##süz · ##lüğünün | hükümsüzlüğünün |
| ModernBERT-tr | hüküm · ##süz · ##lüğünün | hükümsüzlüğünün |
| BGE-M3 | ▁hüküm · süz · lüğünü · n | hükümsüzlüğünün |
| Qwen3 | h · Ã¼k · Ã¼ · ms · Ã¼ · zl · Ã¼ÄŁ · Ã¼nÃ¼n | hükümsüzlüğünün |
| cl100k | h · ük · ü · ms · ü · zl · ü · ğ · ün · ün | hükümsüzlüğünün |
| o200k | h · ük · ü · ms · üz · lüğ · ünün | hükümsüzlüğünün |

### k21 (uzun_ek): `değerlendirilemeyeceğinden`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | değerlendir · ##ile · ##meyeceği · ##nde · ##n | değerlendirilemeyeceğinden |
| ModernBERT-tr | değerlendir · ##ile · ##meyeceği · ##nde · ##n | değerlendirilemeyeceğinden |
| BGE-M3 | ▁değerlendiril · e · meyeceği · nden | değerlendirilemeyeceğinden |
| Qwen3 | de · ÄŁer · l · endir · ile · meye · ce · ÄŁ · inden | değerlendirilemeyeceğinden |
| cl100k | de · ğer · l · endir · ile · m · eye · ce · ğ · inden | değerlendirilemeyeceğinden |
| o200k | de · ğ · erl · endir · ile · meye · ce · ğ · inden | değerlendirilemeyeceğinden |

### k22 (uzun_ek): `sorumluluklarından kurtulamayacaklarını`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | sorumlulukları · ##ndan · kurtula · ##mayacak · ##larını | sorumluluklarından kurtulamayacaklarını |
| ModernBERT-tr | sorumlulukları · ##ndan · kurtula · ##mayacaklarını | sorumluluklarından kurtulamayacaklarını |
| BGE-M3 | ▁sorumluluk · larından · ▁kur · tul · a · mayacak · larını | sorumluluklarından kurtulamayacaklarını |
| Qwen3 | s · orum · l · ul · uk · larÄ±ndan · Ġk · urt · ul · am · ay · acak · larÄ±nÄ± | sorumluluklarından kurtulamayacaklarını |
| cl100k | s · orum · l · ul · uk · ları · nd · an ·  k · urt · ul · am · ay · acak · lar · ını | sorumluluklarından kurtulamayacaklarını |
| o200k | s · orum · l · uluk · larından ·  kurt · ul · amay · acak · larını | sorumluluklarından kurtulamayacaklarını |

### k23 (uzun_ek): `Çekoslovakyalılaştıramadıklarımızdan mısınız`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | Çek · ##os · ##lovak · ##yalı · ##laştır · ##amadı · ##k · ##larımızdan · mısınız | Çekoslovakyalılaştıramadıklarımızdan mısınız |
| ModernBERT-tr | Çek · ##os · ##lovak · ##yalı · ##laştır · ##amadık · ##larımızdan · mısınız | Çekoslovakyalılaştıramadıklarımızdan mısınız |
| BGE-M3 | ▁Çek · o · slova · ky · a · lı · laştı · rama · dıkları · mızda · n · ▁mı · sınız | Çekoslovakyalılaştıramadıklarımızdan mısınız |
| Qwen3 | Ãĩ · ek · os · lovak · yal · Ä± · la · ÅŁt · Ä± · ram · ad · Ä±kl · ar · Ä±mÄ±z · dan · Ġm · Ä±s · Ä±nÄ±z | Çekoslovakyalılaştıramadıklarımızdan mısınız |
| cl100k | Ç · ek · os · lovak · yal · ı · la · şt · ı · ram · ad · ıkl · ar · ım · ız · dan ·  m · ıs · ını · z | Çekoslovakyalılaştıramadıklarımızdan mısınız |
| o200k | Ç · ek · os · lov · ak · yal · ı · la · şt · ı · ram · ad · ık · larımız · dan ·  m · ıs · ınız | Çekoslovakyalılaştıramadıklarımızdan mısınız |

### k24 (uzun_ek): `kiralayanın tahliye edilmesine karar verilmesine`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | kiralaya · ##nın · tahliye · edilmesine · karar · verilmesine | kiralayanın tahliye edilmesine karar verilmesine |
| ModernBERT-tr | kirala · ##yanın · tahliye · edilmesine · karar · verilmesine | kiralayanın tahliye edilmesine karar verilmesine |
| BGE-M3 | ▁kira · la · yanın · ▁tah · liye · ▁edilmesi · ne · ▁karar · ▁verilmesi · ne | kiralayanın tahliye edilmesine karar verilmesine |
| Qwen3 | k · iral · ayan · Ä±n · Ġtah · li · ye · Ġed · il · mes · ine · Ġkar · ar · Ġver · il · mes · ine | kiralayanın tahliye edilmesine karar verilmesine |
| cl100k | k · iral · ayan · ın ·  tah · li · ye ·  ed · il · mes · ine ·  kar · ar ·  ver · il · mes · ine | kiralayanın tahliye edilmesine karar verilmesine |
| o200k | kir · al · ayan · ın ·  tah · liye ·  edil · mesine ·  karar ·  veril · mesine | kiralayanın tahliye edilmesine karar verilmesine |

### k25 (bicim): `Birinci satır.⏎⏎  İkinci satır⇥sekmeli.`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | Birinci · satır · . · İkinci · satır · sek · ##meli · . | Birinci satır. İkinci satır sekmeli. |
| ModernBERT-tr | Birinci · satır · . · İkinci · satır · sek · ##meli · . | Birinci satır. İkinci satır sekmeli. |
| BGE-M3 | ▁Birinci · ▁sa · tır · . · ▁İkinci · ▁sa · tır · ▁sek · meli · . | Birinci satır. İkinci satır sekmeli. |
| Qwen3 | B · ir · inci · Ġsat · Ä±r · .ĊĊ · Ġ · ĠÄ° · k · inci · Ġsat · Ä±r · ĉse · km · eli · . | Birinci satır.⏎⏎  İkinci satır⇥sekmeli. |
| cl100k | B · ir · inci ·  sat · ır · .⏎⏎ ·   ·  İ · k · inci ·  sat · ır · ⇥se · km · eli · . | Birinci satır.⏎⏎  İkinci satır⇥sekmeli. |
| o200k | Bir · inci ·  sat · ır · .⏎⏎ ·   ·  İ · kin · ci ·  sat · ır · ⇥se · km · eli · . | Birinci satır.⏎⏎  İkinci satır⇥sekmeli. |

### k26 (bicim): `“Tırnaklı” — uzun tire – kısa tire … üç nokta`

| tokenizer | parçalar | geri çözülen |
|---|---|---|
| BERTurk | “ · Tır · ##nak · ##lı · ” · — · uzun · tir · ##e · – · kısa · tir · ##e · … · üç · nokta | “ Tırnaklı ” — uzun tire – kısa tire … üç nokta |
| ModernBERT-tr | “ · Tırnak · ##lı · ” · — · uzun · tir · ##e · – · kısa · tir · ##e · … · üç · nokta | “ Tırnaklı ” — uzun tire – kısa tire … üç nokta |
| BGE-M3 | ▁“ · T · ır · nak · lı · ” · ▁— · ▁uzun · ▁tire · ▁– · ▁kısa · ▁tire · ▁... · ▁üç · ▁nokta | “Tırnaklı” — uzun tire – kısa tire ... üç nokta |
| Qwen3 | âĢľ · T · Ä±r · nak · lÄ± · âĢĿ · ĠâĢĶ · Ġuz · un · Ġtire · ĠâĢĵ · ĠkÄ±sa · Ġtire · ĠâĢ¦ · ĠÃ¼Ã§ · Ġnok · ta | “Tırnaklı” — uzun tire – kısa tire … üç nokta |
| cl100k | “ · T · ır · nak · lı · ” ·  — ·  uz · un ·  tire ·  – ·  k · ı · sa ·  tire ·  … ·  ü · ç ·  nok · ta | “Tırnaklı” — uzun tire – kısa tire … üç nokta |
| o200k | “T · ır · nak · lı · ” ·  — ·  uzun ·  tire ·  – ·  kısa ·  tire ·  … ·  üç ·  nok · ta | “Tırnaklı” — uzun tire – kısa tire … üç nokta |

