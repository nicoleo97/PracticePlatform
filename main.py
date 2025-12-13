# main.py
import streamlit as st

import funktionen_allgemein
import lineare_funktionen
import lineare_gleichungssysteme
import matrizen
import quadratische_funktionen
import trigonometrie
import exponentialfunktionen
import aenderungsmass
import exponentialgleichungen


st.set_page_config(
    page_title="Mathe Practice Plattform",
    page_icon="📘",
    layout="centered"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Kapitel",
    [
        "🏠 Start",
        "Funktionen allgemein",
        "Lineare Funktionen",
        "Lineare Gleichungssysteme",
        "Matrizen",
        "Quadratische Funktionen",
        "Trigonometrie",
        "Exponentialfunktionen",
        "Änderungsmaße",
        "Exponentialgleichungen",
    ]
)

# =========================
#   STARTSEITE
# =========================
if page == "🏠 Start":
    st.title("Mathe Practice Plattform")
    st.markdown(
        """
        **Willkommen!**

        Wähle links ein **Kapitel**, um Übungsaufgaben zu starten.

        **Hinweise:**
        - Alle Aufgaben sind **zufällig generiert**
        """
    )

# =========================
#   KAPITEL
# =========================
elif page == "Funktionen allgemein":
    funktionen_allgemein.run()

elif page == "Lineare Funktionen":
    lineare_funktionen.run()

elif page == "Lineare Gleichungssysteme":
    lineare_gleichungssysteme.run()

elif page == "Matrizen":
    matrizen.run()

elif page == "Quadratische Funktionen":
    quadratische_funktionen.run()

elif page == "Trigonometrie":
    trigonometrie.run()

elif page == "Exponentialfunktionen":
    exponentialfunktionen.run()

elif page == "Änderungsmaße":
    aenderungsmass.run()

elif page == "Exponentialgleichungen":
    exponentialgleichungen.run()
