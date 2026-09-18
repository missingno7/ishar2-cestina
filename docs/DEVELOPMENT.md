# Práce se zdroji lokalizace

## Co je veřejné a co zůstává lokální

Veřejné vstupy jsou čisté české texty, slovníček, změny pixelů fontu a metadata
slotů. Kompletní původní texty ani bitmapy nejsou ve zdrojích potřeba. Všechny
importy z vlastní hry ukládejte do `.local/`, kterou Git ignoruje.

Původní pracovní projekt používal rozbalenou kopii prostředků a izolované
spouštění herního dekodéru z dumpu EXE. Tento repozitář tuto závislost nemá:
Python i instalátor obsahují vlastní implementaci datového formátu A1.
Žádný dump, disassemblace, binární testovací fixture ani vendor knihovna
emulátoru se do veřejného repozitáře nepřenáší.

## Překlad

1. `python tools/project.py import --game-dir "D:\MojeHry\ISHAR2"`
2. Pro vlastní kontrolu použijte `.local/context.json`. Pro práci s AI je
   `.local/translation-request.md`, který spojuje lokálně načtené reference,
   český překlad, slovníček a styl. Tyto soubory nepublikujte.
3. Upravujte `translation/cs.json`. `cs` je úplný český význam; `lines[].cs`
   jsou skutečně zobrazované řádky. Neměňte ID ani nepište herní kódy znaků.
4. Přípustné pády a zkratky termínů doplňte v `translation/glossary.json`.
   `units` určuje jejich použití; nepřidávejte chybné tvary jen kvůli testu.
5. `python tools/project.py check`

Kontroluje se úplnost, duplicity, čísla a chráněné tokeny, použití slovníčku,
znaková sada a skutečná délka po převodu. Automatická kontrola nenahrazuje
redakční kontrolu významu a přirozenosti češtiny. Odkazy v `metadata/layout.json`
obsahují pouze názvy souborů, offsety a délky; čitelný původní text se načte
až při importu z uživatelovy hry.

Slovníček v repozitáři úmyslně neobsahuje původní anglická hesla. Odpovídající
kontext lze dohledat pomocí seznamu `units` v lokálně importovaných referencích.

## Fonty

Publikovaná `translation/font-delta.json` obsahuje 15 záznamů. U každého jsou
rozměry, pozice bitmapy a dvojice `[index_pixelu, nová_hodnota]`; hodnota je
paletový index 0–15. Nezměněné pixely se čerpají výhradně z originální hry.
Aktuální zdroje obsahují 376 změněných pixelů, nikoli kompletní bitmapy.

Pro běžné kreslení si nainstalujte volitelný Pillow a vytvořte lokální PNG:

```powershell
python -m pip install Pillow
python tools/fonts.py export --game-dir "D:\MojeHry\ISHAR2"
```

PNG jsou v `.local/font/`. Nástroj odmítne přepsat existující obrázky, aby
nezničil rozpracované úpravy. Zachovejte rozměry a používejte existující
barvy bez vyhlazování. Po úpravách:

```powershell
python tools/fonts.py import --game-dir "D:\MojeHry\ISHAR2"
python tools/project.py build --game-dir "D:\MojeHry\ISHAR2"
```

Import přepíše pouze rozdílový JSON; do commitu patří tento JSON, ne PNG.
Kódy, rozměry a pozice glyfů neměňte při obyčejném překreslování.

## Build

`prepare` ověří originál, připraví všechny změny v paměti a vytvoří pouze
`build/patch_data.h` a `build/manifest.json`:

```powershell
python tools/project.py prepare --game-dir "D:\MojeHry\ISHAR2"
```

`build` navíc zkompiluje C++17 Win32 instalátor s MinGW-w64 a vytvoří ZIP.
Nepotřebuje původní pracovní repozitář, Codex, Unicorn ani dump EXE. Používá
`g++` a `windres` z PATH nebo z argumentů `--cxx`, `--windres` (alternativně
proměnné `CXX`, `WINDRES`). Cesty se předávají jako argumenty procesu,
nikoli skládáním shellového příkazu; mezery v cestách jsou podporované.

Po změně vydané verze zvyšte `metadata/profile.json:version` a upravte
uživatelskou dokumentaci a čísla v `src/app.rc` / `src/app.manifest`.
Patcher kontroluje přesnou shodu originálu nebo svého vlastního výstupu;
automatická migrace z jiné české verze není implementovaná. Nejprve obnovte
originál předchozím patchem nebo použijte čistou instalaci.

`reference_release_sha256` uchovává kontrolní součty schváleného vydání v1.1.
Nezamyká další překlady: nové výstupní součty se odvodí ze skutečných zdrojů
při každém sestavení a vloží do patche.

## Testy

Bez hry a bez kompilátoru:

```powershell
python tools/audit_public.py
python -m unittest discover -s tests -v
```

CI spouští pouze tyto kontroly nad veřejnými zdroji a syntetickými daty.
Žádná hra ani privátní assety se do GitHub Actions nenahrávají.

Po sestavení na Windows lze spustit integrační testy skutečného EXE:

```powershell
$env:ISHAR2_GAME_DIR = "D:\MojeHry\ISHAR2"
python -m unittest discover -s tests -v
```

Testy používají kopie devíti prostředků a START.EXE v `.local/tests`, které
po sobě odstraní. Původní hru nepatchují. Ověřují přesnou shodu výstupu,
instalaci a obnovu, opakování, neznámou verzi, neplatnou zálohu, částečnou
instalaci, zámek a návrat po selhání zápisu. Testovací EXE s injekcí chyby
zůstává v `build/` a nikdy není v distribučním ZIPu.

Následuje ruční test GUI a hry v DOSBoxu, zejména intro, diakritika,
inventář, dynamické hodnoty, bankovní texty a víceřádkové dialogy.

Volitelný automatický test vlastního GUI na Windows (vyžaduje Pillow) je
`python tools/smoke_gui.py --game-dir "cesta k originální hře"`. Použije
dočasnou kopii, ověří tlačítka Aplikovat a Obnovit a uloží snímek pouze
vlastního okna do `.local/gui/gui-preview.png`. Na chvíli zobrazí testované
okno bez aktivace; nepořizuje snímek celé plochy.

## Delší texty od v1.1

`slots[].relocation` obsahuje hranice a SHA-256 původní instrukce, schválený rozpočet a `retained_cs` (starší české znění v nyní nedostupné části původní instrukce, pro přesnou reprodukci otestovaných dat). `profile.relocation_order` určuje deterministické pořadí připojených bloků. Není třeba žádný soukromý výzkumný nástroj: vše sestaví `tools/project.py` a `tools/relocation.py` z vlastní hry.
