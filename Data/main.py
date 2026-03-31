from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_dataset(filename: str) -> pd.DataFrame:
    # Resolve project root (.. from Data/) and the dataset folder
    project_root = Path(__file__).resolve().parent.parent
    dataset_dir = project_root / "dataset"

    if not dataset_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta dataset en: {dataset_dir}")

    csv_path = dataset_dir / filename
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")

    return pd.read_csv(csv_path)


def exploratory_analysis(df: pd.DataFrame) -> None:
    print("Vista rápida (primeras 5 filas):")
    print(df.head(5))
    print()

    print("Dimensiones del dataset:")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    print()

    print("Nombres de columnas:")
    print(list(df.columns))
    print()

    print("Tipos de datos y nulos:")
    print(df.info())
    print()

    print("Valores nulos por columna:")
    print(df.isna().sum())
    print()

    print("Resumen estadístico (solo numéricas):")
    print(df.describe())


def plot_top_10_songs(df: pd.DataFrame, output_dir: Path) -> None:
    top10 = df.sort_values("total_streams_billions", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(top10["song_title"], top10["total_streams_billions"])
    plt.gca().invert_yaxis()
    plt.title("Top 10 canciones más escuchadas")
    plt.xlabel("Total streams (billions)")
    plt.ylabel("Song title")
    plt.tight_layout()

    output_path = output_dir / "top_10_canciones_mas_escuchadas.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"Grafico guardado en: {output_path}")


def plot_genre_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    genre_counts = df["primary_genre"].value_counts()

    plt.figure(figsize=(10, 6))
    plt.bar(genre_counts.index, genre_counts.values)
    plt.title("Distribucion de generos en el Top 100")
    plt.xlabel("Primary genre")
    plt.ylabel("Cantidad de canciones")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = output_dir / "distribucion_generos_top100.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"Grafico guardado en: {output_path}")


def main():
    filename = "spotify_alltime_top100_songs.csv"
    df = load_dataset(filename)
    exploratory_analysis(df)

    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    plot_top_10_songs(df, output_dir)
    plot_genre_distribution(df, output_dir)


if __name__ == "__main__":
    main()
