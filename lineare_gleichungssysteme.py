# lineare_gleichungssysteme.py
import streamlit as st
import random
from fractions import Fraction


# ==========================================================
#   HELPERS
# ==========================================================

def _fmt_frac(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return rf"\frac{{{x.numerator}}}{{{x.denominator}}}"

def _fmt_money_2(x) -> str:
    if isinstance(x, Fraction):
        val = float(x.numerator / x.denominator)
    else:
        val = float(x)
    return f"{val:.2f}".replace(".", ",")

def _fmt_int(x) -> str:
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return str(int(round(float(x))))
    return str(int(x))

def _solve_2x2(a, b, c, d, e, f):
    det = a*e - b*d
    if det == 0:
        return None
    x = Fraction(c*e - b*f, det)
    y = Fraction(a*f - c*d, det)
    return x, y

def _rand_nonzero(lo, hi, exclude=None):
    exclude = exclude or set()
    while True:
        v = random.randint(lo, hi)
        if v != 0 and v not in exclude:
            return v

def _pick_name_gender():
    male = ["Ben", "David", "Lukas", "Jonas", "Felix", "Max"]
    female = ["Anna", "Clara", "Eva", "Mia", "Sophie", "Lea"]
    return (random.choice(male), "m") if random.random() < 0.5 else (random.choice(female), "w")

def _pronouns(g):
    return ("Er", "er") if g == "m" else ("Sie", "sie")

def _latex_eq_axby(a, b, c):
    def part(coeff, var):
        if coeff == 1:
            return var
        if coeff == -1:
            return "-" + var
        return f"{coeff}{var}"
    left = f"{part(a,'x')} + {part(b,'y')}" if b > 0 else f"{part(a,'x')} - {part(abs(b),'y')}"
    return rf"{left} = {c}"

def _latex_line_from_axby(a, b, c):
    # ax+by=c  -> y=mx+n or x=const
    if b != 0:
        m = Fraction(-a, b)
        n = Fraction(c, b)
        if n >= 0:
            return rf"y = {_fmt_frac(m)}x + {_fmt_frac(n)}"
        return rf"y = {_fmt_frac(m)}x - {_fmt_frac(-n)}"
    x0 = Fraction(c, a)
    return rf"x = {_fmt_frac(x0)}"


# ==========================================================
#   TAB 1 – EINDEUTIG LÖSBAR (3 FORMEN)
# ==========================================================

def _gen_unique_formA():
    x0 = random.randint(-6, 6)
    y0 = random.randint(-6, 6)
    if x0 == 0 and y0 == 0:
        x0 = 2

    a = _rand_nonzero(-7, 7)
    b = _rand_nonzero(-7, 7)
    d = _rand_nonzero(-7, 7, exclude={a})
    e = _rand_nonzero(-7, 7, exclude={b})

    while a*e - b*d == 0:
        d = _rand_nonzero(-7, 7, exclude={a})
        e = _rand_nonzero(-7, 7, exclude={b})

    c = a*x0 + b*y0
    f = d*x0 + e*y0
    return ("A", a, b, c, d, e, f)

def _gen_unique_formB():
    a = _rand_nonzero(-5, 5)
    c = _rand_nonzero(-5, 5, exclude={a})

    x0 = random.randint(-6, 6)
    y0 = random.randint(-6, 6)
    if x0 == 0 and y0 == 0:
        y0 = 3

    b = y0 - a*x0
    d0 = y0 - c*x0
    return ("B", a, b, c, d0)

def _gen_unique_formC():
    x0 = random.randint(-6, 6)
    y0 = random.randint(-6, 6)
    if x0 == 0 and y0 == 0:
        x0 = 4

    a = _rand_nonzero(-7, 7)
    b = _rand_nonzero(-7, 7)

    e0 = random.choice([-3, -2, -1, 0, 1, 2, 3])
    d0 = x0 - e0*y0
    c = a*x0 + b*y0

    if a*e0 + b == 0:
        choices = [-3, -2, -1, 1, 2, 3]
        random.shuffle(choices)
        for ee in choices:
            if a*ee + b != 0:
                e0 = ee
                d0 = x0 - e0*y0
                break

    return ("C", a, b, c, d0, e0)

def _tab1_unique():
    key = "lgs_tab1"
    if st.button("Neues Beispiel", key="lgs_tab1_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        form = random.choice(["A", "B", "C"])
        st.session_state[key] = {"A": _gen_unique_formA, "B": _gen_unique_formB, "C": _gen_unique_formC}[form]()

    data = st.session_state[key]

    st.subheader("Eindeutig lösbares LGS")
    st.markdown("**Aufgabe:** Ermittle $x$ und $y$.")

    if data[0] == "A":
        _, a, b, c, d, e, f = data
        st.latex(rf"\text{{I: }} {_latex_eq_axby(a,b,c)}")
        st.latex(rf"\text{{II: }} {_latex_eq_axby(d,e,f)}")
        if st.button("Lösung anzeigen", key="lgs_tab1_sol"):
            x, y = _solve_2x2(a, b, c, d, e, f)
            st.latex(rf"x = {_fmt_frac(x)}, \quad y = {_fmt_frac(y)}")

    elif data[0] == "B":
        _, a, b, c, d0 = data
        st.latex(rf"\text{{I: }} y = {a}x + {b}")
        st.latex(rf"\text{{II: }} y = {c}x + {d0}")
        if st.button("Lösung anzeigen", key="lgs_tab1_sol"):
            x = Fraction(d0 - b, a - c)
            y = Fraction(a, 1)*x + Fraction(b, 1)
            st.latex(rf"x = {_fmt_frac(x)}, \quad y = {_fmt_frac(y)}")

    else:
        _, a, b, c, d0, e0 = data
        st.latex(rf"\text{{I: }} {_latex_eq_axby(a,b,c)}")
        st.latex(rf"\text{{II: }} x = {d0} + {e0}y")
        if st.button("Lösung anzeigen", key="lgs_tab1_sol"):
            y = Fraction(c - a*d0, a*e0 + b)
            x = Fraction(d0, 1) + Fraction(e0, 1)*y
            st.latex(rf"x = {_fmt_frac(x)}, \quad y = {_fmt_frac(y)}")


# ==========================================================
#   TAB 2 – TEXTBEISPIELE (PREISE / KÖPFE-BEINE)
# ==========================================================

def _gen_text_prices():
    name, g = _pick_name_gender()
    _, subj = _pronouns(g)

    locals_ = [
        ("Café", ["Kaffee", "Kuchen"], (2.5, 6.5)),
        ("Pizzeria", ["Pizza", "Getränk"], (2.5, 14.0)),
        ("Burgerladen", ["Burger", "Pommes"], (2.5, 13.5)),
        ("Kebapstand", ["Döner", "Getränk"], (2.0, 10.0)),
        ("Bäckerei", ["Semmel", "Croissant"], (0.8, 3.5)),
    ]
    place, (A, B), (pmin, pmax) = random.choice(locals_)

    def pick_price():
        steps = int((pmax - pmin) / 0.5)
        return round(pmin + 0.5*random.randint(0, steps), 2)

    pA = pick_price()
    pB = pick_price()
    while abs(pA - pB) < 1e-9:
        pB = pick_price()

    a = random.randint(1, 4)
    b = random.randint(1, 4)
    d = random.randint(1, 4)
    e = random.randint(1, 4)
    while a*e - b*d == 0:
        d = random.randint(1, 4)
        e = random.randint(1, 4)

    c = round(a*pA + b*pB, 2)
    f = round(d*pA + e*pB, 2)

    return {
        "type": "prices",
        "name": name, "g": g, "place": place, "A": A, "B": B,
        "a": a, "b": b, "c": c,
        "d": d, "e": e, "f": f
    }

def _gen_text_animals():
    animals4 = ["Kühe", "Schafe", "Pferde", "Lamas", "Ziegen"]
    animals2 = ["Hühner", "Gänse", "Truthähne", "Pfaue"]

    A4 = random.choice(animals4)
    A2 = random.choice(animals2)

    x = random.randint(3, 20)
    y = random.randint(3, 30)

    heads = x + y
    legs = 4*x + 2*y

    return {"type": "animals", "A4": A4, "A2": A2, "heads": heads, "legs": legs, "x": x, "y": y}

def _tab2_text():
    key = "lgs_tab2"
    if st.button("Neues Beispiel", key="lgs_tab2_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        st.session_state[key] = random.choice([_gen_text_prices(), _gen_text_animals()])

    data = st.session_state[key]
    st.subheader("Textaufgaben")

    if data["type"] == "prices":
        name, g = data["name"], data["g"]
        _, subj = _pronouns(g)
        place, A, B = data["place"], data["A"], data["B"]
        a, b, c = data["a"], data["b"], data["c"]
        d, e, f = data["d"], data["e"], data["f"]

        st.markdown(
            f"{name} geht in ein*e {place} und kauft {a}× **{A}** und {b}× **{B}** und bezahlt **{_fmt_money_2(c)} €**.  \n"
            f"Am nächsten Tag geht {subj} wieder hin und kauft {d}× **{A}** und {e}× **{B}** und bezahlt **{_fmt_money_2(f)} €**.  \n\n"
            f"**Aufgabe:** Ermittle den Preis des jeweiligen Produkts."
        )

        if st.button("Lösung anzeigen", key="lgs_tab2_sol"):
            st.markdown("**a) LGS aufstellen**")
            st.latex(rf"\text{{I: }} {a}x + {b}y = {_fmt_money_2(c)}")
            st.latex(rf"\text{{II: }} {d}x + {e}y = {_fmt_money_2(f)}")

            st.markdown("**b) LGS lösen**")
            c_cent = int(round(c*100))
            f_cent = int(round(f*100))
            x_cent, y_cent = _solve_2x2(a, b, c_cent, d, e, f_cent)
            st.latex(rf"x = {_fmt_frac(x_cent)}\text{{ Cent}}, \quad y = {_fmt_frac(y_cent)}\text{{ Cent}}")

            st.markdown("**c) Lösung interpretieren**")
            x_eur = float(x_cent) / 100.0
            y_eur = float(y_cent) / 100.0
            st.success(f"Ein {A} kostet {x_eur:.2f} € und ein {B} kostet {y_eur:.2f} €.".replace(".", ","))

    else:
        A4, A2 = data["A4"], data["A2"]
        heads, legs = data["heads"], data["legs"]

        st.markdown(
            f"Auf einer Wiese stehen **{A4}** und **{A2}**. Zusammen haben sie **{heads} Köpfe** und **{legs} Beine**.  \n\n"
            f"**Aufgabe:** Ermittle die Anzahl der jeweiligen Tiere."
        )

        if st.button("Lösung anzeigen", key="lgs_tab2_sol"):
            st.markdown("**a) LGS aufstellen**")
            st.latex(rf"\text{{I: }} x + y = {heads}")
            st.latex(rf"\text{{II: }} 4x + 2y = {legs}")

            st.markdown("**b) LGS lösen**")
            x = Fraction(legs - 2*heads, 2)
            y = Fraction(heads, 1) - x
            st.latex(rf"x = {_fmt_frac(x)}, \quad y = {_fmt_frac(y)}")

            st.markdown("**c) Lösung interpretieren**")
            st.success(f"Es gibt {_fmt_int(x)} {A4} und {_fmt_int(y)} {A2}.")


# ==========================================================
#   TAB 3 – LÖSUNGSMENGE + GRAFIK-KONTEXT
# ==========================================================

def _gen_solution_type_formA_complex():
    # returns ("A3", soltype, a,b,c,d,e,f)
    soltype = random.choice(["one", "none", "inf"])

    a = _rand_nonzero(-6, 6)
    b = _rand_nonzero(-6, 6)

    if soltype == "one":
        d = _rand_nonzero(-6, 6)
        e = _rand_nonzero(-6, 6)
        while a*e - b*d == 0:
            d = _rand_nonzero(-6, 6)
            e = _rand_nonzero(-6, 6)
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        c = a*x0 + b*y0
        f = d*x0 + e*y0
        return ("A3", soltype, a, b, c, d, e, f)

    # complex: II is a multiple of I (and for "none" constant differs)
    k = random.choice([2, 3, -2, -3, 4, -4])
    x0 = random.randint(-5, 5)
    y0 = random.randint(-5, 5)
    c = a*x0 + b*y0

    d, e = k*a, k*b
    f = k*c if soltype == "inf" else k*c + random.choice([1, -1, 2, -2, 3, -3])

    return ("A3", soltype, a, b, c, d, e, f)

def _gen_solution_type_formB():
    # returns ("B3", a,b,c,d0)
    soltype = random.choice(["one", "none", "inf"])

    if soltype == "one":
        a = _rand_nonzero(-5, 5)
        c = _rand_nonzero(-5, 5, exclude={a})
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        b = y0 - a*x0
        d0 = y0 - c*x0
        return ("B3", a, b, c, d0)

    a = _rand_nonzero(-5, 5)
    b = random.randint(-6, 6)

    if soltype == "inf":
        c, d0 = a, b
    else:
        c, d0 = a, b + random.choice([1, -1, 2, -2, 3])

    return ("B3", a, b, c, d0)

def _gen_solution_type_formC():
    # returns ("C3", a,b,c,d0,e0) or ("C3P", a,b,c1,d0,e0) for parallel/same construction
    soltype = random.choice(["one", "none", "inf"])

    a = _rand_nonzero(-6, 6)
    b = _rand_nonzero(-6, 6)

    if soltype == "one":
        e0 = random.choice([-3, -2, -1, 0, 1, 2, 3])
        while a*e0 + b == 0:
            e0 = random.choice([-3, -2, -1, 1, 2, 3])

        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        c = a*x0 + b*y0
        d0 = x0 - e0*y0
        return ("C3", a, b, c, d0, e0)

    # build II: x - e y = d0 ; I is multiple of that (complex)
    e0 = random.choice([-3, -2, -1, 1, 2, 3])
    d0 = random.randint(-6, 6)
    k = random.choice([2, 3, -2, -3, 4, -4])

    a1, b1, c1 = k*1, k*(-e0), k*d0
    if soltype == "inf":
        return ("C3P", a1, b1, c1, d0, e0)
    return ("C3P", a1, b1, c1 + random.choice([1, -1, 2, -2, 3]), d0, e0)

def _tab3_solution_set():
    key = "lgs_tab3"
    if st.button("Neues Beispiel", key="lgs_tab3_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        form = random.choice(["A", "B", "C"])
        if form == "A":
            st.session_state[key] = _gen_solution_type_formA_complex()
        elif form == "B":
            st.session_state[key] = _gen_solution_type_formB()
        else:
            st.session_state[key] = _gen_solution_type_formC()

    data = st.session_state[key]
    st.subheader("Lösungsmenge + grafischer Kontext")
    st.markdown("**Aufgabe:** Ermittle die Lösungsmenge. Gib auch die Bedeutung im grafischen Kontext an.")

    kind = data[0]

    if kind == "A3":
        _, _, a, b, c, d, e, f = data
        st.latex(rf"\text{{I: }} {_latex_eq_axby(a,b,c)}")
        st.latex(rf"\text{{II: }} {_latex_eq_axby(d,e,f)}")

        if st.button("Lösung anzeigen", key="lgs_tab3_sol"):
            det = a*e - b*d
            if det != 0:
                x, y = _solve_2x2(a, b, c, d, e, f)
                st.latex(rf"L = \left\{{\left({_fmt_frac(x)}/{_fmt_frac(y)}\right)\right\}}")
                st.success("Grafisch: zwei Geraden schneiden sich in genau **einem** Punkt.")
            else:
                inf = (a*f - c*d == 0) and (b*f - c*e == 0)
                if inf:
                    line = _latex_line_from_axby(a, b, c)
                    st.latex(rf"L = \left\{{(x/y)\in\mathbb{{R}}^2 \mid {line}\right\}}")
                    st.success("Grafisch: **dieselbe** Gerade → unendlich viele Lösungen.")
                else:
                    st.latex(r"L = \{\}")
                    st.success("Grafisch: **parallele** Geraden → keine Lösung.")

    elif kind == "B3":
        _, a, b, c, d0 = data
        st.latex(rf"\text{{I: }} y = {a}x + {b}")
        st.latex(rf"\text{{II: }} y = {c}x + {d0}")

        if st.button("Lösung anzeigen", key="lgs_tab3_sol"):
            if a != c:
                x = Fraction(d0 - b, a - c)
                y = Fraction(a, 1)*x + Fraction(b, 1)
                st.latex(rf"L = \left\{{\left({_fmt_frac(x)}/{_fmt_frac(y)}\right)\right\}}")
                st.success("Grafisch: Geraden mit **verschiedenen Steigungen** → Schnittpunkt.")
            else:
                if b == d0:
                    st.latex(rf"L = \left\{{(x/y)\in\mathbb{{R}}^2 \mid y = {a}x + {b}\right\}}")
                    st.success("Grafisch: **dieselbe** Gerade → unendlich viele Lösungen.")
                else:
                    st.latex(r"L = \{\}")
                    st.success("Grafisch: **parallele** Geraden → keine Lösung.")

    elif kind == "C3":
        _, a, b, c, d0, e0 = data
        st.latex(rf"\text{{I: }} {_latex_eq_axby(a,b,c)}")
        st.latex(rf"\text{{II: }} x = {d0} + {e0}y")

        if st.button("Lösung anzeigen", key="lgs_tab3_sol"):
            denom = a*e0 + b
            if denom != 0:
                y = Fraction(c - a*d0, denom)
                x = Fraction(d0, 1) + Fraction(e0, 1)*y
                st.latex(rf"L = \left\{{\left({_fmt_frac(x)}/{_fmt_frac(y)}\right)\right\}}")
                st.success("Grafisch: zwei Geraden schneiden sich in genau **einem** Punkt.")
            else:
                if c == a*d0:
                    line = _latex_line_from_axby(a, b, c)
                    st.latex(rf"L = \left\{{(x/y)\in\mathbb{{R}}^2 \mid {line}\right\}}")
                    st.success("Grafisch: **dieselbe** Gerade → unendlich viele Lösungen.")
                else:
                    st.latex(r"L = \{\}")
                    st.success("Grafisch: **parallele** Geraden → keine Lösung.")

    else:  # "C3P"
        _, a, b, c1, d0, e0 = data
        st.latex(rf"\text{{I: }} {_latex_eq_axby(a,b,c1)}")
        st.latex(rf"\text{{II: }} x - ({e0})y = {d0}")

        if st.button("Lösung anzeigen", key="lgs_tab3_sol"):
            # both are parallel/same by construction
            same_dir = (a * (-e0) == b)
            if same_dir and (a*d0 == c1):
                line = _latex_line_from_axby(a, b, c1)
                st.latex(rf"L = \left\{{(x/y)\in\mathbb{{R}}^2 \mid {line}\right\}}")
                st.success("Grafisch: **dieselbe** Gerade → unendlich viele Lösungen.")
            else:
                st.latex(r"L = \{\}")
                st.success("Grafisch: **parallele** Geraden → keine Lösung.")


# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Lineare Gleichungssysteme")

    # optional: reset button (hilft bei Session-Altlasten)
    with st.sidebar:
        if st.button("Reset (LGS)"):
            st.session_state.pop("lgs_tab1", None)
            st.session_state.pop("lgs_tab2", None)
            st.session_state.pop("lgs_tab3", None)
            st.rerun()

    tab1, tab2, tab3 = st.tabs([
        "Eindeutig lösbar",
        "Textaufgaben",
        "Lösungsmenge + Grafik",
    ])

    with tab1:
        _tab1_unique()

    with tab2:
        _tab2_text()

    with tab3:
        _tab3_solution_set()
