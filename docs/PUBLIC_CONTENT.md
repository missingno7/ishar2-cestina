# Původ veřejných zdrojů a hranice distribuce

Projekt byl oddělen od pracovního adresáře lokalizace. Nejde o jeho kopii.

| Veřejný vstup | Jak vznikl |
| --- | --- |
| `translation/cs.json` | Česká pole hotového překladu: ID, úplný text, stav a herní řádky. Původní korpus ani pracovní poznámky se nepřevzaly. |
| `translation/glossary.json` | České termíny a tvary; anglická hesla se odstranila, vazba je přes ID jednotek. |
| `translation/font-delta.json` | Porovnání upravených glyfů s originálem; uloženy jen nové hodnoty změněných pixelů, bez původních PNG. |
| `metadata/layout.json` | Adresy, délky, zarovnání a kontrolní pravidla. Původní texty byly nahrazené adresovými referencemi. |
| `metadata/profile.json` | Kontrolní součty kompatibilní verze a malé technické parametry nutné k sestavení. |
| `src/` | Vlastní přenosný Win32 patcher; payload se generuje až při lokálním buildu. |
| `tools/` | Samostatné sestavení, import referencí, práce s pixelovými rozdíly a kontrola veřejného stromu. |
| `tests/` | Syntetické testy bez hry a oddělené integrační testy nad uživatelovou kopií. |

Nepřevzaly se originální IO/FIC/EXE/STP, úplné upravené IO, rozbalené herní
prostředky, originální katalogy EN/DE/FR, dump paměti, disassemblace, emulátor
ani jeho vendor knihovny. Nepřevzaly se ani hotové fontové PNG: české glyfy
vycházejí z původního písma, proto je veřejný pouze rozdíl a lokální export.
Veřejné zdroje nevyžadují žádné soubory z původního pracovního projektu.

Ověření samostatnosti při oddělení projektu:

- Build z veřejných zdrojů a originální hry vytvořil všech devět prostředků
  přesně podle referenčních SHA-256 v1.0.
- Lokální import rekonstruoval všech 382 anglických referencí stejně jako
  původní pracovní katalog, aniž by byl tento katalog součástí projektu.
- Export fontů rekonstruoval viditelné pixely všech 15 dodaných glyfů.
  Opakovaný import nezměnil jejich rozdílové zdroje.
- Prošlo 5 testů veřejných zdrojů a 12 integračních testů instalátoru,
  včetně návratu po chybě zápisu. Ověřena byla i tlačítka skutečného GUI.

Tento popis dokládá technické oddělení dat. Nepředstavuje licenci na původní
hru ani právní posouzení odvozeného překladu; rozsah licence je v LICENSING.md.
