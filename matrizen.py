# matrizen.py
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

def _mat(rows, cols, lo=-6, hi=9):
    return [[random.randint(lo, hi) for _ in range(cols)] for __ in range(rows)]

def _dims_str(A):
    return f"{len(A)}×{len(A[0])}"

def _add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def _mul(A, B):
    r, k = len(A), len(A[0])
    k2, c = len(B), len(B[0])
    assert k == k2
    out = [[0 for _ in range(c)] for __ in range(r)]
    for i in range(r):
        for j in range(c):
            out[i][j] = sum(A[i][t] * B[t][j] for t in range(k))
    return out

def _latex_matrix(M, unknown=None):
    # unknown = (i,j,"x") or None
    lines = []
    for i, row in enumerate(M):
        parts = []
        for j, v in enumerate(row):
            if unknown and i == unknown[0] and j == unknown[1]:
                parts.append(unknown[2])
            else:
                parts.append(str(v))
        lines.append(" & ".join(parts))
    body = r" \\ ".join(lines)
    return rf"\begin{{bmatrix}} {body} \end{{bmatrix}}"


# ==========================================================
#   TAB 1 – MATRIX-ADDITION
# ==========================================================

def _tab_add():
    key = "mat_add"
    if st.button("Neues Beispiel", key="mat_add_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        n = random.choice([2, 3])
        A = _mat(n, n, -6, 9)
        B = _mat(n, n, -6, 9)
        st.session_state[key] = (A, B)

    A, B = st.session_state[key]

    st.subheader("Matrix-Addition")
    st.markdown("**Aufgabe:** Ermittle das Ergebnis der Addition.")
    st.latex(rf"{_latex_matrix(A)} + {_latex_matrix(B)} = \ ?")

    if st.button("Lösung anzeigen", key="mat_add_sol"):
        st.latex(rf"{_latex_matrix(_add(A,B))}")


# ==========================================================
#   TAB 2 – MATRIX-MULTIPLIKATION I
# ==========================================================

def _tab_mul():
    key = "mat_mul"
    if st.button("Neues Beispiel", key="mat_mul_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        r = random.randint(1, 3)
        k = random.randint(1, 3)
        c = random.randint(1, 3)

        A = _mat(r, k, -4, 6)

        # 50% möglich / 50% nicht möglich
        if random.random() < 0.5:
            B = _mat(k, c, -4, 6)  # möglich
        else:
            k_wrong = random.choice([x for x in [1, 2, 3] if x != k])
            B = _mat(k_wrong, c, -4, 6)  # nicht möglich

        st.session_state[key] = (A, B)

    A, B = st.session_state[key]

    st.subheader("Matrix-Multiplikation I")
    st.markdown("**Aufgabe:** Falls möglich, ermittle das Ergebnis der Multiplikation.")
    st.markdown(f"Dimensionen:  $({_dims_str(A)})\\cdot({_dims_str(B)})$")
    st.latex(rf"{_latex_matrix(A)}\cdot {_latex_matrix(B)} = \ ?")

    if st.button("Lösung anzeigen", key="mat_mul_sol"):
        if len(A[0]) != len(B):
            st.error("Nicht definiert: Spaltenzahl der linken Matrix ≠ Zeilenzahl der rechten Matrix.")
        else:
            st.latex(rf"{_latex_matrix(_mul(A,B))}")


# ==========================================================
#   TAB 3 – MATRIX-MULTIPLIKATION II (fehlendes Element)
#   Anzeige: A*B=C nur als Matrizen (keine Buchstaben)
# ==========================================================

def _tab_missing():
    key = "mat_missing"
    if st.button("Neues Beispiel", key="mat_missing_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        # small and clean: (2x2)*(2x2) or (2x3)*(3x2)
        r, k, c = random.choice([(2, 2, 2), (2, 3, 2)])

        A = _mat(r, k, -4, 6)
        B = _mat(k, c, -4, 6)

        # unknown in A at (i,j)
        i = random.randrange(r)
        j = random.randrange(k)

        # use product entry (i, col)
        col = random.randrange(c)

        # ensure coefficient B[j][col] != 0
        tries = 0
        while B[j][col] == 0 and tries < 30:
            j = random.randrange(k)
            col = random.randrange(c)
            tries += 1
        if B[j][col] == 0:
            B[j][col] = random.choice([-3, -2, -1, 1, 2, 3])

        x_true = random.randint(-5, 5)
        A[i][j] = x_true
        Cmat = _mul(A, B)

        # hide
        A[i][j] = "x"

        st.session_state[key] = {
            "A": A, "B": B, "C": Cmat,
            "pos": (i, j), "use": (i, col),
            "x_true": x_true
        }

    data = st.session_state[key]
    A, B, Cmat = data["A"], data["B"], data["C"]
    i, j = data["pos"]
    ri, cj = data["use"]
    x_true = data["x_true"]

    st.subheader("Matrix-Multiplikation II")
    st.markdown("**Aufgabe:** Ermittle das fehlende Element.")
    st.latex(rf"{_latex_matrix(A, unknown=(i,j,'x'))}\cdot {_latex_matrix(B)} = {_latex_matrix(Cmat)}")

    if st.button("Lösung anzeigen", key="mat_missing_sol"):
        coeff = B[j][cj]
        rhs = Cmat[ri][cj]

        # rest = sum_{t!=j} A[ri][t]*B[t][cj]
        rest = 0
        for t in range(len(B)):
            if t == j:
                continue
            rest += A[ri][t] * B[t][cj]

        x = Fraction(rhs - rest, coeff)

        st.latex(rf"{coeff}\,x + ({rest}) = {rhs}")
        st.latex(rf"x = \frac{{{rhs} - ({rest})}}{{{coeff}}} = {_fmt_frac(x)}")
        st.success(f"Kontrolle: x = {x_true}")


# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Matrizen")

    tab1, tab2, tab3 = st.tabs([
        "Matrix-Addition",
        "Matrix-Multiplikation I",
        "Matrix-Multiplikation II",
    ])

    with tab1:
        _tab_add()

    with tab2:
        _tab_mul()

    with tab3:
        _tab_missing()
