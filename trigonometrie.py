# trigonometrie.py
import streamlit as st
import random
import math

# ==========================================================
#   HELPERS
# ==========================================================

def fmt(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",")

# ==========================================================
#   GENERATOR
# ==========================================================

def gen_problem():
    # rechter Winkel bei C
    alpha = random.choice([20, 25, 30, 35, 40, 45, 50, 55, 60])
    beta = 90 - alpha

    mode = random.choice(["two_sides", "side_angle"])

    c = random.choice([8, 9, 10, 12, 15, 18])
    a = c * math.sin(math.radians(alpha))
    b = c * math.cos(math.radians(alpha))

    given = {}

    if mode == "two_sides":
        give = random.choice([("a","b"), ("a","c"), ("b","c")])
        for k in give:
            given[k] = {"a": a, "b": b, "c": c}[k]
    else:
        side = random.choice(["a","b","c"])
        ang = random.choice(["alpha","beta"])
        given[side] = {"a": a, "b": b, "c": c}[side]
        given[ang] = {"alpha": alpha, "beta": beta}[ang]

    return {
        "a": a, "b": b, "c": c,
        "alpha": alpha, "beta": beta,
        "given": given
    }

# ==========================================================
#   TAB 1
# ==========================================================

def tab1():
    key = "trig_tab1"

    if st.button("Neues Beispiel", key="trig_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = gen_problem()

    p = st.session_state[key]
    g = p["given"]

    st.subheader("Rechtwinkliges Dreieck")

    # 👉 FIXES BILD
    st.image(
        "assets/rechtwinkliges_dreieck.png",
        use_container_width=True
    )

    tags = []
    if "a" in g: tags.append(rf"$a={fmt(g['a'])}$")
    if "b" in g: tags.append(rf"$b={fmt(g['b'])}$")
    if "c" in g: tags.append(rf"$c={fmt(g['c'])}$")
    if "alpha" in g: tags.append(rf"$\alpha={g['alpha']}^\circ$")
    if "beta" in g: tags.append(rf"$\beta={g['beta']}^\circ$")

    st.markdown("**Gegeben:** " + ", ".join(tags))
    st.markdown("**Aufgabe:** Bestimme die restlichen Seiten und Winkel des Dreiecks.")

    if st.button("Lösung anzeigen", key="trig_sol"):
        st.markdown("**Lösung:**")
        st.latex(
            rf"a \approx {fmt(p['a'])},\quad b \approx {fmt(p['b'])},\quad c = {fmt(p['c'])}"
        )
        st.latex(
            rf"\alpha = {p['alpha']}^\circ,\quad \beta = {p['beta']}^\circ,\quad \gamma = 90^\circ"
        )

# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Trigonometrie")

    (t1,) = st.tabs(["Rechtwinkliges Dreieck"])

    with t1:
        tab1()
