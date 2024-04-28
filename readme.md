# Repozitář k diplomové práci vyhodnocení agentů hlubokého Q-učení pomocí testu algoritmického IQ
- Vysoká škola ekonomická v Praze Fakulta informatiky a statistiky
- Studijní program: Znalostní a webové technologie
- Autor: Bc. Michal Dvořák
- Vedoucí práce: Ing. Ondřej Vadinský, Ph.D.
- Praha, červen 2024

### Struktura
- Adresář [`AIQ-test`](AIQ-test) obsahuje kód AIQ společně s:
  - Kodém `DQ_l` a `DDQ_l` agentů a jejich podůrných kódů:
    - [`DQ_l` agent](AIQ-test/agents/DQ_l.py)
    - [`DDQ_l` agent](AIQ-test/agents/DDQ_l.py)
    - podpůrný kód [`deepq_l`](AIQ-test/agents/deepq_l)
  - Mechanismem pro evoluční vyhledávání:
    - hlavní skript[`FindParamsGenetic.py`](AIQ-test/FindParamsGenetic.py)
    - adresář s hlavní logikou [`genetics`](AIQ-test/genetics)
- adresář [`vysledky-experimentu`](vysledky-experimentu) obsahuje všechna data k experimentům z diplomové práce. Jedná se o:
  - Logy z evolučního prohledávání agentů hlubokého Q-učení [`logy-evolucniho-prohledavani`](vysledky-experimentu/logy-evolucniho-prohledavani).
  - Porovnání nalezených konfigurací proti konfiguraci z původního článku agenta `DQ_l` [`evoluce-vs-clanek-dql`](vysledky-experimentu/evoluce-vs-clanek-dql).
  - Porovnání nalezených konfigurací proti konfiguraci z původního článku agenta `DDQ_l` [`evoluce-vs-clanek-ddql`](vysledky-experimentu/evoluce-vs-clanek-ddql).
  - Porovnání agentů `DQ_l` a `DDQ_l` mezi sebou s konfigurací z původního článku [`dql-clanek-vs-ddql-clanek`](vysledky-experimentu/dql-clanek-vs-ddql-clanek).
  - Porovnání agentů `DQ_l` a `DDQ_l` mezi sebou s konfigurací z evolučního prohledávání [`nejlepsi-dql-vs-nejlepsi-ddql`](vysledky-experimentu/nejlepsi-dql-vs-nejlepsi-ddql).
  - Porovnání agentů `Q_l`, `DQ_l` a `DDQ_l` mezi sebou se statickou hodnotou epsilon [`ql-vs-dql-vs-ddql-staticke-epsilon`](vysledky-experimentu/ql-vs-dql-vs-ddql-staticke-epsilon).
  - Finální porovnání všech agentů AIQ testu s jejich nejlepšími konfiguracemi [`nejlepsi-konfigurace-agentu`](vysledky-experimentu/nejlepsi-konfigurace-agentu).