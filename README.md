**Projektetnamn**

Ekonomiresan

**Syfte**

Att med hjälp av Python undersöka hur börsen reagerar på stora geopolitiska och makroekonomiska händelser. Samt att visualisera detta i en interaktiv tidsresa.

**Metodik**

Jämförelse av två urvalsindex som jag själv har skapat, ett svenskt och ett amerikanskt, över perioden 2015-2025. Datan hämtas via yfinance, hanteras och bearbetas med hjälp av Pandas och lagras i en SQLite databas. Därefter sker visualiseringar med hjälp av Plotly och allt paketeras i en Streamlit applikation.

**Struktur**

`streamlit_app.py` - Huvudfil för applikationen. Här styrs applikationens struktur och flöde.

`utils.py` - Här samlas den huvudsakliga funktionaliteten för hämtning och bearbetning av data.

`info_page.py` - Används för att presentera information om projektet och ge användaren en överblick.

`visualisation_page.py` - Filen för att visualisera data.

`data_page.py` - Denna fil presenterar projektet och dess uppbyggnad i en Streamlit-sida.

`data` - Denna mapp innehåller events.csv som används för presentation av händelser.

`data/database` - Denna mapp innehåller tickers.sqlite, databasen där yfinance-datan sparas.

**Konfiguration**  
Se *requirements.txt* för applikationens krav och beroenden. Rekommenderade visnings-settings i Streamlit är "Light"
