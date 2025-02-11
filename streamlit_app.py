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

pg = st.navigation(pages=[home_page, about_page, flashcards_page])

pg.run()
