# Návaznosti a role textů

Kontextová revize po v1.0: 392 jednotek / 550 řetězců. Jde o statickou kontrolu textů, řádkových příkazů, manuálu a dohledaného kontextu; nejde o odehrání všech větví hry.

## Pravidla pro další překlad

- Fyzické sousedství řetězců neznamená návaznost. Podmíněné repliky a alternativní číselné větve nespojovat.
- Krátký inventární název a dlouhý obchodní název mohou být záměrně odlišné; musí zachovat identitu předmětu a bonus.
- Jména vkládaná za běhu nejsou skloňovaná. Česká věta musí fungovat s mužským i ženským jménem.
- Čistý překlad může být delší. Herní řádky mají samostatný limit a německé pořadí větví.
- `textin.015–016` jsou lektvary. Klerik není učenec. Náhrdelník z prvního ostrova nezaměňovat s přívěskem od enta.

## Doložené významové opravy

Klerik, lektvary a hlasování: původní EN/DE/FR a manuál, strany PDF 11, 13, 15–16. Umírající žena, účinky Jablou/Humbolgu a přívěsek do Blue Velvetu: [dobový hintbook](https://www.mocagh.org/miscgame/ishar2-hintbook.pdf), etapy 1, 6, 7 a 11.

Nulový bankovní zůstatek (`textin.060`): původní x86 vyhodnocovač potvrzuje podmínku obou složek částky rovných nule. Proto „je prázdný!“, nikoli „je přečerpaný!“. Ověřeno na šesti kombinacích hodnot. Dále ověřeno sestavení odmítnutí pomoci se dvěma jmény, získání jména chybějícího člena a spojení bankovního textu s číslem. Jde o izolované nativní rutiny s modelovým stavem, ne průchod hrou v DOSBoxu.

## Zbývající nejasnosti

- `textin.031`: redakčně uzavřeno na pokyn autora: 4 podle shodné EN/DE, odlišná FR 14 se nepřebírá. Toto rozhodnutí neprokazuje časovou podmínku herního skriptu.
- `textin.035`: EN šeptalové, DE šeptání, FR buřiči. Kontext potvrzuje plán krádeže, ale konkrétní adresát zůstává neurčený. Zachována EN varianta; nejde o pokyn přesunout družinu do jiné lokace.
- `textin.036`: EN starostova dcera, FR/DE dcera studnaře. Identitu nelze bezpečně spojit se Zeldy jen podle sousedství textů; ponecháno EN.
- `textin.030`: časy ve hře a v návodech si odporují. Ponechány 2–4 ze všech tří herních jazyků; časové podmínky se nepatchují.
- V DOSBoxu ověřit celé bankovní větve, první pomoc s oběma pohlavími, zmizení člena, modlitbu za Zeldy, nové popisky a intro.

## Kompletní index

| Jednotka | Role | Návaznost / použití |
|---|---|---|
| `message.0002D4` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.0002F3` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.000314` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.00033E` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.00035A` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.000382` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.0003BE` | system_fragment | Alternativní větve mechanik A/DF0/B; neskládat všechny možnosti za sebe. |
| `message.000478` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.000494` | system_fragment | Alternativní větve mechanik A/DF0/B; neskládat všechny možnosti za sebe. |
| `message.000510` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.00052F` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.00054D` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.00056B` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000589` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0005A7` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0005CA` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0005EE` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.00060F` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000630` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000651` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000672` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000697` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0006B2` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0006DE` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.00070A` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000736` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000762` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.00078D` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0007B8` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000824` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000843` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000863` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.000882` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0008A1` | stat_label | Samostatný nadpis nebo popisek vlastnosti doplněný hodnotou. |
| `message.0008C5` | dynamic_fragment | Hlasování: nadpis a jednotlivá jména doplněná stavem pro/neutrální/proti. |
| `message.0008F2` | dynamic_fragment | Hlasování: nadpis a jednotlivá jména doplněná stavem pro/neutrální/proti. |
| `message.000919` | dynamic_fragment | Hlasování: nadpis a jednotlivá jména doplněná stavem pro/neutrální/proti. |
| `message.000944` | dynamic_fragment | Hlasování: nadpis a jednotlivá jména doplněná stavem pro/neutrální/proti. |
| `message.000963` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.000988` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.0009AE` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.0009D1` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.0009F8` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.000AC7` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000AEC` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000B1D` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000B43` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000B7B` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000BA9` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000BD1` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000BFA` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000C2B` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000C52` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000C76` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000CA0` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000CE8` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000D18` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000D36` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000D6D` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.000D9B` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.000DBB` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.000E54` | system_fragment | Dynamické číslo paměti + kB; původní jednotka německého skriptu, nikoli anglické bytes. |
| `message.000F77` | system_fragment | Třířádková německá instalace, EN má čtyři řádky; bez přesouvání příkazu INSTALL nebo označení disku. |
| `message.001028` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.00105C` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.001078` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.0010A4` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0010C3` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0010DF` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.00110E` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001126` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.00114F` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001181` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0011AC` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.0011DA` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.001207` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.001221` | dialogue_fragment | Navazující řádky jedné promluvy; pořadí potvrzeno řádkovými příkazy v MESSAGED.IO. |
| `message.001245` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001278` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0012AF` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0012D7` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001301` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001325` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001362` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0013A6` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0013D4` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0013F7` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001425` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001468` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0014AC` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.0014E5` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.00150B` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.00152B` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001548` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.00156C` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001588` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001611` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001642` | utterance | Reakce družiny/NPC. Bez doložené vazby se sousedními řetězci zůstává samostatná. |
| `message.001944` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.001960` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.001985` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001994` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.0019A6` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.0019BE` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.0019CD` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.0019DB` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.0019FF` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A13` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A21` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A31` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A41` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A51` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A60` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A6F` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A84` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001A99` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001AAE` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001AC3` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001AD8` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001AE9` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001AF7` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B07` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B15` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B2E` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B49` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B5F` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B78` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001B8D` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001BA5` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001BBE` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001BD1` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001BED` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C02` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C23` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C38` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C4D` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C62` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C78` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001C8F` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001CA4` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001CB9` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001CCB` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001CDD` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001CF2` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D07` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D1C` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D31` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D4F` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D63` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D77` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001D8C` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001DA1` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001DBA` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001DD1` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001DE3` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001DF7` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E0B` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E20` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E35` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E49` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E5D` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E74` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001E87` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001EA3` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001EC5` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001EDA` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001EEE` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001F02` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001F16` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001F29` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001F3F` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001F52` | item | Krátký inventární název, případně obecnější než označení z obchodu. |
| `message.001F68` | ui | Samostatný výsledek akce nebo omezení předmětu. |
| `message.001FA0` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.001FAF` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.001FBC` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.001FCB` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.001FD8` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.00201A` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002031` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002042` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002052` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002065` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002074` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002085` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002097` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.0020A7` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.0020B4` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.0020C4` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.0020D7` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.0020E7` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.0020F9` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.00210C` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.00211F` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.00212E` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002143` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002158` | class_or_race | Samostatný název povolání či rasy; zkratka může být nutná. |
| `message.002164` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.00218A` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.0021C2` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.0021D9` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.0021F4` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `message.002207` | system_fragment | Systémová hláška nebo ovládací instrukce; nevyvozovat dialog z fyzického pořadí. |
| `textin.000` | dialogue | Gordbnoeuf: podmíněné stavy zatčení / žádost / neúspěch / odměna / další návštěva; neslepovat do jedné řeči. |
| `textin.001` | dialogue | Gordbnoeuf: podmíněné stavy zatčení / žádost / neúspěch / odměna / další návštěva; neslepovat do jedné řeči. |
| `textin.002` | dialogue | Gordbnoeuf: podmíněné stavy zatčení / žádost / neúspěch / odměna / další návštěva; neslepovat do jedné řeči. |
| `textin.003` | dialogue | Gordbnoeuf: podmíněné stavy zatčení / žádost / neúspěch / odměna / další návštěva; neslepovat do jedné řeči. |
| `textin.004` | dialogue | Gordbnoeuf: podmíněné stavy zatčení / žádost / neúspěch / odměna / další návštěva; neslepovat do jedné řeči. |
| `textin.005` | dialogue | Gordbnoeuf: podmíněné stavy zatčení / žádost / neúspěch / odměna / další návštěva; neslepovat do jedné řeči. |
| `textin.006` | dialogue | Umírající žena u kamenného kruhu; ženský rod a přerývané věty. |
| `textin.007` | dialogue | Velitel Zachova ostrova: související repliky, nikoli prokázaný automatický sled. |
| `textin.008` | dialogue | Velitel Zachova ostrova: související repliky, nikoli prokázaný automatický sled. |
| `textin.009` | dialogue | Velitel Zachova ostrova: související repliky, nikoli prokázaný automatický sled. |
| `textin.010` | dialogue | Chrám: uvítání, ztracená modla a její vrácení jsou různé stavy úkolu. |
| `textin.011` | dialogue | Chrám: uvítání, ztracená modla a její vrácení jsou různé stavy úkolu. |
| `textin.012` | dialogue | Chrám: uvítání, ztracená modla a její vrácení jsou různé stavy úkolu. |
| `textin.013` | event | Odměna po přepadení banky, nikoli zůstatek osobního účtu. |
| `textin.014` | dialogue | Nalezení mapy v knihovně; oddělené od knih o lektvarech. |
| `textin.015` | potion_list | Dvě související stránky popisů lektvarů; řádky jsou samostatné receptové položky. |
| `textin.016` | potion_list | Dvě související stránky popisů lektvarů; řádky jsou samostatné receptové položky. |
| `textin.017` | dialogue | Knižní vtip o hrách Silmarils; nemíchat s recepty. |
| `textin.018` | dialogue | Různé zásahy stráží: zatčení / vykázání; nejsou jednou větou. |
| `textin.019` | dialogue | Různé zásahy stráží: zatčení / vykázání; nejsou jednou větou. |
| `textin.020` | dialogue | Olbarův příběh a navazující vzpomínka na báseň; obsahová návaznost, ne tvrzení o automatickém zobrazení. |
| `textin.021` | dialogue | Olbarův příběh a navazující vzpomínka na báseň; obsahová návaznost, ne tvrzení o automatickém zobrazení. |
| `textin.022` | dialogue | Oslovení Dwildyho -> modlitba za Zeldy. Chybějící první řádek doplněn. |
| `textin.023` | dialogue | Samostatné vzývání Shandara; odlišný adresát od modlitby za Zeldy. |
| `textin.024` | dialogue | Souvislý historický výklad: Shandar -> bratři Grimz/Griml -> dva odlišné způsoby návratu k životu. |
| `textin.025` | dialogue | Souvislý historický výklad: Shandar -> bratři Grimz/Griml -> dva odlišné způsoby návratu k životu. |
| `textin.026` | dialogue | Souvislý historický výklad: Shandar -> bratři Grimz/Griml -> dva odlišné způsoby návratu k životu. |
| `textin.027` | dialogue | Souvislý historický výklad: Shandar -> bratři Grimz/Griml -> dva odlišné způsoby návratu k životu. |
| `textin.028` | dialogue | Souvislý historický výklad: Shandar -> bratři Grimz/Griml -> dva odlišné způsoby návratu k životu. |
| `textin.029` | dialogue | Souvislý historický výklad: Shandar -> bratři Grimz/Griml -> dva odlišné způsoby návratu k životu. |
| `textin.030` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.031` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.032` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.033` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.034` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.035` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.036` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.037` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.038` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.039` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.040` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.041` | dialogue | Samostatné městské rozhovory, klepy a rady; sousedství v souboru neprokazuje stejného mluvčího. |
| `textin.042` | menu | Čtyři alternativní akce v hospodě; nečíst jako větu. |
| `textin.043` | dynamic_fragment | Cena + číslo + měna. Jídlo a pokoj jsou oddělené obrazovky. |
| `textin.044` | dynamic_fragment | Cena + číslo + měna. Jídlo a pokoj jsou oddělené obrazovky. |
| `textin.045` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.046` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.047` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.048` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.049` | dynamic_fragment | Cena + číslo + měna. Jídlo a pokoj jsou oddělené obrazovky. |
| `textin.050` | dynamic_fragment | Cena + číslo + měna. Jídlo a pokoj jsou oddělené obrazovky. |
| `textin.051` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.052` | dynamic_fragment | Český prefix + jméno; rodově neutrální a bez potřeby skloňovat jméno. |
| `textin.053` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.054` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.055` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.056` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.057` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.058` | ui | Samostatná hláška hospody či obchodu; bez automatického spojování sousedů. |
| `textin.059` | dynamic_fragment | Úvod banky -> buď hláška o prázdném účtu, NEBO datum a částka. Nezobrazují se jako jeden dialog. |
| `textin.060` | dynamic_fragment | Úvod banky -> buď hláška o prázdném účtu, NEBO datum a částka. Nezobrazují se jako jeden dialog. |
| `textin.061` | menu | Vklad / Výběr jsou dvě akce. |
| `textin.062` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.063` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.064` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.065` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.066` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.067` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.068` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.069` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.070` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.071` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.072` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.073` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.074` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.075` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.076` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.077` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.078` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.079` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.080` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.081` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.082` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.083` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.084` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.085` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.086` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.087` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.088` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.089` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.090` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.091` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.092` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.093` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.094` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.095` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.096` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.097` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.098` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.099` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.100` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.101` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.102` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.103` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.104` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.105` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.106` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.107` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.108` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.109` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.110` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.111` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.112` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.113` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.114` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.115` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.116` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.117` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.118` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.119` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.120` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.121` | item | Rozšířené obchodní názvy; inventář používá samostatné kratší varianty. |
| `textin.122` | menu | Samostatný návrat z obrazovky. |
| `textin.123` | dynamic_fragment | Pořadí slova / řádek / stránka manuálu; zachovat vnitřní volná místa pro čísla. |
| `intro.00` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.01` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.02` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.03` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.04` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.05` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.06` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.07` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `intro.08` | intro | Jeden Jonův vzkaz: 00–01 oslovení, 02–03 představení, 04–05 metafora, 06–08 výzva a hrozba. |
| `menu.language_name` | language_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.GERDEP.IO:001995` | place_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.GERDEP.IO:0019BC` | place_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.GERDEP.IO:0019E3` | place_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.GERDEP.IO:001A09` | place_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.GERDEP.IO:001A2E` | place_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.GERDEP.IO:001A55` | place_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAP.IO:00003F` | ui | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MARCHAND.IO:0000CE` | ui | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MARCHAND.IO:0000DD` | ui | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TAVERNE.IO:0002B9` | ui | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TAVERNE.IO:0002C8` | ui | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TAVERNE.IO:000988` | ui | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E3C` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E4C` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E5D` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E6C` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E7C` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E8B` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001E99` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001EAA` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001EB9` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001EC8` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001ED7` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001EEA` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001EFB` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F0C` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F1E` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F33` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F47` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F58` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F6C` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001F96` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001FA5` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001FB2` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.TABLEAU.IO:001FBF` | class_name | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:0039CC` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:0039F6` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003A20` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003A4A` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003BD1` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003BEE` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003C08` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003C28` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003C45` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `shared.MAIN.IO:003C5F` | shared_menu | Sdílený popisek; změna může být vidět i při jiné jazykové volbě. |
| `context.healing_refusal` | dynamic_fragment | Prefix + neohýbané jméno příjemce + suffix odmítnutí pomoci. |
| `context.preview_vitality` | stat_label | Popisek a číslo; stejná vlastnost jako v přehledu postavy. |
| `context.preview_agility` | stat_label | Popisek a číslo; stejná vlastnost jako v přehledu postavy. |
| `context.preview_strength` | stat_label | Popisek a číslo; stejná vlastnost jako v přehledu postavy. |
| `context.preview_constitution` | stat_label | Popisek a číslo; stejná vlastnost jako v přehledu postavy. |
| `context.zeldy_invocation` | dialogue | Oslovení Dwildyho -> modlitba za Zeldy. Chybějící první řádek doplněn. |
| `context.bank_date` | dynamic_fragment | Úvod banky -> buď hláška o prázdném účtu, NEBO datum a částka. Nezobrazují se jako jeden dialog. |
| `context.bank_withdrawal` | dynamic_label | Čtyři alternativní větve formátování každé částky, ve všech shodný popisek. |
| `context.bank_deposit` | dynamic_label | Čtyři alternativní větve formátování každé částky, ve všech shodný popisek. |
| `context.bank_currency` | dynamic_fragment | Úvod banky -> buď hláška o prázdném účtu, NEBO datum a částka. Nezobrazují se jako jeden dialog. |
