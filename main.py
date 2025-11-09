import streamlit as st

st.set_page_config(page_title="Übungsplattform Mathematik", page_icon="🧮")

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
