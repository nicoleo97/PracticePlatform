import streamlit as st

# Seitenkonfiguration
st.set_page_config(page_title="Übungsplattform Mathematik", page_icon="🧮")

# === Imports für 2AK-Seiten ===
import ak2_funktionen_allgemein as ak2_f_allg      # aus ehemalig pages/1_FunktionenAllgemein.py
import ak2_lineare_funktionen as ak2_lin_fkt       # aus ehemalig pages/2_LineareFunktionen.py
import ak2_alltag_wirtschaft as ak2_alltag         # aus ehemalig pages/3_Beispiele_Alltag+Wirtschaft.py

# === Imports für 3AK-Seiten ===
import ak3_exp_glg as ak3_exp_glg

import ak3_aenderungsmass_faktoren as ak3_aend     # aus 02_3AK_aFaktoren.py
import ak3_exp_fkt as ak3_exp_fkt                  # aus 03_3AK_ExpFkt.py

# Oberste Tabs: 2AK / 3AK
tab_2ak, tab_3ak = st.tabs(["2AK", "3AK"])

# ===================== 2AK =====================
with tab_2ak:
    sub_2ak = st.tabs([
        "Hauptmenü",
        "Funktionen allgemein",
        "Lineare Funktionen",
        "Beispiele im Alltag und Wirtschaft",
    ])

    # 2AK – Hauptmenü (dein bisheriger main.py-Text 1:1)
    with sub_2ak[0]:
        st.title("Übungsplattform Mathematik")

        st.markdown(
            """
            Auf der linken Seite findest du zwei Themenbereiche:
            **„Funktionen allgemein“** und **„Lineare Funktionen“**.  
            Bei jedem Beispiel kannst du über die Schaltflächen
            *„Lösung anzeigen“* und *„Neues Beispiel“* selbstständig üben,
            vergleichen und beliebig viele neue Aufgaben generieren.

            Wenn du Fragen hast oder dir irgendwo ein Fehler auffällt,
            kannst du mich jederzeit über den **Chat auf Microsoft Teams** erreichen. 💬
            """
        )

        st.markdown("Folgende Arten an Aufgaben gibt es:")
        st.subheader("Funktionen allgemein")

        st.markdown(
            """
            **Besondere Punkte einer Funktion:**  
            Es wird der Graph einer Funktion angezeigt.  
            Du sollst die **besonderen Punkte**
            – also **Nullstellen**, **Maxima**, **Minima** und den **Achsenabschnitt** –
            erkennen und einzeichnen können.

            **Abhängige und unabhängige Variablen:**  
            Gegeben ist ein kurzer **Text** aus einer Alltagssituation.  
            Du sollst zuerst die **Variablen** (mit **Symbol**, **Bedeutung** und **Einheit**) korrekt bestimmen
            und anschließend eine **sprachliche Aussage** als **mathematischen Ausdruck** formulieren.
            """
        )

        st.subheader("Lineare Funktionen")

        st.markdown(
            """
            **Zeichnen:**  
            Gegeben ist eine **lineare Funktion**.  
            Zeichne den Graphen dieser Funktion **mit Hilfe eines Steigungsdreiecks** in ein Koordinatensystem.  
            Bei der **leichten Version** sind nur **ganze Zahlen** zugelassen,  
            bei der **schweren Version** sind auch **Brüche** möglich.

            **Ermitteln:**  
            Gegeben ist der **Graph** einer linearen Funktion.  
            Bestimme die **Funktionsgleichung** mithilfe des Steigungsdreiecks.  
            Auch hier gilt: In der **leichten Version** sind nur ganze Zahlen erlaubt,  
            in der **schweren Version** gibt es keine Einschränkungen.

            **Differenzenquotient:**  
            Gegeben ist eine **Wertetabelle** mit drei Punkten.  
            Berechne zweimal den **Differenzenquotienten** und beurteile,
            ob es sich um einen **linearen Zusammenhang** handelt.
            """
        )

    # 2AK – Funktionen allgemein
    with sub_2ak[1]:
        ak2_f_allg.run()

    # 2AK – Lineare Funktionen
    with sub_2ak[2]:
        ak2_lin_fkt.run()

    # 2AK – Beispiele im Alltag und Wirtschaft
    with sub_2ak[3]:
        ak2_alltag.run()

# ===================== 3AK =====================
with tab_3ak:
    sub_3ak = st.tabs([
        "Hauptmenü",
        "Exponentialgleichungen",
        "Änderungsmaße & Änderungsfaktoren",
        "Exponentialfunktionen",
    ])

    # 3AK – Hauptmenü (eigener Text)
    with sub_3ak[0]:
        st.title("3AK – Exponentialfunktionen und Änderungsmaße")
        st.markdown(
            """
            Hier findest du Übungsaufgaben zu **Exponentialgleichungen**,  
            **Änderungsmaßen & Änderungsfaktoren** sowie **Exponentialfunktionen**.

            Wähle oben den passenden Reiter, um mit den Aufgaben zu starten.
            """
        )

    # 3AK – Exponentialgleichungen
    with sub_3ak[1]:   # Exponentialgleichungen
        ak3_exp_glg.run()


    # 3AK – Änderungsmaße & Änderungsfaktoren
    with sub_3ak[2]:
        ak3_aend.run()

    # 3AK – Exponentialfunktionen
    with sub_3ak[3]:
        ak3_exp_fkt.run()
