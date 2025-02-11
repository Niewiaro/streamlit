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

flashcards_page = st.Page(
    page="views/flashcards.py",
    title="Flashcards",
    icon=":material/playing_cards:",
)

# pg = st.navigation(pages=[home_page, about_page, flashcards_page])
pg = st.navigation(
    {
        "Main": [home_page, about_page],
        "Projects": [flashcards_page],
    }
)

st.logo("assets/niewiaro.png")
st.sidebar.text("Made with ❤ by Niewiaro")

pg.run()
