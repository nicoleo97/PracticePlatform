import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

tab1 = st.tabs(["Besondere Punkte"])

x = np.linspace(-5,5)
y = .5*x**2+2*x+1


# Koordinatensystem erstellen
fig, ax = plt.subplots()

ax.spines["left"].set_position("zero")
ax.spines["bottom"].set_position("zero")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(True, which='both',linewidth=.5, color='lightgray')
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.grid(True, which='minor', linestyle=':', linewidth=0.5)
ax.yaxis.set_minor_locator(MultipleLocator(1))


ax.plot(x,y)




# Graph auf Streamlit ausgeben
st.pyplot(fig)