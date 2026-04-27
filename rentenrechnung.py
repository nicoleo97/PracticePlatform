import streamlit as st
import random


def euro(x):
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def _mode_renten_erkennen():
    key = "rente_task"

    if st.button("Neues Beispiel", key="rente_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = {
            "R": random.choice([500, 800, 1000, 1200, 1500]),
            "n": random.randint(4, 10),
            "i": random.choice([2, 2.5, 3, 3.5, 4, 5]),
            "typ": random.choice(["BW_nach", "BW_vor", "EW_nach", "EW_vor"])
        }

    d = st.session_state[key]
    R, n, i, typ = d["R"], d["n"], d["i"], d["typ"]
    q = 1 + i / 100

    st.subheader("Rentenrechnung erkennen und berechnen")

    if typ == "BW_nach":
        text = f"Frau Berger erhält am Ende jedes Jahres {euro(R)}, insgesamt {n} Jahre lang. Zinssatz: {i} % p.a. Wie viel ist diese Zahlungsreihe heute wert?"
        formel = r"B = R \cdot \frac{q^n - 1}{q-1} \cdot \frac{1}{q^n}"
        wert = R * (q**n - 1) / (q - 1) * (1 / q**n)
        art = "Barwert, nachschüssig"

    elif typ == "BW_vor":
        text = f"Herr Müller erhält zu Beginn jedes Jahres {euro(R)}, insgesamt {n} Jahre lang. Zinssatz: {i} % p.a. Wie viel ist diese Zahlungsreihe heute wert?"
        formel = r"B = R \cdot \frac{q^n - 1}{q-1} \cdot \frac{1}{q^{n-1}}"
        wert = R * (q**n - 1) / (q - 1) * (1 / q**(n - 1))
        art = "Barwert, vorschüssig"

    elif typ == "EW_nach":
        text = f"Frau Novak zahlt am Ende jedes Jahres {euro(R)} ein, insgesamt {n} Jahre lang. Zinssatz: {i} % p.a. Wie viel ist direkt nach der letzten Einzahlung vorhanden?"
        formel = r"E = R \cdot \frac{q^n - 1}{q-1}"
        wert = R * (q**n - 1) / (q - 1)
        art = "Endwert, nachschüssig"

    else:
        text = f"Herr Steiner zahlt zu Beginn jedes Jahres {euro(R)} ein, insgesamt {n} Jahre lang. Zinssatz: {i} % p.a. Wie viel ist am Ende der Laufzeit vorhanden?"
        formel = r"E = R \cdot \frac{q^n - 1}{q-1} \cdot q"
        wert = R * (q**n - 1) / (q - 1) * q
        art = "Endwert, vorschüssig"

    st.markdown(f"**Aufgabe:** {text}")

    if st.button("Lösung anzeigen", key="rente_sol"):
        st.write(f"Gemeint ist: **{art}**")
        st.latex(fr"q = {q:.4f}")
        st.latex(formel)
        st.latex(fr"= {R} \cdot \frac{{{q:.4f}^{n} - 1}}{{{q:.4f} - 1}}")
        st.success(f"Ergebnis: {euro(wert)}")


def run():
    st.title("Rentenrechnung")
    _mode_renten_erkennen()