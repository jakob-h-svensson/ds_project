import streamlit as st
from utils import extract_load

st.set_page_config(page_title="Data Science Project: Ekonomiresan", layout="centered")

st.title("Ekonomiresan: 10+ år av turbulens och tillväxt")
st.markdown("""
### En interaktiv visualisering av marknaden 2015–2025

Välkommen till **Ekonomiresan**. De senaste tio åren har varit några av de mest händelserika perioderna i modern ekonomisk historia. 
Vi har rört oss från en era av nollräntor och låg inflation, genom en global pandemi och leveranskedjekriser, till krig i Europa, energichocker och en explosiv AI-boom.

Denna applikation syftar till att besvara en central fråga:
> *Hur reagerar egentligen börsen på stora geopolitiska och makroekonomiska händelser?*

Genom att kombinera finansiell data med en tidslinje av nyhetshändelser kan du här utforska sambanden mellan rubrikerna och kursrörelserna.
""")

st.divider()

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("Marknaderna vi följer")
    st.markdown("""
    Analys görs av två distinkta marknader genom att jämföra några av de 30 mest tongivande bolagen från respektive marknad.
    
    **Urvalsindex Sverige**
    *Det svenska industriundret.*
    Listan innehåller de 30 mest omsatta aktierna på Stockholmsbörsen. Här dominerar verkstad (t.ex. Atlas Copco, Volvo), bank och traditionell industri, kompletterat med moderna tillväxtbolag som Evolution och Sinch.
    
    **Urvalsindex USA**
    *Den globala tillväxtmotorn.*
    Jag har valt ut några av de största och mest inflytelserika bolagen på Nasdaq-börsen. Här ser vi tydliga effekter av digitalisering och AI-utveckling genom jättar som Apple, Nvidia och Microsoft, men även bioteknik och modern handel.
    """)

with col_info2:
    st.subheader("Metodik & Data")
    st.markdown("""
    För att möjliggöra en rättvis jämförelse över tid har jag konstruerat egna index baserade på aktuella aktiekorgar:
    
    * **Normerad utveckling:** Alla aktiekurser är normerade från startdatumet. Indexet du ser i grafen är ett genomsnitt av den procentuella utvecklingen för bolagen i korgen.
    * **Data:** Datan hämtas via `yfinance`. yfinance är ett bibliotek som använder Yahoo Finance publika API:er för att hämta data.
    * **Datahantering:** Datan hämtas för lagring i en SQLite databas. Detta för att möjliggöra snabbare och mer stabil åtkomst för analysen.
    """)

st.info(
    """
    **Gå till sidan 'Tidsresan'** i menyfliken till vänster eller uppdatera databasen och gå vidare genom att klicka nedan för att starta 
    tidsresan. Använd tidsreglaget för att se hur världen – och din fiktiva portfölj – förändrades, månad för månad.
    
    """)

if st.button("Uppdatera databasen", width=170):
    return_message, status = extract_load()
    if status == "Success":
        st.success(return_message)
    else:
        st.error(return_message)

if st.button("Gå till Visualiseringar", width=170):
    st.switch_page("visualisation_page.py")
