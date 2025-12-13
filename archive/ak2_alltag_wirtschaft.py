import streamlit as st
import random

def run():
    st.set_page_config(page_title="Lineare Funktionen – Alltag & Wirtschaft")
    st.title("Beispiele zu linearen Funktionen")

    tab_alltag, tab_wirtschaft = st.tabs(["Alltag", "Wirtschaft (Kosten/Erlös)"])


    # -------------------------------------------------------------
    # FUNKTION: ALLTAGSBEISPIEL GENERIEREN
    # -------------------------------------------------------------
    def generate_alltag_example():
        typ = random.choice([
            "eis", "akku", "glas", "keller",
            "lama", "ballon", "getraenk", "kerze"
        ])

        # ------------------- Eisfigur schmilzt -------------------
        if typ == "eis":
            start = random.randrange(60, 121, 5)
            r = random.randrange(1, 4)
            t_b = random.randint(10, 30)

            return {
                "titel": "Eisfigur schmilzt",
                "text": (
                    f"Eine Eisfigur hat zu Beginn eine Masse von **{start} g**. "
                    f"Sie schmilzt gleichmäßig um **{r} g pro Minute**.\n\n"
                    "a) Stelle die Funktionsgleichung für die Masse in Abhängigkeit von t auf."
                ),
                "f": f"f(t) = {start} - {r}·t",
                "b_text": f"b) Wie viel Masse hat die Figur nach **{t_b} Minuten**?",
                "b_loesung": f"{start} - {r}·{t_b} = **{start - r*t_b} g**",
                "c_text": "c) Welche Bedeutung hat die Nullstelle im Kontext?",
                "c_loesung": (
                    f"Die Nullstelle liegt bei t = {start}/{r} = **{start/r:.1f} min**.\n"
                    "Dann ist die Eisfigur vollständig geschmolzen."
                ),
            }

        # ------------------- Akku lädt -------------------
        if typ == "akku":
            start = random.randint(1, 15)
            r = random.choice([0.5, 0.8, 1.0])
            t_b = random.randint(20, 60)
            voll = (100 - start) / r

            return {
                "titel": "Akku lädt",
                "text": (
                    f"Der Akku eines Smartphones besitzt zu Beginn **{start} %**. "
                    f"Er lädt sich gleichmäßig um **{r} % pro Minute**.\n\n"
                    "a) Stelle die Funktionsgleichung für den Ladezustand auf."
                ),
                "f": f"f(t) = {start} + {r}·t",
                "b_text": f"b) Wie hoch ist die Ladung nach **{t_b} Minuten**?",
                "b_loesung": f"{start} + {r}·{t_b} = **{start + r*t_b:.1f} %**",
                "c_text": "c) Nach welcher Zeit erreicht der Akku 100 %?",
                "c_loesung": (
                    f"t = (100 - {start})/{r} = **{voll:.1f} min**."
                ),
            }

        # ------------------- Glas wird gefüllt -------------------
        if typ == "glas":
            rate = random.randrange(80, 161, 10)
            vol = random.randrange(400, 801, 50)
            t_b = random.randint(1, 5)

            return {
                "titel": "Glas wird gefüllt",
                "text": (
                    f"Ein leeres Glas soll befüllt werden. Es fasst **{vol} ml**. "
                    f"Das Wasser fließt mit **{rate} ml pro Sekunde** ein.\n\n"
                    "a) Stelle die Funktionsgleichung für die Füllmenge auf."
                ),
                "f": f"f(t) = {rate}·t",
                "b_text": f"b) Wie viel Wasser befindet sich nach **{t_b} Sekunden** im Glas?",
                "b_loesung": f"{rate}·{t_b} = **{rate*t_b} ml**",
                "c_text": "c) Nach welcher Zeit ist das Glas vollständig gefüllt?",
                "c_loesung": (
                    f"t = {vol}/{rate} = **{vol/rate:.2f} s**."
                ),
            }

        # ------------------- Keller wird ausgepumpt -------------------
        if typ == "keller":
            h0 = random.randrange(80, 161, 10)
            r = random.randrange(5, 16, 5)
            t_b = random.randint(2, 10)

            return {
                "titel": "Keller wird ausgepumpt",
                "text": (
                    f"Ein Keller steht nach einem Unwetter **{h0} cm** unter Wasser. "
                    f"Eine Pumpe senkt den Wasserstand gleichmäßig um **{r} cm pro Stunde**.\n\n"
                    "a) Stelle die Funktionsgleichung für die Wasserhöhe auf."
                ),
                "f": f"f(t) = {h0} - {r}·t",
                "b_text": f"b) Wie hoch steht das Wasser nach **{t_b} Stunden**?",
                "b_loesung": f"{h0} - {r}·{t_b} = **{h0 - r*t_b} cm**",
                "c_text": "c) Welche Bedeutung hat die Nullstelle?",
                "c_loesung": (
                    f"t = {h0}/{r} = **{h0/r:.1f} h** → Keller ist leer."
                ),
            }

        # ------------------- Lama (Spaßaufgabe) -------------------
        if typ == "lama":
            start = random.randint(20, 40)
            r = random.randint(3, 8)
            t_b = random.randint(3, 10)

            return {
                "titel": "Lama spuckt in eine Schüssel",
                "text": (
                    f"In einer Schüssel befinden sich zu Beginn **{start} ml** Wasser. "
                    f"Ein Lama spuckt gleichmäßig **{r} ml pro Minute** hinein.\n\n"
                    "a) Stelle die Funktionsgleichung auf."
                ),
                "f": f"f(t) = {start} + {r}·t",
                "b_text": f"b) Wie viel Wasser enthält die Schüssel nach **{t_b} Minuten**?",
                "b_loesung": f"{start + r*t_b} ml",
                "c_text": "c) Wann enthält die Schüssel **200 ml**?",
                "c_loesung": f"t = (200 - {start})/{r} = **{(200-start)/r:.2f} min**",
            }

        # ------------------- Ballon wird aufgeblasen -------------------
        if typ == "ballon":
            start = random.randint(200, 400)
            r = random.randint(20, 60)
            t_b = random.randint(2, 6)

            return {
                "titel": "Ballon wird aufgeblasen",
                "text": (
                    f"Ein Luftballon enthält zu Beginn **{start} ml** Luft. "
                    f"Pro Sekunde kommen **{r} ml** hinzu.\n\n"
                    "a) Stelle die Funktionsgleichung auf."
                ),
                "f": f"f(t) = {start} + {r}·t",
                "b_text": f"b) Wie viel Luft enthält der Ballon nach **{t_b} Sekunden**?",
                "b_loesung": f"{start + r*t_b} ml",
                "c_text": "c) Wann erreicht der Ballon **1000 ml**?",
                "c_loesung": f"t = (1000 - {start})/{r} = **{(1000-start)/r:.2f} s**",
            }

        # ------------------- Getränk wird getrunken -------------------
        if typ == "getraenk":
            start = random.randint(300, 600)
            r = random.randint(50, 120)
            t_b = random.randint(1, 4)

            return {
                "titel": "Getränk wird ausgetrunken",
                "text": (
                    f"Eine Flasche enthält zu Beginn **{start} ml**. "
                    f"Eine Person trinkt gleichmäßig **{r} ml pro Minute**.\n\n"
                    "a) Stelle die Funktionsgleichung für den verbleibenden Inhalt auf."
                ),
                "f": f"f(t) = {start} - {r}·t",
                "b_text": f"b) Wie viel ist nach **{t_b} Minuten** noch übrig?",
                "b_loesung": f"{start - r*t_b} ml",
                "c_text": "c) Wann ist die Flasche leer?",
                "c_loesung": f"t = {start}/{r} = **{start/r:.2f} min**",
            }

        # ------------------- Kerze brennt ab -------------------
        if typ == "kerze":
            start = random.randint(15, 30)
            r = random.uniform(0.5, 2.0)
            t_b = random.randint(1, 10)

            return {
                "titel": "Kerze brennt ab",
                "text": (
                    f"Eine Kerze ist zu Beginn **{start} cm** hoch. "
                    f"Sie brennt gleichmäßig um **{r:.1f} cm pro Stunde** ab.\n\n"
                    "a) Stelle die Funktionsgleichung für die Höhe auf."
                ),
                "f": f"f(t) = {start} - {r:.1f}·t",
                "b_text": f"b) Wie hoch ist die Kerze nach **{t_b} Stunden**?",
                "b_loesung": f"{start - r*t_b:.1f} cm",
                "c_text": "c) Wann ist die Kerze vollständig abgebrannt?",
                "c_loesung": f"t = {start}/{r:.1f} = **{start/r:.2f} h**",
            }


    # -------------------------------------------------------------
    # FUNKTION: WIRTSCHAFTSBEISPIEL GENERIEREN
    # -------------------------------------------------------------
    def generate_wirtschaft_example():
        produkte = [
            {"sing": "T-Shirt", "pl": "T-Shirts"},
            {"sing": "Notizbuch", "pl": "Notizbücher"},
            {"sing": "Trinkflasche", "pl": "Trinkflaschen"},
            {"sing": "Handyhülle", "pl": "Handyhüllen"},
            {"sing": "Schokoriegel", "pl": "Schokoriegel"},
        ]
        p = random.choice(produkte)

        # Deckungsbeitrag so wählen, dass Break-Even ein glattes Stück ist
        db = random.choice([5, 10, 15, 20])          # Deckungsbeitrag pro Stück
        kv = random.randrange(10, 51, 5)            # variable Kosten
        preis = kv + db                              # Verkaufspreis
        bep_stueck = random.randint(20, 80)         # Break-Even-Stückzahl
        miete = db * bep_stueck                     # Fixkosten = db * x_BE

        # Texte
        text = (
            f"Wir produzieren **{p['pl']}**.\n\n"
            f"Die Miete unserer Fabrik beträgt **{miete} €** pro Monat. "
            f"Zusätzlich entstehen Produktionskosten von **{kv} € pro Stück**.\n\n"
            "a) Stelle die Kostenfunktion **K(x)** für x produzierte Stück auf."
        )

        b_text = (
            f"b) Wir verkaufen unsere {p['pl']} zum Preis von **{preis} € pro Stück**.\n"
            "   Stelle die Erlösfunktion **E(x)** auf."
        )

        c_text = (
            "c) Stelle die Gewinnfunktion **G(x)** auf und berechne den "
            "Break-even-Point (Gewinnschwelle)."
        )

        # Funktionen
        K = f"K(x) = {miete} + {kv}·x   (in €)"
        E = f"E(x) = {preis}·x   (in €)"
        G = f"G(x) = E(x) − K(x) = ({preis} − {kv})·x − {miete} = {db}·x − {miete}"

        bep_text = (
            f"Break-even-Point:\n\n"
            f"{preis}·x = {miete} + {kv}·x\n"
            f"⇒ ({preis} − {kv})·x = {miete}\n"
            f"⇒ {db}·x = {miete}\n"
            f"⇒ x = {miete} / {db} = **{bep_stueck} Stück**.\n\n"
            "Ab dieser Produktions- und Verkaufsmenge wird erstmals Gewinn erzielt."
        )

        return {
            "titel": f"Wirtschaftsbeispiel: {p['pl']}",
            "text": text,
            "K": K,
            "b_text": b_text,
            "E": E,
            "c_text": c_text,
            "G": G,
            "bep": bep_text,
        }


    # -------------------------------------------------------------
    # TAB: ALLTAG
    # -------------------------------------------------------------
    with tab_alltag:
        st.header("Zufälliges Alltagsbeispiel")

        # State
        if "alltag" not in st.session_state:
            st.session_state["alltag"] = generate_alltag_example()
            st.session_state["a"] = False
            st.session_state["b"] = False
            st.session_state["c"] = False

        if st.button("🔄 Neues Alltagsbeispiel erzeugen"):
            st.session_state["alltag"] = generate_alltag_example()
            st.session_state["a"] = False
            st.session_state["b"] = False
            st.session_state["c"] = False

        bsp = st.session_state["alltag"]

        st.subheader(bsp["titel"])
        st.markdown(bsp["text"])

        if st.button("Lösung (a) – Funktionsgleichung"):
            st.session_state["a"] = True
        if st.session_state["a"]:
            st.markdown("**Lösung (a):** " + bsp["f"])
            st.write("---")
            st.markdown(bsp["b_text"])

        if st.session_state["a"] and st.button("Lösung (b) – Funktionswert"):
            st.session_state["b"] = True
        if st.session_state["b"]:
            st.markdown("**Lösung (b):** " + bsp["b_loesung"])
            st.write("---")
            st.markdown(bsp["c_text"])

        if st.session_state["b"] and st.button("Lösung (c) – Kontext / Nullstelle"):
            st.session_state["c"] = True
        if st.session_state["c"]:
            st.markdown("**Lösung (c):** " + bsp["c_loesung"])


    # -------------------------------------------------------------
    # TAB: WIRTSCHAFT
    # -------------------------------------------------------------
    with tab_wirtschaft:
        st.header("Zufälliges Wirtschaftsbeispiel (Kosten, Erlös, Gewinn)")

        # State
        if "wirt" not in st.session_state:
            st.session_state["wirt"] = generate_wirtschaft_example()
            st.session_state["w_a"] = False
            st.session_state["w_b"] = False
            st.session_state["w_c"] = False

        if st.button("🔄 Neues Wirtschaftsbeispiel erzeugen"):
            st.session_state["wirt"] = generate_wirtschaft_example()
            st.session_state["w_a"] = False
            st.session_state["w_b"] = False
            st.session_state["w_c"] = False

        wb = st.session_state["wirt"]

        st.subheader(wb["titel"])
        st.markdown(wb["text"])

        # (a) Kostenfunktion
        if st.button("Lösung (a) – Kostenfunktion K(x)"):
            st.session_state["w_a"] = True
        if st.session_state["w_a"]:
            st.markdown("**Lösung (a):** " + wb["K"])
            st.write("---")
            st.markdown(wb["b_text"])

        # (b) Erlösfunktion
        if st.session_state["w_a"] and st.button("Lösung (b) – Erlösfunktion E(x)"):
            st.session_state["w_b"] = True
        if st.session_state["w_b"]:
            st.markdown("**Lösung (b):** " + wb["E"])
            st.write("---")
            st.markdown(wb["c_text"])

        # (c) Gewinn + Break-even
        if st.session_state["w_b"] and st.button("Lösung (c) – Gewinn & Break-even"):
            st.session_state["w_c"] = True
        if st.session_state["w_c"]:
            st.markdown("**Lösung (c) – Gewinnfunktion:**")
            st.markdown(wb["G"])
            st.write("---")
            st.markdown("**Break-even-Point:**")
            st.markdown(wb["bep"])
