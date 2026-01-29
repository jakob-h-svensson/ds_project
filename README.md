**Projektetnamn**

Ekonomiresan

**Syfte**

Att med hjälp av Python undersöka hur börsen reagerar på stora geopolitiska och makroekonomiska händelser. Samt att visualisera detta i en interaktiv tidsresa.

**Metodik/Data**

Jämförelse av två urvalsindex som jag själv har skapat, ett svenskt och ett amerikanskt, över perioden 2015-2025. Datan som hämtas in är olika aktiedata (Stängningspris, Öppningspris, Högsta pris, Lägsta pris, Volym per datum och aktie) för perioden 2014-2025. Datan hämtas via yfinance och lagras i en SQLite databas. Utöver detta har jag även tagit fram data om stora geopolitiska och makroekonomiska händelser från en CSV-fil.



**Struktur**

`streamlit_app.py` - Huvudfil för applikationen. Här styrs applikationens struktur och flöde.

`utils.py` - Här samlas den huvudsakliga funktionaliteten för hämtning och bearbetning av data.

`info_page.py` - Används för att presentera information om projektet och ge användaren en överblick.

`visualisation_page.py` - Används för presentation av visualiseringar och interaktion med data.

`data_page.py` - Används för presentation av data och dess uppbyggnad.

`data` - Innehåller events.csv som används för presentation av händelser.

`data/database` - Innehåller tickers.sqlite, databasen där yfinance-datan sparas.

**Konfiguration**  
Se *requirements.txt* för applikationens krav och beroenden. Rekommenderade visnings-settings i Streamlit är "Light"
