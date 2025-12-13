# quadratische_funktionen.py
import streamlit as st
import random
import math
from fractions import Fraction

# ==========================================================
#   HELPERS
# ==========================================================

def _latex_quad(a, b, c, var="x"):
    def term(coeff, t):
        if coeff == 0:
            return ""
        if t == f"{var}^2":
            if coeff == 1:  return f"{var}^2"
            if coeff == -1: return f"-{var}^2"
        if t == var:
            if coeff == 1:  return var
            if coeff == -1: return f"-{var}"
        return f"{coeff}{t}"

    parts = [term(a, f"{var}^2"), term(b, var), term(c, "")]
    out = ""
    for p in parts:
        if not p:
            continue
        if out == "":
            out = p
        else:
            out += (" - " + p[1:]) if p.startswith("-") else (" + " + p)
    return out if out else "0"

def _money(x):
    return f"{x:.2f}".replace(".", ",")

def _fmt2(x):
    return f"{x:.2f}"

# ==========================================================
#   TAB 1 – DISKRIMINANTE / ANZAHL NULLSTELLEN (+ Nullstellen als Punkte)
# ==========================================================

def _gen_quadratic_eq():
    while True:
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-12, 12)
        c = random.randint(-12, 12)
        if b == 0 and c == 0:
            continue
        D = b*b - 4*a*c
        if abs(D) <= 400:
            return a, b, c, D

def _tab1():
    key = "quad_tab1"
    if st.button("Neues Beispiel", key="quad_tab1_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = _gen_quadratic_eq()

    a, b, c, D = st.session_state[key]

    st.subheader("Diskriminante & Nullstellen")
    st.markdown("**Aufgabe:** Ermittle die Anzahl der Nullstellen und begründe deine Antwort mit der Diskriminante.")
    st.latex(rf"{_latex_quad(a,b,c)} = 0")

    if st.button("Lösung anzeigen", key="quad_tab1_sol"):
        st.latex(rf"D = b^2 - 4ac = ({b})^2 - 4\cdot({a})\cdot({c}) = {D}")

        if D > 0:
            st.success("Da \(D>0\), gibt es **2 reelle Nullstellen**.")
            sqrtD = math.sqrt(D)
            x1 = (-b - sqrtD) / (2*a)
            x2 = (-b + sqrtD) / (2*a)
            lo, hi = sorted([x1, x2])
            st.latex(rf"N_1({ _fmt2(lo) }/0),\quad N_2({ _fmt2(hi) }/0)")
        elif D == 0:
            st.success("Da \(D=0\), gibt es **1 reelle (doppelte) Nullstelle**.")
            x0 = (-b) / (2*a)
            st.latex(rf"N_1({ _fmt2(x0) }/0)")
        else:
            st.success("Da \(D<0\), gibt es **keine reellen Nullstellen**.")

# ==========================================================
#   TAB 2 – ERLÖS / GEWINN (2 Buttons, Gewinnspanne nach innen runden)
# ==========================================================

def _gen_economics():
    while True:
        m = random.choice([-9,-8,-7,-6,-5,-4,-3,-2,-1]) / 10  # -0.9..-0.1
        n = random.randint(12, 30)

        u = random.choice([1,2,3]) / 10                        # 0.1..0.3
        v = random.randint(2, 10) / 10                         # 0.2..1.0
        w = random.randint(10, 60)

        A = m - u               # <0
        B = n - v
        C = -w

        D = B*B - 4*A*C
        if D <= 0:
            continue

        sqrtD = math.sqrt(D)
        x1 = (-B - sqrtD) / (2*A)
        x2 = (-B + sqrtD) / (2*A)
        lo, hi = sorted([x1, x2])

        if hi <= 0 or (hi - lo) < 5 or hi > 200:
            continue
        if m*hi + n <= 1:
            continue

        return dict(m=m, n=n, u=u, v=v, w=w, A=A, B=B, C=C, x1=lo, x2=hi)

def _tab2():
    key = "quad_tab2"
    stage_key = "quad_tab2_stage"  # 0=none, 1=E shown, 2=profit shown

    if st.button("Neues Beispiel", key="quad_tab2_new"):
        st.session_state.pop(key, None)
        st.session_state.pop(stage_key, None)

    if key not in st.session_state:
        st.session_state[key] = _gen_economics()
    if stage_key not in st.session_state:
        st.session_state[stage_key] = 0

    d = st.session_state[key]
    stage = st.session_state[stage_key]

    m, n = d["m"], d["n"]
    u, v, w = d["u"], d["v"], d["w"]
    A, B, C = d["A"], d["B"], d["C"]
    x1, x2 = d["x1"], d["x2"]

    st.subheader("Erlös- und Gewinnfunktion")

    st.markdown("**Preisfunktion gegeben:**")
    st.latex(rf"p(x) = {m:.2f}x + {n}".replace(".", ","))

    st.markdown("**Aufgabe 1:** Bestimme die Erlösfunktion.")

    if st.button("Lösung 1 anzeigen", key="quad_tab2_sol1"):
        st.session_state[stage_key] = 1
        st.rerun()

    if stage >= 1:
        st.latex(rf"E(x)= {m:.2f}x^2 + {n}x".replace(".", ","))

        st.markdown("---")
        st.markdown("**Kostenfunktion gegeben:**")
        st.latex(rf"K(x) = {u:.2f}x^2 + {v:.2f}x + {w}".replace(".", ","))

        st.markdown("**Aufgabe 2:** Ermittle die Gewinnfunktion, die Gewinnspanne und den maximalen Gewinn.")

        if st.button("Lösung 2 anzeigen", key="quad_tab2_sol2"):
            st.session_state[stage_key] = 2
            st.rerun()

    if stage >= 2:
        st.latex(rf"G(x)= {A:.2f}x^2 + {B:.2f}x {C:+.0f}".replace(".", ","))

        # Gewinnspanne nach innen runden:
        lo_in = math.ceil(x1)
        hi_in = math.floor(x2)

        x_star = -B / (2*A)
        G_star = A*x_star*x_star + B*x_star + C

        st.markdown(f"**Gewinnspanne:** von **{lo_in}** bis **{hi_in}**")
        st.markdown(f"**Max. Gewinn:** **{_money(G_star)} €**")

# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Quadratische Funktionen")

    tab1, tab2 = st.tabs(["Diskriminante", "Erlös & Gewinn"])

    with tab1:
        _tab1()

    with tab2:
        _tab2()
