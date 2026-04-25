import streamlit as st
import random
import math

def run():
    st.title("Beschränkte Zunahme")

    if "bza_data" not in st.session_state:
        st.session_state.bza_data = generate()

    d = st.session_state.bza_data

    st.markdown("### Angabe")
    st.write(d["context"])
    st.latex(d["func"])

    st.markdown("### Fragen")
    st.write(f"1. Berechne den Funktionswert nach {d['t1']} Jahren.")
    st.write(f"2. Nach wie vielen Jahren beträgt der Wert {d['target']}?")
    st.write("3. Bestimme die Schranke der Funktion.")

    if st.button("Lösung anzeigen"):
        solve(d)

    if st.button("Neues Beispiel"):
        st.session_state.bza_data = generate()
        st.rerun()


def generate():
    S = random.choice([5000, 8000, 10000, 12000, 15000])
    a = round(random.uniform(0.70, 0.95), 2)
    lam = round(math.log(a), 3)

    typ = random.choice([1, 2])

    if typ == 1:
        func = rf"N(t) = {S}\cdot(1 - {a}^t)"
        plain = f"{S}*(1-{a}^t)"
        mode = "a"

    else:
        func = rf"N(t) = {S}\cdot(1 - e^{{{lam}t}})"
        plain = f"{S}*(1-e^({lam}t))"
        mode = "e"

    t1 = random.choice([2, 3, 4, 5, 6])
    target = random.choice([
        int(S * 0.5),
        int(S * 0.6),
        int(S * 0.7),
        int(S * 0.8),
        int(S * 0.9),
    ])

    context = (
        "Die Nutzerzahl einer neuen Lernplattform wächst mit der Zeit. "
        "Da es langfristig eine maximale Anzahl möglicher Nutzer*innen gibt, "
        "wird das Wachstum durch eine beschränkte Zunahme modelliert."
    )

    return {
        "S": S,
        "a": a,
        "lam": lam,
        "func": func,
        "plain": plain,
        "mode": mode,
        "t1": t1,
        "target": target,
        "context": context,
    }


def solve(d):
    S = d["S"]
    a = d["a"]
    lam = d["lam"]
    t1 = d["t1"]
    target = d["target"]

    if d["mode"] == "a":
        value = S * (1 - a**t1)
        t = math.log(1 - target / S) / math.log(a)

    else:
        value = S * (1 - math.e**(lam * t1))
        t = math.log(1 - target / S) / lam

    st.markdown("### Lösung")

    st.write("1. Funktionswert:")
    st.latex(rf"N({t1}) = {value:.2f}")
    st.write(f"Nach {t1} Jahren beträgt der Wert ungefähr **{round(value)}**.")

    st.write("2. Zeitpunkt:")
    st.latex(rf"N(t) = {target}")
    st.code(f"Löse({d['plain']} = {target})", language="text")
    st.write(f"Ergebnis: **t ≈ {t:.2f} Jahre**")

    st.write("3. Schranke:")
    st.latex(rf"S = {S}")
    st.write(f"Die Funktion nähert sich langfristig dem Wert **{S}** an.")