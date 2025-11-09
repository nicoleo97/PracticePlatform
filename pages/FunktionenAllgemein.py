import random
from dataclasses import dataclass
from typing import List, Dict, Optional

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# ---------- Keys ----------
CUBIC_PROBLEM_KEY = "cubic_problem"
CUBIC_SOLUTION_KEY = "cubic_show_solution"
VARIABLE_PROBLEM_KEY = "variable_problem"
VARIABLE_SOLUTION_KEY = "variable_show_solution"


# ---------- Modelle / Hilfen ----------
@dataclass
class CriticalPoint:
    x: float
    y: float
    kind: str  # "Maximum" oder "Minimum"


def classify_extremum(poly: np.poly1d, x_value: float) -> str:
    return "Maximum" if poly.deriv(2)(x_value) < 0 else "Minimum"


def generate_problem(kind: Optional[str] = None) -> dict:
    """
    Erzeugt entweder:
    - eine Kubik (3 reelle Nullstellen, klare Extrema, Vorzeichen ±),
    - oder eine Quadratik a(x-h)^2 + k (Vorzeichen ±, klarer Scheitel, versetzt).
    Rückgabe vereinheitlicht: roots, critical_points, intercept, x, y.
    """
    rng = np.random.default_rng()

    def cubic():
        # Drei deutlich getrennte Wurzeln
        while True:
            roots = np.sort(rng.choice(np.arange(-6, 7), size=3, replace=False))
            if np.all(np.diff(roots) >= 2):
                break
        sign = rng.choice([1, -1])            # erlaubt "flipped"
        scale = int(rng.integers(2, 5)) * sign
        coeffs = np.poly(roots) * scale
        poly = np.poly1d(coeffs)

        # Extrema
        cps: List[CriticalPoint] = []
        for z in poly.deriv().r:
            if abs(z.imag) > 1e-8:
                continue
            x = float(z.real)
            cps.append(CriticalPoint(x=x, y=float(poly(x)), kind=classify_extremum(poly, x)))
        cps.sort(key=lambda p: p.x)

        real_roots = sorted(r.real for r in poly.r if abs(r.imag) <= 1e-8)

        xmin = min(real_roots + [cp.x for cp in cps]) - 3
        xmax = max(real_roots + [cp.x for cp in cps]) + 3
        x = np.linspace(xmin, xmax, 400)
        y = poly(x)

        # Deutlich abgehoben von x-Achse
        if cps and max(abs(cp.y) for cp in cps) < 2:
            return cubic()

        return {
            "poly": poly,
            "roots": real_roots,
            "critical_points": cps,
            "intercept": (0.0, float(poly(0))),
            "x": x,
            "y": y,
        }

    def quadratic():
        # a(x-h)^2 + k mit Vorzeichen ±a, versetzt, klarer Scheitel
        sign = rng.choice([1, -1])  # erlaubt "flipped"
        a = float(sign * rng.uniform(0.8, 2.0))
        h = float(rng.integers(-3, 4))         # -3 … 3
        k = float(rng.choice([-1, 1]) * rng.uniform(3.0, 8.0))  # weit genug von x-Achse

        # Standardform ax^2 + bx + c
        b = -2 * a * h
        c = a * h * h + k
        poly = np.poly1d([a, b, c])

        # Reelle Nullstellen
        real_roots: List[float] = []
        for r in np.roots([a, b, c]):
            if abs(r.imag) <= 1e-8:
                real_roots.append(float(r.real))
        real_roots.sort()

        cp = CriticalPoint(x=h, y=k, kind=("Minimum" if a > 0 else "Maximum"))

        xs = [h] + real_roots if real_roots else [h]
        xmin = min(xs) - 6
        xmax = max(xs) + 6
        x = np.linspace(xmin, xmax, 400)
        y = poly(x)

        if abs(k) < 2:
            return quadratic()

        return {
            "poly": poly,
            "roots": real_roots,
            "critical_points": [cp],
            "intercept": (0.0, float(poly(0))),
            "x": x,
            "y": y,
        }

    if kind is None:
        kind = rng.choice(["cubic", "quadratic"], p=[0.6, 0.4])

    return cubic() if kind == "cubic" else quadratic()


VARIABLE_EXAMPLES = [
    {
        "text": "In einem Labor wird die Temperatur eines Chemieversuchs alle paar Minuten gemessen. "
                "Mit zunehmender Zeit verändert sich die Temperatur der Flüssigkeit.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "min"},
        "dependent": {"symbol": "T", "description": "Temperatur", "unit": "°C"},
    },
    {
        "text": "Eine Läuferin zeichnet auf, wie weit sie bei einem Trainingslauf kommt. "
                "Nach jeder viertel Stunde notiert sie die bereits zurückgelegte Strecke.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "min"},
        "dependent": {"symbol": "s", "description": "Wegstrecke", "unit": "m"},
    },
    {
        "text": "Beim Wachstum eines Kindes wird jedes Jahr die Körpergröße festgehalten, um den Verlauf zu beobachten.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "Jahre"},
        "dependent": {"symbol": "h", "description": "Körpergröße", "unit": "cm"},
    },
    {
        "text": "Ein Autohersteller testet, wie sich die Geschwindigkeit eines Prototyps während einer Testfahrt entwickelt.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "s"},
        "dependent": {"symbol": "v", "description": "Geschwindigkeit", "unit": "m/s"},
    },
    {
        "text": "In einem Physikexperiment wird gemessen, wie hoch ein Körper über dem Boden ist, während er fällt.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "s"},
        "dependent": {"symbol": "h", "description": "Höhe", "unit": "m"},
    },
    {
        "text": "Bei einer Studie zur Stromnutzung wird aufgezeichnet, wie viel Energie ein Haushalt im Laufe eines Tages verbraucht.",
        "independent": {"symbol": "t", "description": "Zeit", "unit": "h"},
        "dependent": {"symbol": "E", "description": "Energieverbrauch", "unit": "kWh"},
    },
]


def get_new_variable_problem() -> dict:
    return random.choice(VARIABLE_EXAMPLES)


UNIT_WORDS: Dict[str, str] = {
    "min": "Minuten",
    "s": "Sekunden",
    "h": "Stunden",
    "m": "Meter",
    "cm": "Zentimeter",
    "°C": "°C",
    "kWh": "kWh",
    "Jahre": "Jahre",
}


def unit_to_words(u: str) -> str:
    return UNIT_WORDS.get(u, u)


def format_var_line(prefix: str, var: dict) -> str:
    # „…“ Ellipse + ausgeschriebene Einheit
    return f"{prefix}: {var['symbol']} … {var['description']} ({unit_to_words(var['unit'])})"


# ---------- Session-State ----------
if CUBIC_PROBLEM_KEY not in st.session_state:
    st.session_state[CUBIC_PROBLEM_KEY] = generate_problem()
    st.session_state[CUBIC_SOLUTION_KEY] = False

if VARIABLE_PROBLEM_KEY not in st.session_state:
    st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
    st.session_state[VARIABLE_SOLUTION_KEY] = False


# ---------- UI ----------
st.title("Funktionen allgemein")
st.write(
    'Arbeite dich durch die Aufgaben in den Tabs. Klicke auf „Lösung“, um zu prüfen. '
    '„Neue Funktion/Neues Beispiel“ erzeugt sofort eine neue Aufgabe.'
)

analyse_tab, variable_tab = st.tabs([
    "Besondere Punkte einer Funktion",
    "Abhängige und unabhängige Variablen",
])


# ===== Besondere Punkte (Kubik/Quadratik) =====
with analyse_tab:
    problem = st.session_state[CUBIC_PROBLEM_KEY]
    show_solution = st.session_state[CUBIC_SOLUTION_KEY]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(problem["x"], problem["y"], label="f(x)")
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlim(problem["x"][0], problem["x"][-1])

    if show_solution:
        # Nullstellen → „N“
        for r in problem["roots"]:
            ax.scatter(r, 0, s=110, facecolors="white", edgecolors="tab:orange", linewidths=2)
            ax.annotate("N", xy=(r, 0), xytext=(0, 10), textcoords="offset points",
                        ha="center", color="tab:orange")

        # Achsenabschnitt → „d“
        ix, iy = problem["intercept"]
        ax.scatter(ix, iy, s=120, facecolors="white", edgecolors="tab:green", linewidths=2)
        ax.annotate("d", xy=(ix, iy), xytext=(10, 10), textcoords="offset points",
                    color="tab:green")

        # Extrema → „Max“ / „Min“
        for cp in problem["critical_points"]:
            col = "tab:red" if cp.kind == "Maximum" else "tab:purple"
            label = "Max" if cp.kind == "Maximum" else "Min"
            ax.scatter(cp.x, cp.y, s=140, facecolors="white", edgecolors=col, linewidths=2)
            ax.annotate(label, xy=(cp.x, cp.y), xytext=(6, 12),
                        textcoords="offset points", color=col)

    st.pyplot(fig)

    st.markdown(
        """
        **Aufgaben**
        - Bestimme die Nullstellen. Wie viele gibt es?
        - Wo befindet sich das Maximum? Wo das Minimum?
        - Wie lautet der Achsenabschnitt?
        """
    )

    cols = st.columns(2)
    if cols[0].button("Lösung zeigen", key="cubic_solution_button"):
        st.session_state[CUBIC_SOLUTION_KEY] = True
        st.rerun()

    if cols[1].button("Neue Funktion", key="cubic_new_example"):
        st.session_state[CUBIC_PROBLEM_KEY] = generate_problem()
        st.session_state[CUBIC_SOLUTION_KEY] = False
        st.rerun()


# ===== Variablen-Tab =====
with variable_tab:
    problem_v = st.session_state[VARIABLE_PROBLEM_KEY]
    show_v = st.session_state[VARIABLE_SOLUTION_KEY]

    st.subheader("Variablen erkennen")
    st.write(problem_v["text"])
    st.markdown(
        "Welche Variable ist unabhängig und welche hängt von ihr ab? "
        "Notiere Symbol, Bedeutung und Einheit."
    )

    if st.button("Lösung", key="variable_solution_button"):
        st.session_state[VARIABLE_SOLUTION_KEY] = True
        st.rerun()

    if show_v:
        indep = problem_v["independent"]
        dep = problem_v["dependent"]
        st.success(format_var_line("Unabhängige Variable", indep))
        st.success(format_var_line("Abhängige Variable", dep))

        if st.button("Neues Beispiel", key="variable_new_example"):
            st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
            st.session_state[VARIABLE_SOLUTION_KEY] = False
            st.rerun()
