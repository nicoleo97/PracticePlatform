import streamlit as st
import random
import math


# ============================
#   EXAMPLE-GENERATOREN
# ============================

def _make_example_A():
    # e^{ax} - b = c
    a = random.randint(11, 100) / 10    # 1.1 … 10.0
    b = random.randint(10, 200) / 10    # 1.0 … 20.0
    c = random.randint(10, 300) / 10    # 1.0 … 30.0
    q = b + c
    w = math.log(q) / a
    return {"type": "A", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_B():
    # e^{ax} + b = (c+b)
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = c
    w = math.log(q) / a
    return {"type": "B", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_C():
    # 10^{ax} - b = c
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = math.log10(q) / a
    return {"type": "C", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_D():
    # 10^{ax} + b = (c+b)
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = c
    w = math.log10(q) / a
    return {"type": "D", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_E():
    # n^{a+x} - b = c
    n = random.randint(2, 10)
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = math.log(q) / math.log(n) - a
    return {"type": "E", "n": n, "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_F():
    # n * x^a - b = c
    n = random.randint(2, 10)
    a = random.randint(1, 5)  # ganzzahliger Exponent
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = (q / n) ** (1 / a)
    return {"type": "F", "n": n, "a": a, "b": b, "c": c, "q": q, "w": w}


# ============================
#   ZUFALLS-LOGIK
# ============================

def _random_mixed():
    # A:B:C:D:E:F = 30:30:15:15:10:15  → 1..115
    r = random.randint(1, 115)
    if r <= 30:
        return _make_example_A()
    elif r <= 60:
        return _make_example_B()
    elif r <= 75:
        return _make_example_C()
    elif r <= 90:
        return _make_example_D()
    elif r <= 100:
        return _make_example_E()
    else:
        return _make_example_F()


def _random_AB():
    return _make_example_A() if random.random() < 0.5 else _make_example_B()


def _random_CD():
    return _make_example_C() if random.random() < 0.5 else _make_example_D()


def _random_F():
    return _make_example_F()


# ============================
#   DARSTELLUNG
# ============================

def _render_example(ex, key_suffix: str):
    t = ex["type"]
    a = ex["a"]
    b = ex["b"]
    c = ex["c"]
    q = ex["q"]
    w = ex["w"]

    # Aufgabentext
    st.markdown(
        """
        **Aufgabe**  
        Ermittle den Wert von $x$ und dokumentiere deine Umformungsschritte.  
        *(Tipp: Überprüfe dein Ergebnis auch mit GeoGebra.)*
        """
    )

    # Angabe
    if t == "A":
        st.latex(rf"e^{{{a}x}} - {b} = {c}")

    elif t == "B":
        right = round(c + b, 1)
        st.latex(rf"e^{{{a}x}} + {b} = {right}")

    elif t == "C":
        st.latex(rf"10^{{{a}x}} - {b} = {c}")

    elif t == "D":
        right = round(c + b, 1)
        st.latex(rf"10^{{{a}x}} + {b} = {right}")

    elif t == "E":
        n = ex["n"]
        st.latex(rf"{n}^{{({a}+x)}} - {b} = {c}")

    elif t == "F":
        n = ex["n"]
        st.latex(rf"{n}\cdot x^{{{a}}} - {b} = {c}")

    st.write("\n\n")

    # Lösung
    st.markdown("**Lösung**")
    show = st.button("Lösung anzeigen", key=f"btn_solution_{key_suffix}")

    if not show:
        return

    if t == "A":
        st.latex(
            rf"""
            \begin{{aligned}}
            e^{{{a}x}} - {b} &= {c} \quad \vert +\,{b} \\
            e^{{{a}x}} &= {q} \quad \vert\ \ln() \\
            {a}x &= \ln({q}) \quad \vert :\,{a} \\
            x &= \frac{{\ln({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )

    elif t == "B":
        right = round(c + b, 1)
        st.latex(
            rf"""
            \begin{{aligned}}
            e^{{{a}x}} + {b} &= {right} \quad \vert -\,{b} \\
            e^{{{a}x}} &= {q} \quad \vert\ \ln() \\
            {a}x &= \ln({q}) \quad \vert :\,{a} \\
            x &= \frac{{\ln({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )

    elif t == "C":
        st.latex(
            rf"""
            \begin{{aligned}}
            10^{{{a}x}} - {b} &= {c} \quad \vert +\,{b} \\
            10^{{{a}x}} &= {q} \quad \vert\ \lg() \\
            {a}x &= \lg({q}) \quad \vert :\,{a} \\
            x &= \frac{{\lg({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )

    elif t == "D":
        right = round(c + b, 1)
        st.latex(
            rf"""
            \begin{{aligned}}
            10^{{{a}x}} + {b} &= {right} \quad \vert -\,{b} \\
            10^{{{a}x}} &= {q} \quad \vert\ \lg() \\
            {a}x &= \lg({q}) \quad \vert :\,{a} \\
            x &= \frac{{\lg({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )

    elif t == "E":
        n = ex["n"]
        st.latex(
            rf"""
            \begin{{aligned}}
            {n}^{{({a}+x)}} - {b} &= {c} \quad \vert +\,{b} \\
            {n}^{{({a}+x)}} &= {q} \quad \vert\ \ln() \\
            ({a} + x)\cdot \ln({n}) &= \ln({q}) \quad \vert :\,\ln({n}) \\
            {a} + x &= \frac{{\ln({q})}}{{\ln({n})}} \quad \vert -{a} \\
            x &= \frac{{\ln({q})}}{{\ln({n})}} - {a}
            \approx {w:.4f}
            \end{{aligned}}
            """
        )

    elif t == "F":
        n = ex["n"]
        st.latex(
            rf"""
            \begin{{aligned}}
            {n}\cdot x^{{{a}}} - {b} &= {c} \quad \vert +\,{b} \\
            {n}\cdot x^{{{a}}} &= {q} \quad \vert :\,{n} \\
            x^{{{a}}} &= \frac{{{q}}}{{{n}}} \\
            x &= \sqrt[{a}]{{\frac{{{q}}}{{{n}}}}}
            \approx {w:.4f}
            \end{{aligned}}
            """
        )


# ============================
#   MODI für die 4 Unter-Tabs
# ============================

def _mode_mixed():
    key = "exp_example_mixed"

    if key not in st.session_state:
        st.session_state[key] = _random_mixed()

    if st.button("Neues Beispiel", key="btn_new_mixed"):
        st.session_state[key] = _random_mixed()

    ex = st.session_state[key]
    _render_example(ex, key_suffix="mixed")


def _mode_AB():
    key = "exp_example_AB"

    if key not in st.session_state:
        st.session_state[key] = _random_AB()

    if st.button("Neues Beispiel", key="btn_new_AB"):
        st.session_state[key] = _random_AB()

    ex = st.session_state[key]
    _render_example(ex, key_suffix="AB")


def _mode_CD():
    key = "exp_example_CD"

    if key not in st.session_state:
        st.session_state[key] = _random_CD()

    if st.button("Neues Beispiel", key="btn_new_CD"):
        st.session_state[key] = _random_CD()

    ex = st.session_state[key]
    _render_example(ex, key_suffix="CD")


def _mode_F():
    key = "exp_example_F"

    if key not in st.session_state:
        st.session_state[key] = _random_F()

    if st.button("Neues Beispiel", key="btn_new_F"):
        st.session_state[key] = _random_F()

    ex = st.session_state[key]
    _render_example(ex, key_suffix="F")


# ============================
#   HAUPT-FUNKTION
# ============================

def run():
    st.title("Exponentialgleichungen")

    tab_gemischt, tab_A, tab_B, tab_C = st.tabs(
        ["Gemischt", "Variante A", "Variante B", "Variante C"]
    )

    with tab_gemischt:
        _mode_mixed()

    with tab_A:
        _mode_AB()

    with tab_B:
        _mode_CD()

    with tab_C:
        _mode_F()
