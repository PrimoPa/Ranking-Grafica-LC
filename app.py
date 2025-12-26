import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Radar Ranking", layout="wide")

axes = [
    "Tiempo en comunidad",
    "Sniper",
    "Automáticas",
    "Trabajo en equipo",
    "Uso del mapa"
]

def radar_chart(values, title, ax, color):
    angles = np.linspace(0, 2*np.pi, len(values), endpoint=False)
    values = values + values[:1]
    angles = np.append(angles, angles[0])

    ax.set_theta_offset(np.pi / 2)   # ⬆️ eje inicial arriba
    ax.set_theta_direction(-1)       # ↻ sentido horario

    ax.plot(angles, values, color=color, linewidth=2, alpha=0.85)
    ax.fill(angles, values, color=color, alpha=0.20)

    ax.set_thetagrids(angles[:-1] * 180/np.pi, axes)
    ax.set_ylim(0, 10)
    ax.set_title(title, size=12)


if "players" not in st.session_state:
    st.session_state.players = []

st.title("🏆 Ranking – Radar Charts (0 a 10)")

with st.sidebar:
    st.header("Agregar / Editar jugador")

    player_names = ["Nuevo jugador"] + [
        p["name"] for p in st.session_state.players
    ]

    selected_preset = st.selectbox(
        "Preset / Jugador existente",
        player_names
    )

    if selected_preset != "Nuevo jugador":
        preset = next(
            p for p in st.session_state.players
            if p["name"] == selected_preset
        )

        name = st.text_input("Nombre", preset["name"])
        stats = []

        for i, axis in enumerate(axes):
            stats.append(
                st.slider(axis, 0, 10, preset["stats"][i])
            )

    else:
        name = st.text_input("Nombre")
        stats = []

        for axis in axes:
            stats.append(
                st.slider(axis, 0, 10, 5)
            )

    if st.button("Agregar al ranking"):
        if name:
            st.session_state.players.append({
                "name": name,
                "stats": stats
            })

cols = st.columns(3)

for i, p in enumerate(st.session_state.players):
    with cols[i % 3]:
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        radar_chart(p["stats"], p["name"], ax, "#C85A2E")
        st.pyplot(fig)

st.divider()
st.subheader("🆚 Comparación directa")

names = [p["name"] for p in st.session_state.players]

selected = st.multiselect(
    "Seleccioná jugadores para comparar",
    names,
    default=names[:2]
)

if len(selected) >= 2:
    fig, ax = plt.subplots(subplot_kw=dict(polar=True))

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 10)

    colors = ["#C85A2E", "#2E6AC8", "#2EC87A", "#C82EC8", "#C8B52E"]

    for i, name in enumerate(selected):
        player = next(p for p in st.session_state.players if p["name"] == name)
        radar_chart(
            player["stats"],
            player["name"],
            ax,
            colors[i % len(colors)]
        )

    st.pyplot(fig)
else:
    st.info("Seleccioná al menos 2 jugadores para comparar")

    st.divider()
    
st.subheader("🗑️ Eliminar jugador")

if st.session_state.players:
    delete_name = st.selectbox(
        "Seleccioná jugador",
        [p["name"] for p in st.session_state.players]
    )

    if st.button("Eliminar jugador"):
        st.session_state.players = [
            p for p in st.session_state.players if p["name"] != delete_name
        ]
        st.experimental_rerun()

if st.button("Guardar cambios"):
    for p in st.session_state.players:
        if p["name"] == selected_preset:
            p["stats"] = stats
    st.experimental_rerun()


