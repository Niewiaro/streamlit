import streamlit as st
import pandas as pd
import re
import random


st.title("Wykresy spalania")

# Nazwa projektu
st.header("Burn-down & Burn-up", divider=True)
st.subheader("Setup", divider=True)

WEEKS = 6
SCOPE = 60
ADDITIONAL_SUM = 5
ADDITIONAL_RANGE = (0, 2)

weeks = st.slider("Ilość tygodni", 1, 16, WEEKS)
scope = st.slider("Ilość zadań", 1, 200, SCOPE)

collect_numbers = lambda x: [int(i) for i in re.split("[^0-9]", x) if i != ""]

completed = (
    [10, 7, 8, 11, 15, 6]
    if weeks == WEEKS and scope == SCOPE
    else [
        random.randint(int(scope / weeks * 0.8), int(scope / weeks * 1.2))
        for _ in range(weeks)
    ]
)
completed_input = st.text_input(
    f"Zadania wykonane w każdym z {weeks} tygodni", completed
)
completed_list = collect_numbers(completed_input)
st.write(completed_list)

additional_range = st.slider(
    "Ilość dodatkowych zadań  w każdym z {weeks} tygodni", 0, 10, (0, 2)
)
additional = (
    [1, 2, 0, 1, 1, 0]
    if weeks == WEEKS and scope == SCOPE and additional_range == ADDITIONAL_RANGE
    else [random.randint(*additional_range) for _ in range(weeks)]
)
additional_input = st.text_input(
    f"Nowe zadania dodane w trakcie realizacji projektu w każdym z {weeks} tygodni",
    additional,
)
additional_list = collect_numbers(additional_input)
st.write(additional_list)
ADDITIONAL_SUM = sum(additional_list)


st.subheader("Treść zadania", divider=True)
st.markdown(
    f"""
    Zespół projektowy pracuje nad stworzeniem aplikacji mobilnej.
    Projekt trwa {weeks} tygodni ({weeks} sprintów po 1 tygodniu). Cały projekt ma {scope} zadań do wykonania.
    W trakcie realizacji projektu zespół może napotkać różne problemy, a jego wydajność może zmieniać się w zależności od trudności zadań i zmieniających się wymagań.

    - Projekt składa się z {scope} zadań (oraz _dodatkowo_ {ADDITIONAL_SUM} nowych, które będą dodane w trakcie realizacji projektu).
    - Zespół pracuje nad zadaniami przez {weeks} tygodni.
    - W każdym tygodniu zespół wykonuje część zadań, ale nie zawsze w pełni realizuje zaplanowane zadania.

    Zadanie należy realizować zgodnie z wytycznymi przedstawionymi w kolejnych etapach.
    """
)


df = pd.DataFrame(
    {
        # "Tydzień": [
        #     f"Tydzień {week}" if week != 0 else "Start" for week in range(weeks + 1)
        # ],
        # "Zaplanowane zadania": [
        #     scope / weeks if week != weeks else 0 for week in range(weeks + 1)
        # ],
        # "Zadania wykonane": [
        #     completed_list[week - 1] if week != 0 else 0 for week in range(weeks + 1)
        # ],
        "Tydzień": [f"Tydzień {week+1}" for week in range(weeks)],
        "Zaplanowane": [scope / weeks for _ in range(weeks)],
        "Wykonane": [int(completed_list[week]) for week in range(weeks)],
        "Pozostałe": "",
        "Nowe": [int(additional_list[week]) for week in range(weeks)],
        "Pozostałe po sprincie": "",
    }
)
df["Pozostałe"] = scope - df["Wykonane"].cumsum()

# Inicjalizacja pierwszej wartości
df.loc[0, "Pozostałe po sprincie"] = scope - df.loc[0, "Wykonane"] + df.loc[0, "Nowe"]

# Iteracyjne obliczanie dla kolejnych sprintów
for i in range(1, len(df)):
    df.loc[i, "Pozostałe po sprincie"] = (
        df.loc[i - 1, "Pozostałe po sprincie"]
        - df.loc[i, "Wykonane"]
        + df.loc[i, "Nowe"]
    )

st.table(df)
