# matrizen.py
import streamlit as st
import random
from fractions import Fraction

# ==========================================================
#   HELPERS
# ==========================================================

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

def _dot_graph(components, inter, products, C, I, demA, demB):
    # components: 4, inter: 3, products: 2
    # C: 4x3, I: 3x2
    # demand shown per branch (3 branches): demA, demB are lists length 3
    dot = "digraph G {\nrankdir=LR;\nnode [shape=box, style=rounded];\n"
    dot += 'subgraph cluster0 { label="Bestandteile";\n'
    for n in components: dot += f'"{n}";\n'
    dot += "}\n"
    dot += 'subgraph cluster1 { label="Zwischenprodukte";\n'
    for n in inter: dot += f'"{n}";\n'
    dot += "}\n"
    dot += 'subgraph cluster2 { label="Endprodukte";\n'
    for n in products: dot += f'"{n}";\n'
    dot += "}\n"

    # edges components -> inter (labels from C)
    for i, comp in enumerate(components):
        for j, mid in enumerate(inter):
            w = C[i][j]
            if w != 0:
                dot += f'"{comp}" -> "{mid}" [label="{w}"];\n'

    # edges inter -> products (labels from I)
    for j, mid in enumerate(inter):
        for k, prod in enumerate(products):
            w = I[j][k]
            if w != 0:
                dot += f'"{mid}" -> "{prod}" [label="{w}"];\n'

    # show branch demand as note nodes
    dot += 'node [shape=note, style="filled", fillcolor="#f5f5f5"];\n'
    for idx in range(3):
        dot += f'"Filiale {idx+1}\\nSet A: {demA[idx]}\\nSet B: {demB[idx]}" -> "Set A" [style=dashed, arrowhead=none];\n'
        dot += f'"Filiale {idx+1}\\nSet A: {demA[idx]}\\nSet B: {demB[idx]}" -> "Set B" [style=dashed, arrowhead=none];\n'

    dot += "}\n"
    return dot


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
    st.latex(rf"A = {_latex_matrix(A)} \quad,\quad B = {_latex_matrix(B)}")
    st.latex(r"A + B = \ ?")

    if st.button("Lösung anzeigen", key="mat_add_sol"):
        st.latex(rf"A+B = {_latex_matrix(_add(A,B))}")


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

        # 50%: möglich, 50%: nicht möglich
        if random.random() < 0.5:
            B = _mat(k, c, -4, 6)  # möglich
            possible = True
        else:
            k_wrong = random.choice([x for x in [1,2,3] if x != k])
            B = _mat(k_wrong, c, -4, 6)  # nicht möglich
            possible = False

        st.session_state[key] = (A, B, possible)

    A, B, possible = st.session_state[key]

    st.subheader("Matrix-Multiplikation I")
    st.markdown("**Aufgabe:** Falls möglich, ermittle das Ergebnis der Multiplikation.")
    st.markdown(f"Dimensionen:  $A\\in\\mathbb{{R}}^{{{_dims_str(A)}}}$  und  $B\\in\\mathbb{{R}}^{{{_dims_str(B)}}}$")
    st.latex(rf"A = {_latex_matrix(A)}")
    st.latex(rf"B = {_latex_matrix(B)}")
    st.latex(r"A\cdot B = \ ?")

    if st.button("Lösung anzeigen", key="mat_mul_sol"):
        if len(A[0]) != len(B):
            st.latex(r"A\cdot B \ \text{ist nicht definiert (Spaltenzahl von A ≠ Zeilenzahl von B).}")
        else:
            st.latex(rf"A\cdot B = {_latex_matrix(_mul(A,B))}")


# ==========================================================
#   TAB 3 – MATRIX-MULTIPLIKATION II (fehlendes Element)
# ==========================================================

def _tab_missing():
    key = "mat_missing"
    if st.button("Neues Beispiel", key="mat_missing_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        # keep it small and solvable: (2x2)*(2x2) or (2x3)*(3x2)
        choice = random.choice([(2,2,2), (2,3,2)])  # (r,k,c)
        r, k, c = choice

        A = _mat(r, k, -4, 6)
        B = _mat(k, c, -4, 6)

        # pick unknown in A at (i,j) such that corresponding coefficient in equation != 0
        i = random.randrange(r)
        j = random.randrange(k)
        # choose which product entry to use: (i, col) with col random
        col = random.randrange(c)
        # coefficient is B[j][col]
        tries = 0
        while B[j][col] == 0 and tries < 30:
            j = random.randrange(k)
            col = random.randrange(c)
            tries += 1
        if B[j][col] == 0:
            # force a nonzero
            B[j][col] = random.choice([-3,-2,-1,1,2,3])

        x_true = random.randint(-5, 5)
        A[i][j] = x_true

        P = _mul(A, B)

        # now hide A[i][j]
        A[i][j] = "x"

        st.session_state[key] = {
            "A": A, "B": B, "P": P,
            "pos": (i, j), "use": (i, col),
            "x_true": x_true
        }

    data = st.session_state[key]
    A, B, P = data["A"], data["B"], data["P"]
    i, j = data["pos"]
    pi, pj = data["use"]
    x_true = data["x_true"]

    st.subheader("Matrix-Multiplikation II")
    st.markdown("**Aufgabe:** Ermittle das fehlende Element.")
    st.latex(rf"A = {_latex_matrix(A, unknown=(i,j,'x'))}")
    st.latex(rf"B = {_latex_matrix(B)}")
    st.latex(rf"A\cdot B = {_latex_matrix(P)}")

    if st.button("Lösung anzeigen", key="mat_missing_sol"):
        # compute x from one entry of the product: P[pi][pj]
        # P[pi][pj] = sum_t A[pi][t]*B[t][pj], where A[pi][j]=x
        # => x*B[j][pj] + rest = P[pi][pj]
        coeff = B[j][pj]
        rest = 0
        for t in range(len(B)):
            if t == j:
                continue
            rest += (A[pi][t] if isinstance(A[pi][t], int) else 0) * B[t][pj]

        # but A has "x" only at (i,j). If pi!=i then it wouldn't appear; we ensured pi=i
        # build rest from original row values in A (except x)
        # reconstruct row with ints:
        row_vals = []
        for t in range(len(A[0])):
            if t == j:
                row_vals.append(None)
            else:
                row_vals.append(A[pi][t])

        rest = sum(row_vals[t] * B[t][pj] for t in range(len(B)) if t != j)

        rhs = P[pi][pj]
        # x = (rhs - rest)/coeff
        x = Fraction(rhs - rest, coeff)

        st.latex(rf"\text{{Nutze z.B. das Element }}(i={pi+1},j={pj+1})\text{{ von }}A\cdot B.")
        st.latex(rf"{coeff}\,x + ({rest}) = {rhs}")
        st.latex(rf"x = \frac{{{rhs} - ({rest})}}{{{coeff}}} = {_fmt_frac(x)}")
        st.success(f"Kontrolle: x = {x_true}")


# ==========================================================
#   TAB 4 – GOZINTOGRAPH (Regale / Filialen)
# ==========================================================

def _tab_gozinto():
    key = "mat_gozinto"
    if st.button("Neues Beispiel", key="mat_gozinto_new"):
        st.session_state.pop(key, None)

    if key not in st.session_state:
        components = ["Seitenwände", "Bodenbretter", "Schrauben", "Dübel"]
        inter = ["Basisregal", "CD-Einsatz", "DVD-Einsatz"]
        products = ["Set A", "Set B"]

        # Komponenten -> Zwischenprodukte (4x3), kleine Stückzahlen
        C = [
            [2, 0, 0],  # Seitenwände pro Basis/ CD / DVD
            [3, 0, 0],  # Bodenbretter
            [12, 6, 6], # Schrauben
            [8, 4, 4],  # Dübel
        ]

        # Zwischenprodukte -> Endprodukte (3x2)
        # Set A = Basis + CD, Set B = Basis + DVD (oder auch beides mal anders)
        I = [
            [1, 1],  # Basisregal
            [1, 0],  # CD-Einsatz
            [0, 1],  # DVD-Einsatz
        ]

        # 3 Filialen: Nachfrage nach Sets
        demA = [random.randint(2, 8) for _ in range(3)]
        demB = [random.randint(2, 8) for _ in range(3)]

        st.session_state[key] = {
            "components": components, "inter": inter, "products": products,
            "C": C, "I": I, "demA": demA, "demB": demB
        }

    d = st.session_state[key]
    components, inter, products = d["components"], d["inter"], d["products"]
    C, I, demA, demB = d["C"], d["I"], d["demA"], d["demB"]

    st.subheader("Gozintographen")
    st.markdown("**Aufgabe:** Wieviele Bestandteile müssen im Zentrallager vorhanden sein, um alle Filialen zu beliefern?")

    dot = _dot_graph(components, inter, products, C, I, demA, demB)
    st.graphviz_chart(dot)

    if st.button("Lösung anzeigen", key="mat_gozinto_sol"):
        # total sets across all branches
        totalA = sum(demA)
        totalB = sum(demB)

        # sets vector (2x1)
        S = [[totalA], [totalB]]  # 2x1

        # compute inter totals: (3x2)*(2x1) = 3x1
        # need I as 3x2, so multiply I * S
        inter_tot = [[I[r][0]*S[0][0] + I[r][1]*S[1][0]] for r in range(3)]

        # components totals: (4x3)*(3x1) = 4x1
        comp_tot = [[C[r][0]*inter_tot[0][0] + C[r][1]*inter_tot[1][0] + C[r][2]*inter_tot[2][0]] for r in range(4)]

        st.markdown("**Zusammenfassung (gesamt über alle 3 Filialen):**")
        st.latex(rf"\text{{Set A gesamt}} = {totalA}, \quad \text{{Set B gesamt}} = {totalB}")

        st.markdown("**Matrix-Rechnung:**")
        st.latex(rf"I = {_latex_matrix(I)} \quad,\quad S = {_latex_matrix(S)}")
        st.latex(rf"Z = I\cdot S = {_latex_matrix(inter_tot)}")
        st.latex(rf"C = {_latex_matrix(C)}")
        st.latex(rf"B = C\cdot Z = {_latex_matrix(comp_tot)}")

        st.markdown("**Benötigte Bestandteile im Zentrallager:**")
        for idx, name in enumerate(components):
            st.success(f"{name}: {comp_tot[idx][0]}")


# ==========================================================
#   RUN
# ==========================================================

def run():
    st.title("Matrizen")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Matrix-Addition",
        "Matrix-Multiplikation I",
        "Matrix-Multiplikation II",
        "Gozintographen",
    ])

    with tab1:
        _tab_add()

    with tab2:
        _tab_mul()

    with tab3:
        _tab_missing()

    with tab4:
        _tab_gozinto()
