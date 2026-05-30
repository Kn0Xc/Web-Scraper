# Projekt - Volební Scraper

Tento program slouží ke stahování výsledků voleb.

## Instalace (příklad u mě)

zadáte do CMD

1. pip install -r requirements.txt

2. cd C:\Users\jakub\OneDrive\Desktop\projekt_scraper (v průzkumníku souborů akorát zkopírujete cestu ke složce)

3. pip freeze > requirements.txt

## Spuštění
Program se spouští pomocí dvou parametrů:
1. Odkaz na územní celek
2. Název souboru, kam se data uloží (stáhne se soubor pojmenovaný tak jak jste zapsaly)

**Příklad:**
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"
