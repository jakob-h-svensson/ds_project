import streamlit as st

info_page = st.Page(
    "info_page.py",
    title="Information om resan"
)

visualisation_page = st.Page(
    "visualisation_page.py",
    title="Tidsresan"
)

data_page = st.Page(
    "data_page.py",
    title="Projektmetodik & data"
)

pg = st.navigation([    
    info_page,
    visualisation_page,
    data_page
])

pg.run()