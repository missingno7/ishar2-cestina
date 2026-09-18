# Historie korekcí zahrnutých ve v1.1

Níže uvedené korekce jsou součástí v1.1. Závěrečné rozšíření názvů a další změny shrnuje [přehled vydání](RELEASE-v1.1.md).

| ID | Původní herní řádek | Upravený herní řádek |
|---|---|---|
| message.0006B2 | Páčení zámků: | Otevírání zámků: |
| message.000736 | Zbraně pro 1 ruku: | Jednoruční zbraně: |
| message.000762 | Zbraně pro 2 ruce: | Obouruční zbraně: |
| message.0008C5 | Hlas družiny: | Hlasování: |
| message.001FD8 | ještěří muž | ještěrovec |
| textin.015 | Schloumz: tělesná obnova | Schloumz: obnova tělesné energie |
| textin.015 | Ghoslam: duševní obnova | Ghoslam: obnova duševní energie |
| textin.023 | jež zchladí tvou žízeň! Dwidongdingue! | jež uhasí tvou žízeň! Dwidongdingue! |
| textin.035 | Hračka! Jak vánek! | Úplná hračka! |
| textin.037 | Snif! Její poslední vzkaz: 'Můj | Vzlyk! Její poslední vzkaz: 'Můj |
| textin.052 | Během spánku se ztrácí | Zatímco jste spali, zmizel |

Označení hlasování ověřeno ve všech třech jazykových verzích a podle sousedních výsledků hlasování. U hlášky o zmizení člena zbývá ověřit spojení se jménem v DOSBoxu.

Import vlastní hry nově vytváří také soukromý čitelný přehled `.local/review-languages.md` (EN/DE/FR/CS). Nikdy jej necommitujte.

## Kontextová revize 18. 9. 2026

Klerik a lektvary opraveny podle manuálu a původních jazyků. Blue Velvet vyžaduje přívěsek; umírající dívka mluví v ženském rodě. Zmizení člena a první pomoc používají jména bez skloňování.

Přidáno 20 přehlédnutých řetězců (10 jednotek): bankovní datum, vklad/výběr, měna, odmítnutí první pomoci, čtyři popisky vlastností a oslovení před modlitbou za Zeldy. Celkem 392 jednotek a 550 řetězců. Žádné adresy ani délky prostředků se neposouvají.

[Úplný kontextový index a nejasnosti](TEXT_CONTEXT.md).

| Jednotka | Původní herní text | Nový herní text |
|---|---|---|
| `message.002074` | učenec | klerik |
| `textin.006` | unikl... přívěsek... pro vás... ptáci... | unikla... přívěsek... pro vás... ptáci... |
| `textin.016` | Jablou: poplach entů | Jablou: probudí enta |
| `textin.016` | Humbolg: neklidný kněz | Humbolg: pro neklidného kněze |
| `textin.034` | Nezapomeňte oblek a náhrdelník. | Nezapomeňte oblek a přívěsek. |
| `textin.052` | Zatímco jste spali, zmizel | Po probuzení v družině chybí |
| `shared.TABLEAU.IO:001E8B` | učen. | kler. |
| `context.healing_refusal` | dosud nepřeloženo | Pomoc: / - odmítnuta. |
| `context.preview_vitality` | dosud nepřeloženo | Životy: |
| `context.preview_agility` | dosud nepřeloženo | Obratnost: |
| `context.preview_strength` | dosud nepřeloženo | Síla: |
| `context.preview_constitution` | dosud nepřeloženo | Odolnost: |
| `context.zeldy_invocation` | dosud nepřeloženo | Dwildy, duchu Silmarils, |
| `context.bank_date` | dosud nepřeloženo | má ke dni |
| `context.bank_withdrawal` | dosud nepřeloženo | Lze vybrat: / Lze vybrat: / Lze vybrat: / Lze vybrat: |
| `context.bank_deposit` | dosud nepřeloženo | Lze vložit: / Lze vložit: / Lze vložit: / Lze vložit: |
| `context.bank_currency` | dosud nepřeloženo | zl / zl / zl / zl |

## Ověření původním skriptovým vyhodnocovačem

`textin.060`: „je přečerpaný!“ → „je prázdný!“. Původní podmínka kontroluje nulový zůstatek, nikoli dluh. Francouzský význam odpovídá chování hry; EN/DE jsou zavádějící. Bankovní logika zůstává stejná.

Izolované nativní testy s modelovým stavem potvrzují také skládání odmítnutí pomoci se jménem, získání jména chybějícího člena a připojení čísla k bankovnímu popisku. Vykreslení celých scén je nadále potřeba ověřit v DOSBoxu.

## Zarovnání a redakční pravidla

Opraveno doplňování mezer u 26 pevných popisků: dvojtečka zůstává na původní pozici. Přidána explicitní metadata `colon_column` a regresní testy soukromého i veřejného sestavovače. Čisté české znění zůstává bez výplně.

Čas knihovny uzavřen podle přání autora na 4 (shoda EN/DE). Malé počáteční písmeno u obecných názvů ras, povolání a předmětů ponecháno jako jednotný český styl. Zkratky čar./trp. zachovány: nejkratší sloty mají 5/4 bajty, plná slova se nevejdou. Delší jiné jazykové prostředky neposkytují prostor německému slotu.

Finální v1.1 nahrazuje výše zmiňované zkratky čar./trp. plnými názvy pomocí explicitních přesměrování.
