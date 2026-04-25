import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("Beschränkte Zu-/Abnahme")

    # Fix für alte session_state Daten
    if "bza_data" in st.session_state and "context" not in st.session_state.bza_data:
        del st.session_state["bza_data"]

    if "bza_data" not in st.session_state:
        st.session_state.bza_data = generate()

    d = st.session_state.bza_data

    st.markdown("### Aufgabe")
    st.write(d["context"])
    st.latex(d["func"])
    st.write("Dabei ist t die Zeit in Jahren.")

    st.markdown("### Fragen")
    st.write(f"1. Berechne den Funktionswert nach {d['t1']} Jahren.")
    st.write(f"2. Nach wie vielen Jahren beträgt die Nutzerzahl {d['target']}?")
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
    target = int(S * random.choice([0.5, 0.6, 0.7, 0.8, 0.9]))

    context = (
        "Die Nutzerzahl einer neuen Lernplattform wächst mit der Zeit. "
        "Sie nähert sich langfristig einer maximalen Nutzerzahl an."
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


def N(d, t):
    if d["mode"] == "a":
        return d["S"] * (1 - d["a"]**t)
    else:
        return d["S"] * (1 - math.e**(d["lam"] * t))


def solve(d):
    S = d["S"]
    t1 = d["t1"]
    target = d["target"]

    value = N(d, t1)

    if d["mode"] == "a":
        t = math.log(1 - target / S) / math.log(d["a"])
    else:
        t = math.log(1 - target / S) / d["lam"]

    st.markdown("### Lösung")

    st.write("1. Funktionswert:")
    st.latex(rf"N({t1}) = {value:.2f}")
    st.write(f"Nach {t1} Jahren: **{round(value)}**")

    st.write("2. Zeitpunkt:")
    st.latex(rf"N(t) = {target}")
    st.code(f"Löse({d['plain']} = {target})", language="text")
    st.write(f"t ≈ {t:.2f} Jahre")

    st.write("3. Schranke:")
    st.latex(rf"S = {S}")

    st.markdown("### Plot")
    x = np.linspace(0, 20, 200)
    y = [N(d, xi) for xi in x]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(S, linestyle="--")
    ax.set_xlabel("t")
    ax.set_ylabel("N(t)")
    ax.grid(True)

    st.pyplot(fig)