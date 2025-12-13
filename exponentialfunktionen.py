import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import numpy as np


# ==========================================================
#   Exponentialfunktionen
# ==========================================================

def _mode_graph():
    key = "expfkt_graph"

    if st.button("Neues Beispiel", key="expfkt_graph_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        while True:
            N0 = random.randint(1, 5)

            if random.random() < 0.5:
                N1 = random.randint(N0 + 1, N0 + 12)
            else:
                if N0 == 1:
                    continue
                N1 = random.randint(1, N0 - 1)

            a = N1 / N0
            N3 = N0 * (a ** 3)
            if 0 < N3 <= 40:
                break

        ts = [0, 1, 2, 3]
        Ns = [N0 * (a ** t) for t in ts]
        st.session_state[key] = {"N0": N0, "a": a, "ts": ts, "Ns": Ns}

    data = st.session_state[key]
    N0, a, Ns = data["N0"], data["a"], data["Ns"]

    st.subheader("Funktion aus Graph")

    st.markdown(
        """
        **Aufgabe:**  
        Lies aus dem Graphen den Startwert $N_0$ und den Änderungsfaktor $a$ ab  
        und stelle die Funktionsgleichung $N(t)$ auf.
        """
    )

    fig, ax = plt.subplots()
    x_vals = np.linspace(0, 3, 400)
    y_vals = N0 * (a ** x_vals)

    ax.plot(x_vals, y_vals, linewidth=2)
    ax.set_xlim(0, 3)

    y_max = max(N0 * (a ** np.array([0, 1, 2, 3])))
    y_max = max(y_max * 1.1, max(N0, N0 * a) + 2)
    ax.set_ylim(0, y_max)

    ax.set_yticks(np.arange(0, math.ceil(y_max) + 1, 1))
    ax.set_xticks([0, 1, 2, 3])
    ax.grid(True)
    ax.set_xlabel("t")
    ax.set_ylabel("N(t)")

    st.pyplot(fig)

    if st.button("Lösung anzeigen", key="expfkt_graph_sol"):
        N1 = Ns[1]
        st.latex(rf"N_0 = {N0}")
        st.latex(rf"a = \frac{{{N1}}}{{{N0}}} = {a:.4f}")
        st.latex(rf"N(t) = {N0}\cdot {a:.4f}^t")


def _mode_aufstellen():
    key = "expfkt_fun"

    if st.button("Neues Beispiel", key="expfkt_fun_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        scenario_type = random.choice(["schimmel", "tiere"])

        if scenario_type == "schimmel":
            objekt = random.choice(["einem Apfel", "einer Brotscheibe", "einem Käseblock"])
            flaeche_einheit = random.choice(["mm²", "cm²"])
            zeit_einheit = random.choice(["Stunden", "Tagen"])

            N0 = random.choice([5, 10, 20, 25, 50])
            t1 = random.randint(2, 5)
            a = random.randint(12, 30) / 10
            N_t1 = round(N0 * (a ** t1), 2)

            text = (
                f"Schimmel breitet sich exponentiell auf {objekt} aus. "
                f"Zu Beginn sind {N0} {flaeche_einheit} bedeckt. "
                f"Nach {t1} {zeit_einheit} sind {N_t1} {flaeche_einheit} bedeckt."
            )
        else:
            tier = random.choice(["Hasen", "Schafe"])
            zeit_einheit = random.choice(["Monaten", "Jahren"])

            N0 = random.randint(2, 20)
            t1 = random.randint(2, 5)
            a = random.randint(12, 25) / 10
            N_t1 = round(N0 * (a ** t1))

            text = (
                f"Eine Population von {tier} wächst exponentiell. "
                f"Zu Beginn sind es {N0} {tier}. "
                f"Nach {t1} {zeit_einheit} sind es {N_t1} {tier}."
            )

        st.session_state[key] = {"text": text, "N0": N0, "t1": t1, "N_t1": N_t1}

    data = st.session_state[key]
    text, N0, t1, N_t1 = data["text"], data["N0"], data["t1"], data["N_t1"]

    st.subheader("Funktion aus Textangabe")
    st.markdown(f"**Angabe:** {text}")
    st.markdown("**Aufgabe:** Stelle eine passende Funktionsgleichung $N(t)$ auf.")

    if st.button("Lösung anzeigen", key="expfkt_fun_sol"):
        q = N_t1 / N0
        a = q ** (1 / t1)
        lam = math.log(q) / t1

        st.latex(rf"N(t) = {N0}\cdot {a:.4f}^t")
        st.latex(rf"N(t) = {N0}\cdot e^{{{lam:.4f}t}}")


def _mode_linear_vs_exp():
    key = "expfkt_linexp"

    if st.button("Neues Beispiel", key="expfkt_linexp_new"):
        st.session_state.pop(key, None)
        st.session_state.pop("linexp_show_main", None)
        st.session_state.pop("linexp_show_extra", None)

    if key not in st.session_state:
        name = random.choice(["Ben", "Anna", "Lukas", "Clara"])
        t_star = random.randint(2, 4)
        N0_lin = random.randint(80, 150)
        m = random.randint(5, 15)

        V = N0_lin + m * t_star
        a = random.uniform(1.05, 1.12)
        N0_exp = V / (a ** t_star)

        st.session_state[key] = {
            "name": name,
            "m": m,
            "a": a,
            "N0_lin": N0_lin,
            "N0_exp": N0_exp,
        }

    data = st.session_state[key]

    st.subheader("Linear vs. Exponentiell")
    st.markdown(f"{data['name']} vergleicht eine lineare und eine exponentielle Entwicklung.")

    if st.button("Lösung anzeigen", key="expfkt_linexp_sol"):
        st.latex(rf"W_L(t) = {data['N0_lin']} + {data['m']}t")
        st.latex(rf"W_E(t) = {data['N0_exp']:.2f}\cdot {data['a']:.4f}^t")


def run():
    st.title("Exponentialfunktionen")

    tab1, tab2, tab3 = st.tabs(
        ["Funktion aus Graph", "Funktion aus Textangabe", "Linear vs. Exponentiell"]
    )

    with tab1:
        _mode_graph()

    with tab2:
        _mode_aufstellen()

    with tab3:
        _mode_linear_vs_exp()
