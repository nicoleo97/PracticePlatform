import random
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


CUBIC_PROBLEM_KEY = "cubic_problem"
CUBIC_SOLUTION_KEY = "cubic_show_solution"
VARIABLE_PROBLEM_KEY = "variable_problem"
VARIABLE_SOLUTION_KEY = "variable_show_solution"


@dataclass
class CriticalPoint:
    x: float
    y: float
    kind: str  # "Maximum" oder "Minimum"


def classify_extremum(poly: np.poly1d, x_value: float) -> str:
    second_derivative = poly.deriv(2)
    curvature = second_derivative(x_value)
    return "Maximum" if curvature < 0 else "Minimum"


def generate_cubic_problem() -> dict:
    rng = np.random.default_rng()
    while True:
        roots = rng.choice(np.arange(-5, 6), size=3, replace=False)
        scale = rng.integers(1, 4)
        coeffs = np.poly(roots) * scale
        poly = np.poly1d(coeffs)
        real_roots = sorted(
            root.real for root in poly.r if abs(root.imag) <= 1e-8
        )
        if len(real_roots) < 3:
            continue
        derivative = poly.deriv()
        critical_points: List[CriticalPoint] = []
        for critical in derivative.r:
            if abs(critical.imag) > 1e-8:
                continue
            x_value = critical.real
            y_value = poly(x_value)
            kind = classify_extremum(poly, x_value)
            critical_points.append(CriticalPoint(x=x_value, y=y_value, kind=kind))
        if len(critical_points) < 2:
            continue
        critical_points.sort(key=lambda point: point.x)
        intercept_y = poly(0)
        x_values = np.linspace(min(real_roots) - 3, max(real_roots) + 3, 400)
        y_values = poly(x_values)
        return {
            "poly": poly,
            "coeffs": coeffs,
            "roots": real_roots,
            "critical_points": critical_points,
            "intercept": (0.0, intercept_y),
            "x": x_values,
            "y": y_values,
        }


VARIABLE_EXAMPLES = [
    {
        "text": (
            "In einem Labor wird die Temperatur eines Chemieversuchs alle paar Minuten gemessen. "
            "Mit zunehmender Zeit verändert sich die Temperatur der Flüssigkeit."
        ),
        "independent": {
            "symbol": "t",
            "description": "Zeit",
            "unit": "min",
            "unit_long": "Minuten",
        },
        "dependent": {
            "symbol": "T",
            "description": "Temperatur",
            "unit": "°C",
            "unit_long": "Grad Celsius",
        },
    },
    {
        "text": (
            "Eine Läuferin zeichnet auf, wie weit sie bei einem Trainingslauf kommt. "
            "Nach jeder viertel Stunde notiert sie die bereits zurückgelegte Strecke."
        ),
        "independent": {
            "symbol": "t",
            "description": "Zeit",
            "unit": "min",
            "unit_long": "Minuten",
        },
        "dependent": {
            "symbol": "s",
            "description": "Wegstrecke",
            "unit": "m",
            "unit_long": "Meter",
        },
    },
    {
        "text": (
            "Beim Wachstum eines Kindes wird jedes Jahr die Körpergröße festgehalten, um den Verlauf zu beobachten."
        ),
        "independent": {
            "symbol": "t",
            "description": "Zeit",
            "unit": "Jahre",
            "unit_long": "Jahre",
        },
        "dependent": {
            "symbol": "h",
            "description": "Körpergröße",
            "unit": "cm",
            "unit_long": "Zentimeter",
        },
    },
    {
        "text": (
            "Ein Autohersteller testet, wie sich die Geschwindigkeit eines Prototyps während einer Testfahrt entwickelt."
        ),
        "independent": {
            "symbol": "t",
            "description": "Zeit",
            "unit": "s",
            "unit_long": "Sekunden",
        },
        "dependent": {
            "symbol": "v",
            "description": "Geschwindigkeit",
            "unit": "m/s",
            "unit_long": "Meter pro Sekunde",
        },
    },
    {
        "text": (
            "In einem Physikexperiment wird gemessen, wie hoch ein Körper über dem Boden ist, während er fällt."
        ),
        "independent": {
            "symbol": "t",
            "description": "Zeit",
            "unit": "s",
            "unit_long": "Sekunden",
        },
        "dependent": {
            "symbol": "h",
            "description": "Höhe",
            "unit": "m",
            "unit_long": "Meter",
        },
    },
    {
        "text": (
            "Bei einer Studie zur Stromnutzung wird aufgezeichnet, wie viel Energie ein Haushalt im Laufe eines Tages verbraucht."
        ),
        "independent": {
            "symbol": "t",
            "description": "Zeit",
            "unit": "h",
            "unit_long": "Stunden",
        },
        "dependent": {
            "symbol": "E",
            "description": "Energieverbrauch",
            "unit": "kWh",
            "unit_long": "Kilowattstunden",
        },
    },
]


def get_new_variable_problem() -> dict:
    return random.choice(VARIABLE_EXAMPLES)


if CUBIC_PROBLEM_KEY not in st.session_state:
    st.session_state[CUBIC_PROBLEM_KEY] = generate_cubic_problem()
    st.session_state[CUBIC_SOLUTION_KEY] = False

if VARIABLE_PROBLEM_KEY not in st.session_state:
    st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
    st.session_state[VARIABLE_SOLUTION_KEY] = False


st.title("Funktionen allgemein")

beschreibung = (
    "Arbeite dich durch die Aufgaben in den Tabs. Nutze die Schaltfläche \"Lösung\", um die Antwort zu prüfen."
)
st.write(beschreibung)

analyse_tab, variable_tab = st.tabs([
    "Polynomfunktion 3. Grades",
    "Abhängige und unabhängige Variablen",
])

with analyse_tab:
    problem = st.session_state[CUBIC_PROBLEM_KEY]
    show_solution = st.session_state[CUBIC_SOLUTION_KEY]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(problem["x"], problem["y"], label="f(x)", color="#1f77b4")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Polynomfunktion 3. Grades")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlim(problem["x"][0], problem["x"][-1])

    if show_solution:
        for root in problem["roots"]:
            ax.scatter(root, 0, s=120, facecolors="white", edgecolors="#ff7f0e", linewidths=2)
            ax.annotate(
                "Nullstelle",
                xy=(root, 0),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                color="#ff7f0e",
            )

        intercept_x, intercept_y = problem["intercept"]
        ax.scatter(
            intercept_x,
            intercept_y,
            s=120,
            facecolors="white",
            edgecolors="#2ca02c",
            linewidths=2,
        )
        ax.annotate(
            "Achsenabschnitt",
            xy=(intercept_x, intercept_y),
            xytext=(40, 10),
            textcoords="offset points",
            color="#2ca02c",
        )

        for critical in problem["critical_points"]:
            color = "#d62728" if critical.kind == "Maximum" else "#9467bd"
            ax.scatter(
                critical.x,
                critical.y,
                s=140,
                facecolors="white",
                edgecolors=color,
                linewidths=2,
            )
            ax.annotate(
                critical.kind,
                xy=(critical.x, critical.y),
                xytext=(5, 15),
                textcoords="offset points",
                color=color,
            )

    st.pyplot(fig)

    st.subheader("Aufgabenstellung")
    st.markdown(
        """
        * Bestimme die Nullstellen. Wie viele gibt es?
        * Wo befindet sich das Maximum? Wo das Minimum?
        * Wie lautet der Achsenabschnitt?
        """
    )

    st.button(
        "Lösung",
        key="cubic_solution_button",
        on_click=lambda: st.session_state.update({CUBIC_SOLUTION_KEY: True}),
    )

    if st.session_state[CUBIC_SOLUTION_KEY]:
        roots_text = ", ".join(f"x = {root:.2f}" for root in problem["roots"])
        st.success(
            f"Nullstellen: {roots_text} (insgesamt {len(problem['roots'])})"
        )

        max_points = [pt for pt in problem["critical_points"] if pt.kind == "Maximum"]
        min_points = [pt for pt in problem["critical_points"] if pt.kind == "Minimum"]
        if max_points:
            maximum = max_points[0]
            st.info(f"Maximum: ({maximum.x:.2f} | {maximum.y:.2f})")
        if min_points:
            minimum = min_points[-1]
            st.info(f"Minimum: ({minimum.x:.2f} | {minimum.y:.2f})")

        intercept_x, intercept_y = problem["intercept"]
        st.info(f"Achsenabschnitt: ({intercept_x:.0f} | {intercept_y:.2f})")

        st.button(
            "Neues Beispiel",
            key="cubic_new_example",
            on_click=lambda: st.session_state.update(
                {
                    CUBIC_PROBLEM_KEY: generate_cubic_problem(),
                    CUBIC_SOLUTION_KEY: False,
                }
            ),
        )

with variable_tab:
    variable_problem = st.session_state[VARIABLE_PROBLEM_KEY]

    st.subheader("Variablen erkennen")
    st.write(variable_problem["text"])
    st.markdown(
        """
        Welche Variable ist unabhängig und welche hängt von ihr ab?
        Notiere Symbol, Bedeutung und Einheit.
        """
    )

    st.button(
        "Lösung",
        key="variable_solution_button",
        on_click=lambda: st.session_state.update({VARIABLE_SOLUTION_KEY: True}),
    )

    if st.session_state[VARIABLE_SOLUTION_KEY]:
        independent = variable_problem["independent"]
        dependent = variable_problem["dependent"]
        st.success(
            f"Unabhängige Variable: {independent['symbol']} ... {independent['description']} ({independent['unit_long']})"
        )
        st.success(
            f"Abhängige Variable: {dependent['symbol']} ... {dependent['description']} ({dependent['unit_long']})"
        )

        st.button(
            "Neues Beispiel",
            key="variable_new_example",
            on_click=lambda: st.session_state.update(
                {
                    VARIABLE_PROBLEM_KEY: get_new_variable_problem(),
                    VARIABLE_SOLUTION_KEY: False,
                }
            ),
        )
