import streamlit as st
from utils import create_calculated_columns, calculate_index, get_nearest_trading_day, get_events, get_stocks
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


@st.cache_data(ttl=3600 * 24)
def fetch_data():
    df_all_tickers = create_calculated_columns()
    df_norm_index = calculate_index()
    events_df = get_events()
    swe_stocks, usa_stocks = get_stocks()
    return df_all_tickers, df_norm_index, events_df, swe_stocks, usa_stocks

df_all_tickers, df_norm_index, events_df, swe_stocks, usa_stocks = fetch_data()

df_all_tickers['Date'] = pd.to_datetime(df_all_tickers['Date'])
df_norm_index['Date'] = pd.to_datetime(df_norm_index['Date'])


st.set_page_config(
    page_title="Tidsresan",
    layout="wide"
)

st.title("Tidsresan")


# Date selection start --------------- #
if "selected_date" not in st.session_state:
    st.session_state.selected_date = dt.date(2015, 2, 18)
col1, col2, col3 = st.columns(3)
with col1:
    subcol1, subcol2, subcol3 = st.columns(3)
    with subcol1:
        if st.button("Hoppa 5 dagar"):
            st.session_state.selected_date += dt.timedelta(days=5)
    with subcol2:
        if st.button("Hoppa 10 dagar"):
            st.session_state.selected_date += dt.timedelta(days=10)
    with subcol3:
        if st.button("Hoppa 30 dagar"):
            st.session_state.selected_date += dt.timedelta(days=30)

col1, col2 = st.columns([5, 2])
with col1:
    selected_date = st.slider(
        "Välj ett datum",
        min_value=dt.date(2015, 2, 18),
        max_value=dt.date(2025, 12, 31),
        value=st.session_state.selected_date,
        format="YYYY-MM-DD"
    )
    if selected_date:
        st.session_state.selected_date = selected_date

    selected_ts = pd.Timestamp(selected_date)

    # Filter the frames
    df_norm_index_selected = df_norm_index[(df_norm_index['Date'] <= selected_ts) & (df_norm_index['Date'] >= "2015-01-01")]
    # Date selection end ----------------- #
    
    tab_2_1_index, tab_2_2_1_volume, tab_2_2_volatility, tab_2_3_stocks = st.tabs(["Indexutveckling", "Volymutveckling", "Volatilitet", "Aktier"])
    with tab_2_1_index:
        with st.expander("Indexjämförelse, information", expanded=False):
            st.markdown("""
            Här kan du se en jämförelse mellan de utvalda aktierna från svenska och amerikanska aktiemarknaden. 
            Grafen visar dels aktiernas **`indexutveckling`** under perioden 2015-2025 (linjerna), samt händelser som har varit relevanta under samma period (streck och stjärnor). Indexberäkningen bygger på **`normerade värden`**, d.v.s. alla aktiers ursprungliga värden normaliseras mot 2015. En uppgång motsvarar en ökning av indexvärdet, en nedgång motsvarar en minkande indexvärdet. \n
            Använd slidern ovan för att navigera mellan olika datum i tidslinjen, eller klicka dig fram 5, 10 eller 30 dagar med knapparna.
            """)
            
        # Find the maximum value for the Y-axis so we know where to place the stars
        if not df_norm_index_selected.empty:
            max_y_val = df_norm_index_selected["norm_close"].max()
            marker_y_pos = max_y_val * 1.05
        else:
            marker_y_pos = 100

        fig = px.line(
            df_norm_index_selected,
            x="Date", 
            y="norm_close", 
            color='Market', 
            title="Indexutveckling: Sverige vs USA",
            template="plotly_white"
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
                text=event_texts, 
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>%{text}<extra></extra>"
            ))


        st.plotly_chart(fig, use_container_width=True)
    
    with tab_2_2_1_volume:
        df_norm_index_selected = df_norm_index_selected.copy()
        with st.expander("Volymutveckling, information", expanded=True):
            st.markdown("""
                Här visas en jämförelse mellan utvalda aktier på den svenska och amerikanska aktiemarknaden.

                Staplarna visar **`handelsvolymen`** mellan 2015 och 2025 för vald marknad, det vill säga hur många aktier som har köpts och sålts under perioden. Hög volym betyder stort intresse och mycket handel, medan låg volym tyder på att marknaden är mer avvaktande. Linjen visar vald marknads **`index`**, vilket gör det lättare att se hur volymen förhåller sig till marknadens utveckling.

                Använd slidern ovan för att bläddra mellan datum, eller knapparna för att hoppa 5, 10 eller 30 dagar.  
                Välj även marknad nedan.
                """)
            market_choice_combined = st.radio("Välj marknad att analysera:", ["Sverige (urval)", "USA (urval)"])
            if market_choice_combined == "Sverige (urval)":
                combined_frame = df_norm_index_selected[df_norm_index_selected['Market'] == "SWE"].copy()
            else:
                combined_frame = df_norm_index_selected[df_norm_index_selected['Market'] == "USA"].copy()

        combined_frame = combined_frame[(combined_frame['Date'] <= selected_ts) & (combined_frame['Date'] >= "2015-01-01")]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Staplar för volym
        fig.add_trace(
            go.Bar(
                x=combined_frame['Date'],
                y=combined_frame['Volume'],
                name='Volym',
                opacity=0.7
            ),
            secondary_y=False
        )

        # Linje för index
        fig.add_trace(
            go.Scatter(
                x=combined_frame['Date'],   # Viktigt! annars fel
                y=combined_frame['norm_close'],
                name='Index',
                mode='lines',
            ),
            secondary_y=True
        )

        # Axis-titlar
        fig.update_xaxes(title_text="Datum")
        fig.update_yaxes(title_text="Total Volym", secondary_y=False)
        fig.update_yaxes(title_text="Indexvärde", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)
        
    with tab_2_2_volatility:
        df_norm_index_selected = df_norm_index_selected.copy()

        with st.expander("Volatilitet, information", expanded=False):
            st.markdown("""
            Här kan du se en jämförelse mellan de utvalda aktierna från svenska och amerikanska aktiemarknaden. 
            Grafen visar marknadernas **`volatilitet`** under perioden 2015-2025. Volatilitet mäter hur mycket priset svänger upp och ner över tid; \n
            * Hög volatilitet betyder stora, snabba förändringar (mer risk och potential) \n
            * Låg volatilitet indikerar stabila, små rörelser (mindre risk). \n
            Detta mäts ofta med **`standardavvikelse`** från medelvärdet för en given period, i detta fall beräknas måttet som 30-dagars historisk standardavvikelse. \n
            Använd slidern ovan för att navigera mellan olika datum i tidslinjen, eller klicka dig fram 5, 10 eller 30 dagar med knapparna.
            """)
        if selected_ts <= pd.Timestamp("2015-02-17"):
            st.warning("Ingen data tillgänglig för detta datum. Volatilitet beräknas som 30-dagars historisk standardavvikelse. Därför visas ingen volatilitet under de första 30 handelsdagarna i den analyserade perioden.", icon="⚠️")
        
        col_vol1, col_vol2 = st.columns(2)

        # Filter on selected date
        curr_omx_vol = df_norm_index_selected[df_norm_index_selected['Market'] == "SWE"].loc[df_norm_index_selected['Date'] <= selected_ts, 'Volatility'].iloc[-1]
        curr_nasdaq_vol = df_norm_index_selected[df_norm_index_selected['Market'] == "USA"].loc[df_norm_index_selected['Date'] <= selected_ts, 'Volatility'].iloc[-1]

        with col_vol1:
            st.metric("Sverige Volatilitet (Risk)", f"{curr_omx_vol:.1f}%", delta_color="inverse")
        with col_vol2:
            st.metric("USA Volatilitet (Risk)", f"{curr_nasdaq_vol:.1f}%", delta_color="inverse")

        # Area-chart to show historical fear
        vol_fig = make_subplots(specs=[[{"secondary_y": True}]])
        vol_fig.add_trace(go.Scatter(x=df_norm_index_selected[df_norm_index_selected['Market'] == "SWE"]['Date'], y=df_norm_index_selected[df_norm_index_selected['Market'] == "SWE"]['Volatility'], fill='tozeroy', name='Sverige', line_color='#005293'))
        vol_fig.add_trace(go.Scatter(x=df_norm_index_selected[df_norm_index_selected['Market'] == "USA"]['Date'], y=df_norm_index_selected[df_norm_index_selected['Market'] == "USA"]['Volatility'], fill='tozeroy', name='USA', line_color='#EF3340', opacity=0.5))
        vol_fig.update_layout(height=300, title="Historisk volatilitet", margin=dict(t=30, b=0))
        st.plotly_chart(vol_fig, use_container_width=True)

    with tab_2_3_stocks:
        with st.expander("Bolagsanalys, information", expanded=True):
            st.markdown("""
                I den här delen kan du jämföra **ett enskilt bolag** med de utvalda marknaderna som helhet.

                Börja med att välja vilken marknad du vill analysera – Sverige eller USA. Därefter väljer du ett bolag från listan.
                

                Grafen som visas jämför:
                - **Bolagets kursutveckling** (grön linje)
                - **Marknadens index** (grå streckad linje)

                Både bolaget och indexet är **`normerade`**, vilket betyder att de startar på samma nivå. Det gör det enkelt att se om bolaget har gått bättre eller sämre än marknaden över tid, oberoende av prisnivå.

                Om bolagets linje ligger över index har bolaget utvecklats starkare än marknaden. Ligger den under har bolaget gått svagare. Använd denna visualsiering för att snabbt få en känsla för bolagets relativa prestation.

                > :red[Observera att det kan förekomma aktier som inte varit börsnoterade under hela den analyserade perioden. Dessa visas först från och med det datum då de noterades!]

                """)

            # Select market
            market_choice = st.radio("Välj marknad att analysera:", ["Sverige (OMXS30-urval)", "USA (Nasdaq-urval)"], horizontal=True)

            if market_choice == "Sverige (OMXS30-urval)":
                stock_dict = swe_stocks
                raw_data = df_all_tickers[df_all_tickers['Market'] == "SWE"]
                comp_index = df_norm_index[df_norm_index['Market'] == "SWE"]
            else:
                stock_dict = usa_stocks
                raw_data = df_all_tickers[df_all_tickers['Market'] == "USA"]
                comp_index = df_norm_index[df_norm_index['Market'] == "USA"]

            # Select stock
            selected_ticker = st.selectbox("Välj bolag:", options=stock_dict.keys(), format_func=lambda x: stock_dict[x])

        if selected_ticker:
            # Get data for selected stock
            stock_df = (
                raw_data
                .loc[raw_data['Ticker'] == selected_ticker, ['Date', 'Close']]
                .sort_values('Date')
            )
            stock_df = stock_df[stock_df['Date'] > '2015-01-01']
            stock_df = stock_df[stock_df['Date'] <= selected_ts]

            index_df = comp_index[comp_index['Date'] <= selected_ts]
            
            # Normalize stock to start at the same level as the index for comparison
            if not stock_df.empty:
                stock_df['Normalized'] = stock_df['Close'] / stock_df['Close'].iloc[0]
                
                # Compare with index (which is already normalized in your 'index_value')
                comp_fig = go.Figure()
                
                # Stock line
                comp_fig.add_trace(go.Scatter(
                    x=stock_df['Date'], 
                    y=stock_df['Normalized'], 
                    name=stock_dict[selected_ticker],
                    line=dict(color='green', width=2)
                ))
                
                # Index line
                comp_fig.add_trace(go.Scatter(
                    x=index_df['Date'], 
                    y=index_df['norm_close'], 
                    name="Jämförelseindex",
                    line=dict(color='gray', dash='dot')
                ))
                
                comp_fig.update_layout(title=f"{stock_dict[selected_ticker]} vs Index (Normerat)", xaxis_title="")
                st.plotly_chart(comp_fig, use_container_width=True)

with col2:
    st.subheader("30 dagars förändringar")
    # Splitting the stock- and index-dataframes into Swe and USA
    df_all_swe = df_all_tickers[df_all_tickers['Market'] == "SWE"].dropna()
    df_all_usa = df_all_tickers[df_all_tickers['Market'] == "USA"].dropna()

    df_index_swe = df_norm_index[df_norm_index['Market'] == "SWE"].dropna()
    df_index_usa = df_norm_index[df_norm_index['Market'] == "USA"].dropna()

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

    col1, col2 = st.columns(2)
    with col1:
        col1.subheader("Sverige")
        st.metric(label="Index", value=f"{swe_index_value:.2f}%")
        st.metric(label=f"Vinnare: {winner_swe_name}", value=f"{winner_swe_value:.2f}%")
        st.metric(label=f"Förlorare: {loser_swe_name}", value=f"{loser_swe_value:.2f}%")
        
    with col2:
        col2.subheader("USA")
        st.metric(label="Index", value=f"{usa_index_value:.2f}%")
        st.metric(label=f"Vinnare: {winner_usa_name}", value=f"{winner_usa_value:.2f}%")
        st.metric(label=f"Förlorare: {loser_usa_name}", value=f"{loser_usa_value:.2f}%")
    
for _, row in events_df.iterrows():
    if row['date'] <= selected_ts:
        st.markdown(f"""
        #### :blue-background[{row['date'].date()} - {row['event']}]
        {row['description']}
        """)