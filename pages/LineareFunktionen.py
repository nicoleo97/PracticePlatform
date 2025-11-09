import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
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
    # d ∈ {-2,-1,1,2} (für Tab 3)
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
    # d ∈ {-2,-1,0,1,2} (für Tab 2)
    return random.choice([-2, -1, 0, 1, 2])

def ensure_not_both_zero(k: float, d: float) -> Tuple[float, float]:
    if abs(k) < 1e-12 and abs(d) < 1e-12:
        k = 1.0
    return k, d

def slope_triangle_run_rise(k: float) -> Tuple[int, int]:
    """Steigungsdreieck-Regel."""
    if abs(k) < 1e-12:
        return 1, 0
    if abs(k - round(k)) < 1e-12:
        return 1, int(round(k))
    frac = Fraction(k).limit_denominator(5)
    return abs(frac.denominator), int(frac.numerator)

def latex_linear(k: float, d: float) -> str:
    """f(x)=kx+d in LaTeX (auch für Brüche)."""
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
        k_part = "x" if abs(num) == den else rf"\frac{{{num}}}{{{den}}}x"
        if abs(num) == den and num < 0:
            k_part = "-x"
    if abs(d) < 1e-12:
        d_part = ""
    else:
        d_part = f" {'+' if d > 0 else '-'} {abs(int(round(d)))}"
    return rf"f(x) = {k_part}{d_part}"


# -------- Achsen & Plot --------
def apply_axes_style(ax):
    """Quadratisch (1:1), Achsen durch Ursprung, 1er-Ticks, ohne Beschriftungen, Bereich [-10,10]."""
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which="both", linestyle="--", alpha=0.4)

    # Achsen durch (0,0)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.spines["left"].set_linewidth(1.2)
    ax.spines["bottom"].set_linewidth(1.2)

    # keine Achsentitel
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
}

@dataclass
class LinFunc:
    k: float
    d: float


# -------- Problem-Generatoren --------
def gen_tab1() -> LinFunc:
    while True:
        k = float(choose_k_simple())
        d = float(choose_d_simple())
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab2() -> LinFunc:
    while True:
        k = choose_k_hard_limited()
        d = float(choose_d_hard_limited())  # d ∈ {-2,-1,0,1,2}
        k, d = ensure_not_both_zero(k, d)
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab3() -> LinFunc:
    while True:
        k = float(choose_k_simple())
        d = float(choose_d_simple_limited())  # d ∈ {-2,-1,1,2}
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab4() -> LinFunc:
    while True:
        k = choose_k_hard_limited()
        d = float(random.randint(-4, 4))     # schwer, breiteres d
        k, d = ensure_not_both_zero(k, d)
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)


# -------- UI --------
st.title("Lineare Funktionen – Steigungsdreieck & Funktionsgleichung")
st.markdown(
    """
**Was ist zu tun?**
- **Zeichnen (leicht):** Gegeben ist die Funktion. Zeichne den Graphen der Funktion **mit Hilfe eines Steigungsdreiecks** ein.  
- **Zeichnen (schwer):** Wie links; nicht-ganzzahliges \(k\) als gekürzter Bruch mit \(|\mathrm{Zähler}|, \mathrm{Nenner} \le 5\). Zeichne den Graphen der Funktion **mit Hilfe eines Steigungsdreiecks** ein.  
- **Ermitteln(einfach):** Aus dem Graphen die **Funktionsgleichung** über das Steigungsdreieck bestimmen.  
- **Ermitteln(schwer):** Wie links; \(k\) ggf. als Bruch mit kleinem Nenner denken (\(\le 5\)).
  
**Koordinatensystem:** quadratisch (1:1), Achsen durch den Ursprung, 1er-Ticks, Bereich **−10…10**.
"""
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Zeichnen (leicht)",
    "Zeichnen (schwer)",
    "Ermitteln(einfach)",
    "Ermitteln(schwer)",
])

# Init Session
for key, names in KEYS.items():
    if names["prob"] not in st.session_state:
        if key == "t1":
            st.session_state[names["prob"]] = gen_tab1()
        elif key == "t2":
            st.session_state[names["prob"]] = gen_tab2()
        elif key == "t3":
            st.session_state[names["prob"]] = gen_tab3()
        else:
            st.session_state[names["prob"]] = gen_tab4()
    if names["show"] not in st.session_state:
        st.session_state[names["show"]] = False


# -------- Rendering-Helfer --------
def draw_tab(tab_key: str, mode: str):
    """
    mode:
      - 'draw_easy' / 'draw_hard' (Tab1/2): Graph erst BEI LÖSUNG anzeigen (mit Dreieck)
      - 'det_easy'  / 'det_hard'  (Tab3/4): Graph VOR LÖSUNG ohne Dreieck; BEI LÖSUNG k,d + Gleichung + Graph mit Dreieck
    """
    prob: LinFunc = st.session_state[KEYS[tab_key]["prob"]]
    show: bool = st.session_state[KEYS[tab_key]["show"]]

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

    # Anzeige-Logik
    if mode.startswith("draw"):
        # Tab1/2: VOR Lösung KEIN Graph
        if show:
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=True)
            st.pyplot(fig)
            st.markdown(f"**k =** {prob.k:g}, **d =** {prob.d:g}")
    else:
        # Tab3/4: VOR Lösung Graph OHNE Dreieck
        if not show:
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=False)
            st.pyplot(fig)
        else:
            # BEI Lösung: k,d + Gleichung + Graph MIT Dreieck
            st.markdown(f"**k =** {prob.k:g}, **d =** {prob.d:g}")
            st.latex(latex_linear(prob.k, prob.d))
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=True)
            st.pyplot(fig)


# -------- Tabs ausführen --------
with tab1:
    draw_tab("t1", "draw_easy")
with tab2:
    draw_tab("t2", "draw_hard")
with tab3:
    draw_tab("t3", "det_easy")
with tab4:
    draw_tab("t4", "det_hard")
