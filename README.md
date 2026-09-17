# Ishar 2 – čeština

Česká lokalizace DOS verze **Ishar 2**. Překlad vychází z angličtiny a ve hře
nahrazuje německou jazykovou variantu. Obsahuje 382 překladových jednotek,
530 herních řetězců, českou diakritiku v malých písmenech a velká Č a Ž.

**Projekt neobsahuje původní hru. Musíte vlastnit a dodat vlastní kompatibilní
kopii hry.** V Git repozitáři jsou zdrojové kódy, české překladové zdroje,
technická metadata a změny fontu. Hotový instalátor patří do **GitHub Releases**.

## Instalace hotové češtiny

1. Stáhněte **[Ishar2-Cestina-v1.0.zip](https://github.com/missingno7/ishar2-cestina/releases/download/v1.0/Ishar2-Cestina-v1.0.zip)** z [Releases](https://github.com/missingno7/ishar2-cestina/releases). Archiv „Source code“ je pro vývojáře.
2. ZIP rozbalte a spusťte `Ishar2-Cestina.exe` (64bitové Windows).
3. Ukončete hru. Vyberte její složku obsahující `START.EXE` a klikněte na
   **Aplikovat češtinu**.
4. Hru spusťte obvyklým způsobem v DOSBoxu a zvolte **3 – Čeština**.

Instalátor je přenosný, nevyžaduje Python, .NET ani instalaci dalších knihoven.
Potřebuje oprávnění k zápisu do složky hry. Před změnou ověří verzi a vytvoří
zálohu devíti souborů v `.ishar2-cs-backup-v1.0`. Tlačítko **Obnovit originál**
vrátí původní soubory. Zálohu proto nemažte. Uložené pozice, konfigurace
DOSBoxu ani herní EXE se nemění.

## Stav a podporovaná verze

Aktuální základ je **v1.0, první veřejné vydání**. Podporovaná je ověřená DOS verze
obsahující angličtinu, francouzštinu a němčinu. Shoda se určuje přesnými
SHA-256 součty v [`metadata/profile.json`](metadata/profile.json), nikoli
podle názvu obchodu nebo adresáře. Jiná vydání či dříve upravené prostředky
instalátor odmítne; pro jiné verze zatím není připravená migrace.

Instalace, obnova a shoda výsledných souborů s v1.0 byly otestovány na kopiích
hry. Provedené technické testy nenahrazují odehrání hry. Celý překlad a
opravené intro stále potřebují ověření hraním v DOSBoxu. EXE není digitálně
podepsaný.

Známá omezení:

- **Č a Ž** zůstávají velká s diakritikou. **Ú → ú**, **Š → š**, **Á → A**.
  Ostatní nepodporovaná velká písmena ztrácejí diakritiku. Čisté překladové
  zdroje zůstávají ve správné Unicode češtině; změny probíhají jen při exportu.
- Řádky musí dodržet původní německé délky. Sestavovač příliš dlouhé texty
  odmítá, automaticky je neusekává.
- Písmo a některé popisky jsou společné, takže úpravy ovlivní i ostatní
  jazykové volby. Češtinu vybírejte číslem 3.
- Nápisy zapečené do grafiky nebo dosud nenalezené texty mohou zůstat původní.

## Sestavení ze zdrojových kódů

Potřebujete **Python 3.10+**, **MinGW-w64 pro Windows x64** (`g++`, `windres`)
a vlastní **neupravenou kompatibilní instalaci**. Běžné sestavení používá
jen standardní knihovnu Pythonu; Pillow je volitelné pro práci s PNG fontů.

Z kořene repozitáře:

```powershell
python tools/project.py check
python tools/project.py build --game-dir "D:\MojeHry\ISHAR2"
```

Kompilátor musí být v `PATH`. Cesty lze zadat také přes `--cxx` a `--windres`,
například `--cxx "C:\msys64\mingw64\bin\g++.exe"` a
`--windres "C:\msys64\mingw64\bin\windres.exe"`.

Vznikne `build/Ishar2-Cestina.exe`, `dist/Ishar2-Cestina-v1.0.zip` a
`dist/SHA256SUMS.txt`. **K releasu přiložte ZIP a kontrolní součty.** Adresáře
`build/` a `dist/` necommitujte. Sestavení původní instalaci nijak nepřepisuje.
Podrobnosti jsou v [návodu pro vývoj](docs/DEVELOPMENT.md) a
[postupu vydání](docs/RELEASING.md).

## Úpravy překladu a fontů

- [`translation/cs.json`](translation/cs.json): čistý český text `cs` a kratší
  herní řádky `lines[].cs`, propojené stabilními ID.
- [`translation/glossary.json`](translation/glossary.json): české termíny,
  povolené tvary a jednotky, kde se mají používat.
- [`translation/font-delta.json`](translation/font-delta.json): pouze změny
  jednotlivých pixelů 15 glyfů, nikoli kompletní původní font ani hotové PNG.
- [`metadata/`](metadata/): verze, kontrolní součty, adresy textových slotů,
  jejich limity a odkazy na původní texty bez jejich obsahu.

Anglické, německé a francouzské reference se importují teprve z vlastní hry:

```powershell
python tools/project.py import --game-dir "D:\MojeHry\ISHAR2"
```

Vzniklý `.local/context.json` je soukromý pracovní podklad. **Nepřidávejte ho
do Gitu ani k releasu.** Stejně platí pro vyexportované fontové PNG.
Postup s obrázky a zadáním pro AI popisuje [vývojový návod](docs/DEVELOPMENT.md).
Překlad má dodržovat [jazykový styl](docs/TRANSLATION_STYLE.md).

## Co patch mění

Upravuje devět prostředků: `MESSAGED.IO`, `TEXTIND.IO`, `PRESENT.IO`,
`MAIN.IO`, `GERDEP.IO`, `TABLEAU.IO`, `MAP.IO`, `MARCHAND.IO`, `TAVERNE.IO`.
Mění texty, pixely českých glyfů a pozici jednoho řádku dialogu. EXE se
nepatchuje a adresy textů ani velikosti rozbalených prostředků se neposouvají.

Instalátor rozbalí původní data z uživatelovy hry, aplikuje rozdíly a sestaví
nové prostředky. `PRESENT.IO` znovu komprimuje do A1, aby se vyhnul chybě
načítání velkého nekomprimovaného souboru. Balíček nepotřebuje obsahovat celé
původní nebo upravené `.IO` soubory. Viz [technický popis](docs/FORMAT.md).

## Hlášení chyb

Použijte **Issues** tohoto repozitáře. Uveďte verzi češtiny, zda jde o překlad
nebo instalátor, místo ve hře a postup reprodukce. U překlepu připište text
nebo ID jednotky; u instalátoru přesné znění chyby a verzi Windows.
U zobrazení ve hře pomůže verze DOSBoxu a malý snímek dotčeného místa.
Nepřikládejte celou hru, EXE, herní prostředky ani extrahovaný korpus.

## Licence

Vlastní kód patcheru a nástrojů je pod **MIT**. Tato licence se automaticky
nevztahuje na překlad, odvozené změny fontů ani původní obsah hry.
Přesný rozsah popisuje [LICENSING.md](LICENSING.md).

## Podpora projektu

Čeština je a zůstane zdarma. Stažení ani používání není podmíněné platbou.
Pokud se vám projekt líbí a chcete podpořit vznik dalších překladů, source
portů a projektů kolem starých her, můžete mě dobrovolně podpořit na
[Patreonu](https://www.patreon.com/cw/JiriVestfy).
