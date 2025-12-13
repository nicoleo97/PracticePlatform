import streamlit as st
import random


# ==========================================================
#   HILFSFUNKTIONEN
# ==========================================================

def _random_table():
    years = sorted(random.sample(range(1995, 2025), 4))
    start = random.uniform(100, 900)

    scenario = random.choice(["sparbuch", "briefmarken", "muenzen"])
    values = [round(start, 2)]

    for _ in range(3):
        if scenario == "sparbuch":
            values.append(round(values[-1] + random.uniform(20, 120), 2))
        elif scenario == "briefmarken":
            values.append(round(values[-1] - random.uniform(10, 80), 2))
        else:
            values.append(round(values[-1] + random.uniform(50, 200), 2))

    return years, values, scenario


def _scenario_text(name, scenario):
    if scenario == "sparbuch":
        return f"{name} legt Geld auf einem Sparbuch an. Die folgende Tabelle zeigt den Wert des Sparbuchs in Euro zum jeweiligen Jahr:"
    if scenario == "briefmarken":
        return f"{name} besitzt eine Briefmarkensammlung, die an Wert verliert. Die folgende Tabelle zeigt den Wert in Euro zum jeweiligen Jahr:"
    return f"{name} hat eine Münzsammlung, die an Wert gewinnt. Die folgende Tabelle zeigt den Wert in Euro zum jeweiligen Jahr:"


# ==========================================================
#   ÄNDERUNGSMAßE
# ==========================================================

def _mode_abs():
    key = "aend_abs"

    if st.button("Neues Beispiel", key="btn_abs_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        years, vals, scen = _random_table()
        st.session_state[key] = {
            "years": years,
            "vals": vals,
            "scenario": scen,
            "name": random.choice(["Anna", "Ben", "Clara", "David", "Eva", "Felix"]),
            "i1": None,
            "i2": None,
        }

    data = st.session_state[key]
    years, vals, scen, name = data["years"], data["vals"], data["scenario"], data["name"]

    st.subheader("Absolute Änderung")
    st.write(_scenario_text(name, scen))
    st.dataframe({"t [Jahr]": years, "W(t) [Euro]": vals}, hide_index=True)

    if data["i1"] is None:
        data["i1"], data["i2"] = sorted(random.sample(range(4), 2))

    i1, i2 = data["i1"], data["i2"]
    t1, t2 = years[i1], years[i2]
    w1, w2 = vals[i1], vals[i2]

    st.markdown(f"**Aufgabe:** Ermittle die absolute Änderung zwischen **{t1}** und **{t2}**.")

    if st.button("Lösung anzeigen", key="btn_abs_sol"):
        diff = round(w2 - w1, 2)
        st.latex(rf"W({t2}) - W({t1}) = {w2} - {w1} = {diff}\ \text{{Euro}}")


def _mode_mittel():
    key = "aend_mittel"

    if st.button("Neues Beispiel", key="btn_mittel_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        years, vals, scen = _random_table()
        st.session_state[key] = {
            "years": years,
            "vals": vals,
            "scenario": scen,
            "name": random.choice(["Anna", "Ben", "Clara", "David", "Eva", "Felix"]),
            "i1": None,
            "i2": None,
        }

    data = st.session_state[key]
    years, vals, scen, name = data["years"], data["vals"], data["scenario"], data["name"]

    st.subheader("Mittlere Änderung")
    st.write(_scenario_text(name, scen))
    st.dataframe({"t [Jahr]": years, "W(t) [Euro]": vals}, hide_index=True)

    if data["i1"] is None:
        data["i1"], data["i2"] = sorted(random.sample(range(4), 2))

    i1, i2 = data["i1"], data["i2"]
    t1, t2 = years[i1], years[i2]
    w1, w2 = vals[i1], vals[i2]

    st.markdown(f"**Aufgabe:** Ermittle die mittlere Änderung zwischen **{t1}** und **{t2}**.")

    if st.button("Lösung anzeigen", key="btn_mittel_sol"):
        avg = round((w2 - w1) / (t2 - t1), 2)
        st.latex(
            rf"\frac{{W({t2}) - W({t1})}}{{{t2}-{t1}}} = "
            rf"\frac{{{w2}-{w1}}}{{{t2-t1}}} = {avg}\ \text{{Euro/Jahr}}"
        )


def _mode_rel():
    key = "aend_rel"

    if st.button("Neues Beispiel", key="btn_rel_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        years, vals, scen = _random_table()
        st.session_state[key] = {
            "years": years,
            "vals": vals,
            "scenario": scen,
            "name": random.choice(["Anna", "Ben", "Clara", "David", "Eva", "Felix"]),
            "i1": None,
            "i2": None,
        }

    data = st.session_state[key]
    years, vals, scen, name = data["years"], data["vals"], data["scenario"], data["name"]

    st.subheader("Relative Änderung")
    st.write(_scenario_text(name, scen))
    st.dataframe({"t [Jahr]": years, "W(t) [Euro]": vals}, hide_index=True)

    if data["i1"] is None:
        data["i1"], data["i2"] = sorted(random.sample(range(4), 2))

    i1, i2 = data["i1"], data["i2"]
    t1, t2 = years[i1], years[i2]
    w1, w2 = vals[i1], vals[i2]

    st.markdown(f"**Aufgabe:** Ermittle die relative Änderung zwischen **{t1}** und **{t2}**.")

    if st.button("Lösung anzeigen", key="btn_rel_sol"):
        rel_dec = round((w2 - w1) / w1, 4)
        rel_pct = round(rel_dec * 100, 2)

        st.latex(
            rf"\frac{{W({t2}) - W({t1})}}{{W({t1})}} = "
            rf"\frac{{{w2}-{w1}}}{{{w1}}} = {rel_dec}"
        )
        st.markdown(f"**≈ {rel_pct}%**")


# ==========================================================
#   ÄNDERUNGSFAKTOREN
# ==========================================================

def _changer_single():
    if st.button("Neues Beispiel", key="af_new"):
        st.session_state.pop("af_single", None)

    if "af_single" not in st.session_state:
        perc = random.choice([round(random.uniform(0.5, 50), 1), random.randint(1, 70)])
        direction = random.choice(["steigt", "sinkt"])
        item = random.choice([
            "Der Wert eines Handys",
            "Der Preis einer Jacke",
            "Der Wert einer Aktie",
            "Der Wert eines Fahrrads"
        ])
        st.session_state["af_single"] = (item, direction, perc)

    item, direction, perc = st.session_state["af_single"]

    st.markdown(f"**Angabe:** {item} {direction} um **{perc}%**.")
    st.markdown("**Aufgabe:** Ermittle den Änderungsfaktor.")

    if st.button("Lösung anzeigen", key="af_sol"):
        p_dec = round(perc / 100, 4)
        a = 1 + p_dec if direction == "steigt" else 1 - p_dec
        op = "+" if direction == "steigt" else "-"
        st.latex(rf"a = 1 {op} {p_dec} = {a:.4f}")


def _changer_total():
    if st.button("Neues Beispiel", key="afg_new"):
        st.session_state.pop("af_ges", None)

    if "af_ges" not in st.session_state:
        steps = []
        for _ in range(3):
            perc = random.choice([round(random.uniform(0.5, 50), 1), random.randint(1, 70)])
            direction = random.choice(["steigt", "sinkt"])
            a = round(1 + perc/100, 4) if direction == "steigt" else round(1 - perc/100, 4)
            steps.append((direction, perc, a))

        item = random.choice([
            "Der Wert eines Handys",
            "Der Preis einer Jacke",
            "Der Wert einer Aktie",
            "Der Wert eines Fahrrads"
        ])

        st.session_state["af_ges"] = (item, steps)

    item, steps = st.session_state["af_ges"]

    text = f"{item} "
    for i, (direction, perc, _) in enumerate(steps):
        if i == 0:
            text += f"{direction} zuerst um {perc}%"
        elif i == 1:
            text += f", {direction} im 2. Jahr um {perc}%"
        else:
            text += f" und {direction} im 3. Jahr um {perc}%"
    text += "."

    st.markdown(f"**Angabe:** {text}")
    st.markdown("**Aufgabe:** Ermittle den gesamten Änderungsfaktor.")

    if st.button("Lösung anzeigen", key="afg_sol"):
        facs = [a for (_, _, a) in steps]
        prod = 1
        for f in facs:
            prod *= f

        latex_chain = " \\cdot ".join([f"{f:.4f}" for f in facs])
        st.latex(rf"a_\text{{gesamt}} = {latex_chain} = {prod:.4f}")


def _changer_mean():
    if "af_mittel" in st.session_state and len(st.session_state["af_mittel"]) != 3:
        st.session_state.pop("af_mittel")

    if st.button("Neues Beispiel", key="afm_new"):
        st.session_state.pop("af_mittel", None)

    if "af_mittel" not in st.session_state:
        steps = []
        for _ in range(3):
            perc = random.choice([round(random.uniform(0.5, 50), 1), random.randint(1, 70)])
            direction = random.choice(["steigt", "sinkt"])
            a = round(1 + perc/100, 4) if direction == "steigt" else round(1 - perc/100, 4)
            steps.append((direction, perc, a))

        unit = random.choice(["Monat", "Woche", "Jahr"])
        item = random.choice([
            "Der Wert eines Handys",
            "Der Preis einer Jacke",
            "Der Wert einer Aktie",
            "Der Wert eines Fahrrads"
        ])

        st.session_state["af_mittel"] = (item, steps, unit)

    item, steps, unit = st.session_state["af_mittel"]

    text = f"{item} "
    for i, (direction, perc, _) in enumerate(steps):
        if i == 0:
            text += f"{direction} im 1. {unit} um {perc}%"
        elif i == 1:
            text += f", {direction} im 2. {unit} um {perc}%"
        else:
            text += f" und {direction} im 3. {unit} um {perc}%"
    text += "."

    st.markdown(f"**Angabe:** {text}")
    st.markdown("**Aufgabe:** Ermittle den mittleren Änderungsfaktor.")

    if st.button("Lösung anzeigen", key="afm_sol"):
        facs = [a for (_, _, a) in steps]
        prod = 1
        for f in facs:
            prod *= f

        a_mittel = prod ** (1/3)
        latex_chain = " \\cdot ".join([f"{f:.4f}" for f in facs])

        st.latex(rf"a_\text{{gesamt}} = {latex_chain} = {prod:.4f}")
        st.latex(rf"a_\text{{mittel}} = \sqrt[3]{{{prod:.4f}}} = {a_mittel:.4f}")


# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Änderungsmaße")

    tab1, tab2 = st.tabs(["Änderungsmaße", "Änderungsfaktoren"])

    with tab1:
        t1, t2, t3 = st.tabs(["Absolute Änderung", "Mittlere Änderung", "Relative Änderung"])
        with t1:
            _mode_abs()
        with t2:
            _mode_mittel()
        with t3:
            _mode_rel()

    with tab2:
        f1, f2, f3 = st.tabs(["Änderungsfaktor", "Gesamter Änderungsfaktor", "Mittlerer Änderungsfaktor"])
        with f1:
            _changer_single()
        with f2:
            _changer_total()
        with f3:
            _changer_mean()
