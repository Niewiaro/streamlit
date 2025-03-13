import streamlit as st
import pandas as pd
import re
import random


st.title("Wykresy spalania")

# Nazwa projektu
st.header("Burn-down & Burn-up", divider=True)
st.subheader("Setup", divider=True)

WEEKS_RANGE = (1, 16)
WEEKS = 6

SCOPE_RANGE = (1, 130)
SCOPE = 60

COMPLETED = [10, 7, 8, 11, 15, 6]
COMPLETED_RANDOM = (-3, 3)
COMPLETED_RANDOM_RANGE = (-10, 10)

ADDITIONAL = [1, 2, 0, 1, 1, 0]
ADDITIONAL_RANDOM = (0, 2)
ADDITIONAL_RANDOM_RANGE = (0, 10)
ADDITIONAL_SUM = 5
ADDITIONAL_RANGE = (0, 2)


# Weeks
weeks = st.slider("Ilość tygodni", *WEEKS_RANGE, WEEKS)
# Scope
scope = st.slider("Ilość zadań", *SCOPE_RANGE, SCOPE)


collect_numbers = lambda x: [int(i) for i in re.split("[^0-9]", x) if i != ""]

completed_list = [
    COMPLETED[week] if week < len(COMPLETED) else 0 for week in range(weeks)
]
additional_list = [
    ADDITIONAL[week] if week < len(ADDITIONAL) else 0 for week in range(weeks)
]

# Completed
completed_input = st.text_input(
    f"Zadania wykonane w każdym z {weeks} tygodni", completed_list
)
completed_list = collect_numbers(completed_input)


# Buttons Input or Random
col1, col2 = st.columns(2)
with col2:
    completed_random = st.slider(
        "Select a range of values", *COMPLETED_RANDOM_RANGE, COMPLETED_RANDOM
    )

left, right = st.columns(2)
if left.button(
    "Input Completed",
    type="primary",
    icon=":material/bookmark:",
    use_container_width=True,
):
    left.write(completed_list)

if right.button("Random", icon=":material/ifl:", use_container_width=True):
    completed_list = [
        random.randint(
            int(scope / weeks + completed_random[0]),
            int(scope / weeks + completed_random[1]),
        )
        for _ in range(weeks)
    ]
    right.write(completed_list)


# Additional
additional_input = st.text_input(
    f"Nowe zadania dodane w trakcie realizacji projektu w każdym z {weeks} tygodni",
    additional_list,
)
additional_list = collect_numbers(additional_input)

# Buttons Input or Random
col1, col2 = st.columns(2)
with col2:
    additional_random = st.slider(
        "Select a range of values", *ADDITIONAL_RANDOM_RANGE, ADDITIONAL_RANDOM
    )

left, right = st.columns(2)
if left.button(
    "Input Additional",
    type="primary",
    icon=":material/bookmark:",
    use_container_width=True,
):
    left.write(additional_list)

if right.button("Random", icon=":material/casino:", use_container_width=True):
    additional_list = [random.randint(*additional_random) for _ in range(weeks)]
    right.write(additional_list)

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

# Zadanie 2
st.header("Zadanie 2", divider=True)
st.subheader("Przygotowanie wykresu burn-up.", divider=True)

st.markdown(
    """
    Wykres burn-up pokazuje, jak zespół osiąga postęp w projekcie, uwzględniając również wprowadzenie nowych zadań. 

    1. Stworzenie wykresu burn-up dla projektu. Oś X to czas (tygodnie), a oś Y to całkowita liczba zrealizowanych zadań (łącznie z nowymi zadaniami).
    2. Na wykresie należy uwzględnić łączną liczbę ukończonych zadań dla każdego tygodnia (faktyczna realizacja) oraz łączną liczbę zadań wprowadzonych do projektu (łączna praca).
    """
)

chart_data_burn_up = pd.DataFrame(df["Wykonane"])
chart_data_burn_up["Wykonane"] = chart_data_burn_up["Wykonane"].cumsum()
chart_data_burn_up["Łączna praca"] = scope + df["Nowe"].cumsum()

st.caption("Tabela danych do wykresu.")
st.table(chart_data_burn_up[["Łączna praca", "Wykonane"]])

st.line_chart(
    chart_data_burn_up,
    x_label="Czas [tygodnie]",
    y_label="Nakład pracy [ilość zadań]",
    color=["#FF0000", "#0000FF"],
)
st.caption(
    "Wykres Burn-up, czyli przebieg wykonanych zadań do całkowitego nakładu pracy."
)

# Zadanie 3
st.header("Zadanie 3", divider=True)
st.subheader("Analiza i porównanie wykresów.", divider=True)

col1, col2 = st.columns(2)

with col1:
    st.line_chart(
        chart_data_burn_down,
        x_label="Czas [tygodnie]",
        y_label="Pozostały nakład pracy [ilość zadań]",
        color=["#0000FF", "#FF0000"],
    )
    st.caption("Wykres Burn-down.")

with col2:
    st.line_chart(
        chart_data_burn_up,
        x_label="Czas [tygodnie]",
        y_label="Nakład pracy [ilość zadań]",
        color=["#FF0000", "#0000FF"],
    )
    st.caption("Wykres Burn-up.")

completed_output = df["Pozostałe"].iloc[-1]

if completed_output > 0:
    zadanie3_burn_down = f"""
    Analizując wykres Burn-down można zauważyć, że praca zaplanowana nie została zrealizowana w wyznaczonym terminie.
    Pozostało {completed_output} nieukończonych zadań.
    """

elif completed_output < 0:
    zadanie3_burn_down = f"""
    Analizując wykres Burn-down można zauważyć, że praca zaplanowana została zrealizowana w wyznaczonym terminie.
    Ukończono {abs(completed_output)} więcej zadań niż zostało to zaplanowane.
    """

else:
    zadanie3_burn_down = "Analizując wykres Burn-down można zauważyć, że praca zaplanowana została zrealizowana w wyznaczonym terminie."

st.markdown(zadanie3_burn_down)

if ADDITIONAL_SUM == 0:
    zadanie3_burn_up = "Patrząc na wykres Burn-up widać, że przebieg łącznej pracy jest stały, co implikuje, że do scope zadań nie zostały dorzucone dodatkowe aktywności."

else:
    zadanie3_burn_up = f"Patrząc na wykres Burn-up widać, że przebieg łącznej pracy nie jest stały. Spowodowane to zostało dodaniem do scope {ADDITIONAL_SUM} zadań."

st.markdown(zadanie3_burn_up)
