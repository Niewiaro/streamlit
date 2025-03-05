import streamlit as st
import pandas as pd

st.title("Karta projektu")

# Nazwa projektu
st.header("Nazwa projektu", divider=True)
st.subheader("_AI excellence employee match_")

# Uzasadnienie / tło
st.header("Uzasadnienie / tło", divider=True)
st.subheader(
    "Po co chcemy realizować taki projekt i czy jesteśmy go w stanie zrealizować?",
    divider=True,
)
st.markdown(
    """
    Projekt ma na celu wspieranie wysokiego szczebla zarządzania w skutecznym odnajdywaniu idealnych kandydatów do konkretnych zadań.
    Dodatkowo otworzy on pętlę feedbacku dla pracowników, umożliwiając im rozwój w obszarach zgodnych z ich zainteresowaniami i kompetencjami.
    Dzięki zastosowaniu przyjaznej dla użytkownika sztucznej inteligencji projekt wpłynie na poprawę jakości pracy oraz zwiększenie satysfakcji zawodowej.
    """
)
st.subheader("Jakie będą konsekwencje jeśli nie uda się go wykonać?", divider=True)
st.markdown(
    """
    Najgorszym scenariuszem dla tego projektu jest utrzymanie obecnego modelu zarządzania, w którym menedżerowie kierują swoimi zespołami w tradycyjny sposób.
    Obecne podejście znacząco ogranicza możliwość wysokopoziomowego wglądu w kompetencje pracowników oraz utrudnia interakcje na poziomie „skip-level”,
    co może hamować efektywne dopasowanie talentów do potrzeb organizacji.
    """
)

# Cele
st.header("Cele", divider=True)
st.subheader(
    "Rezultaty jakie planujemy osiągnąć poprzez realizację projektu określone zgodnie z metodą SMART:",
    divider=True,
)
st.markdown(
    """
    - Tworzenie listy najbardziej dopasowanych kandydatów na podstawie określonych parametrów.
    - Webowa platforma dostępna wewnątrz firmy.
    - Intuicyjny i łatwy w obsłudze interfejs użytkownika.
    - Zakładany czas realizacji: 4 man weeks.
    - Usprawnienie procesu wyszukiwania odpowiedniego kandydata do danego zadania.
    - Lepsza i bardziej przejrzysta ścieżka rozwoju dla pracowników.
    """
)

# Opis
st.header("Opis", divider=True)
st.subheader(
    "To, co chcemy osiągnąć realizując projekt",
    divider=True,
)
st.markdown(
    """
    Projekt zakłada stworzenie nowoczesnej platformy, która umożliwi wysokiemu szczeblowi zarządzania skuteczne i przejrzyste zarządzanie pracownikami na wszystkich poziomach organizacji. Celem rozwiązania jest usprawnienie procesu identyfikacji i przypisywania najlepszych kandydatów do konkretnych zadań na podstawie precyzyjnie określonych kryteriów wyszukiwania.

    Dzięki zastosowaniu zaawansowanej sztucznej inteligencji system automatycznie analizuje dostępne dane i generuje listę najbardziej odpowiednich kandydatów, uwzględniając ich kompetencje, doświadczenie, preferencje zawodowe oraz potrzeby organizacyjne. Proces ten odbywa się w sposób intuicyjny i przyjazny dla użytkownika, eliminując konieczność ręcznego przeszukiwania profili pracowników i minimalizując ryzyko subiektywnych decyzji kadrowych.

    Platforma, dostępna w ramach wewnętrznego systemu firmy, zapewni wysoką użyteczność poprzez intuicyjny interfejs oraz czytelny sposób prezentacji wyników. Użytkownicy będą mieli możliwość filtrowania, sortowania i dostosowywania wyników w czasie rzeczywistym, co znacząco przyspieszy podejmowanie decyzji dotyczących alokacji zasobów ludzkich.

    Wdrożenie tego rozwiązania przyniesie korzyści na kilku poziomach. Z jednej strony usprawni proces zarządzania zasobami ludzkimi, zwiększając efektywność i transparentność podejmowanych decyzji. Z drugiej strony stworzy bardziej dynamiczną ścieżkę rozwoju dla pracowników, umożliwiając im angażowanie się w projekty zgodne z ich kompetencjami i aspiracjami.

    Dzięki platformie firma zyska możliwość lepszego wykorzystania talentów i kompetencji wewnętrznych, co przełoży się na wzrost produktywności, większą satysfakcję pracowników oraz bardziej efektywne zarządzanie zasobami ludzkimi w organizacji.
    """
)

# Zakres
df = pd.DataFrame(
    {
        "Kryterium": [
            "**Miary**",
            "**Kryteria sukcesu**",
            "**Produkty**",
            "**Wykluczenia**",
        ],
        "Opis": [
            "output wyszukiwania, feedback",
            "skuteczność dopasowania kandydatów, satysfakcja pracowników",
            "platforma Web",
            "source danych do analizy (potrzebny access do wewnętrznych źródeł)",
        ],
    }
)
st.header("Zakres", divider=True)
st.table(df)

# Kamienie milowe
df = pd.DataFrame(
    {
        "Data": [
            "**CW12**",
            "**CW15**",
            "**CW16**",
            "**CW17**",
            "**CW19**",
            "**CW20**",
            "**CW24**",
            "**CW25**",
            "**CW26+**",
        ],
        "Kamień milowy": [
            "Front-End oraz Demo na _dummy data_",
            "Wdrożenie feedback oraz implementacja Back-End",
            "Uzupełnianie danych ręcznie dla małej grupy badawczej",
            "Pozyskanie dostępów do danych z serwisów wewnętrznych organizacji",
            "Serializacja oraz przechowywanie danych pracowników",
            "Dodanie nowych danych jako kryteria wyszukiwania",
            "Wdrożenie feedback oraz deploy",
            "Udostępnienie platformy w organizacji",
            "maintenance & feedback",
        ],
    }
)
st.header("Kamienie milowe", divider=True)
st.table(df)

# Zasoby
st.header("Zasoby", divider=True)
st.subheader(
    "Zasoby finansowe (budżet, pożyczki), materialne (urządzenia, materiały, biura), ludzkie (członkowie zespołu, wykonawcy), czas",
    divider=True,
)
st.markdown(
    """
    Zasoby finansowe:
    - regular salary,
    - licencja chmury do hostu.

    Materialne:
    - 3 x laptop,
    - przestrzeń biurowa do pracy.

    Ludzkie:
    - 2 x programista,
    - 1 x DevOps.

    Czas:
    - 4560 man hours.
    """
)

# Kluczowe ryzyka
df = pd.DataFrame(
    {
        "Ryzyko": [
            "Dane",
            "Server",
        ],
        "Opis": ["Brak zdalnego dostępu do niektórych danych", "Awaria serwerów"],
        "Wpływ": [
            "Zmniejszona automatyzacja procesu",
            "Utrata dostępu do platformy",
        ],
        "Prawdopodobieństwo (1-5)": [
            "3",
            "1",
        ],
        "Rozwiązanie": [
            "Implementacja ręczna przez managerów",
            "Regularny Backup",
        ],
    }
)
st.header("Kluczowe ryzyka", divider=True)
st.table(df)

# Osoby
st.header("Osoby", divider=True)
st.subheader(
    "Interesariusze",
    divider=True,
)
st.markdown(
    """
    - wysoki management,
    - managerowi,
    - pracownicy regularni.
    """
)
st.subheader("Zespół projektowy", divider=True)
st.markdown(
    """
    Programiści:
    - Jakub _Niewiaro_ Niewiarowski,
    - Michał _Jabol_ Jabłoński.

    DevOps:
    - pozycja otwarta.
    """
)
