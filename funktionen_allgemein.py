import random
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st


# ==========================================================
#   FUNKTIONEN ALLGEMEIN
# ==========================================================

# ----------------- Session Keys -----------------
POLY_PROBLEM_KEY = "poly_problem_coeff_v1"
POLY_SHOW_KEY    = "poly_show_solution_coeff_v1"
POLY_LAST_DEGREE = "poly_last_degree_coeff_v1"   # 2 oder 3

VARIABLE_PROBLEM_KEY = "variable_problem_v2"
VARIABLE_SHOW_KEY    = "variable_show_solution_v2"
STATEMENT_DATA_KEY   = "variable_statement_data_v2"
STATEMENT_STAGE_KEY  = "variable_statement_stage_v2"


# ----------------- Dataclass -----------------
@dataclass
class CriticalPoint:
    x: float
    y: float
    kind: str  # "Maximum" or "Minimum"


# ----------------- Helpers -----------------
def _axes_origin(ax):
    for s in ("right", "top"):
        ax.spines[s].set_color("none")
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_linewidth(1.2)
    ax.spines["bottom"].set_linewidth(1.2)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    ax.grid(True, linestyle="--", alpha=0.35)


# ----------------- Generators -----------------
def build_cubic_coeff(rng: np.random.Generator) -> dict:
    def pick_ab():
        a = (-1 if rng.random() < 0.5 else 1) * rng.uniform(0.15, 0.30)
        b = rng.uniform(1.0, 2.0) if rng.random() < 0.5 else rng.uniform(-2.0, -1.0)
        return float(a), float(b)

    while True:
        a, b = pick_ab()
        c = float(rng.uniform(0.1, 3.0))
        d = float(rng.uniform(-2.0, 2.0))
        poly = np.poly1d([a, b, c, d])

        der = poly.deriv()
        crit = [z.real for z in der.r if abs(z.imag) < 1e-10]
        if len(crit) != 2:
            continue
        crit.sort()

        if not all(-8.0 <= x0 <= 8.0 for x0 in crit):
            continue

        y_abs = [abs(float(poly(x0))) for x0 in crit]
        mean_abs = max(np.mean(y_abs), 1e-9)
        target = rng.uniform(5.0, 7.5)
        scale = target / mean_abs
        poly = poly * scale

        roots = [r.real for r in poly.r if abs(r.imag) < 1e-10]

        cps = []
        ok = True
        for x0 in crit:
            y0 = float(poly(x0))
            if not (4.0 <= abs(y0) <= 9.0):
                ok = False
                break
            if roots and min(abs(x0 - r) for r in roots) < 1.0:
                ok = False
                break
            k2 = float(poly.deriv(2)(x0))
            kind = "Maximum" if k2 < 0 else "Minimum"
            cps.append(CriticalPoint(x=float(x0), y=y0, kind=kind))

        if not ok:
            continue

        return {
            "degree": 3,
            "poly": poly,
            "roots": roots,
            "critical_points": cps,
            "intercept": (0.0, float(poly(0.0))),
        }


def build_quadratic_roots(rng: np.random.Generator) -> dict:
    scale_choices = [1, -1, 2, -2]
    candidates = [x for x in np.arange(-6.0, 6.5, 0.5) if abs(x) > 1e-9]

    while True:
        r1, r2 = rng.choice(candidates, size=2, replace=False)
        if abs(r2 - r1) < 0.75:
            continue
        s = float(rng.choice(scale_choices))

        a = s
        b = -s * (r1 + r2)
        c = s * r1 * r2
        poly = np.poly1d([a, b, c])

        xv = -b / (2 * a)
        if not (-8 <= xv <= 8):
            continue
        yv = float(poly(xv))
        if not (3.0 <= abs(yv) <= 8.0):
            continue

        y0 = float(poly(0.0))
        if abs(y0) < 1e-9:
            continue

        kind = "Minimum" if a > 0 else "Maximum"
        cps = [CriticalPoint(x=float(xv), y=float(yv), kind=kind)]
        roots = [float(r1), float(r2)]
        return {
            "degree": 2,
            "poly": poly,
            "roots": roots,
            "critical_points": cps,
            "intercept": (0.0, y0),
        }


def generate_alternating_poly() -> dict:
    rng = np.random.default_rng()
    last = st.session_state.get(POLY_LAST_DEGREE, 3)
    if last == 3:
        prob = build_quadratic_roots(rng)
        st.session_state[POLY_LAST_DEGREE] = 2
    else:
        prob = build_cubic_coeff(rng)
        st.session_state[POLY_LAST_DEGREE] = 3
    return prob


# ----------------- Plot -----------------
def plot_poly_with_markers(problem: dict, show_solution: bool):
    poly = problem["poly"]
    x_left, x_right = -10.0, 10.0
    y_bottom, y_top = -10.0, 10.0

    fig, ax = plt.subplots(figsize=(7.8, 5.4))

    xx = np.linspace(x_left - 2, x_right + 2, 1600)
    yy = poly(xx)
    line, = ax.plot(xx, yy, linewidth=2.0)
    line.set_clip_on(True)

    _axes_origin(ax)
    ax.set_xlim(x_left, x_right)
    ax.set_ylim(y_bottom, y_top)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    if show_solution:
        roots = [r.real for r in problem.get("poly").r if abs(r.imag) < 1e-10]
        for r in roots:
            if np.isfinite(r) and x_left <= r <= x_right:
                ax.scatter(r, 0, s=120, facecolors="white", edgecolors="#ff7f0e", linewidths=2, zorder=3)
                ax.annotate("N", xy=(r, 0), xytext=(0, 10), textcoords="offset points",
                            ha="center", color="#ff7f0e", fontsize=12, fontweight="bold")

        x0, y0 = problem["intercept"]
        if y_bottom <= y0 <= y_top:
            ax.scatter(x0, y0, s=120, facecolors="white", edgecolors="#2ca02c", linewidths=2, zorder=3)
            ax.annotate("d", xy=(x0, y0), xytext=(10, 10), textcoords="offset points",
                        color="#2ca02c", fontsize=12, fontweight="bold")

        for cp in problem.get("critical_points", []):
            if x_left <= cp.x <= x_right and y_bottom <= cp.y <= y_top:
                color = "#d62728" if cp.kind == "Maximum" else "#9467bd"
                label = "Max" if cp.kind == "Maximum" else "Min"
                ax.scatter(cp.x, cp.y, s=130, facecolors="white", edgecolors=color, linewidths=2, zorder=3)
                ax.annotate(label, xy=(cp.x, cp.y), xytext=(6, 12), textcoords="offset points",
                            color=color, fontsize=12, fontweight="bold")

    fig.tight_layout()
    return fig


# ----------------- Variable-Tab -----------------
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


def generate_statement_for(problem: dict) -> dict:
    ind, dep = problem["independent"], problem["dependent"]
    x = random.choice(range(1, 11))
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

    if ind["unit"] in ("h", "Stunden", "Std.", "hour"):
        time_phrase = f"nach {x} Stunden"
    elif ind["unit"] in ("min", "Minuten"):
        time_phrase = f"nach {x} Minuten"
    elif ind["unit"] in ("s", "Sekunden"):
        time_phrase = f"nach {x} Sekunden"
    elif ind["unit"] in ("Jahre", "Jahr"):
        time_phrase = f"nach {x} Jahren"
    else:
        time_phrase = f"bei {ind['description']} = {x} {ind['unit']}"

    return {
        "text": f"{time_phrase} beträgt die {dep['description']} {y} {dep['unit']}.",
        "expr": f"{dep['symbol']}({x}) = {y}",
    }


# ==========================================================
#   RUN
# ==========================================================

def run():
    if POLY_PROBLEM_KEY not in st.session_state:
        st.session_state[POLY_LAST_DEGREE] = 2
        st.session_state[POLY_PROBLEM_KEY] = generate_alternating_poly()
        st.session_state[POLY_SHOW_KEY] = False

    if VARIABLE_PROBLEM_KEY not in st.session_state:
        st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
        st.session_state[VARIABLE_SHOW_KEY] = False

    if STATEMENT_STAGE_KEY not in st.session_state:
        st.session_state[STATEMENT_STAGE_KEY] = 0
    if STATEMENT_DATA_KEY not in st.session_state:
        st.session_state[STATEMENT_DATA_KEY] = None

    st.title("Funktionen allgemein")

    tab1, tab2 = st.tabs(["Besondere Punkte einer Funktion", "Abhängige & unabhängige Variablen"])

    with tab1:
        problem = st.session_state[POLY_PROBLEM_KEY]
        show = st.session_state[POLY_SHOW_KEY]

        st.subheader("Aufgabenstellung")
        st.markdown(
            """
            Zeichne den Graphen und bestimme die **besonderen Punkte**:
            - Nullstellen (**N**)
            - Extrempunkte (**Max / Min**)
            - y-Achsenabschnitt (**d**)
            """
        )

        st.pyplot(plot_poly_with_markers(problem, show))

        c1, c2 = st.columns(2)
        if c1.button("Lösung"):
            st.session_state[POLY_SHOW_KEY] = True
            st.rerun()
        if c2.button("Neue Funktion"):
            st.session_state[POLY_PROBLEM_KEY] = generate_alternating_poly()
            st.session_state[POLY_SHOW_KEY] = False
            st.rerun()

    with tab2:
        vp = st.session_state[VARIABLE_PROBLEM_KEY]
        show_vars = st.session_state[VARIABLE_SHOW_KEY]
        stage = st.session_state[STATEMENT_STAGE_KEY]

        st.subheader("Variablen erkennen")
        st.write(vp["text"])
        st.markdown(
            "**Aufgabe 1:** Bestimme **unabhängige** und **abhängige** Variable. "
            "Notiere **Symbol**, **Bedeutung** und **Einheit**."
        )

        if st.button("Lösung (Variablen)"):
            st.session_state[VARIABLE_SHOW_KEY] = True
            st.session_state[STATEMENT_STAGE_KEY] = 1
            st.session_state[STATEMENT_DATA_KEY] = generate_statement_for(vp)
            st.rerun()

        if show_vars:
            ind, dep = vp["independent"], vp["dependent"]
            st.success(f"Unabhängige Variable: {ind['symbol']} … {ind['description']} ({ind['unit']})")
            st.success(f"Abhängige Variable: {dep['symbol']} … {dep['description']} ({dep['unit']})")

        if stage >= 1 and st.session_state[STATEMENT_DATA_KEY] is not None:
            s = st.session_state[STATEMENT_DATA_KEY]
            st.markdown("---")
            st.subheader("Mathematische Aussage formulieren")
            ind, dep = vp["independent"], vp["dependent"]
            st.markdown(
                f"**Formel/Notation:** {dep['symbol']}({ind['symbol']}) – "
                f"{dep['description']} in Abhängigkeit von {ind['description']}."
            )
            st.write(f"**Aussage:** {s['text']}")

            if st.button("Lösung (Aussage → Ausdruck)"):
                st.session_state[STATEMENT_STAGE_KEY] = 2
                st.rerun()
            if st.session_state[STATEMENT_STAGE_KEY] >= 2:
                st.success(s["expr"])

            if st.button("Neues Beispiel"):
                st.session_state[VARIABLE_PROBLEM_KEY] = get_new_variable_problem()
                st.session_state[VARIABLE_SHOW_KEY] = False
                st.session_state[STATEMENT_STAGE_KEY] = 0
                st.session_state[STATEMENT_DATA_KEY] = None
                st.rerun()
