import streamlit as st

st.set_page_config(
    page_title="Practice Plattform Mathematik",
    layout="wide",
)

st.sidebar.title("Kapitel")

kapitel = st.sidebar.radio(
    "Auswahl",
    [
        "Funktionen Allgemein",
        "Lineare Funktionen",
        "Lineare Gleichungssysteme",
        "Matrizen",
        "Quadratische Funktionen",
        "Trigonometrie",
        "Exponentialgleichungen",
        "Änderungsmaße",
        "Exponentialfunktionen",
    ],
)

if kapitel == "Funktionen Allgemein":
    import funktionen_allgemein
    funktionen_allgemein.run()

elif kapitel == "Lineare Funktionen":
    import lineare_funktionen
    lineare_funktionen.run()

elif kapitel == "Lineare Gleichungssysteme":
    import lineare_gleichungssysteme
    lineare_gleichungssysteme.run()

elif kapitel == "Matrizen":
    import matrizen
    matrizen.run()

elif kapitel == "Quadratische Funktionen":
    import quadratische_funktionen
    quadratische_funktionen.run()

elif kapitel == "Trigonometrie":
    import trigonometrie
    trigonometrie.run()

elif kapitel == "Exponentialgleichungen":
    import exponentialgleichungen
    exponentialgleichungen.run()

elif kapitel == "Änderungsmaße":
    import aenderungsmass
    aenderungsmass.run()

elif kapitel == "Exponentialfunktionen":
    import exponentialfunktionen
    exponentialfunktionen.run()
