"""
election-scraper.py: třetí projekt do Engeto Online Python Akademie

author: Ondřej Romaniuk
email: romaniuko73@gmail.com
"""

#LIBRARIES
from requests import get
from bs4 import BeautifulSoup as soup
import csv
import re
import sys

#VARIABLES
party_names = [                                                                                                 # fixed order of political parties
    "Občanská demokratická strana",
    "Řád národa - Vlastenecká unie",
    "CESTA ODPOVĚDNÉ SPOLEČNOSTI",
    "Česká str.sociálně demokrat.",
    "Radostné Česko",
    "STAROSTOVÉ A NEZÁVISLÍ",
    "Komunistická str.Čech a Moravy",
    "Strana zelených",
    "ROZUMNÍ-stop migraci,diktát.EU",
    "Strana svobodných občanů",
    "Blok proti islam.-Obran.domova",
    "Občanská demokratická aliance",
    "Česká pirátská strana",
    "Referendum o Evropské unii",
    "TOP 09",
    "ANO 2011",
    "Dobrá volba 2016",
    "SPR-Republ.str.Čsl. M.Sládka",
    "Křesť.demokr.unie-Čs.str.lid.",
    "Česká strana národně sociální",
    "REALISTÉ",
    "SPORTOVCI",
    "Dělnic.str.sociální spravedl.",
    "Svob.a př.dem.-T.Okamura (SPD)",
    "Strana Práv Občanů"
]

#DEF SUPP FUNCT.

def data_scrapper(url):                                                                                     ### FOR DIRECT SCRAPPING OF DATA FROM THE WEBSITE VOLBY.CZ ###
    """
    Downloads and processes election results from the municipality URL.

    Args:
        url (str): URL address of the election results page for a municipality.

    Returns:
        dict: A dictionary containing municipality information and party results.
              Keys include 'Kód obce' (Municipality Code), 'Název obce' (Municipality Name),
              'Registrovaní voliči' (Registered Voters), 'Odevzdané obálky' (Submitted Envelopes),
              'Platné hlasy' (Valid Votes), and political party names.
    """

    # function body
    answer = get(url)

    sep_html_muni = soup(answer.text, features="html.parser")                                                   # HTML page on municipality level

#DATA FROM URL
    code = url.split("xobec=")[-1].split("&")[0]                                                                # municipality code
    location = sep_html_muni.find_all("h3")[2].text.replace("Obec:", "").strip()                    # municipality name

# DATA VIA TAGS
    registered = sep_html_muni.find("td", attrs={'headers': 'sa2'})                                       # num. of registered voters
    envelopes = sep_html_muni.find_all('td', attrs={'headers': 'sa5'})                                    # num. of submitted envelopes
    valid = sep_html_muni.find_all('td', attrs={'headers': 'sa6'})                                        # num. of valid votes

# SAFETY FOR WEB CHANGES
    # Safely extract text content or use a fallback value ("N/A")
    # if the expected HTML elements are missing or empty.
    registered_text = registered.text if registered else "N/A"
    envelopes_text = envelopes[0].text if envelopes else "N/A"
    valid_text = valid[0].text if valid else "N/A"

# POLITICAL PARTIES AND VOTES
    votes = [td.text.strip() for td in
             sep_html_muni.find_all('td', headers=re.compile(r"^(t1sa2 t1sb3|t2sa2 t2sb3)$"))]            # votes per party

    party_results = dict(zip(party_names, votes))                                                               # union of lists (viz VARIABLES)

    return {                                                                                                    # dict with complete data per municipality
        "Kód obce": code,
        "Název obce": location,
        "Registrovaní voliči": registered_text,
        "Odevzdané obálky": envelopes_text,
        "Platné hlasy": valid_text,
        **party_results
    }

def csv_upload_all(arg_url, output_filename):                                                               ### UPLOADER FROM DATA_SCRAPPER TO CSV TABLES ###
    """
    Processes the regional URL and saves data from all municipalities into a CSV file.

    Args:
        arg_url (str): URL of the regional page containing municipality links.
        output_filename (str): Name of the output CSV file.

    Returns:
        None
    """
    # function body
    urls = municip_url_loader(arg_url)
    print(f"STAHUJI DATA Z VYBRANEHO URL: {arg_url}")

    with open(output_filename, mode="w", newline="", encoding="utf-8") as new_report:
        fieldnames = ["Kód obce", "Název obce", "Registrovaní voliči", "Odevzdané obálky", "Platné hlasy"] + party_names
        writer = csv.DictWriter(new_report, fieldnames=fieldnames)

        writer.writeheader()
        for url in urls:
            try:
                data = data_scrapper(url)

                for key, value in data.items():                                                                 # Replacement of non-breaking spaces everywhere in string values

                    if isinstance(value, str):
                        data[key] = value.replace('\xa0', ' ')

                writer.writerow(data)
            except Exception as e:
                print(f"Chyba při zpracování URL: {url}\n{e}")

def municip_url_loader(arg_url):                                                                            ### LOADER OF MUNICIPALITIES' URLs FROM REGIONAL PAGE ###
    """
    Loads and returns unique URLs of municipalities from a regional page.

    Args:
        arg_url (str): URL of the regional page.

    Returns:
        list[str]: List of URLs for individual municipalities.
    """
    # function body
    base_url = "https://www.volby.cz/pls/ps2017nss/"                                                            # regional URL provided by user (f.e. okres Prostějov, okres Přerov)

    base = get(arg_url)
    sep_html_base = soup(base.text, features="html.parser")

    raw_links = sep_html_base.find_all("td", class_="cislo",
                                       headers = re.compile(r"^(t1sa1 t1sb1|t2sa1 t2sb1|t3sa1 t3sb1)$"))

    seen = set()                                                                                                # set for removing duplicity URLs
    ordered_unique_urls = []                                                                                    # list for maintaining order

    for td in raw_links:
        a_tag = td.find("a")
        if a_tag:
            full_url = base_url + a_tag["href"]
            if full_url not in seen:
                seen.add(full_url)
                ordered_unique_urls.append(full_url)

    return ordered_unique_urls

if __name__ == "__main__":                                                                                  ### SCRIPT RUNNER ###
    if len(sys.argv) != 3:
        print(r"❌ Correct Usage: python election-scraper.py <REGIONAL_URL> <OUTPUT_FILENAME.csv>")
        sys.exit(1)

    arg_url = sys.argv[1]                                                                                       # 1st entry argument for script
    output_filename = sys.argv[2]                                                                               # 2nd entry argument for script

    csv_upload_all(arg_url, output_filename)
    print(f"""✅ UKLADAM DO SOUBORU: {output_filename}
UKONCUJI election-scraper""")
