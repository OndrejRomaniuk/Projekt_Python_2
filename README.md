# Engeto-pa-3-projekt
Třetí projekt na **Python Akademii od Engeta.**

## Popis projektu
Tento projekt slouží k extraahování výsledků parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete **[zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)**.

## Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

```bash
$ pip3 --version                             # overim verzi manazeru
$ pip3 install -r requirements.txt           # nainstalujeme knihovny
```

## Spuštění projektu
Spuštění souboru `election-scraper.py` v rámci příkazového řádku požaduje dva povinné argumenty.

```bash
python election-scraper.py <odkaz-uzemniho-celku> <vysledny-soubor>
```

Následně se vám stáhnou výsledky jako soubor s příponou `.csv`.

**!!!** Je **NUTNÉ** používat URL odkaz ze stránky **`Výsledky hlasování za územní celky – výběr územní úrovně`** pod symbolem **`X`** ve sloupci **`Výběr obce`**.

## Ukázka projektu
Výsledky hlasování v okrese Olomouc:

   1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102`
   2. argument: `vysledky_olomouc.csv`

Spuštění programu:

```bash
python election-scraper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102 vysledky_olomouc.csv
```

Průběh stahování:

```bash
STAHUJI DATA Z VYBRANEHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102
✅ UKLADAM DO SOUBORU: vysledky_olomouc.csv
UKONCUJI election-scraper
```

Částečný výstup:
```bash
Kód obce,Název obce,Registrovaní voliči,Odevzdané obálky,Platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
552356,Babice,370,256,254,13,0,0,10,0,18,25,1,5,2,1,0,17,0,5,79,0,0,9,0,0,2,0,66,1
500526,Bělkovice-Lašťany,1 801,1 078,1 069,97,0,0,83,1,44,81,18,6,15,1,1,104,0,32,333,1,2,75,0,6,8,1,153,7
...
```



