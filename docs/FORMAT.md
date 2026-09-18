# Technické minimum pro údržbu

## Prostředky

Hlavička IO obsahuje v prvních třech bajtech little-endian rozbalenou délku,
v bajtu 3 příznak komprese a v bajtech 4–5 typ. Typ 0 má hlavičku dlouhou
22 bajtů, ostatní používané prostředky 6 bajtů. A1 je bitově orientovaný
formát se střídáním literálů a zpětných referencí. Implementace jsou v
`tools/resource_codec.py` a `src/installer.cpp`.

Python build i C++ instalátor čtou původní soubory až od uživatele. Všechny
vstupy musí přesně odpovídat profilu. Kontrolní součty a adresy jsou technická
metadata, nikoli soubory hry. Rozbalování je omezené deklarovanou velikostí
a povoluje nejvýše 16 bajtů nulového dočtení za fyzickým koncem proudu.
Výsledek se kontroluje SHA-256.

Některé původní proudy mají konec mírně odlišný od deklarované délky.
MARCHAND.IO má jedinou evidovanou normalizaci posledního bajtu na hodnotu 163,
aby bezpečný dekodér dal stejný výsledek jako dříve ověřená herní rutina.
Je to jeden bajt profilu, nikoli přibalený blok původní grafiky.

## Texty a font

Texty jsou jedno-bajtové vlastní kódy glyfů, nikoli UTF-8 ani CP852.
Unicode čeština se převádí až při sestavení. Velké ASCII písmeno má za sebou
mezerník kvůli šířce původního fontu. U běžných slotů se původní délka a ukončující nula
zachovají; zbytek se doplní mezerami. U pevných popisků `colon_column`
určuje pozici dvojtečky; výplň se vloží před ni.

Velká Č a Ž zachovávají 12px posun (kód glyfu + mezera). Ú a Š se při
exportu mění na malá ú a š s běžným 6px posunem; Á se mění na A.

| Český znak | Herní kód |
| --- | --- |
| Č, Ž | 24, 5E |
| á, é | 2F, 5B (existující glyfy) |
| č, ň, ř, š | 23, 25, 26, 2A |
| ť, ý, ě, ž | 3C, 3D, 3E, 5C |
| ó, í, ů, ď, ú | 5D, 5F, 60, 7B, 7D |

Pixely fontu jsou čtyřbitové indexy, dva v každém bajtu. Veřejný fontový
JSON ukládá jen přepsané pixely a jejich souřadnice; původní bitmapu získá
nástroj při lokálním exportu. Hlavičky glyfů ani tabulky adres se nemění.

Vedle přesměrování delších textů se mění operand pozice čtvrtého řádku jednoho dialogu:
TEXTIND.IO na 0x1CFB mění řádek 2 na 3. Sestavovač ověří původní hodnotu.
Překlad odměny v textin.013 používá anglických 100 000; samotný ekonomický
skript hry se nemění. Rozdíly zdrojových jazyků se řeší redakčně podle EN.

## Proč komprimujeme úvod

Původní nekomprimovaný loader počítá s úplným načtením bloku 65 535 bajtů.
Následující blok začíná s DX=15 a DOSBox může čtení zkrátit na 65 521 bajtů.
Loader tuto skutečnou délku nezohlední a poškodí další data. Ve v1.0 se proto
PRESENT.IO vrací do původního formátu A1, jehož načítání používá malé bloky.
Obecně komprimujeme data delší než 131 056 bajtů bez hlavičky.

Souvislost s DOS čtením popisuje implementace
[DOSBox Staging, DOS_GetAmount](https://raw.githubusercontent.com/dosbox-staging/dosbox-staging/main/src/dos/dos.cpp).
Výzkumné dumpy a disassemblace se nezveřejňují a nejsou potřebné k buildu.

## Distribuční patch

Generovaná data patche obsahují jména souborů, kontrolní součty originálů,
bezpečně rozbalených vstupů i konečných výstupů a bloky `[offset, délka, nové
bajty]`. Nevkládají se nezměněné bloky grafiky, původní EXE ani celé prostředky.
Výchozí payload v1.0 má 25 641 bajtů, z toho 11 741 změněných bajtů.

Patcher nejprve připraví všechny výsledky a zálohy, potom vymění jednotlivé
soubory. Při zachycené chybě vrací provedené změny. Nejde o jedinou atomickou
operaci pro všech devět souborů: po výpadku napájení lze dokončit směs
ověřených originálů a cílových souborů nebo obnovit zálohu. Po takovém výpadku
může zůstat pracovní složka či zámek `.ishar2-cs-lock`.

## Přesměrování v1.1

23 ověřených přiřazení literálů je nahrazeno čtyřbajtovým relativním skokem na připojený blok s českým textem, původním typem cíle a skokem zpět. Podporované cíle jsou lokální řetězec s jedno/dvoubajtovou adresou a konkrétní výraz pro řádek s indexem nula. Původní instrukce se ověří hashem. Jiné tvary, segment od 64 KiB nebo skok mimo ±32 KiB se odmítají. Hlavička prostředku dostane novou délku.

Instalátor nejprve rozbalí původní deklarovanou délku a ověří SHA-256. Potom zvětší pracovní buffer na cílovou délku a aplikuje rozdílové bloky včetně přidaného konce; nakonec ověří výsledný SHA-256. Připojené bloky obsahují české texty a nezbytné instrukce, nikoli kopie původních assetů.
