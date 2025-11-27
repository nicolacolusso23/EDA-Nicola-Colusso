# scripts/eda_years.py
import matplotlib.pyplot as plt
import pandas as pd
from utils_cleaning import classify_length, filter_finance, load_dataset, initial_cleaning, drop_unused_columns, deduplicate_imdb

# ============================
# FUNCIONES DE VISUALIZACIÓN
# ============================

def plot_movies_per_year(df):
    df_count_year = df.groupby("release_year").size().reset_index(name="movie_count")
    plt.figure(figsize=(12,6))
    plt.bar(df_count_year["release_year"], df_count_year["movie_count"], color="skyblue")
    plt.xlabel("Year")
    plt.ylabel("Number of Movies")
    plt.title("Movies Released per Year")
    plt.xticks(rotation=45)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()

def plot_movies_by_length(df):
    df["length_class"] = df["runtime"].apply(classify_length)
    df_length_year = df.groupby(["release_year", "length_class"]).size().reset_index(name="movie_count")
    df_pivot_length = df_length_year.pivot(index="release_year", columns="length_class", values="movie_count").fillna(0)

    plt.figure(figsize=(14,7))
    for col in df_pivot_length.columns:
        plt.plot(df_pivot_length.index, df_pivot_length[col], marker="o", label=col)
    plt.xlabel("Year")
    plt.ylabel("Number of Movies")
    plt.title("Movies by Length Class per Year")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title="Length Class")
    plt.tight_layout()
    plt.show()

def plot_finances(df):
    df_finance = filter_finance(df)
    df_finance_year = df_finance.groupby("release_year").agg(
        budget_sum=("budget", "sum"),
        revenue_sum=("revenue", "sum")
    ).reset_index()
    df_finance_year["profit"] = df_finance_year["revenue_sum"] - df_finance_year["budget_sum"]

    plt.figure(figsize=(14,7))
    plt.plot(df_finance_year["release_year"], df_finance_year["budget_sum"]/1e6, marker="o", label="Budget (M)")
    plt.plot(df_finance_year["release_year"], df_finance_year["revenue_sum"]/1e6, marker="o", label="Revenue (M)")
    plt.plot(df_finance_year["release_year"], df_finance_year["profit"]/1e6, marker="o", label="Profit (M)")
    plt.xlabel("Year")
    plt.ylabel("Amount (Million USD)")
    plt.title("Budget, Revenue and Profit per Year")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_avg_vote_per_year(df):
    df_filtered = df[df["vote_count"] != 0]
    percentil_75 = df_filtered["vote_count"].quantile(0.75)
    df_quant = df_filtered[df_filtered["vote_count"] > percentil_75].copy()
    df_quant["release_year"] = df_quant["release_date"].dt.year
    avg_vote_per_year = df_quant.groupby("release_year")["vote_average"].mean()

    plt.figure(figsize=(12,6))
    plt.plot(avg_vote_per_year.index, avg_vote_per_year.values, marker="o")
    plt.xlabel("Año de lanzamiento")
    plt.ylabel("Promedio de voto")
    plt.title("Promedio de voto por año (solo películas con alto número de votos)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ============================
# EJEMPLO DE USO
# ============================

if __name__ == "__main__":
    df_path = "/Users/nicolacolusso/Downloads/Data Science/test1001/data/TMDB_movie_dataset_v11.csv"
    df = load_dataset(df_path)
    df = initial_cleaning(df)
    df = drop_unused_columns(df)
    df = deduplicate_imdb(df)

    plot_movies_per_year(df)
    plot_movies_by_length(df)
    plot_finances(df)
    plot_avg_vote_per_year(df)
