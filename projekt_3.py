"""
projekt_3.py
author: Jakub Šabla
email: Sabla71006@mot.sps-dopravni.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def main():
    # 1. Kontrola zda je zadáno správně odkaz a název souboru jak se stáhne
    if len(sys.argv) != 3:
        print("CHYBA: Musíš zadat odkaz a název souboru.")
        print("Příklad: python projekt_3.py <odkaz> <vysledky.csv>")
        sys.exit()

    url_adresat = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    # Vzor vyžaduje přesně tento text na začátku
    print(f"ZÍSKÁVÁM DATA Z URL: {url_adresat}")
    
    # 2. Stažení dat ze stránky
    try:
        odpoved = requests.get(url_adresat)
        soup = BeautifulSoup(odpoved.text, 'html.parser')
    except Exception as e:
        print(f"Nepodařilo se načíst stránku: {e}")
        sys.exit()

    obce_data = []
    hlavicka = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    hlavicka_hotova = False

    odkaz_zaklad = "https://volby.cz/pls/ps2017nss/"
    radky = soup.find_all('tr')
    
    # 3. Procházení obcí
    for radek in radky:
        td_kod = radek.find('td', class_='cislo')
        td_nazev = radek.find('td', class_='overflow_name')

        if td_kod and td_nazev:
            kod = td_kod.text.strip()
            nazev = td_nazev.text.strip()
            
            relativni_link = td_kod.find('a')['href']
            odkaz_obec = odkaz_zaklad + relativni_link
            
            # Výpis každé stahované URL adrese obce
            print(f"ZÍSKÁVÁM DATA Z URL: {odkaz_obec}")
            
            res_obec = requests.get(odkaz_obec)
            soup_obec = BeautifulSoup(res_obec.text, 'html.parser')

            # Načtení základních počtů
            volici = soup_obec.find('td', headers='sa2').text.replace('\xa0', ' ').strip()
            obalky = soup_obec.find('td', headers='sa3').text.replace('\xa0', ' ').strip()
            hlasy = soup_obec.find('td', headers='sa6').text.replace('\xa0', ' ').strip()

            # Načtení názvů stran a procentuálních výsledků 
            strany_nazvy = soup_obec.find_all('td', headers=['t1sa1 t1sb2', 't2sa1 t2sb2'])
            
            # Vzor na obrázku ukládá procenta, bere sloupce s procenty
            strany_procenta = soup_obec.find_all('td', headers=['t1sa4 t1sb5', 't2sa4 t2sb5'])
            if not strany_procenta:
                # Záloha tabulek
                strany_procenta = soup_obec.find_all('td', headers=['t1sa3 t1sb4', 't2sa3 t2sb4'])

            if not hlavicka_hotova:
                for s in strany_nazvy:
                    hlavicka.append(s.text.strip())
                hlavicka_hotova = True

            radek_obce = [kod, nazev, volici, obalky, hlasy]
            for p in strany_procenta:
                radek_obce.append(p.text.replace('\xa0', ' ').strip())
            
            obce_data.append(radek_obce)

    # 4. Zápis do CSV
    print(f"UKLÁDÁM DATA DO SOUBORU: {vystupni_soubor}")
    with open(vystupni_soubor, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(hlavicka)
        writer.writerows(obce_data)
    
    print("DOKONČUJI: volby17.py")

if __name__ == "__main__":
    main()
