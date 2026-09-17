# Vydání patche

Git obsahuje zdrojové kódy, české zdroje a metadata. GitHub Release obsahuje
hotový instalační ZIP. Celá hra ani `.local/` se nezveřejňují žádnou z cest.

1. Dokončete úpravy překladu a fontových rozdílů. Při novém vydání zvyšte
   verzi profilu a údaje programu podle DEVELOPMENT.md.
2. Spusťte `python tools/audit_public.py`, `python tools/project.py check`
   a `python -m unittest discover -s tests -v`.
3. Z vlastní neupravené hry vytvořte release příkazem
   `python tools/project.py build --game-dir "cesta k originální hře"`.
4. Nastavte `ISHAR2_GAME_DIR` a spusťte také integrační testy Windows EXE.
   Ručně ověřte výběr složky, instalaci a obnovu a přehrajte intro v DOSBoxu.
5. Zkontrolujte Git diff, stav a seznam souborů plánovaných k přidání.
   Audit odmítá binární podklady a kontroluje i omylem již sledované soubory.
   Neobcházejte `.gitignore` pomocí `git add -f` pro herní nebo build data.
6. Commitněte zdroje a vytvořte odpovídající tag. Na GitHubu ručně vytvořte
   Release a popište změny, podporovaný profil a stav herního testování.
7. Přiložte pouze `dist/Ishar2-Cestina-<verze>.zip` a `dist/SHA256SUMS.txt`.

ZIP obsahuje finální EXE, krátký návod a vymezené licenční informace.
Nepřidávejte `build/installer-test.exe`, `patch_data.h`, celé přeložené
prostředky, zálohy hry nebo původní vstupy. Soukromé herní soubory neposílejte
ani do CI či build služby. Veřejný CI job kontroluje jen veřejné zdroje.

Pro zveřejnění repozitáře není potřeba ani vhodné commitovat připravený ZIP.
Konkrétní remote URL a GitHub účet nastaví správce projektu. Tento projekt
sám nic nepushuje ani nevytváří veřejný release.
