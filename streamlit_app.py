from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


@st.cache_data
def load_dataset() -> pd.DataFrame:
    project_root = Path(__file__).resolve().parent
    csv_path = project_root / "dataset" / "spotify_alltime_top100_songs.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")
    return pd.read_csv(csv_path)


def plot_top_10_songs(df: pd.DataFrame):
    top10 = df.sort_values("total_streams_billions", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top10,
        x="total_streams_billions",
        y="song_title",
        ax=ax,
        color="#2a9d8f",
    )
    ax.invert_yaxis()
    ax.set_title("Top 10 canciones mas escuchadas")
    ax.set_xlabel("Total streams (billions)")
    ax.set_ylabel("Song title")
    fig.tight_layout()
    return fig


def plot_genre_distribution(df: pd.DataFrame):
    genre_counts = df["primary_genre"].value_counts().reset_index()
    genre_counts.columns = ["primary_genre", "count"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=genre_counts,
        x="primary_genre",
        y="count",
        ax=ax,
        color="#264653",
    )
    ax.set_title("Distribucion de generos en el Top 100")
    ax.set_xlabel("Primary genre")
    ax.set_ylabel("Cantidad de canciones")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def plot_evolution_by_year(df: pd.DataFrame):
    year_counts = (
        df.groupby("release_year")["song_title"]
        .count()
        .reset_index(name="count")
        .sort_values("release_year")
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=year_counts,
        x="release_year",
        y="count",
        marker="o",
        ax=ax,
        color="#e76f51",
    )
    ax.set_title("Evolucion de canciones por ano")
    ax.set_xlabel("Release year")
    ax.set_ylabel("Cantidad de canciones")
    fig.tight_layout()
    return fig


def main():
    st.set_page_config(
        page_title="Spotify Top 100 - Exploracion",
        layout="wide",
    )

    st.title("Spotify All-Time Top 100 - Exploracion")
    st.write(
        "Dashboard simple para ver el Top 10 de canciones mas escuchadas y la "
        "distribucion de generos en el Top 100."
    )

    df = load_dataset()

    sns.set_theme(style="whitegrid")

    st.sidebar.title("Filtros")
    genres = sorted(df["primary_genre"].dropna().unique().tolist())
    selected_genres = st.sidebar.multiselect(
        "Genero",
        options=genres,
        default=genres,
    )

    min_year = int(df["release_year"].min())
    max_year = int(df["release_year"].max())
    selected_years = st.sidebar.slider(
        "Rango de anos",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

    explicit_options = ["Todos", "Solo explicitas", "Solo no explicitas"]
    selected_explicit = st.sidebar.selectbox("Contenido explicito", explicit_options)

    filtered = df[
        (df["primary_genre"].isin(selected_genres))
        & (df["release_year"].between(selected_years[0], selected_years[1]))
    ].copy()

    if selected_explicit == "Solo explicitas":
        filtered = filtered[filtered["explicit"] == True]
    elif selected_explicit == "Solo no explicitas":
        filtered = filtered[filtered["explicit"] == False]

    st.subheader("Vista rapida del dataset")
    st.dataframe(filtered.head(10), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 canciones mas escuchadas")
        st.pyplot(plot_top_10_songs(filtered), clear_figure=True)

    with col2:
        st.subheader("Distribucion de generos")
        st.pyplot(plot_genre_distribution(filtered), clear_figure=True)

    st.subheader("Storytelling: evolucion por ano")
    st.write(
        "Este grafico muestra como se distribuyen las canciones del Top 100 "
        "segun su ano de lanzamiento. Usa los filtros para ver cambios por "
        "genero, rango de anos y contenido explicito."
    )
    st.pyplot(plot_evolution_by_year(filtered), clear_figure=True)

    st.subheader("Conclusiones")
    st.write(
        "Insights rapidos:\n"
        "- El Top 10 concentra una gran parte de los streams totales, lo que "
        "sugiere un liderazgo claro de pocos hits.\n"
        "- La distribucion de generos permite ver si el Top 100 esta dominado "
        "por un estilo o si hay diversidad.\n"
        "- La evolucion por ano ayuda a detectar periodos con mayor presencia "
        "de lanzamientos en el ranking.\n"
        "Ajusta los filtros para validar estos patrones en segmentos especificos."
    )


if __name__ == "__main__":
    main()
