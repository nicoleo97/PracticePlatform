import streamlit as st
import random
import matplotlib.pyplot as plt


def euro(x):
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def _draw_timeline(payments, n_max, title=None):
    fig, ax = plt.subplots(figsize=(9, 2.4))

    ax.hlines(0, 0, n_max + 0.4, linewidth=2)
    ax.annotate(
        "",
        xy=(n_max + 0.7, 0),
        xytext=(n_max + 0.4, 0),
        arrowprops=dict(arrowstyle="->", linewidth=2),
    )

    for t in range(n_max + 1):
        ax.vlines(t, -0.08, 0.08, linewidth=1.5)
        ax.text(t, -0.28, str(t), ha="center", fontsize=12)

    for t, amount in payments:
        ax.annotate(
            "",
            xy=(t, 0.08),
            xytext=(t, 0.75),
            arrowprops=dict(arrowstyle="-|>", linewidth=2),
        )
        ax.text(t, 0.88, euro(amount), ha="center", fontsize=12)

    ax.text(n_max + 0.85, -0.05, "Zeit in Jahren", fontsize=12)

    if title:
        ax.text(n_max / 2, 1.2, title, ha="center", fontsize=14)

    ax.set_ylim(-0.5, 1.35)
    ax.axis("off")
    st.pyplot(fig)


def _mode_barwert():
    key = "zz_barwert"

    if key in st.session_state and "K_n" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_barwert_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = {
            "name": random.choice(["Frau Berger", "Herr Müller", "Frau Novak", "Herr Steiner"]),
            "ziel": random.choice(["eine Reise", "ein neues Auto", "eine Ausbildung"]),
            "K_n": random.choice([2000, 3000, 5000, 8000, 10000]),
            "n": random.randint(2, 8),
            "i": random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        }

    d = st.session_state[key]
    q = 1 + d["i"] / 100

    st.subheader("Barwert berechnen")

    st.markdown(
        f"**Aufgabe:** {d['name']} möchte in {d['n']} Jahren {euro(d['K_n'])} "
        f"für {d['ziel']} am Sparbuch haben. Der Zinssatz beträgt {d['i']} % p.a. "
        f"Wie viel muss heute angelegt werden?"
    )

    if st.button("Lösung anzeigen", key="zz_barwert_sol"):
        K_0 = d["K_n"] * q ** (-d["n"])

        _draw_timeline([(d["n"], d["K_n"])], d["n"], "Abzinsung auf jetzt")

        st.write("Es wird **abgezinst**, weil von einem späteren Zeitpunkt auf heute zurückgerechnet wird.")
        st.latex(fr"q = {q:.4f}")
        st.latex(r"K_0 = K_n \cdot q^{-n}")
        st.latex(fr"K_0 = {d['K_n']:.2f} \cdot {q:.4f}^{{-{d['n']}}} = {K_0:.2f}")

        st.success(f"Heute müssen {euro(K_0)} angelegt werden.")


def _mode_endwert():
    key = "zz_endwert"

    if key in st.session_state and "K_0" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_endwert_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = {
            "name": random.choice(["Frau Berger", "Herr Müller", "Frau Novak", "Herr Steiner"]),
            "ziel": random.choice(["eine Reise", "ein neues Auto", "eine Ausbildung"]),
            "K_0": random.choice([1000, 2000, 3000, 5000]),
            "n": random.randint(2, 8),
            "i": random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        }

    d = st.session_state[key]
    q = 1 + d["i"] / 100

    st.subheader("Endwert berechnen")

    st.markdown(
        f"**Aufgabe:** {d['name']} legt heute {euro(d['K_0'])} "
        f"für {d['ziel']} am Sparbuch an. Der Zinssatz beträgt {d['i']} % p.a. "
        f"Wie viel Geld ist in {d['n']} Jahren vorhanden?"
    )

    if st.button("Lösung anzeigen", key="zz_endwert_sol"):
        K_n = d["K_0"] * q ** d["n"]

        _draw_timeline([(0, d["K_0"])], d["n"], f"Aufzinsung bis Jahr {d['n']}")

        st.write("Es wird **aufgezinst**, weil der heutige Wert in die Zukunft gerechnet wird.")
        st.latex(fr"q = {q:.4f}")
        st.latex(r"K_n = K_0 \cdot q^n")
        st.latex(fr"K_n = {d['K_0']:.2f} \cdot {q:.4f}^{d['n']} = {K_n:.2f}")

        st.success(f"In {d['n']} Jahren sind {euro(K_n)} vorhanden.")


def _mode_barwert_mehrere():
    key = "zz_barwert_mehrere"

    if key in st.session_state and "name" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_barwert_mehrere_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        n = random.randint(2, 8)
        st.session_state[key] = {
            "name": random.choice(["Frau Berger", "Herr Müller", "Frau Novak", "Herr Steiner"]),
            "ziel": random.choice(["eine Reise", "ein neues Auto", "eine Ausbildung"]),
            "K_0": random.choice([1000, 2000, 3000]),
            "K_n": random.choice([2000, 3000, 5000, 8000]),
            "n": n,
            "i": random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        }

    d = st.session_state[key]
    q = 1 + d["i"] / 100

    st.subheader("Barwert mehrerer Zahlungen")

    st.markdown(
        f"**Aufgabe:** {d['name']} möchte für {d['ziel']} sofort {euro(d['K_0'])} "
        f"und in {d['n']} Jahren {euro(d['K_n'])} erhalten. "
        f"Der Zinssatz beträgt {d['i']} % p.a. "
        f"Wie groß ist der Barwert dieser Zahlungen?"
    )

    if st.button("Lösung anzeigen", key="zz_barwert_mehrere_sol"):
        payments = [(0, d["K_0"]), (d["n"], d["K_n"])]
        BW = d["K_0"] + d["K_n"] * q ** (-d["n"])

        _draw_timeline(payments, d["n"], "Abzinsung auf jetzt")

        st.write("Die erste Zahlung liegt bereits bei **jetzt**. Die zweite Zahlung wird abgezinst.")
        st.latex(fr"q = {q:.4f}")
        st.latex(r"BW = K_0 + K_n \cdot q^{-n}")
        st.latex(fr"BW = {d['K_0']:.2f} + {d['K_n']:.2f}\cdot {q:.4f}^{{-{d['n']}}} = {BW:.2f}")

        st.success(f"Der Barwert beträgt {euro(BW)}.")


def _mode_endwert_mehrere():
    key = "zz_endwert_mehrere"

    if key in st.session_state and "name" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_endwert_mehrere_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        n = random.randint(2, 8)
        st.session_state[key] = {
            "name": random.choice(["Frau Berger", "Herr Müller", "Frau Novak", "Herr Steiner"]),
            "ziel": random.choice(["eine Reise", "ein neues Auto", "eine Ausbildung"]),
            "K_0": random.choice([1000, 2000, 3000]),
            "K_n": random.choice([2000, 3000, 5000, 8000]),
            "n": n,
            "i": random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        }

    d = st.session_state[key]
    q = 1 + d["i"] / 100

    st.subheader("Endwert mehrerer Zahlungen")

    st.markdown(
        f"**Aufgabe:** {d['name']} legt für {d['ziel']} heute {euro(d['K_0'])} "
        f"und in {d['n']} Jahren {euro(d['K_n'])} an. "
        f"Der Zinssatz beträgt {d['i']} % p.a. "
        f"Wie viel Geld ist direkt nach der zweiten Einzahlung vorhanden?"
    )

    if st.button("Lösung anzeigen", key="zz_endwert_mehrere_sol"):
        payments = [(0, d["K_0"]), (d["n"], d["K_n"])]
        EW = d["K_0"] * q ** d["n"] + d["K_n"]

        _draw_timeline(payments, d["n"], f"Aufzinsung bis Jahr {d['n']}")

        st.write("Die erste Zahlung wird aufgezinst. Die zweite Zahlung liegt bereits beim Endzeitpunkt.")
        st.latex(fr"q = {q:.4f}")
        st.latex(r"EW = K_0 \cdot q^n + K_n")
        st.latex(fr"EW = {d['K_0']:.2f}\cdot {q:.4f}^{d['n']} + {d['K_n']:.2f} = {EW:.2f}")

        st.success(f"Der Endwert beträgt {euro(EW)}.")


def _mode_angebote():
    key = "zz_angebote"

    if key in st.session_state and "angebot_a" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_angebote_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        n_max = random.randint(3, 6)

        angebot_a = sorted([
            (0, random.choice([20000, 30000, 40000])),
            (random.randint(1, n_max), random.choice([20000, 30000, 40000])),
        ])

        angebot_b = sorted([
            (0, random.choice([10000, 20000, 30000])),
            (random.randint(1, n_max), random.choice([20000, 30000, 40000])),
            (random.randint(1, n_max), random.choice([10000, 20000, 30000])),
        ])

        st.session_state[key] = {
            "angebot_a": angebot_a,
            "angebot_b": angebot_b,
            "i": random.choice([2, 2.5, 3, 3.5, 4]),
            "n_max": n_max,
        }

    d = st.session_state[key]
    q = 1 + d["i"] / 100

    st.subheader("Angebote vergleichen")

    def angebot_text(payments):
        teile = []
        for t, b in payments:
            if t == 0:
                teile.append(f"{euro(b)} sofort")
            else:
                teile.append(f"{euro(b)} in {t} Jahren")
        return ", ".join(teile)

    st.markdown(
        f"**Aufgabe:** Ein Grundstück soll verkauft werden. Zwei Personen machen Angebote. "
        f"Der Vergleichszinssatz beträgt {d['i']} % p.a.\n\n"
        f"**Angebot A:** {angebot_text(d['angebot_a'])}\n\n"
        f"**Angebot B:** {angebot_text(d['angebot_b'])}\n\n"
        f"Welches Angebot ist besser?"
    )

    if st.button("Lösung anzeigen", key="zz_angebote_sol"):
        BW_A = sum(betrag * q ** (-t) for t, betrag in d["angebot_a"])
        BW_B = sum(betrag * q ** (-t) for t, betrag in d["angebot_b"])

        st.markdown("### Zeitachsen")

        st.write("**Angebot A**")
        _draw_timeline(d["angebot_a"], d["n_max"])

        st.write("**Angebot B**")
        _draw_timeline(d["angebot_b"], d["n_max"])

        st.markdown("### Vergleich auf jetzt")
        st.write(
            "Zum Vergleichen werden beide Angebote auf **jetzt** abgezinst. "
            "Man könnte auch einen anderen gemeinsamen Vergleichszeitpunkt wählen."
        )

        st.latex(fr"q = {q:.4f}")

        rech_a = " + ".join(
            [fr"{betrag:.2f}\cdot {q:.4f}^{{-{t}}}" for t, betrag in d["angebot_a"]]
        )
        rech_b = " + ".join(
            [fr"{betrag:.2f}\cdot {q:.4f}^{{-{t}}}" for t, betrag in d["angebot_b"]]
        )

        st.latex(fr"BW_A = {rech_a} = {BW_A:.2f}")
        st.latex(fr"BW_B = {rech_b} = {BW_B:.2f}")

        if BW_A > BW_B:
            st.success(f"Man sollte Angebot A wählen, weil der Barwert mit {euro(BW_A)} größer ist.")
        elif BW_B > BW_A:
            st.success(f"Man sollte Angebot B wählen, weil der Barwert mit {euro(BW_B)} größer ist.")
        else:
            st.success("Beide Angebote sind gleichwertig.")

def _mode_kest():
    key = "zz_kest"

    if st.button("Neues Beispiel", key="zz_kest_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = {
            "art": random.choice(["ohne_zu_mit", "mit_zu_ohne"]),
            "i": random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        }

    d = st.session_state[key]
    faktor = 0.75

    st.subheader("KESt")

    if d["art"] == "ohne_zu_mit":
        st.markdown(
            f"**Aufgabe:** Der Zinssatz ohne KESt beträgt {d['i']} % p.a. "
            f"Berechne den Zinssatz mit KESt."
        )

        if st.button("Lösung anzeigen", key="zz_kest_sol_btn"):
            i_mit = d["i"] * faktor

            st.latex(r"i_{\text{mit}} = i_{\text{ohne}} \cdot 0{,}75")
            st.latex(fr"i_{{\text{{mit}}}} = {d['i']:.2f}\cdot 0.75 = {i_mit:.3f}\%")

            st.success(f"Der Zinssatz mit KESt beträgt {i_mit:.3f} % p.a.")

    else:
        st.markdown(
            f"**Aufgabe:** Der Zinssatz mit KESt beträgt {d['i']} % p.a. "
            f"Berechne den Zinssatz ohne KESt."
        )

        if st.button("Lösung anzeigen", key="zz_kest_sol_btn"):
            i_ohne = d["i"] / faktor

            st.latex(r"i_{\text{ohne}} = \frac{i_{\text{mit}}}{0{,}75}")
            st.latex(fr"i_{{\text{{ohne}}}} = \frac{{{d['i']:.2f}}}{{0.75}} = {i_ohne:.3f}\%")

            st.success(f"Der Zinssatz ohne KESt beträgt {i_ohne:.3f} % p.a.")

def _mode_theoretische_verzinsung():
    key = "zz_theoretisch"

    if key in st.session_state and "ganze_jahre" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_theoretisch_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = {
            "art": random.choice(["endwert", "barwert"]),
            "ganze_jahre": random.randint(1, 3),
            "ganze_monate": random.randint(1, 10),
            "ganze_tage": random.choice([5, 10, 15, 20, 25]),
            "K_0": random.choice([1000, 2000, 3000, 5000]),
            "K_n": random.choice([2000, 3000, 5000, 8000]),
            "i": random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        }

    d = st.session_state[key]
    q = 1 + d["i"] / 100
    n = d["ganze_jahre"] + d["ganze_monate"] / 12 + d["ganze_tage"] / 360

    st.subheader("Theoretische Verzinsung")

    laufzeit = f"{d['ganze_jahre']} Jahre, {d['ganze_monate']} Monate und {d['ganze_tage']} Tage"

    if d["art"] == "endwert":
        st.markdown(
            f"**Aufgabe:** Es werden {euro(d['K_0'])} angelegt. "
            f"Der Zinssatz beträgt {d['i']} % p.a. "
            f"Die Laufzeit beträgt {laufzeit}. Berechne den Endwert."
        )

        if st.button("Lösung anzeigen", key="zz_theoretisch_sol"):
            K_n = d["K_0"] * q ** n

            st.latex(
                fr"n = {d['ganze_jahre']} + \frac{{{d['ganze_monate']}}}{{12}} + "
                fr"\frac{{{d['ganze_tage']}}}{{360}} = {n:.4f}"
            )
            st.latex(fr"q = {q:.4f}")
            st.latex(r"K_n = K_0 \cdot q^n")
            st.latex(fr"K_n = {d['K_0']:.2f}\cdot {q:.4f}^{{{n:.4f}}} = {K_n:.2f}")
            st.success(f"Der Endwert beträgt {euro(K_n)}.")

    else:
        st.markdown(
            f"**Aufgabe:** Nach {laufzeit} sollen {euro(d['K_n'])} vorhanden sein. "
            f"Der Zinssatz beträgt {d['i']} % p.a. Berechne den Barwert."
        )

        if st.button("Lösung anzeigen", key="zz_theoretisch_sol"):
            K_0 = d["K_n"] * q ** (-n)

            st.latex(
                fr"n = {d['ganze_jahre']} + \frac{{{d['ganze_monate']}}}{{12}} + "
                fr"\frac{{{d['ganze_tage']}}}{{360}} = {n:.4f}"
            )
            st.latex(fr"q = {q:.4f}")
            st.latex(r"K_0 = K_n \cdot q^{-n}")
            st.latex(fr"K_0 = {d['K_n']:.2f}\cdot {q:.4f}^{{-{n:.4f}}} = {K_0:.2f}")
            st.success(f"Der Barwert beträgt {euro(K_0)}.")

def _mode_unterjaehrig():
    key = "zz_unterjaehrig"

    if key in st.session_state and "m" not in st.session_state[key]:
        st.session_state.pop(key, None)

    if st.button("Neues Beispiel", key="zz_unterjaehrig_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = {
            "gesucht": random.choice(["endwert", "barwert"]),
            "m": random.choice([2, 4, 12]),
            "i_a": random.choice([2, 2.5, 3, 3.5, 4, 5]),
            "n_perioden": random.randint(3, 14),
            "K_0": random.choice([1000, 2000, 3000, 5000]),
            "K_n": random.choice([2000, 3000, 5000, 8000]),
        }

    d = st.session_state[key]

    m = d["m"]
    i_a = d["i_a"] / 100
    q_a = 1 + i_a
    i_m = q_a ** (1 / m) - 1
    q_m = 1 + i_m
    n_jahre = d["n_perioden"] / m

    periode = {2: "Semester", 4: "Quartale", 12: "Monate"}[m]

    st.subheader("Unterjährige Verzinsung")

    if d["gesucht"] == "endwert":
        st.markdown(
            f"**Aufgabe:** Es werden {euro(d['K_0'])} angelegt. "
            f"Der effektive Jahreszinssatz beträgt {d['i_a']} % p.a. "
            f"Die Laufzeit beträgt {d['n_perioden']} {periode}. Berechne den Endwert."
        )

        if st.button("Lösung anzeigen", key="zz_unterjaehrig_sol"):
            K_n = d["K_0"] * q_a ** n_jahre

            st.markdown("### Variante 1: Zeit umrechnen")
            st.latex(fr"n = \frac{{{d['n_perioden']}}}{{{m}}} = {n_jahre:.4f}")
            st.latex(fr"q = {q_a:.4f}")
            st.latex(fr"K_n = {d['K_0']:.2f}\cdot {q_a:.4f}^{{{n_jahre:.4f}}} = {K_n:.2f}")

            st.markdown("### Variante 2: Zinssatz umrechnen")
            st.latex(r"i_m = \sqrt[m]{1+i} - 1")
            st.latex(fr"i_m = \sqrt[{m}]{{1+{i_a:.4f}}} - 1 = {i_m:.6f}")
            st.latex(fr"q_m = 1+i_m = {q_m:.6f}")
            st.latex(fr"K_n = {d['K_0']:.2f}\cdot {q_m:.6f}^{{{d['n_perioden']}}} = {K_n:.2f}")

            st.success(f"Der Endwert beträgt {euro(K_n)}.")

    else:
        st.markdown(
            f"**Aufgabe:** Nach {d['n_perioden']} {periode} sollen {euro(d['K_n'])} vorhanden sein. "
            f"Der effektive Jahreszinssatz beträgt {d['i_a']} % p.a. Berechne den Barwert."
        )

        if st.button("Lösung anzeigen", key="zz_unterjaehrig_sol"):
            K_0 = d["K_n"] * q_a ** (-n_jahre)

            st.markdown("### Variante 1: Zeit umrechnen")
            st.latex(fr"n = \frac{{{d['n_perioden']}}}{{{m}}} = {n_jahre:.4f}")
            st.latex(fr"q = {q_a:.4f}")
            st.latex(fr"K_0 = {d['K_n']:.2f}\cdot {q_a:.4f}^{{-{n_jahre:.4f}}} = {K_0:.2f}")

            st.markdown("### Variante 2: Zinssatz umrechnen")
            st.latex(r"i_m = \sqrt[m]{1+i} - 1")
            st.latex(fr"i_m = \sqrt[{m}]{{1+{i_a:.4f}}} - 1 = {i_m:.6f}")
            st.latex(fr"q_m = 1+i_m = {q_m:.6f}")
            st.latex(fr"K_0 = {d['K_n']:.2f}\cdot {q_m:.6f}^{{-{d['n_perioden']}}} = {K_0:.2f}")

            st.success(f"Der Barwert beträgt {euro(K_0)}.")

def run():
    st.title("Zinseszins")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Barwert",
        "Endwert",
        "Barwert mehrere Zahlungen",
        "Endwert mehrere Zahlungen",
        "Angebote vergleichen",
        "KESt",
        "Theoretische Verzinsung",
        "Unterjährige Verzinsung",
    ])

    with tab1:
        _mode_barwert()

    with tab2:
        _mode_endwert()

    with tab3:
        _mode_barwert_mehrere()

    with tab4:
        _mode_endwert_mehrere()

    with tab5:
        _mode_angebote()

    with tab6:
        _mode_kest()

    with tab7:
        _mode_theoretische_verzinsung()

    with tab8:
        _mode_unterjaehrig()