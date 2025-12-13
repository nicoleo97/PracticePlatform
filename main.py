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
    page_title="PRACTICE PLATFORM",
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
    st.title("PRACTICE PLATFORM")

    st.markdown(
        """
        Willkommen zu einer Übungsplattform für Mathematik.

        Auf der linken Seite findest du verschiedene **Themenbereiche**.  
        Bei jedem Beispiel kannst du über die Schaltflächen  
        *„Lösung anzeigen“* und *„Neues Beispiel“* selbstständig üben,
        vergleichen und beliebig viele neue Aufgaben generieren.

        Wenn du Fragen hast oder dir irgendwo ein Fehler auffällt,
        kannst du mich jederzeit über den **Chat auf Microsoft Teams** erreichen.
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
