import random
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# =========================
# Session Keys
# =========================
CUBIC_PROBLEM_KEY = "cubic_problem_v2"
CUBIC_SHOW_KEY    = "cubic_show_solution_v2"

VARIABLE_PROBLEM_KEY   = "variable_problem_v2"
VARIABLE_SHOW_KEY      = "variable_show_solution_v2"
STATEMENT_DATA_KEY     = "variable_statement_data_v2"
STATEMENT_STAGE_KEY    = "variable_statement_stage_v2"   # 0=noch nichts, 1=Variablen gelöst → zeige Aussage, 2=Aussage gelöst


# =========================
# Dataklassen
# =========================
@dataclass
class CriticalPoint:
    x: float
    y: float
    kind: str  # "Maximum" oder "Minimum"


# =========================
# Generator für kubisches Problem
# =========================
def generate_clear_cubic() -> dict:
    """
    Kubische f(x) mit:
      - drei reellen Nullstellen (keine bei x=0)
      - zwei Extrempunkten mit |f(x*)| >= THRESH_Y (klar abgehoben)
    """
    rng = np.random.default_rng()
    THRESH_Y = 6.0
    SCALE_CHOICES = [1, -1, 2, -2]  # ggf. 3/-3 ergänzen, falls öfter zu klein

    candidates = [x for x in range(-5, 6) if x != 0]  # keine Wurzel bei 0

    while True:
        roots = sorted(rng.choice(candidates, size=3, replace=False))
        # Abstände der Wurzeln >= 1 (kurz prüfen)
        if not (abs(roots[1] - roots[0]) >= 1 and abs(roots[2] - roots[1]) >= 1):
            continue

        scale = rng.choice(SCALE_CHOICES)
        coeffs = np.poly(roots) * scale
        poly = np.poly1d(coeffs)

        # Ableitung & Extrempunkte bestimmen
        derivative = poly.deriv()
        crit_real = [c.real for c in derivative.r if abs(c.imag) < 1e-10]
        if len(crit_real) != 2:
            continue  # wir wollen genau zwei reelle Extremstellen

        crit_real.sort()
        cps = []
        ok = True
        for x0 in crit_real:
            y0 = float(poly(x0))
            # 2. Ableitung zur Klassifikation
            curvature = float(poly.deriv(2)(x0))
            kind = "Maximum" if curvature < 0 else "Minimum"
            cps.append(CriticalPoint(x=float(x0), y=y0, kind=kind))
            # Abhebungs-Kriterium
            if abs(y0) < THRESH_Y:
                ok = False

        if not ok:
            continue

        # y-Achsenabschnitt
        intercept_y = float(poly(0.0))

        # Plotbereich rund um die Wurzeln
        x_min = min(roots) - 2.5
        x_max = max(roots) + 2.5
        x_vals = np.linspace(x_min, x_max, 600)
        y_vals = poly(x_vals)

        return {
            "poly": poly,
            "coeffs": coeffs,
            "roots": [float(r) for r in roots],
            "critical_points": cps,
            "intercept": (0.0, intercept_y),
            "x": x_vals,
            "y": y_vals,
        }


# =========================
# Variable-Beispiele
# =========================
VARIABLE_EXAMPLES = [
    {
        "text": "In einem Labor wird die Temperatur eines Chemieversuchs alle paar Minuten gemessen.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "min"},
        "dependent": {"symbol": "T", "description": "Temperatur", "unit": "°C"},
    },
    {
        "text": "Eine Läuferin zeichnet auf, wie weit sie nach jeder Viertelstunde gekommen ist.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "min"},
        "dependent": {"symbol": "s", "description": "Wegstrecke", "unit": "m"},
    },
    {
        "text": "Beim Wachstum eines Kindes wird jedes Jahr die Körpergröße festgehalten.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "Jahre"},
        "dependent": {"symbol": "h", "description": "Körpergröße", "unit": "cm"},
    },
    {
        "text": "Ein Autohersteller testet die Geschwindigkeit während einer Testfahrt.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "s"},
        "dependent": {"symbol": "v", "description": "Geschwindigkeit", "unit": "m/s"},
    },
    {
        "text": "Im Physikexperiment wird die Höhe eines fallenden Körpers gemessen.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "s"},
        "dependent": {"symbol": "h", "description": "Höhe", "unit": "m"},
    },
    {
        "text": "Der tägliche Energieverbrauch eines Haushalts wird aufgezeichnet.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "h"},
        "dependent": {"symbol": "E", "description": "Energieverbrauch", "unit": "kWh"},
    },
]

def get_new_variable_problem() -> dict:
    return random.choice(VARIABLE_EXAMPLES)


# Aussagen-Generator (Stufe 2)
def generate_statement_for(problem: dict) -> dict:
    ind = problem["independent"]
    dep = problem["dependent"]

    x = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    unit = dep["unit"]
    if unit in ("°C", "C°"):
        y = random.randint(10, 30)
    elif unit == "m":
        y = random.randint(50, 500)
    elif unit == "cm":
        y = random.randint(50, 150)
    elif unit == "kWh":
        y = random.randint(1, 20)
    elif unit == "m/s":
        y = random.randint(1, 15)
    else:
        y = random.randint(1, 50)

    ind_unit = ind["unit"]
    if ind_unit in ("h", "Stunden", "Std.", "hour"):
        time_phrase = f"nach {x} Stunden"
    elif ind_unit in ("min", "Minuten"):
        time_phrase = f"nach {x} Minuten"
    elif ind_unit in ("s", "Sekunden"):
        time_phrase = f"nach {x} Sekunden"
    elif ind_unit in ("Jahre", "Jahr"):
        time_phrase = f"nach {x} Jahren"
    else:
        time_phrase = f"bei {ind['description']} = {x} {ind['unit']}"

    statement_text = f"{time_phrase} beträgt die {dep['description']} {y} {dep['unit']}."
    math_expr = f"{dep['symbol']}({x}) = {y}"
    return {"x": x, "y": y, "text": statement_text, "expr": math_expr}


# =========================
# Session-Init
# =========================
if CUBIC_PROBLEM_KEY not in st.session_state:
    st.session_state[CUBIC_PROBLEM_KEY] = generate_clear_cubic()
    st.session_state[CUBIC_SHOW_KEY] = False

if VARIABLE_PROBLEM_KEY not in st.session_state:
    st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
    st.session_state[VARIABLE_SHOW_KEY] = False

if STATEMENT_STAGE_KEY not in st.session_state:
    st.session_state[STATEMENT_STAGE_KEY] = 0
if STATEMENT_DATA_KEY not in st.session_state:
    st.session_state[STATEMENT_DATA_KEY] = None


# =========================
# UI
# =========================
st.set_page_config(page_title="Funktionen allgemein", page_icon="🧮")

st.title("Funktionen allgemein")

st.markdown(
    """
    Es wird angenommen, dass die gezeigte Funktion an beiden Enden ins **Unendliche** verläuft.
    Das bedeutet:
    """
)
st.latex(r"D = \mathbb{R}")
st.latex(r"W = \mathbb{R}")

st.markdown(
    """
    Beim Ermitteln der Variablen ist das **Symbol frei wählbar** – du kannst selbst entscheiden,
    wie du die Variablen abkürzt. Die **Bedeutung** ist durch den Text vorgegeben.

    Die **Einheit** hat mehrere Möglichkeiten (z. B. kann **Zeit** in Stunden, Minuten oder Jahren
    angegeben werden; **Weg** in Metern, Kilometern, …).  
    In der Lösung wird die **am besten passende Einheit** angezeigt.
    """
)

tab1, tab2 = st.tabs([
    "Besondere Punkte einer Funktion",
    "Abhängige und unabhängige Variablen",
])

# ---------- TAB 1: Besondere Punkte ----------
with tab1:
    problem = st.session_state[CUBIC_PROBLEM_KEY]
    show = st.session_state[CUBIC_SHOW_KEY]

    st.subheader("Aufgabenstellung")
    st.markdown(
        """
Zeichne den Graphen und bestimme **besondere Punkte**:
- **N**: Nullstellen  
- **Max** / **Min**: Extrempunkte  
- **d**: y-Achsenabschnitt  
        """
    )

    # Plot
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(problem["x"], problem["y"], linewidth=2.0)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Besondere Punkte einer Funktion")

    if show:
        # Nullstellen: Marker + Label "N"
        for r in problem["roots"]:
            ax.scatter(r, 0, s=110, facecolors="white", edgecolors="#ff7f0e", linewidths=2)
            ax.annotate("N", xy=(r, 0), xytext=(0, 10), textcoords="offset points",
                        ha="center", color="#ff7f0e", fontsize=12, fontweight="bold")

        # y-Achsenabschnitt: Label "d"
        x0, y0 = problem["intercept"]
        ax.scatter(x0, y0, s=110, facecolors="white", edgecolors="#2ca02c", linewidths=2)
        ax.annotate("d", xy=(x0, y0), xytext=(10, 10), textcoords="offset points",
                    color="#2ca02c", fontsize=12, fontweight="bold")

        # Extrempunkte: "Max"/"Min"
        for cp in problem["critical_points"]:
            color = "#d62728" if cp.kind == "Maximum" else "#9467bd"
            ax.scatter(cp.x, cp.y, s=130, facecolors="white", edgecolors=color, linewidths=2)
            ax.annotate("Max" if cp.kind == "Maximum" else "Min",
                        xy=(cp.x, cp.y), xytext=(6, 12), textcoords="offset points",
                        color=color, fontsize=12, fontweight="bold")

    st.pyplot(fig)

    c1, c2 = st.columns(2)
    if c1.button("Lösung"):
        st.session_state[CUBIC_SHOW_KEY] = True
        st.rerun()
    if c2.button("Neue Funktion"):
        st.session_state[CUBIC_PROBLEM_KEY] = generate_clear_cubic()
        st.session_state[CUBIC_SHOW_KEY] = False
        st.rerun()


# ---------- TAB 2: Variablen + Aussage ----------
with tab2:
    variable_problem = st.session_state[VARIABLE_PROBLEM_KEY]
    show_vars = st.session_state[VARIABLE_SHOW_KEY]
    stage = st.session_state[STATEMENT_STAGE_KEY]
    stmt = st.session_state[STATEMENT_DATA_KEY]

    st.subheader("Variablen erkennen")
    st.write(variable_problem["text"])
    st.markdown(
        """
**Aufgabe 1:** Bestimme **unabhängige** und **abhängige** Variable.  
Notiere **Symbol**, **Bedeutung** und **Einheit**.
        """
    )

    if st.button("Lösung (Variablen)"):
        st.session_state[VARIABLE_SHOW_KEY] = True
        st.session_state[STATEMENT_STAGE_KEY] = 1
        st.session_state[STATEMENT_DATA_KEY] = generate_statement_for(variable_problem)
        st.rerun()

    if show_vars:
        ind = variable_problem["independent"]
        dep = variable_problem["dependent"]
        # Format mit "…"
        st.success(f"Unabhängige Variable: {ind['symbol']} … {ind['description']} ({ind['unit']})")
        st.success(f"Abhängige Variable: {dep['symbol']} … {dep['description']} ({dep['unit']})")

    # Stufe 2: Aussage → Mathe-Ausdruck
    if stage >= 1 and st.session_state[STATEMENT_DATA_KEY] is not None:
        s = st.session_state[STATEMENT_DATA_KEY]
        st.markdown("---")
        st.subheader("Mathematische Aussage formulieren")

        ind = variable_problem["independent"]
        dep = variable_problem["dependent"]
        st.markdown(
            f"**Formel/Notation:** {dep['symbol']}({ind['symbol']}) – "
            f"{dep['description']} in Abhängigkeit von {ind['description']}."
        )
        st.write(f"**Aussage:** {s['text']}")

        if st.button("Lösung (Aussage → Ausdruck)"):
            st.session_state[STATEMENT_STAGE_KEY] = 2
            st.rerun()

        if st.session_state[STATEMENT_STAGE_KEY] >= 2:
            st.success(s["expr"])  # z. B. T(3) = 20

        if st.button("Neues Beispiel"):
            st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
            st.session_state[VARIABLE_SHOW_KEY] = False
            st.session_state[STATEMENT_STAGE_KEY] = 0
            st.session_state[STATEMENT_DATA_KEY] = None
            st.rerun()
