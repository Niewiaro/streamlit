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
        "Tydzień": [
            f"Tydzień {week}" if week != 0 else "Start" for week in range(weeks + 1)
        ],
        "Zaplanowane": [scope / weeks if week != 0 else 0 for week in range(weeks + 1)],
        "Wykonane": [
            int(completed_list[week - 1]) if week != 0 else 0
            for week in range(weeks + 1)
        ],
        "Pozostałe": "",
        "Nowe": [
            int(additional_list[week - 1]) if week != 0 else 0
            for week in range(weeks + 1)
        ],
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
# st.dataframe(df)

# Zadanie 1
st.header("Zadanie 1", divider=True)
st.subheader("Przygotowanie wykresu burn-down.", divider=True)

st.markdown(
    """
    Wykres burn-down pokazuje, ile zadań pozostało do wykonania w projekcie na koniec każdego tygodnia.

    1. Wyznaczenie linii reprezentującej zaplanowaną liczbę zadań (tzn. ile zadań powinno być ukończone na koniec każdego tygodnia w idealnym scenariuszu realizacji projektu).
    2. Przygotowanie wykresu burn-down dla projektu na podstawie danych (faktyczna realizacja). Oś X to czas (tygodnie), a oś Y to liczba pozostałych zadań.
    """
)

# Tworzymy nowy DataFrame na potrzeby wykresu
chart_data_burn_down = pd.DataFrame(df["Pozostałe"])  # Konwersja na DataFrame

# Obliczamy idealne tempo wykonania na podstawie "Zaplanowane"
chart_data_burn_down["Idealne"] = scope - df["Zaplanowane"].cumsum()

st.caption("Tabela danych do wykresu.")
st.table(chart_data_burn_down[["Idealne", "Pozostałe"]])

st.line_chart(
    chart_data_burn_down,
    x_label="Czas [tygodnie]",
    y_label="Pozostały nakład pracy [ilość zadań]",
    color=["#0000FF", "#FF0000"],
)
st.caption(
    "Wykres Burn-down, czyli przebieg zaplanowany pierwotnie (idealnie) do faktycznego stanu w każdym z tygodni."
)

# # Realny burndown
# st.subheader(
#     "Jednak w praktyce ilość zadań zmienia się w trakcie sprintów.", divider=True
# )

# chart_data_burn_down_real = pd.DataFrame(df["Pozostałe po sprincie"])
# chart_data_burn_down_real["Realne"] = (
#     scope - df["Zaplanowane"].cumsum() + df["Nowe"].cumsum()
# )

# ordered_columns = ["Realne", "Pozostałe po sprincie"]  # Ustalona kolejność
# chart_data_burn_down_real = chart_data_burn_down_real[ordered_columns]

# st.caption("Tabela danych do wykresu.")
# st.table(chart_data_burn_down_real)

# st.line_chart(
#     chart_data_burn_down_real,
#     x_label="Czas [tygodnie]",
#     y_label="Pozostały nakład pracy [ilość zadań]",
#     color=["#FF0000", "#0000FF"],
# )
# st.caption(
#     "Wykres Burn-down, czyli przebieg zaplanowany (uwzględniając zmianę scope) do faktycznego stanu w każdym z tygodni."
# )
