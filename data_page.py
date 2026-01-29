import streamlit as st
from utils import extract_load, fetch_and_transform_data, get_events

st.set_page_config(
    page_title="Data",
    layout="centered"
)


# --------- DATA ---------
swe_stocks = {
    "ALFA.ST": "Alfa Laval",
    "ASSA-B.ST": "Assa Abloy",
    "ATCO-A.ST": "Atlas Copco A",
    "ATCO-B.ST": "Atlas Copco B",
    "AZN.ST": "AstraZeneca",
    "BOL.ST": "Boliden",
    "ELUX-B.ST": "Electrolux",
    "ERIC-B.ST": "Ericsson",
    "ESSITY-B.ST": "Essity",
    "GETI-B.ST": "Getinge",
    "HEXA-B.ST": "Hexagon",
    "HM-B.ST": "H&M",
    "INVE-B.ST": "Investor B",
    "NDA-SE.ST": "Nordea",
    "SAND.ST": "Sandvik",
    "SCA-B.ST": "SCA",
    "SEB-A.ST": "SEB A",
    "SHB-A.ST": "Handelsbanken A",
    "SKF-B.ST": "SKF B",
    "SSAB-A.ST": "SSAB A",
    "SWED-A.ST": "Swedbank A",
    "TELIA.ST": "Telia Company",
    "VOLV-B.ST": "Volvo B",
    "KINV-B.ST": "Kinnevik B",
    "LATO-B.ST": "Latour B",
    "NIBE-B.ST": "Nibe Industrier",
    "SAAB-B.ST": "Saab B",
    "LIFCO-B.ST": "Lifco B",
    "EVO.ST": "Evolution",
    "SINCH.ST": "Sinch"
}



# Data start and end dates
start = "2014-01-01"
start_journey = "2015-01-01"
end = "2025-12-31"


tickers = swe_stocks
market = "SWE"
df_long, unique_tickers = fetch_and_transform_data(tickers, start, end, market)


events = get_events()

st.markdown("""
**Projektetnamn**  \n Ekonomiresan  \n
**Syfte**  \n Att undersöka hur börsen reagerar på stora geopolitiska och makroekonomiska händelser. Samt att visualisera detta i en interaktiv tidsresa.  \n
**Metodik**  \n Jämförelse av två urvalsindex som jag själv har skapat, ett svenskt och ett amerikanskt, över perioden 2015-2025. Datan hämtas via yfinance, hanteras och bearbetas med hjälp av Pandas och lagras i en SQLite databas. Därefter sker visualiseringar med hjälp av Plotly och allt paketeras i en Streamlit applikation.  \n
**Struktur** \n
`streamlit_app.py` - Huvudfil för applikationen. Här styrs applikationens struktur och flöde.

`utils.py` - Här samlas den huvudsakliga funktionaliteten för hämtning och bearbetning av data.

`info_page.py` - Används för att presentera information om projektet och ge användaren en överblick.

`visualisation_page.py` - Används för presentation av visualiseringar och interaktion med data.

`data_page.py` - Används för presentation av data och dess uppbyggnad.

`data` - Innehåller events.csv som används för presentation av händelser.

`data/database` - Innehåller tickers.sqlite, databasen där yfinance-datan sparas.

**Konfiguration**  \n Se *requirements.txt* för applikationens krav och beroenden. Rekommenderade visnings-settings i Streamlit är "Light" \n
""")



st.write("Nedan följer en genomgång av funktionaliteten i applikationen och hur den är uppbyggd.")
with st.expander("### 0. Requirements", expanded=False):
    st.markdown("""
    streamlit>=1.36.0 \n
    pandas \n
    numpy \n
    yfinance \n
    plotly \n
    xgboost \n
    SQLAlchemy""")

#-------------------------------------------------------------------------
with st.expander("### 1. Förutsättningar", expanded=False):
    st.write("Grunddata och förutsättningar för att köra applikationen skapas:")
    code_settings = """
    # Defining tickers/stocks
    swe_stocks = {
        "ALFA.ST": "Alfa Laval",
        "ASSA-B.ST": "Assa Abloy",
        "ATCO-A.ST": "Atlas Copco A",
        "ATCO-B.ST": "Atlas Copco B",
        "AZN.ST": "AstraZeneca",
        "BOL.ST": "Boliden",
        "ELUX-B.ST": "Electrolux",
        "ERIC-B.ST": "Ericsson",
        "ESSITY-B.ST": "Essity",
        "GETI-B.ST": "Getinge",
        "HEXA-B.ST": "Hexagon",
        "HM-B.ST": "H&M",
        "INVE-B.ST": "Investor B",
        "NDA-SE.ST": "Nordea",
        "SAND.ST": "Sandvik",
        "SCA-B.ST": "SCA",
        "SEB-A.ST": "SEB A",
        "SHB-A.ST": "Handelsbanken A",
        "SKF-B.ST": "SKF B",
        "SSAB-A.ST": "SSAB A",
        "SWED-A.ST": "Swedbank A",
        "TELIA.ST": "Telia Company",
        "VOLV-B.ST": "Volvo B",
        "KINV-B.ST": "Kinnevik B",
        "LATO-B.ST": "Latour B",
        "NIBE-B.ST": "Nibe Industrier",
        "SAAB-B.ST": "Saab B",
        "LIFCO-B.ST": "Lifco B",
        "EVO.ST": "Evolution",
        "SINCH.ST": "Sinch"
    }

    usa_stocks = {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet",
        "AMZN": "Amazon",
        "META": "Meta Platforms",
        "NVDA": "Nvidia",
        "TSLA": "Tesla",
        "AVGO": "Broadcom",
        "INTC": "Intel",
        "AMD": "Advanced Micro Devices",
        "CSCO": "Cisco Systems",
        "PEP": "PepsiCo",
        "COST": "Costco Wholesale",
        "ADBE": "Adobe",
        "NFLX": "Netflix",
        "TXN": "Texas Instruments",
        "QCOM": "Qualcomm",
        "AMGN": "Amgen",
        "HON": "Honeywell",
        "INTU": "Intuit",
        "MDLZ": "Mondelez International",
        "SBUX": "Starbucks",
        "BKNG": "Booking Holdings",
        "GILD": "Gilead Sciences",
        "ISRG": "Intuitive Surgical",
        "LRCX": "Lam Research",
        "MU": "Micron Technology",
        "REGN": "Regeneron Pharmaceuticals",
        "VRTX": "Vertex Pharmaceuticals",
        "ADP": "Automatic Data Processing"
    }

    # Data start and end dates
    start = "2014-01-01"
    start_journey = "2015-01-01"
    end = "2025-12-31"
    """
    st.code(code_settings, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
with st.expander("### 2. Hämta data från yfinance", expanded=False):
    st.write("Här hämtas data från yfinance. Eftersom datan kommer i multi-index format, används stack för att få den i en enkel dataframe:")
    code_fetch_data = """
    def fetch_and_transform_data(tickers, start, end, market):
    #Fetch data from yfinance and return:
    #- Long-format price dataframe
    #- Unique tickers dataframe with market info

    list_tickers = []
    unique_tickers = {} 
    
    for ticker, name in tickers.items():
        list_tickers.append(ticker)
    try:
        df = yf.download(
            list_tickers,
            start=start,
            end=end,
            progress=False
        )
    
        df_long = df.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index()
        

        for i in df_long['Ticker'].unique():
            unique_tickers[i] = market
        
        unique_tickers = pd.DataFrame(unique_tickers.items(), columns=["Ticker", "Market"])

        return df_long, unique_tickers
        
    except Exception as e:
        print(e)
        return "Data not fetched"
    """
    st.code(code_fetch_data, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")
    st.write("Så här ser den hämtade datan (df_long) ut i sin råa form:")
    st.dataframe(df_long.head())
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
with st.expander("### 3. Load till SQL-databas", expanded=False):
    st.write("Jag har skapat en gemensam funktion för att interagera med databasen, denna används dels för att skriva hämtad data till databasen, dels för att läsa in data från databasen.")
    code_close_and_volume = """
    def interact_with_db(interaction, purpose, table=None, list_tickers=None, tickers=None, ticker_values=None): 
        #Interacting with the database, takes interaction, purpose, table, list_tickers, tickers and desired 
        #ticker_values as arguments. Returns a dataframe or a string

        conn = get_db_connection()
        
        # Creating WHERE clause
        where_clause = ""
        if list_tickers:
            where_clause = f"WHERE ticker_name IN ({', '.join(['"' + ticker + '"' for ticker in list_tickers])})"
        
        # Reading from the database
        ## Getting tickers (potentially a future feature where user can select any tickers for comparison)
        if interaction == "read" and purpose == "get tickers":
            return pd.read_sql(f"SELECT * FROM tickers", conn)
        
        ## Getting ticker values
        if interaction == "read" and purpose == "get values":

            query = 
            SELECT 
                ticker_price.Date,
                ticker_price.Ticker,
                ticker_price.Open,
                ticker_price.High,
                ticker_price.Low,
                ticker_price.Close,
                ticker_price.Volume,
                tickers.Market
            FROM ticker_price
            JOIN tickers ON ticker_price.Ticker = tickers.Ticker
            {where_clause}
            
            return pd.read_sql(query, conn)
            

        # Writing to the database
        ## Posting tickers and prices
        if interaction == "write" and purpose == "post tickers":
            try:
                tickers.to_sql(
                    name=table,
                    con=conn,
                    if_exists="append",
                    index=False
                )
                return True
            except Exception as e:
                print(f"Error writing to {table}: {e}")
                raise
        """
    st.code(code_close_and_volume, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")
    st.write("Funktionen **extract_load()** använder sig av **interact_with_db()** och **fetch_and_transform_data()** ovan för att hämta data från yfinance och lagra data i databasen.")
    code_extract_load = """
    def extract_load():
        # Extracting data from yfinance and loading it into the database

        try:
            data_swe, unique_tickers_swe = fetch_and_transform_data(swe_stocks, start, end, market="SWE")
            return1 = interact_with_db("write", "post tickers", table="ticker_price", tickers=data_swe)
            return2 = interact_with_db("write", "post tickers", table="tickers", tickers=unique_tickers_swe)

            data_usa, unique_tickers_usa = fetch_and_transform_data(usa_stocks, start, end, market="USA")
            return3 = interact_with_db("write", "post tickers", table="ticker_price", tickers=data_usa)
            return4 = interact_with_db("write", "post tickers", table="tickers", tickers=unique_tickers_usa)

            
            if all([return1, return2, return3, return4]):
                return "Data extracted, transformed and loaded successfully"
            else:
                return "Data extraction, transformation or loading failed"
                
        except Exception as e:
            print(e)
            return f"Data extraction, transformation or loading failed: {e}"
        """
    st.code(code_extract_load, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")


with st.expander("### 4. Bearbetning av data från databasen", expanded=False):
    st.write("Här hämtas aktielistorna från databasen och en beräkning görs av förändring de senaste 30 dagarnas stängningsvärde för varje enskild aktie, denna information presenteras sedan baserat på valt datum i slidern. Funktionen använder sig av **interact_with_db()** för att hämta data från databasen. För själva beräkningen används **.transform()** med **lambda** - för varje rad i dataframen kontrolleras förändringen i % jämfört med samma värde för 30 rader/handelsdagar tidigare.")
    code_create_calculated_columns = """
        def create_calculated_columns():
            df_all_tickers = interact_with_db("read", "get values")
            df_all_tickers = df_all_tickers.copy()
            df_all_tickers['pct_change_30'] = df_all_tickers.groupby('Ticker')['Close'].transform(lambda x: x.pct_change(periods=30))
            return df_all_tickers
        """
    st.code(code_create_calculated_columns, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")
    st.markdown(f"Här beräknas ett **marknadsindex** samt dess **volatilitet (risk)**. Först tas den dagliga avkastningen fram genom att jämföra indexets stängningsvärde mot föregående dag. Därefter beräknas volatiliteten genom att använda **.transform()** med **lambda**. För varje marknad beräknas standardavvikelsen på den dagliga avkastningen över ett rullande fönster på 30 dagar **(.rolling(30).std())**.  \n \n Slutligen skalas detta värde upp till årsbasis genom att multipliceras med roten ur 252 (genomsnittligt antal handelsdagar på ett år) och presenteras i procent.")
    code_calculate_index = """
    def calculate_index():
        # Reading from DB. Sorting by ticker/date and filtering to keep data from start_journey onwards
        df_long = interact_with_db("read", "get values")
        df_long = df_long.sort_values(["Ticker", "Date"]).copy()
        df_long = df_long[df_long['Date'] >= start_journey]

        # Normalizing the closing price for each ticker
        df_long["norm_close"] = df_long.groupby(["Ticker", 'Market'])["Close"].transform(
            lambda x: x / x.iloc[0]
        )


        # Calculating the index using the mean of the normalized closing price, and summing the volume for each market and date.
        # Mean values are used to get equally weighted averages (all tickers have the same weight). 
        df_norm_index = df_long.groupby(["Date", "Market"]).agg({
            "norm_close": "mean",
            "Volume": "sum"}).reset_index()


        # Calculates the volatility of the index.
        ## Starting with daily return
        df_norm_index['Daily_return'] = df_norm_index.groupby('Market')['norm_close'].pct_change()

        ## Then calculating rolling standard deviation (risk) and getting yearly volatility (x root of 252 trading days)
        df_norm_index['Volatility'] = df_norm_index.groupby('Market')['Daily_return'].transform(
            lambda x: x.rolling(30).std() * (252**0.5) * 100
        )

        # Calculates the percentage change of the index column over the last 30 days.
        df_norm_index['Pct_change_30'] = df_norm_index.groupby('Market')['norm_close'].transform(lambda x: x.pct_change(periods=30))
        return df_norm_index
        """
    st.code(code_calculate_index, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")

    st.markdown("Ovan funktioner används för visualiseringar och för beräkning av KPIer. För visualiseringar används även funktionen **get_events()**, som hämtar händelser under perioden som bedömts påverka marknaden. Händelserna har jag valt att ha i en enkel CSV-fil.")
    code_get_events = """
    def get_events():
        events_df = pd.read_csv(f"{PROCESSED_DATA_PATH}/events.csv")
        events_df["date"] = pd.to_datetime(events_df["date"])
        events_df = events_df.sort_values("date", ascending=False)
        return events_df
    """
    st.code(code_get_events, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")
    
    st.write("Så här är events_df uppbyggd:")
    st.dataframe(events.head())

with st.expander("### 5. Visualiseringar", expanded=False):
    st.markdown("""
    1. Visualiseringarna presenteras i fyra olika flikar (Marknadsindex, Volatilitet, Volymutveckling, Aktier)
        Innehållet i samtliga flikar är styrda av vilket datum användaren valt i slidern. D.v.s. endast datum från "starten av resan" fram till valt datum filtreras fram. Nedan följer hur logiken kring datumväljaren är uppbyggd:
    """)

    code_slider = """
        selected_date = st.slider(
        "Välj ett datum",
        min_value=dt.date(2015, 1, 2),
        max_value=dt.date(2025, 12, 31),
        value=st.session_state.selected_date,
        format="YYYY-MM-DD"
        )

        if selected_date:
            st.session_state.selected_date = selected_date

        selected_ts = pd.Timestamp(selected_date)

        # Filter the frames
        df_norm_index_selected = df_norm_index[(df_norm_index['Date'] <= selected_ts) & (df_norm_index['Date'] >= "2015-01-01")]
    """
    st.code(code_slider, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")

    st.markdown("""
    2. Därefter definierar jag utseende på min visualisering (grunden). Jag använder **Plotly Express** för att skapa ett linjediagram för de båda marknaderna (Sverige och USA). Därefter uppdaterar jag layouten med läsbar titel för y-axeln.
    Linjeförklaringarna flyttar jag till övre högra hörnet av diagrammet och tar bort titel med hjälp av **legend**.
    
        Jag lägger även till en **hovermode** för att att kunna se båda linjernas värde när jag för muspekaren över diagrammet någonstans på x-axeln.
        **margin** justeras för att göra plats för titeln.
    """)

    code_fig_base = """
        fig = px.line(
            df_norm_index_selected,
            x="Date", 
            y="norm_close", 
            color='Market', 
            title="Indexutveckling: Sverige vs USA",
            template="plotly_white",
            color_discrete_map={"Sverige": "#005293", "USA": "#EF3340"}
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Index",
            legend=dict(
                orientation="h",
                yanchor="bottom", 
                y=1.02,
                xanchor="right", 
                x=1,
                title=None
            ),
            hovermode="x unified",
            margin=dict(t=80)
        )
    """
    st.code(code_fig_base, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")

    st.markdown("""
        3. För att plotta ut händelserna på diagrammet, behöver jag matcha in dem på tidslinjen (x-axeln) i takt med att de dyker upp.
        
            Jag loopar igenom alla händelser i events_df. För varje händelse som inträffat fram till och med det valda datumet (**selected_ts**), ritas vertikal linje (**add_vline**) på x-axeln.
            
            Listorna **event_dates** och **event_texts** fylls i loopen och används som underlag för att plotta ut symboler (stjärnor) för varje händelse på diagrammet med hjälp av **go.Scatter**. Stjärnorna placeras längs x-axeln, och på en fast y-position (**marker_y_pos**).

            Jag hittade även en hovertemplate som visar just den specifika händelsens datum och beskrivning när användaren för muspekaren över stjärnan. Därefter ritas grafen upp.
    """)

    code_fig_events_plot = """
        # Events logic
        event_dates = []
        event_texts = []

        # Looping through events and adding vertical lines for each event on the x axis
        for _, row in events_df.iterrows():
            if row['date'] <= selected_ts:
                fig.add_vline(
                    x=row["date"],
                    line_width=1,
                    line_dash="dot",
                    line_color="grey",
                    opacity=0.5,
                )

                # Only add events to the lists if they are within the last 6 months, for cleaner display
                if row['date'] >= selected_ts - dt.timedelta(days=182):
                    event_dates.append(row['date'])
                    event_texts.append(row['event'])

        # Adding a star symbol for each event on the x axis
        if event_dates:
            fig.add_trace(go.Scatter(
                x=event_dates,
                y=[marker_y_pos] * len(event_dates), 
                mode='markers', 
                name='Händelser',
                marker=dict(
                    symbol='star', 
                    size=12,
                    color='#EF3340', 
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                text=scatter_texts, 
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>%{text}<extra></extra>"
            ))


        st.plotly_chart(fig, use_container_width=True)
    """
    st.code(code_fig_events_plot, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")

    st.markdown("""
        4. På visualiseringssidorna finns även KPIer som är baserade på valt datum. Dessa visar indexutvecklingen senaste 30 dagarna för de olika marknaderna. Samt högsta och lägsta prisutveckling för enskilda aktier för samma period.
        """)

    code_fig_kpi = """
        # Splitting the stock- and index-dataframes into Swe and USA
        df_all_swe = df_all_tickers[df_all_tickers['Market'] == "SWE"]
        df_all_usa = df_all_tickers[df_all_tickers['Market'] == "USA"]

        df_index_swe = df_norm_index[df_norm_index['Market'] == "SWE"]
        df_index_usa = df_norm_index[df_norm_index['Market'] == "USA"]

        # Filtering the frames based on selected date
        swe_row = get_nearest_trading_day(df_all_swe, selected_ts)
        usa_row = get_nearest_trading_day(df_all_usa, selected_ts)

        swe_row = swe_row.dropna()
        usa_row = usa_row.dropna()

        swe_index_row = get_nearest_trading_day(df_index_swe, selected_ts)
        usa_index_row = get_nearest_trading_day(df_index_usa, selected_ts)

        # Finding all the tickers and pct change values for the date
        sorted_swe = df_all_swe[['Ticker', 'pct_change_30']][df_all_swe['Date'] == swe_row.name].sort_values(by='pct_change_30', ascending=False)
        sorted_usa = df_all_usa[['Ticker', 'pct_change_30']][df_all_usa['Date'] == usa_row.name].sort_values(by='pct_change_30', ascending=False)

        # Getting the index value and the top and bottom tickers for the date
        swe_index_value = swe_index_row['Pct_change_30']*100
        winner_swe_name = swe_stocks[sorted_swe['Ticker'].iloc[0]]
        winner_swe_value = sorted_swe['pct_change_30'].iloc[0] * 100
        loser_swe_name = swe_stocks[sorted_swe['Ticker'].iloc[-1]]
        loser_swe_value = sorted_swe['pct_change_30'].iloc[-1] * 100

        usa_index_value = usa_index_row['Pct_change_30']*100
        winner_usa_name = usa_stocks[sorted_usa['Ticker'].iloc[0]]
        winner_usa_value = sorted_usa['pct_change_30'].iloc[0]*100
        loser_usa_name = usa_stocks[sorted_usa['Ticker'].iloc[-1]]
        loser_usa_value = sorted_usa['pct_change_30'].iloc[-1]*100
    """
    st.code(code_fig_kpi, language="python", line_numbers=False, wrap_lines=False, height="content", width="stretch")


