import streamlit as st
import random
import math


# ============================
#   EXAMPLE-GENERATOREN
# ============================

def _make_example_A():
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = math.log(q) / a
    return {"type": "A", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_B():
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = c
    w = math.log(q) / a
    return {"type": "B", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_C():
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = math.log10(q) / a
    return {"type": "C", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_D():
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = c
    w = math.log10(q) / a
    return {"type": "D", "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_E():
    n = random.randint(2, 10)
    a = random.randint(11, 100) / 10
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = math.log(q) / math.log(n) - a
    return {"type": "E", "n": n, "a": a, "b": b, "c": c, "q": q, "w": w}


def _make_example_F():
    n = random.randint(2, 10)
    a = random.randint(1, 5)
    b = random.randint(10, 200) / 10
    c = random.randint(10, 300) / 10
    q = b + c
    w = (q / n) ** (1 / a)
    return {"type": "F", "n": n, "a": a, "b": b, "c": c, "q": q, "w": w}


# ============================
#   ZUFALLS-LOGIK
# ============================

def _random_mixed():
    r = random.randint(1, 115)
    if r <= 30:
        return _make_example_A()
    if r <= 60:
        return _make_example_B()
    if r <= 75:
        return _make_example_C()
    if r <= 90:
        return _make_example_D()
    if r <= 100:
        return _make_example_E()
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

    st.markdown(
        """
        **Aufgabe**  
        Ermittle den Wert von $x$ und dokumentiere deine Umformungsschritte.  
        *(Tipp: Überprüfe dein Ergebnis auch mit GeoGebra.)*
        """
    )

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

    st.write("")
    st.markdown("**Lösung**")

    if not st.button("Lösung anzeigen", key=f"btn_solution_{key_suffix}"):
        return

    if t == "A":
        st.latex(
            rf"""
            \begin{{aligned}}
            e^{{{a}x}} - {b} &= {c} \ \vert +\,{b} \\
            e^{{{a}x}} &= {q} \ \vert\ \ln() \\
            {a}x &= \ln({q}) \ \vert :\,{a} \\
            x &= \frac{{\ln({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )
    elif t == "B":
        right = round(c + b, 1)
        st.latex(
            rf"""
            \begin{{aligned}}
            e^{{{a}x}} + {b} &= {right} \ \vert -\,{b} \\
            e^{{{a}x}} &= {q} \ \vert\ \ln() \\
            {a}x &= \ln({q}) \ \vert :\,{a} \\
            x &= \frac{{\ln({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )
    elif t == "C":
        st.latex(
            rf"""
            \begin{{aligned}}
            10^{{{a}x}} - {b} &= {c} \ \vert +\,{b} \\
            10^{{{a}x}} &= {q} \ \vert\ \lg() \\
            {a}x &= \lg({q}) \ \vert :\,{a} \\
            x &= \frac{{\lg({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )
    elif t == "D":
        right = round(c + b, 1)
        st.latex(
            rf"""
            \begin{{aligned}}
            10^{{{a}x}} + {b} &= {right} \ \vert -\,{b} \\
            10^{{{a}x}} &= {q} \ \vert\ \lg() \\
            {a}x &= \lg({q}) \ \vert :\,{a} \\
            x &= \frac{{\lg({q})}}{{{a}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )
    elif t == "E":
        n = ex["n"]
        st.latex(
            rf"""
            \begin{{aligned}}
            {n}^{{({a}+x)}} - {b} &= {c} \ \vert +\,{b} \\
            {n}^{{({a}+x)}} &= {q} \ \vert\ \ln() \\
            ({a} + x)\ln({n}) &= \ln({q}) \ \vert :\,\ln({n}) \\
            {a} + x &= \frac{{\ln({q})}}{{\ln({n})}} \ \vert -{a} \\
            x &= \frac{{\ln({q})}}{{\ln({n})}} - {a} \approx {w:.4f}
            \end{{aligned}}
            """
        )
    elif t == "F":
        n = ex["n"]
        st.latex(
            rf"""
            \begin{{aligned}}
            {n}\cdot x^{{{a}}} - {b} &= {c} \ \vert +\,{b} \\
            {n}\cdot x^{{{a}}} &= {q} \ \vert :\,{n} \\
            x^{{{a}}} &= \frac{{{q}}}{{{n}}} \\
            x &= \sqrt[{a}]{{\frac{{{q}}}{{{n}}}}} \approx {w:.4f}
            \end{{aligned}}
            """
        )


# ============================
#   MODI (Tabs)
# ============================

def _mode_mixed():
    key = "exp_example_mixed"
    if st.button("Neues Beispiel", key="btn_new_mixed"):
        st.session_state[key] = _random_mixed()
    if key not in st.session_state:
        st.session_state[key] = _random_mixed()
    _render_example(st.session_state[key], key_suffix="mixed")


def _mode_AB():
    key = "exp_example_AB"
    if st.button("Neues Beispiel", key="btn_new_AB"):
        st.session_state[key] = _random_AB()
    if key not in st.session_state:
        st.session_state[key] = _random_AB()
    _render_example(st.session_state[key], key_suffix="AB")


def _mode_CD():
    key = "exp_example_CD"
    if st.button("Neues Beispiel", key="btn_new_CD"):
        st.session_state[key] = _random_CD()
    if key not in st.session_state:
        st.session_state[key] = _random_CD()
    _render_example(st.session_state[key], key_suffix="CD")


def _mode_F():
    key = "exp_example_F"
    if st.button("Neues Beispiel", key="btn_new_F"):
        st.session_state[key] = _random_F()
    if key not in st.session_state:
        st.session_state[key] = _random_F()
    _render_example(st.session_state[key], key_suffix="F")


# ============================
#   RUN
# ============================

def run():
    st.title("Exponentialgleichungen")

    tab1, tab2, tab3, tab4 = st.tabs(["Gemischt", "Variante A", "Variante B", "Variante C"])

    with tab1:
        _mode_mixed()
    with tab2:
        _mode_AB()
    with tab3:
        _mode_CD()
    with tab4:
        _mode_F()
