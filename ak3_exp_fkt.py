import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import numpy as np


# ==========================================================
#   TAB 1 – Funktion aus Graph
# ==========================================================

def _mode_graph():
    key = "expfkt_graph"

    # Neues Beispiel
    if st.button("Neues Beispiel", key="expfkt_graph_new"):
        st.session_state.pop(key, None)

    # Beispiel erzeugen: N(0) und N(1) sollen EXAKT ablesbar sein
    if key not in st.session_state:
        while True:
            # kleiner, gut lesbarer Startwert
            N0 = random.randint(1, 5)          # 1–5

            # 50% Wachstum, 50% Zerfall
            if random.random() < 0.5:
                # Wachstum
                N1 = random.randint(N0 + 1, N0 + 12)
            else:
                # Zerfall – aber N1 darf nicht 0 werden und N0 darf nicht 1 sein
                if N0 == 1:
                    continue
                N1 = random.randint(1, N0 - 1)

            a = N1 / N0

            # prüfen, ob N(3) nicht zu groß wird
            N3 = N0 * (a ** 3)
            if 0 < N3 <= 40:       # Obergrenze, damit der Graph schön im Bild bleibt
                break

        ts = [0, 1, 2, 3]
        Ns = [N0 * (a ** t) for t in ts]

        st.session_state[key] = {"N0": N0, "a": a, "ts": ts, "Ns": Ns}

    data = st.session_state[key]
    N0, a, ts, Ns = data["N0"], data["a"], data["ts"], data["Ns"]

    st.subheader("Funktion aus Graph")

    st.markdown(
        """
        **Aufgabe:**  
        Lies aus dem Graphen den Startwert $N_0$ und den Änderungsfaktor $a$ ab  
        und stelle die Funktionsgleichung $N(t)$ auf.
        """
    )

    # Plot – möglichst simpel: t von 0 bis 3, N(t) >= 0
    fig, ax = plt.subplots()
    x_vals = np.linspace(0, 3, 400)
    y_vals = N0 * (a ** x_vals)

    # Graph (klassische Achsen)
    ax.plot(x_vals, y_vals, linewidth=2)

    # sichtbarer Bereich
    ax.set_xlim(0, 3)
    y_max = max(N0 * (a ** np.array([0, 1, 2, 3])))
    y_max = y_max * 1.1
    if y_max < max(N0, N0 * a) + 2:
        y_max = max(N0, N0 * a) + 2
    ax.set_ylim(0, y_max)

    # Y-Ticks: 1er Schritte
    y_ticks = np.arange(0, math.ceil(y_max) + 1, 1)
    ax.set_yticks(y_ticks)

    # X-Ticks
    ax.set_xticks([0, 1, 2, 3])

    # Grid
    ax.grid(True, which="major", linestyle="-", linewidth=0.5)
    ax.set_xlabel("t")
    ax.set_ylabel("N(t)")

    st.pyplot(fig)

    show = st.button("Lösung anzeigen", key="expfkt_graph_sol")
    if show:
        N1 = Ns[1]
        st.latex(rf"N_0 = N(0) = {N0:.0f}")
        st.latex(rf"a = \frac{{N(1)}}{{N(0)}} = \frac{{{N1:.0f}}}{{{N0:.0f}}} = {a:.4f}")
        st.latex(rf"N(t) = {N0:.0f}\cdot {a:.4f}^t")


# ==========================================================
#   TAB 2 – Funktion aus Textangabe aufstellen
# ==========================================================

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
                f"Zu Beginn sind {N0} {flaeche_einheit} der Oberfläche bedeckt. "
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
                f"Eine Population von {tier} vermehrt sich exponentiell. "
                f"Zu Beginn sind es {N0} {tier}. "
                f"Nach {t1} {zeit_einheit} sind es {N_t1} {tier}."
            )

        st.session_state[key] = {
            "text": text,
            "N0": N0,
            "t1": t1,
            "N_t1": N_t1
        }

    data = st.session_state[key]
    text, N0, t1, N_t1 = data["text"], data["N0"], data["t1"], data["N_t1"]

    st.subheader("Funktion aus Textangabe aufstellen")

    st.markdown(f"**Angabe:** {text}")
    st.markdown("**Aufgabe:** Stelle eine passende Funktionsgleichung $N(t)$ auf.")

    show = st.button("Lösung anzeigen", key="expfkt_fun_sol")
    if show:
        q = N_t1 / N0
        a = q ** (1 / t1)
        lam = math.log(q) / t1

        st.markdown("**Eine mögliche Schreibweise mit Änderungsfaktor $a$:**")
        st.latex(rf"N(t) = {N0:.2f}\cdot {a:.4f}^t")

        st.markdown("**Alternative Schreibweise mit Wachstumskonstante $\\lambda$:**")
        st.latex(rf"N(t) = {N0:.2f}\cdot e^{{{lam:.4f}\,t}}")


# ==========================================================
#   TAB 3 – Linear vs Exponentiell
# ==========================================================

def _mode_linear_vs_exp():
    key = "expfkt_linexp"

    if st.button("Neues Beispiel", key="expfkt_linexp_new"):
        st.session_state.pop(key, None)
        st.session_state.pop("linexp_show_main", None)
        st.session_state.pop("linexp_show_extra", None)

    if key not in st.session_state:
        male_names = ["Ben", "David", "Lukas", "Jonas"]
        female_names = ["Anna", "Clara", "Eva", "Mia"]
        gender = random.choice(["m", "w"])

        if gender == "m":
            name = random.choice(male_names)
            subj = "Er"
            subj_lower = "er"
        else:
            name = random.choice(female_names)
            subj = "Sie"
            subj_lower = "sie"

        while True:
            t_star = random.randint(2, 4)
            N0_lin = random.randint(80, 150)
            m = random.randint(5, 15)

            V = N0_lin + m * t_star

            a = random.uniform(1.05, 1.12)
            N0_exp = V / (a ** t_star)

            if not (0.5 * N0_lin <= N0_exp <= 1.5 * N0_lin):
                continue

            W_lin_10 = N0_lin + 10 * m
            W_exp_10 = N0_exp * (a ** 10)

            max_start = max(N0_lin, N0_exp)
            if W_lin_10 <= 3 * max_start and W_exp_10 <= 3 * max_start:
                break

        st.session_state[key] = {
            "name": name,
            "subj": subj,
            "subj_lower": subj_lower,
            "t_star": t_star,
            "V": V,
            "m": m,
            "a": a,
            "N0_lin": N0_lin,
            "N0_exp": N0_exp
        }

    data = st.session_state[key]
    name = data["name"]
    subj = data["subj"]
    subj_lower = data["subj_lower"]
    m = data["m"]
    a = data["a"]
    N0_lin = data["N0_lin"]
    N0_exp = data["N0_exp"]

    st.subheader("Linear vs. Exponentiell")

    p = (a - 1) * 100

    text = (
        f"{name} möchte eine Sammlung starten. {subj} überlegt, ob {subj_lower} sich ein kleines "
        f"Briefmarken- oder Münz-Sammelset zulegen soll.\n\n"
        f"{subj} recherchiert und findet heraus, dass die **Briefmarkensammlung** zu Beginn "
        f"einen Wert von {N0_lin:.2f} € hat und jedes Jahr um etwa {m} € an Wert dazugewinnt. "
        f"Die **Münzsammlung** hat zu Beginn einen Wert von {N0_exp:.2f} € und ihr Wert steigt "
        f"jedes Jahr um etwa {p:.1f}%."
    )

    st.markdown("**Angabe:**")
    st.markdown(text)

    st.markdown(
        """
        **Aufgabe:**  
        Stelle eine Funktionsgleichung für den Wert der jeweiligen Sammlung auf.
        """
    )

    if "linexp_show_main" not in st.session_state:
        st.session_state["linexp_show_main"] = False
    if "linexp_show_extra" not in st.session_state:
        st.session_state["linexp_show_extra"] = False

    if st.button("Lösung anzeigen", key="expfkt_linexp_sol"):
        st.session_state["linexp_show_main"] = True

    if st.session_state["linexp_show_main"]:
        st.markdown("**Mögliche Funktionsgleichungen:**")

        st.latex(
            rf"W_B(t) = {N0_lin:.2f} + {m} \cdot t \quad (\text{{linear, Briefmarkensammlung}})"
        )
        st.latex(
            rf"W_M(t) = {N0_exp:.2f}\cdot {a:.4f}^t \quad (\text{{exponentiell, Münzsammlung}})"
        )

        st.markdown(
            f"""
            **Zusatzfrage:**  
            Angenommen, {name} möchte die Sammlung als Investition für mehr als 5 Jahre anlegen.  
            Begründe, für welche Sammlung {subj_lower} sich entscheiden sollte.
            """
        )

        if st.button("Lösung zur Zusatzfrage anzeigen", key="expfkt_linexp_extra_sol"):
            st.session_state["linexp_show_extra"] = True

        if st.session_state["linexp_show_extra"]:
            t = 5
            W_lin_5 = N0_lin + m * t
            W_exp_5 = N0_exp * (a ** t)

            if W_exp_5 > W_lin_5:
                empfehlung = "Münzsammlung"
                begruendung = (
                    f"weil die Münzsammlung nach 5 Jahren einen höheren Wert "
                    f"({W_exp_5:.2f} €) als die Briefmarkensammlung ({W_lin_5:.2f} €) hat."
                )
            else:
                empfehlung = "Briefmarkensammlung"
                begruendung = (
                    f"weil die Briefmarkensammlung nach 5 Jahren einen höheren Wert "
                    f"({W_lin_5:.2f} €) als die Münzsammlung ({W_exp_5:.2f} €) hat."
                )

            st.markdown(
                f"**Lösung:** {name} sollte sich für die **{empfehlung}** entscheiden, {begruendung}"
            )


# ==========================================================
#   HAUPT-FUNKTION
# ==========================================================

def run():
    st.title("Exponentialfunktionen – 3AK")

    tab1, tab2, tab3 = st.tabs([
        "Funktion aus Graph",
        "Funktion aus Textangabe",
        "Linear vs. Exponentiell",
    ])

    with tab1:
        _mode_graph()

    with tab2:
        _mode_aufstellen()

    with tab3:
        _mode_linear_vs_exp()
