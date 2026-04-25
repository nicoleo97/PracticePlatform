import streamlit as st
import random
import math

def run():
    st.title("Beschränkte Zu-/Abnahme")

    if "bza_data" not in st.session_state:
        st.session_state.bza_data = generate_task()

    data = st.session_state.bza_data

    st.markdown("### Aufgabe")
    st.write(data["text"])

    st.markdown("**Fragen:**")
    st.write(f"1. Berechne den Funktionswert nach {data['t1']} Jahren.")
    st.write(f"2. Nach wie vielen Jahren beträgt die Nutzerzahl {data['target']}?")
    st.write("3. Bestimme die Schranke der Funktion.")

    if st.button("Lösung anzeigen"):
        show_solution(data)

    if st.button("Neues Beispiel"):
        st.session_state.bza_data = generate_task()
        st.rerun()


def generate_task():
    S = random.choice([5000, 8000, 10000, 12000])
    C = random.choice([3000, 4000, 5000])
    a = random.choice([0.65, 0.7, 0.75, 0.8, 0.85])
    t1 = random.choice([2, 3, 4, 5])
    target = random.choice([int(S * 0.75), int(S * 0.8), int(S * 0.9)])

    text = (
        f"Eine neue Lernplattform gewinnt Nutzerinnen und Nutzer. "
        f"Die Nutzerzahl wird modelliert durch:\n\n"
        f"**N(t) = {S} - {C} · {a}^t**\n\n"
        fDabei ist t die Zeit in Jahren."
    )

    return {
        "S": S,
        "C": C,
        "a": a,
        "t1": t1,
        "target": target,
        "text": text,
    }


def show_solution(data):
    S = data["S"]
    C = data["C"]
    a = data["a"]
    t1 = data["t1"]
    target = data["target"]

    value = S - C * a**t1
    t = math.log((S - target) / C) / math.log(a)

    st.markdown("### Lösung")

    st.write(f"1. **Funktionswert:**")
    st.latex(rf"N({t1}) = {S} - {C} \cdot {a}^{t1} = {value:.2f}")
    st.write(f"Nach {t1} Jahren sind es ca. **{round(value)} Nutzer*innen**.")

    st.write("2. **Zeitpunkt:**")
    st.latex(rf"{target} = {S} - {C} \cdot {a}^t")
    st.latex(rf"t = \frac{{\ln\left(\frac{{{S-target}}}{{{C}}}\right)}}{{\ln({a})}} = {t:.2f}")
    st.write(f"Die Nutzerzahl {target} wird nach ca. **{t:.2f} Jahren** erreicht.")

    st.write("3. **Schranke:**")
    st.write(f"Da der Term `{a}^t` für große t gegen 0 geht, nähert sich die Funktion der Schranke:")
    st.latex(rf"S = {S}")