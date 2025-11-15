import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.ticker import MultipleLocator


# -------- Hilfsfunktionen --------
def choose_int_excluding(low: int, high: int, exclude: set[int]) -> int:
    candidates = [v for v in range(low, high + 1) if v not in exclude]
    return random.choice(candidates)

def choose_k_simple() -> int:
    # k ∈ {-5,…,5}\{0}
    return choose_int_excluding(-5, 5, {0})

def choose_d_simple() -> int:
    # d ∈ {-4,…,4}\{0}
    return choose_int_excluding(-4, 4, {0})

def choose_d_simple_limited() -> int:
    # für Tab 3: d ∈ {-2,-1,1,2}
    return random.choice([-2, -1, 1, 2])

def choose_k_hard_limited() -> float:
    """k als gekürzter Bruch n/d mit |n|,|d| ≤ 5, inkl. 0, |k| ≤ 5."""
    nums = list(range(-5, 6))
    dens = list(range(1, 6))
    while True:
        n = random.choice(nums)
        d = random.choice(dens)
        if n == 0:
            return 0.0
        frac = Fraction(n, d).limit_denominator(5)
        k = float(frac.numerator / frac.denominator)
        if abs(k) <= 5:
            return k

def choose_d_hard_limited() -> int:
    # für Tab 2: d ∈ {-2,-1,0,1,2}
    return random.choice([-2, -1, 0, 1, 2])

def ensure_not_both_zero(k: float, d: float) -> Tuple[float, float]:
    if abs(k) < 1e-12 and abs(d) < 1e-12:
        k = 1.0
    return k, d

def slope_triangle_run_rise(k: float) -> Tuple[int, int]:
    """Dreieck: ganzzahlig k → run=1,rise=k; sonst Bruch p/q mit q≤5."""
    if abs(k) < 1e-12:
        return 1, 0
    if abs(k - round(k)) < 1e-12:
        return 1, int(round(k))
    frac = Fraction(k).limit_denominator(5)
    run = abs(frac.denominator)
    rise = int(frac.numerator)
    return run, rise

def latex_linear(k: float, d: float) -> str:
    """f(x)=kx+d (schön formatiert, inkl. Brüche)."""
    if abs(k - round(k)) < 1e-12:
        k_int = int(round(k))
        if k_int == 1:
            k_part = "x"
        elif k_int == -1:
            k_part = "-x"
        else:
            k_part = f"{k_int}x"
    else:
        frac = Fraction(k).limit_denominator(5)
        num, den = frac.numerator, frac.denominator
        if abs(num) == den:
            k_part = "x" if num > 0 else "-x"
        else:
            k_part = rf"\frac{{{num}}}{{{den}}}x"
    if abs(d) < 1e-12:
        d_part = ""
    else:
        sign = "+" if d > 0 else "-"
        d_part = f" {sign} {abs(int(round(d)))}"
    return rf"f(x) = {k_part}{d_part}"


# -------- Achsen & Plot --------
def apply_axes_style(ax):
    """Quadratisch (1:1), Achsen durch Ursprung, 1er-Ticks, ohne Beschriftungen, Bereich [-10,10]."""
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.spines["left"].set_linewidth(1.2)
    ax.spines["bottom"].set_linewidth(1.2)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_aspect("equal", adjustable="box")

def plot_line_with_triangle(ax, k: float, d: float, show_triangle: bool):
    """Zeichnet f(x)=kx+d im Ausschnitt [-10,10]; optional rotes, halbtransparentes Dreieck."""
    x = np.linspace(-10, 10, 801)
    y = k * x + d
    ax.plot(x, y, linewidth=2.5, color="#1f77b4")
    apply_axes_style(ax)
    if show_triangle:
        run, rise = slope_triangle_run_rise(k)
        x0, y0 = 0.0, d
        x1, y1 = x0 + run, y0
        x2, y2 = x1, y1 + rise
        ax.fill([x0, x1, x2], [y0, y1, y2], color="red", alpha=0.4, edgecolor="none")


# -------- Session Keys --------
KEYS = {
    "t1": {"prob": "t1_prob", "show": "t1_show"},
    "t2": {"prob": "t2_prob", "show": "t2_show"},
    "t3": {"prob": "t3_prob", "show": "t3_show"},
    "t4": {"prob": "t4_prob", "show": "t4_show"},
    # Tab 5 (Differenzenquotient)
    "t5": {"prob": "t5_prob", "stage": "t5_stage"},  # stage: 0=ohne Lösung, 1=Steigungen, 2=Bedeutung
}

@dataclass
class LinFunc:
    k: float
    d: float


# -------- Problem-Generatoren für Tabs 1-4 --------
def gen_tab1() -> LinFunc:
    # Einfach: k,d ganzzahlig, beide ≠ 0
    while True:
        k = float(choose_k_simple())
        d = float(choose_d_simple())
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab2() -> LinFunc:
    # Schwer: k als Bruch (q≤5), d ∈ {-2..2}, nicht beide 0
    while True:
        k = choose_k_hard_limited()
        d = float(choose_d_hard_limited())
        k, d = ensure_not_both_zero(k, d)
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab3() -> LinFunc:
    # Einfach (Ermitteln): k ganzzahlig ≠0, d ∈ {-2,-1,1,2}
    while True:
        k = float(choose_k_simple())
        d = float(choose_d_simple_limited())
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab4() -> LinFunc:
    # Schwer (Ermitteln): k als Bruch (q≤5), d ∈ [-4..4], nicht beide 0
    while True:
        k = choose_k_hard_limited()
        d = float(random.randint(-4, 4))
        k, d = ensure_not_both_zero(k, d)
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)


# -------- Neuer Tab 5: Differenzenquotient (Generator) --------
def gen_tab5_points() -> Dict:
    """
    Drei Punkte aus linearer (75 %) oder quadratischer (25 %) Funktion.
    - x > 0 (ganze Zahlen), ungleiche Abstände
    - y > 0 (durch Koeffizientenwahl/Neuversuch erzwungen)
    - f(x) höchstens 2 Nachkommastellen
    """
    # x: nur positiv, ungleiche Abstände
    xs = sorted(random.sample(range(1, 11), 3))
    while abs(xs[1] - xs[0]) == abs(xs[2] - xs[1]):
        xs = sorted(random.sample(range(1, 11), 3))

    # 3:1 Gewichtung zugunsten linear
    func_type = "linear" if random.random() < 0.75 else "quadratic"

    def pick_quarter(vmin, vmax, step=0.25):
        n = int((vmax - vmin) / step)
        return round(vmin + random.randint(0, n) * step, 2)

    if func_type == "linear":
        # positive Steigung und positiver Achsenabschnitt → y positiv
        k = pick_quarter(0.25, 2.5, 0.25)
        d = pick_quarter(0.5, 5.0, 0.25)
        f = lambda x: k * x + d
        coeffs = {"k": k, "d": d}
    else:
        # quadratisch: a>0, b≥0, c>0 → y positiv
        a_choices = [round(v, 2) for v in (0.25, 0.5, 0.75, 1.0)]
        a = random.choice(a_choices)
        b = pick_quarter(0.25, 2.0, 0.25)
        c = pick_quarter(0.5, 5.0, 0.25)
        f = lambda x: a * x * x + b * x + c
        coeffs = {"a": a, "b": b, "c": c}

    ys = [round(f(x), 2) for x in xs]

    # nur positive y sicherstellen
    if any(y <= 0 for y in ys):
        return gen_tab5_points()

    points = [
        {"x": xs[0], "fx": ys[0]},
        {"x": xs[1], "fx": ys[1]},
        {"x": xs[2], "fx": ys[2]},
    ]

    def slope(p, q):
        return (q["fx"] - p["fx"]) / (q["x"] - p["x"])

    k1 = slope(points[0], points[1])
    k2 = slope(points[1], points[2])

    return {"func_type": func_type, "coeffs": coeffs, "points": points, "k1": k1, "k2": k2}


# -------- UI --------
st.set_page_config(page_title="Lineare Funktionen", page_icon="🧮")

st.title("Lineare Funktionen")

st.markdown(
    """
    Eine lineare Funktion folgt dem Schema:
    """
)

st.latex("f(x) = kx + d")

st.markdown(
    """
    Der Parameter **k** steht für die **Steigung**, der Parameter **d** für den **Achsenabschnitt**.  
    Ein **Steigungsdreieck** wird üblicherweise bei **d** begonnen zu zeichnen.
    Man kann **einen Schritt nach rechts** gehen und dann **k hinauf oder hinunter**,  
    um zurück zur Funktion zu gelangen.

    Falls das zu klein ist (weil die Steigung **k** keine ganze Zahl ist),
    kann ein **größeres Dreieck** gezeichnet werden.

    Die Steigung kann dann mit dem **Differenzenquotienten** ermittelt werden:
    """
)

st.latex("k = \\frac{\\Delta y}{\\Delta x} = \\frac{y_2 - y_1}{x_2 - x_1}")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Zeichnen (leicht)",
    "Zeichnen (schwer)",
    "Ermitteln(einfach)",
    "Ermitteln(schwer)",
    "Differenzenquotient",
])

# Init Session
for key, names in KEYS.items():
    for subkey in names.values():
        if subkey not in st.session_state:
            if key == "t1" and subkey == names["prob"]:
                st.session_state[subkey] = gen_tab1()
            elif key == "t2" and subkey == names["prob"]:
                st.session_state[subkey] = gen_tab2()
            elif key == "t3" and subkey == names["prob"]:
                st.session_state[subkey] = gen_tab3()
            elif key == "t4" and subkey == names["prob"]:
                st.session_state[subkey] = gen_tab4()
            elif key == "t5" and subkey == names["prob"]:
                st.session_state[subkey] = gen_tab5_points()
            else:
                # Default für show/stage
                st.session_state[subkey] = False if "show" in subkey else 0


# -------- Rendering-Helfer für Tabs 1-4 --------
def draw_tab(tab_key: str, mode: str):
    """
    mode:
      - 'draw_easy' / 'draw_hard' (Tab1/2): Graph erst BEI LÖSUNG (mit Dreieck)
      - 'det_easy'  / 'det_hard'  (Tab3/4): Graph VOR LÖSUNG ohne Dreieck; BEI LÖSUNG k,d + Gleichung + Graph mit Dreieck
    """
    prob: LinFunc = st.session_state[KEYS[tab_key]["prob"]]
    show = st.session_state[KEYS[tab_key]["show"]]

    st.subheader("Aufgabe")

    if mode.startswith("draw"):
        st.write("Gegeben ist die Funktion:")
        st.latex(latex_linear(prob.k, prob.d))
        st.write("Zeichne den Graphen der Funktion **mit Hilfe eines Steigungsdreiecks** ein.")
    else:
        st.write("Bestimme die **Funktionsgleichung** über das **Steigungsdreieck**.")

    c1, c2 = st.columns(2)
    if c1.button("Lösung anzeigen", key=f"{tab_key}_show_btn"):
        st.session_state[KEYS[tab_key]["show"]] = True
        st.rerun()
    if c2.button("Neue Aufgabe", key=f"{tab_key}_new_btn"):
        if tab_key == "t1":
            st.session_state[KEYS[tab_key]["prob"]] = gen_tab1()
        elif tab_key == "t2":
            st.session_state[KEYS[tab_key]["prob"]] = gen_tab2()
        elif tab_key == "t3":
            st.session_state[KEYS[tab_key]["prob"]] = gen_tab3()
        else:
            st.session_state[KEYS[tab_key]["prob"]] = gen_tab4()
        st.session_state[KEYS[tab_key]["show"]] = False
        st.rerun()

    if mode.startswith("draw"):
        # Tab1/2: Vor Lösung kein Graph
        if show:
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=True)
            st.pyplot(fig)
            st.markdown(f"**k =** {prob.k:g}, **d =** {prob.d:g}")
    else:
        # Tab3/4: Vor Lösung Graph ohne Dreieck
        if not show:
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=False)
            st.pyplot(fig)
        else:
            st.markdown(f"**k =** {prob.k:g}, **d =** {prob.d:g}")
            st.latex(latex_linear(prob.k, prob.d))
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=True)
            st.pyplot(fig)


# -------- Tabs 1-4 --------
with tab1:
    draw_tab("t1", "draw_easy")
with tab2:
    draw_tab("t2", "draw_hard")
with tab3:
    draw_tab("t3", "det_easy")
with tab4:
    draw_tab("t4", "det_hard")


# -------- Tab 5: Differenzenquotient --------
with tab5:
    data = st.session_state[KEYS["t5"]["prob"]]
    stage = st.session_state[KEYS["t5"]["stage"]]

    st.subheader("Differenzenquotient aus drei Punkten")
    st.markdown(
    """
**Aufgabe 1:** Berechne die Steigung mit dem **Differenzenquotienten**  
zwischen P₁ und P₂ sowie zwischen P₂ und P₃.
"""
)


    # Tabelle (ohne Indexzahlen und ohne "P"-Spalte; P₁/P₂/P₃ als Zeilenlabels)
    df = pd.DataFrame(
        [[p["x"], f"{p['fx']:.2f}"] for p in data["points"]],
        columns=["x", "f(x)"],
    )
    df.index = ["P₁", "P₂", "P₃"]
    st.table(df)

    # Buttons: Lösung 1, Neues Beispiel
    c1, c2 = st.columns(2)
    if c1.button("Lösung (Steigungen)", key="t5_sol1"):
        st.session_state[KEYS["t5"]["stage"]] = 1
        st.rerun()
    if c2.button("Neues Beispiel", key="t5_new"):
        st.session_state[KEYS["t5"]["prob"]] = gen_tab5_points()
        st.session_state[KEYS["t5"]["stage"]] = 0
        st.rerun()

    # Steigungen berechnen
    p1, p2, p3 = data["points"]
    x1, y1 = p1["x"], p1["fx"]
    x2, y2 = p2["x"], p2["fx"]
    x3, y3 = p3["x"], p3["fx"]
    k1 = (y2 - y1) / (x2 - x1)
    k2 = (y3 - y2) / (x3 - x2)

    if stage >= 1:
        st.write("**Berechnungen:**")
        st.latex(
            rf"k_1 = \frac{{f(x_2)-f(x_1)}}{{x_2-x_1}}"
            rf"= \frac{{{y2:.2f}-{y1:.2f}}}{{{x2}-{x1}}} = {k1:.2f}"
        )
        st.latex(
            rf"k_2 = \frac{{f(x_3)-f(x_2)}}{{x_3-x_2}}"
            rf"= \frac{{{y3:.2f}-{y2:.2f}}}{{{x3}-{x2}}} = {k2:.2f}"
        )

        st.markdown("---")
        same = math.isclose(k1, k2, rel_tol=1e-9, abs_tol=1e-9)
        if same:
            st.markdown("**Aufgabe 2:** Was bedeutet es, wenn beide Steigungen **gleich** sind?")
            if st.button("Lösung (Bedeutung)", key="t5_sol2_same"):
                st.success("Es liegt eine **lineare Funktion** vor.")
        else:
            st.markdown("**Aufgabe 2:** Was bedeutet es, wenn die Steigungen **nicht gleich** sind?")
            if st.button("Lösung (Bedeutung)", key="t5_sol2_diff"):
                st.success("Es liegt **keine** lineare Funktion vor.")
