import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.ticker import MultipleLocator


# ==========================================================
#   LINEARE FUNKTIONEN
# ==========================================================

# -------- Hilfsfunktionen --------
def choose_int_excluding(low: int, high: int, exclude: set[int]) -> int:
    candidates = [v for v in range(low, high + 1) if v not in exclude]
    return random.choice(candidates)

def choose_k_simple() -> int:
    return choose_int_excluding(-5, 5, {0})

def choose_d_simple() -> int:
    return choose_int_excluding(-4, 4, {0})

def choose_d_simple_limited() -> int:
    return random.choice([-2, -1, 1, 2])

def choose_k_hard_limited() -> float:
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
    return random.choice([-2, -1, 0, 1, 2])

def ensure_not_both_zero(k: float, d: float) -> Tuple[float, float]:
    if abs(k) < 1e-12 and abs(d) < 1e-12:
        k = 1.0
    return k, d

def slope_triangle_run_rise(k: float) -> Tuple[int, int]:
    if abs(k) < 1e-12:
        return 1, 0
    if abs(k - round(k)) < 1e-12:
        return 1, int(round(k))
    frac = Fraction(k).limit_denominator(5)
    run = abs(frac.denominator)
    rise = int(frac.numerator)
    return run, rise

def latex_linear(k: float, d: float) -> str:
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
    x = np.linspace(-10, 10, 801)
    y = k * x + d
    ax.plot(x, y, linewidth=2.5)
    apply_axes_style(ax)

    if show_triangle:
        run, rise = slope_triangle_run_rise(k)
        x0, y0 = 0.0, d
        x1, y1 = x0 + run, y0
        x2, y2 = x1, y1 + rise
        ax.fill([x0, x1, x2], [y0, y1, y2], alpha=0.35)


# -------- Dataclass --------
@dataclass
class LinFunc:
    k: float
    d: float


# -------- Problem-Generatoren (Tabs 1-4) --------
def gen_tab1() -> LinFunc:
    while True:
        k = float(choose_k_simple())
        d = float(choose_d_simple())
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab2() -> LinFunc:
    while True:
        k = choose_k_hard_limited()
        d = float(choose_d_hard_limited())
        k, d = ensure_not_both_zero(k, d)
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab3() -> LinFunc:
    while True:
        k = float(choose_k_simple())
        d = float(choose_d_simple_limited())
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)

def gen_tab4() -> LinFunc:
    while True:
        k = choose_k_hard_limited()
        d = float(random.randint(-4, 4))
        k, d = ensure_not_both_zero(k, d)
        if abs(k) > 1e-12 or abs(d) > 1e-12:
            return LinFunc(k, d)


# -------- Tab 5: Differenzenquotient --------
def gen_tab5_points() -> Dict:
    xs = sorted(random.sample(range(1, 11), 3))
    while abs(xs[1] - xs[0]) == abs(xs[2] - xs[1]):
        xs = sorted(random.sample(range(1, 11), 3))

    func_type = "linear" if random.random() < 0.75 else "quadratic"

    def pick_quarter(vmin, vmax, step=0.25):
        n = int((vmax - vmin) / step)
        return round(vmin + random.randint(0, n) * step, 2)

    if func_type == "linear":
        k = pick_quarter(0.25, 2.5, 0.25)
        d = pick_quarter(0.5, 5.0, 0.25)
        f = lambda x: k * x + d
    else:
        a = random.choice([0.25, 0.5, 0.75, 1.0])
        b = pick_quarter(0.25, 2.0, 0.25)
        c = pick_quarter(0.5, 5.0, 0.25)
        f = lambda x: a * x * x + b * x + c

    ys = [round(f(x), 2) for x in xs]
    if any(y <= 0 for y in ys):
        return gen_tab5_points()

    points = [{"x": xs[i], "fx": ys[i]} for i in range(3)]
    return {"func_type": func_type, "points": points}


# -------- Rendering Tabs 1-4 --------
def draw_tab(prob: LinFunc, show: bool, mode: str, key_prefix: str):
    st.subheader("Aufgabe")

    if mode.startswith("draw"):
        st.write("Gegeben ist die Funktion:")
        st.latex(latex_linear(prob.k, prob.d))
        st.write("Zeichne den Graphen der Funktion **mit Hilfe eines Steigungsdreiecks** ein.")
    else:
        st.write("Bestimme die **Funktionsgleichung** über das **Steigungsdreieck**.")

    c1, c2 = st.columns(2)
    if c1.button("Lösung anzeigen", key=f"{key_prefix}_show_btn"):
        st.session_state[f"{key_prefix}_show"] = True
        st.rerun()
    if c2.button("Neue Aufgabe", key=f"{key_prefix}_new_btn"):
        gen = {"t1": gen_tab1, "t2": gen_tab2, "t3": gen_tab3, "t4": gen_tab4}[key_prefix]
        st.session_state[f"{key_prefix}_prob"] = gen()
        st.session_state[f"{key_prefix}_show"] = False
        st.rerun()

    if mode.startswith("draw"):
        if show:
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_line_with_triangle(ax, prob.k, prob.d, show_triangle=True)
            st.pyplot(fig)
            st.markdown(f"**k =** {prob.k:g}, **d =** {prob.d:g}")
    else:
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


# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Lineare Funktionen")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Zeichnen (leicht)", "Zeichnen (schwer)", "Ermitteln (einfach)", "Ermitteln (schwer)", "Differenzenquotient"]
    )

    # Session Init
    for t in ["t1", "t2", "t3", "t4"]:
        if f"{t}_prob" not in st.session_state:
            st.session_state[f"{t}_prob"] = {"t1": gen_tab1, "t2": gen_tab2, "t3": gen_tab3, "t4": gen_tab4}[t]()
        if f"{t}_show" not in st.session_state:
            st.session_state[f"{t}_show"] = False

    if "t5_prob" not in st.session_state:
        st.session_state["t5_prob"] = gen_tab5_points()
    if "t5_stage" not in st.session_state:
        st.session_state["t5_stage"] = 0

    with tab1:
        draw_tab(st.session_state["t1_prob"], st.session_state["t1_show"], "draw_easy", "t1")
    with tab2:
        draw_tab(st.session_state["t2_prob"], st.session_state["t2_show"], "draw_hard", "t2")
    with tab3:
        draw_tab(st.session_state["t3_prob"], st.session_state["t3_show"], "det_easy", "t3")
    with tab4:
        draw_tab(st.session_state["t4_prob"], st.session_state["t4_show"], "det_hard", "t4")

    with tab5:
        data = st.session_state["t5_prob"]
        stage = st.session_state["t5_stage"]

        st.subheader("Differenzenquotient aus drei Punkten")
        st.markdown(
            """
            **Aufgabe 1:** Berechne die Steigung mit dem Differenzenquotienten  
            zwischen P₁ und P₂ sowie zwischen P₂ und P₃.
            """
        )

        df = pd.DataFrame([[p["x"], f"{p['fx']:.2f}"] for p in data["points"]], columns=["x", "f(x)"])
        df.index = ["P₁", "P₂", "P₃"]
        st.table(df)

        c1, c2 = st.columns(2)
        if c1.button("Lösung (Steigungen)", key="t5_sol1"):
            st.session_state["t5_stage"] = 1
            st.rerun()
        if c2.button("Neues Beispiel", key="t5_new"):
            st.session_state["t5_prob"] = gen_tab5_points()
            st.session_state["t5_stage"] = 0
            st.rerun()

        p1, p2, p3 = data["points"]
        x1, y1 = p1["x"], p1["fx"]
        x2, y2 = p2["x"], p2["fx"]
        x3, y3 = p3["x"], p3["fx"]

        k1 = (y2 - y1) / (x2 - x1)
        k2 = (y3 - y2) / (x3 - x2)

        if stage >= 1:
            st.write("**Berechnungen:**")
            st.latex(rf"k_1 = \frac{{{y2:.2f}-{y1:.2f}}}{{{x2}-{x1}}} = {k1:.2f}")
            st.latex(rf"k_2 = \frac{{{y3:.2f}-{y2:.2f}}}{{{x3}-{x2}}} = {k2:.2f}")

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
