import streamlit as st

home_page = st.Page(
    page="views/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

about_page = st.Page(
    page="views/about.py",
    title="About",
    icon=":material/info:",
)

project_card_page = st.Page(
    page="views/project_card.py",
    title="Project Card",
    icon=":material/playing_cards:",
)

burn_charts_page = st.Page(
    page="views/burn_charts.py",
    title="Burn-charts",
    icon=":material/local_fire_department:",
)

# pg = st.navigation(pages=[home_page, about_page, project_card_page])
pg = st.navigation(
    {
        "Main": [home_page, about_page],
        "Projects": [project_card_page, burn_charts_page],
    }
)

st.logo("assets/niewiaro.png")
st.sidebar.text("Made with ❤ by Niewiaro")

pg.run()
