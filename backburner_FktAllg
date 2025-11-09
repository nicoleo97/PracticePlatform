# pages/FunktionenAllgemein.py
import streamlit as st, numpy as np, matplotlib.pyplot as plt, math

# ---------- Toleranzen ----------
EPS_CP = 0.1   # Toleranz für kritische Punkte an Intervallgrenzen
EPS_D  = 1e-6  # Toleranz für Ableitungs-Null

# ---------- Reset ----------
def reset_ui():
    for k in list(st.session_state.keys()):
        if k.startswith(("t1_","t2_","t3_","t4_")):
            del st.session_state[k]
    st.session_state.pop("t2_roots", None)
    st.session_state["t4_n_segs"] = 1  # Tab4: Abschnitte auf 1 zurücksetzen

# ---------- Helpers ----------
def new_rng(btn_key):
    if st.button("Neue Funktion", key=btn_key):
        st.session_state.seed = np.random.randint(0, 10**9)
        reset_ui()
    return np.random.default_rng(st.session_state.get("seed", None))

def rand_poly_any(rng, max_deg=3):
    grad = int(rng.integers(1, max_deg + 1))
    coeffs = rng.integers(-5, 6, size=grad + 1)
    coeffs[0] = coeffs[0] or 1
    return np.poly1d(coeffs)

def rand_poly_int_roots(rng):
    deg = int(rng.integers(1, 5))
    pool = [i for i in range(-4, 5)]
    roots = rng.choice(pool, size=deg, replace=False)
    lead = int(rng.integers(-3, 4) or 1)
    p = np.poly1d([lead])
    for r in roots:
        p = np.polymul(p, np.poly1d([1, -r]))
    st.session_state.t2_roots = np.sort(roots.astype(float))
    return p

def plot_poly_square(p, L, tick_labelsize=6, vlines=None):
    x = np.linspace(-L, L, 1200); y = p(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2)
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(range(-L, L + 1)); ax.set_yticks(range(-L, L + 1))
    ax.tick_params(axis='both', which='both', labelsize=tick_labelsize)
    ax.spines['bottom'].set_position('zero'); ax.spines['left'].set_position('zero')
    for s in ['bottom','left','right','top']: ax.spines[s].set_color('none')
    ax.xaxis.set_ticks_position('bottom'); ax.yaxis.set_ticks_position('left')
    ax.annotate("", xy=( L, 0), xytext=(-L, 0), arrowprops=dict(arrowstyle='-|>', lw=0.5))
    ax.annotate("", xy=(0,  L), xytext=(0, -L), arrowprops=dict(arrowstyle='-|>', lw=0.5))
    ax.text(L - 0.4, 0.3, "x", fontsize=tick_labelsize+1)
    ax.text(0.3, L - 0.4, "f(x)", fontsize=tick_labelsize+1)
    if vlines:
        for xv in vlines: ax.axvline(xv, linestyle="--", linewidth=1, alpha=0.7)
    ax.set_xlabel(""); ax.set_ylabel(""); ax.grid(True, which="both", alpha=0.3)
    st.pyplot(fig, use_container_width=True)

def real_roots_unique(p, tol=1e-3):
    r = np.roots(p)
    real = np.real(r[np.isclose(np.imag(r), 0, atol=1e-8)])
    if real.size == 0: return np.array([])
    real = np.sort(real)
    uniq = [real[0]]
    for v in real[1:]:
        if abs(v - uniq[-1]) > tol: uniq.append(v)
    return np.array(uniq)

def crit_points(p):
    dp = np.polyder(p)
    r = np.roots(dp)
    r = np.real(r[np.isclose(np.imag(r), 0, atol=1e-8)])
    return np.sort(r)

def parse_endpoint(label):
    if label in ("-∞", "-inf"): return -np.inf
    if label in ("∞", "inf"):   return  np.inf
    return float(label)

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["Polynom-Quiz", "Nullstellen im Detail", "Achsenabschnitt", "Monotonie"])

# ---------- Tab 1 ----------
with tab1:
    rng = new_rng("btn_new_t1")
    p = rand_poly_any(rng, max_deg=3)
    plot_poly_square(p, L=10, tick_labelsize=6)

    st.radio("Wieviele Nullstellen gibt es?", [0, 1, 2, 3], horizontal=True, key="t1_nullst")
    st.radio("Wieviele Extrempunkte gibt es?", [0, 1, 2], horizontal=True, key="t1_extrema")
    st.radio("Monotonieverhalten?", ["immer steigend", "immer fallend", "beides"], horizontal=True, key="t1_mono")

    if st.button("Antworten prüfen", key="check_t1"):
        r_uni = real_roots_unique(p)
        n_null = len(r_uni)
        dp = np.polyder(p); crit = np.roots(dp)
        n_ext = np.sum(np.isclose(np.imag(crit), 0))
        xs = np.linspace(-10, 10, 2001)
        dvals = np.polyval(dp, xs)
        mono = "immer steigend" if np.all(dvals > EPS_D) else ("immer fallend" if np.all(dvals < -EPS_D) else "beides")
        st.write(("✅" if st.session_state.t1_nullst == n_null else "❌"), f"Nullstellen: {n_null}")
        st.write(("✅" if st.session_state.t1_extrema == n_ext else "❌"), f"Extrema: {n_ext}")
        st.write(("✅" if st.session_state.t1_mono == mono else "❌"), f"Monotonie: {mono}")

# ---------- Tab 2 ----------
with tab2:
    rng = new_rng("btn_new_t2")
    p = rand_poly_int_roots(rng)
    plot_poly_square(p, L=5, tick_labelsize=6)

    st.subheader("Anzahl der Nullstellen wählen")
    count = st.selectbox("", [0, 1, 2, 3, 4], index=0, key="t2_count")
    st.subheader("Eingabe der Nullstelle(n)")
    inputs = [st.number_input(f"x-Koordinate von N_{i}", value=0.0, step=1.0, format="%.0f", key=f"t2_x_{i}")
              for i in range(1, count + 1)]

    if st.button("Antworten prüfen", key="check_t2"):
        correct_roots = st.session_state.get("t2_roots", real_roots_unique(p))
        ok_count = len(correct_roots) == count
        st.write(("✅" if ok_count else "❌"), f"Anzahl: erwartet {len(correct_roots)}, gewählt {count}")
        ok_points = ok_count and all(any(abs(x_u - xr) <= 0.05 for xr in correct_roots) for x_u in inputs)
        st.write(("✅" if ok_points else "❌"),
                 "Nullstellen korrekt eingegeben." if ok_points else f"Korrekte Nullstellen x: {np.round(correct_roots, 3).tolist()}")

# ---------- Tab 3 ----------
with tab3:
    rng = new_rng("btn_new_t3")
    p = rand_poly_any(rng, max_deg=3)
    d_val = float(np.polyval(p, 0))
    L = int(math.ceil(max(5.0, abs(d_val) + 1.0)))
    plot_poly_square(p, L=L, tick_labelsize=6)
    d_user = st.number_input("Achsenabschnitt bei", value=0.0, step=0.5, key="t3_d")
    if st.button("Antworten prüfen", key="check_t3"):
        ok_d = abs(d_user - d_val) <= 0.05
        st.write(("✅" if ok_d else "❌"), f"d = {d_val:.3f}")

# ---------- Tab 4 ----------
with tab4:
    rng = new_rng("btn_new_t4")
    p = rand_poly_any(rng, max_deg=3)

    # --- Plotbereich so wählen, dass Extrema sichtbar sind ---
    dp_global = np.polyder(p)
    cps_global = np.roots(dp_global)
    cps_global = np.real(cps_global[np.isclose(np.imag(cps_global), 0, atol=1e-8)])
    d_here = float(np.polyval(p, 0))
    if cps_global.size:
        max_x = float(np.max(np.abs(cps_global)))
        max_y = float(np.max(np.abs(p(cps_global))))
    else:
        max_x = 0.0
        max_y = 0.0
    L4 = int(math.ceil(max(5.0, abs(d_here)+1.0, max_x+1.0, max_y+1.0)))

    st.subheader("Anzahl der Abschnitte wählen")
    n_segs = st.selectbox("", [1,2,3,4,5], index=0, key="t4_n_segs")
    n_lines = max(0, n_segs - 1)

    defaults = np.linspace(-L4/2, L4/2, max(n_lines,1)+2)[1:-1] if n_lines>0 else []
    lines = [st.slider(f"Trennlinie {i+1}",
                       min_value=float(-L4), max_value=float(L4),
                       value=float(defaults[i]) if i < len(defaults) else 0.0,
                       step=0.1, key=f"t4_line_{i+1}") for i in range(n_lines)]
    lines = sorted(lines)

    plot_poly_square(p, L=L4, tick_labelsize=6, vlines=lines)

    endpoint_labels = ["-∞"] + [f"{x:.3f}" for x in lines] + ["∞"]
    st.subheader("Intervalle wählen & Trend setzen")
    intervals, trends = [], []
    for i in range(1, n_segs + 1):
        c1, c2, c3 = st.columns([1,1,1])
        left_default  = endpoint_labels[i-1]
        right_default = endpoint_labels[i] if i < len(endpoint_labels) else endpoint_labels[-1]
        left_label  = c1.selectbox(f"linker Rand {i}", endpoint_labels, index=endpoint_labels.index(left_default), key=f"t4_l_{i}")
        right_label = c2.selectbox(f"rechter Rand {i}", endpoint_labels, index=endpoint_labels.index(right_default), key=f"t4_r_{i}")
        trend = c3.radio(f"Trend {i}", ["steigend","fallend"], horizontal=True, key=f"t4_trend_{i}")
        a, b = sorted((parse_endpoint(left_label), parse_endpoint(right_label)))
        intervals.append((a, b)); trends.append(trend)

    if st.button("Antworten prüfen", key="check_t4"):
        dp, cps = dp_global, cps_global
        def sign_at(x): return float(np.polyval(dp, x))
        all_ok = True
        for (a,b),trend in zip(intervals, trends):
            lab_a = "-∞" if np.isneginf(a) else f"{a:.3f}"
            lab_b = "∞"  if np.isposinf(b) else f"{b:.3f}"
            A = max(a, -L4) if not np.isneginf(a) else -L4
            B = min(b,  L4) if not np.isposinf(b) else  L4
            if not (A < B):
                all_ok=False; st.write("❌", f"Intervall [{lab_a},{lab_b}] schneidet den sichtbaren Bereich nicht."); continue
            mid=0.5*(A+B); s=sign_at(mid); wanted=1 if trend=="steigend" else -1
            ok_trend=(s>EPS_D and wanted==1) or (s<-EPS_D and wanted==-1)
            has_cp=np.any((cps>a+EPS_CP)&(cps<b-EPS_CP))
            ok_constant_free=not has_cp
            if ok_trend and ok_constant_free:
                st.write("✅", f"[{lab_a},{lab_b}] {trend}")
            else:
                all_ok=False; reason=[]
                if not ok_trend: reason.append("Trend passt nicht")
                if not ok_constant_free: reason.append("Richtungswechsel im Intervall")
                st.write("❌", f"[{lab_a},{lab_b}] {trend} – "+", ".join(reason))
        if all_ok:
            st.success("Alle Abschnitte konsistent.")
        else:
            bounds=[-np.inf]+lines+[np.inf]
            parts=[]
            for i in range(len(bounds)-1):
                a,b=bounds[i],bounds[i+1]
                A=max(a,-L4) if not np.isneginf(a) else -L4
                B=min(b, L4) if not np.isposinf(b) else L4
                if A>=B: continue
                m=0.5*(A+B); s=float(np.polyval(dp, m))
                t="steigend" if s>EPS_D else ("fallend" if s<-EPS_D else "konstant")
                la="-∞" if np.isneginf(a) else f"{a:.3f}"
                rb="∞" if np.isposinf(b) else f"{b:.3f}"
                parts.append(f"[{la},{rb}] {t}")
            if parts:
                st.caption("Monotonie-Aufteilung (global): "+" | ".join(parts))
