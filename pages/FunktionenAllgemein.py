import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt

tab1 = st.tabs(["Besondere Punkte"])

x = np.linspace(-10,10)
y = .5*x**2+2*x+1


# Koordinatensystem erstellen
fig, ax = plt.subplots()


# Achsenbeschriftungen
ax.set_xlabel("x", 'right')
ax.set_ylabel("f(x)", 'top')
# Achsenbereiche
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)  # gleicher Bereich in y, damit 1:1 sichtbar wird
# Verhältnis fixieren: 1 Einheit x = 1 Einheit y
ax.set_aspect("equal", adjustable="box")
# Hauptticks alle 5, feines Gitter alle 1
ax.set_xticks(range(-10, 11, 5))
ax.set_yticks(range(-10, 11, 5))
ax.set_xticks(np.arange(-10, 11, 1), minor=True)
ax.set_yticks(np.arange(-10, 11, 1), minor=True)
# Gitterlinien
ax.grid(which="major", color="grey", linestyle="-", linewidth=0.8)
ax.grid(which="minor", color="lightgrey", linestyle="--", linewidth=0.5)
# Achsen durch Ursprung
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
ax.spines["left"].set_position("zero")
ax.spines["bottom"].set_position("zero")

ax.plot(x,y)




# Graph auf Streamlit ausgeben
st.write(fig)