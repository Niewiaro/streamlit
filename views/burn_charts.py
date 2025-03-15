import streamlit as st
import pandas as pd
import re
import random
import math


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
df["Wydajność"] = df["Wykonane"] / df["Zaplanowane"]

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
# chart_data_burn_down = pd.DataFrame(df["Pozostałe"])  # Konwersja na DataFrame

# Obliczamy idealne tempo wykonania na podstawie "Zaplanowane"
# chart_data_burn_down["Idealne"] = scope - df["Zaplanowane"].cumsum()
df["Idealne"] = scope - df["Zaplanowane"].cumsum()

st.caption("Tabela danych do wykresu.")
# st.table(chart_data_burn_down[["Idealne", "Pozostałe"]])
st.table(df[["Idealne", "Pozostałe"]])

st.line_chart(
    # chart_data_burn_down,
    df[["Idealne", "Pozostałe"]],
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

# chart_data_burn_up = pd.DataFrame(df["Wykonane"])
# chart_data_burn_up["Wykonane"] = chart_data_burn_up["Wykonane"].cumsum()
df["Wykonane łącznie"] = df["Wykonane"].cumsum()
# chart_data_burn_up["Łączna praca"] = scope + df["Nowe"].cumsum()
df["Praca łącznie"] = scope + df["Nowe"].cumsum()

st.caption("Tabela danych do wykresu.")
# st.table(chart_data_burn_up[["Łączna praca", "Wykonane"]])
st.table(df[["Praca łącznie", "Wykonane łącznie"]])

st.line_chart(
    # chart_data_burn_up,
    df[["Praca łącznie", "Wykonane łącznie"]],
    x_label="Czas [tygodnie]",
    y_label="Nakład pracy [ilość zadań]",
    color=["#0000FF", "#FF0000"],
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
        df[["Idealne", "Pozostałe"]],
        x_label="Czas [tygodnie]",
        y_label="Pozostały nakład pracy [ilość zadań]",
        color=["#0000FF", "#FF0000"],
    )
    st.caption("Wykres Burn-down.")

with col2:
    st.line_chart(
        df[["Praca łącznie", "Wykonane łącznie"]],
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


# Zadanie 4
st.header("Zadanie 4", divider=True)
st.subheader("Dodanie ryzyka w projekcie.", divider=True)
st.text(
    "Podczas realizacji projektu może dojść do zmian w zespole projektowym (dołączenie nowego członka lub rezygnacja kogoś z zespołu). Należy uwzględnić wpływ takiej zmiany na tempo realizacji zadań."
)


st.subheader("Nowy programista.", divider=True)

new_programmer_week = 4 if weeks >= 4 else weeks
new_programmer_week = st.slider(
    "Tydzień, w którym programista dołącza.", WEEKS_RANGE[0], weeks, new_programmer_week
)
new_programmer = 30
new_programmer = st.slider(
    "Procent o jaki podnosi przerób zadań.", 0, 100, new_programmer
)

df["Wykonane"] = df["Wykonane"].astype(float)
df.loc[df.index >= new_programmer_week, "Wykonane"] *= new_programmer / 100 + 1
df["Pozostałe"] = scope - df["Wykonane"].cumsum()

st.text(
    f"W {new_programmer_week} tygodniu pracy zespół zatrudnia nowego programistę, który pomaga w realizacji projektu. Podnosi on przerób zadań o {new_programmer}%."
)
st.caption(
    f"Tabela danych po zatrudnieniu programisty w {new_programmer_week} tygodniu."
)
st.table(df[["Idealne", "Wykonane", "Pozostałe"]])
st.line_chart(
    df[["Idealne", "Pozostałe"]],
    x_label="Czas [tygodnie]",
    y_label="Pozostały nakład pracy [ilość zadań]",
    color=["#0000FF", "#FF0000"],
)
st.caption("Wykres Burn-down.")


st.subheader("Utrata testera.", divider=True)

lose_tester_week = 5 if weeks >= 5 else weeks
lose_tester_week = st.slider(
    "Tydzień, w którym odchodzi tester.", WEEKS_RANGE[0], weeks, lose_tester_week
)
lose_tester = 80
lose_tester = st.slider("Procent o jaki spada przerób zadań.", 0, 100, lose_tester)

df.loc[df.index >= lose_tester_week, "Wykonane"] *= 1 - (lose_tester / 100)
df["Pozostałe"] = scope - df["Wykonane"].cumsum()
df["Wykonane łącznie"] = df["Wykonane"].cumsum()


st.text(
    f"W {lose_tester_week} tygodniu pracy zespół traci testera. Strata ta obniża przerób zadań o {lose_tester}%."
)
st.caption(f"Tabela danych po odejściu testera w {lose_tester_week} tygodniu.")
st.table(df[["Idealne", "Wykonane", "Pozostałe"]])
st.line_chart(
    df[["Idealne", "Pozostałe"]],
    x_label="Czas [tygodnie]",
    y_label="Pozostały nakład pracy [ilość zadań]",
    color=["#0000FF", "#FF0000"],
)
st.caption("Wykres Burn-down.")

zadanie4_output = df["Pozostałe"].iloc[-1]
if zadanie4_output > 0:
    zadanie4 = f"Mimo zatrudnienia programisty, utrata testera znacząco wpłynęła na realizację zadań i nie udało się dotrzymać terminu. Do sukcesu zabrakło realizacji {zadanie4_output:.2f} zadań."

else:
    zadanie4 = f"Mimo utraty testera, dzięki zatrudnieniu dodatkowego programisty spowodowało, że udało się dotrzymać terminu. Względem zaplanowanego scope zrealizowano dodatkowo {abs(zadanie4_output):.2f} zadań."

st.markdown(zadanie4)

# Zadanie 5
st.header("Zadanie 5", divider=True)
st.subheader("Usunięcie zadań.", divider=True)
st.text(
    "Podczas realizacji projektu może dojść do zmian w zespole projektowym (dołączenie nowego członka lub rezygnacja kogoś z zespołu). Należy uwzględnić wpływ takiej zmiany na tempo realizacji zadań."
)

deleted_tasks_week = 3 if weeks >= 3 else weeks
deleted_tasks_week = st.slider(
    "Tydzień, w którym usunięto zadania.", WEEKS_RANGE[0], weeks, deleted_tasks_week
)
deleted_tasks = 2
deleted_tasks = st.slider("Ilość usuniętych zadań.", 0, scope, deleted_tasks)

# df["Nowe"][deleted_tasks_week] -= deleted_tasks
df.loc[deleted_tasks_week, "Nowe"] -= deleted_tasks
df["Praca łącznie"] = scope + df["Nowe"].cumsum()
for i in range(1, len(df)):
    df.loc[i, "Pozostałe po sprincie"] = (
        df.loc[i - 1, "Pozostałe po sprincie"]
        - df.loc[i, "Wykonane"]
        + df.loc[i, "Nowe"]
    )

st.caption("Tabela danych do wykresu.")
st.table(df[["Praca łącznie", "Wykonane łącznie"]])

st.line_chart(
    df[["Praca łącznie", "Wykonane łącznie"]],
    x_label="Czas [tygodnie]",
    y_label="Nakład pracy [ilość zadań]",
    color=["#0000FF", "#FF0000"],
)
st.caption("Wykres Burn-up.")


zadanie5_output = df["Pozostałe po sprincie"].iloc[-1]
if zadanie5_output > 0:
    zadanie5 = f"Mimo usunięcia ze scope {deleted_tasks} zadań w {deleted_tasks_week} tygodniu nie udało się dotrzymać terminu. Do sukcesu zabrakło realizacji {zadanie5_output:.2f} zadań."

else:
    zadanie5 = f"Dzięki usunięciu ze scope {deleted_tasks} zadań w {deleted_tasks_week} tygodniu udało się dotrzymać terminu. Zrealizowano {scope} zaplanowanych oraz dodatkowo {abs(zadanie5_output):.2f} zadań."

st.markdown(zadanie5)


# Zadanie 6
st.header("Zadanie 6", divider=True)
st.subheader("Ocena wydajności zespołu.", divider=True)
st.text(
    "Na podstawie danych o ukończonych zadaniach, obliczyć średnią wydajność zespołu w każdym z tygodni."
)
st.latex(
    r"\text{Wydajność w danym tygodniu} = \frac{\text{Ukończone zadania}}{\text{Zaplanowane zadania}}"
)


df["Wydajność końcowa"] = df["Wykonane"] / df["Zaplanowane"]
# df["Wydajność końcowa"] = df["Wydajność końcowa"].apply(
#     lambda x: f"{x:.2%}" if pd.notna(x) else ""
# )

st.table(
    df[["Tydzień", "Wydajność", "Wydajność końcowa"]]
    .iloc[1:]
    .style.format({"Wydajność": "{:.2%}", "Wydajność końcowa": "{:.2%}"})
)

# st.dataframe(df[["Tydzień", "Wydajność", "Wydajność końcowa"]])

wydajnosc_mean = df["Wydajność"].mean()
wydajnosc_koncowa_mean = df["Wydajność końcowa"].mean()

finish = math.ceil(weeks / wydajnosc_mean)
finish_koncowa = math.ceil(weeks / wydajnosc_koncowa_mean)

st.subheader("Wydajność początkowa.", divider=True)

if finish <= weeks:
    zadanie6 = f"Przy wydajności średniej początkowej {wydajnosc_mean:.2%} plan zostanie zrealizowany w {finish} tygodni."
else:
    zadanie6 = f"Przez wydajność średnią początkową {wydajnosc_mean:.2%} plan nie zostanie zrealizowany w {weeks} tygodni. Można oszacować, że zespół zakończy pracę w łącznie {finish} tygodni."

st.markdown(zadanie6)


st.subheader("Wydajność końcowa.", divider=True)

if finish_koncowa <= weeks:
    zadanie6_koncowa = f"Przy wydajności średniej końcowej {wydajnosc_koncowa_mean:.2%} plan zostanie zrealizowany w {finish_koncowa} tygodni."
else:
    zadanie6_koncowa = f"Przez wydajność średnią końcową {wydajnosc_koncowa_mean:.2%} plan nie zostanie zrealizowany w {weeks} tygodni. Można oszacować, że zespół zakończy pracę w łącznie {finish_koncowa} tygodni."

st.markdown(zadanie6_koncowa)


# Zadanie 7
st.header("Zadanie 7", divider=True)
st.subheader("Poprawa tempa.", divider=True)
st.markdown(
    """
    Najważniejsze jest szybkie identyfikowanie problemów i wprowadzanie małych, ale skutecznych usprawnień. Aby poprawić tempo realizacji projektu w kolejnych tygodniach, warto skupić się na kilku kluczowych aspektach:

    1. **Lepsze planowanie sprintów** - upewnić się, że zadania są dobrze zdefiniowane i realnie oszacowane.  
    2. **Usuwanie blokad** - identyfikować przeszkody na Daily Scrum i eliminować je jak najszybciej.  
    3. **Poprawa jakości kodu** - ograniczyć dług techniczny, wdrożyć więcej testów automatycznych.  
    4. **Efektywniejsza współpraca** - usprawnić komunikację zespołową, unikać nadmiernych spotkań.  
    5. **Stabilność priorytetów** - unikać częstych zmian backlogu w trakcie sprintu.  
    """
)
