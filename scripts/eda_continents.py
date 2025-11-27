# scripts/eda_continents.py
import matplotlib.pyplot as plt
import pandas as pd
from utils_cleaning import load_dataset, initial_cleaning, drop_unused_columns, deduplicate_imdb

# ============================
# FUNCIONES PARA CONTINENTES
# ============================

country_to_continent = {
    "United States of America": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Brazil": "South America",
    "Argentina": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Peru": "South America",
    "United Kingdom": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Spain": "Europe",
    "Italy": "Europe",
    "Belgium": "Europe",
    "Netherlands": "Europe",
    "Russia": "Europe",
    "Czech Republic": "Europe",
    "Denmark": "Europe",
    "Norway": "Europe",
    "Sweden": "Europe",
    "Switzerland": "Europe",
    "Portugal": "Europe",
    "Austria": "Europe",
    "Poland": "Europe",
    "China": "Asia",
    "Japan": "Asia",
    "India": "Asia",
    "Hong Kong": "Asia",
    "South Korea": "Asia",
    "Taiwan": "Asia",
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "South Africa": "Africa",
    "Morocco": "Africa"
}

def prepare_continent_df(df):
    df["production_countries"] = df["production_countries"].astype(str)
    df_countries = (
        df.assign(production_countries=df["production_countries"].str.split(", "))
          .explode("production_countries")
    )
    df_countries["continent"] = df_countries["production_countries"].map(country_to_continent)
    df_cont = df_countries[df_countries["continent"].notna()].copy()
    return df_cont

def map_countries_to_continent(df):
    df["production_countries"] = df["production_countries"].astype(str)
    df_countries = (
        df.assign(production_countries=df["production_countries"].str.split(", "))
          .explode("production_countries")
    )
    df_countries["continent"] = df_countries["production_countries"].map(country_to_continent)
    df_cont = df_countries[df_countries["continent"].notna()].copy()
    return df_cont

def plot_movies_per_continent(df_cont):
    movies_per_continent = df_cont["continent"].value_counts()
    plt.figure(figsize=(10,6))
    movies_per_continent.plot(kind="bar", color="skyblue")
    plt.xlabel("Continente")
    plt.ylabel("Total películas")
    plt.title("Total de películas producidas por continente")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_budget_vs_revenue_continent(df_cont):
    df_fin = df_cont.copy()
    df_fin["budget"] = pd.to_numeric(df_fin["budget"], errors="coerce")
    df_fin["revenue"] = pd.to_numeric(df_fin["revenue"], errors="coerce")

    budget_revenue_continent = df_fin.groupby("continent")[["budget", "revenue"]].sum()
    plt.figure(figsize=(12,7))
    budget_revenue_continent.plot(kind="bar", figsize=(12,7))
    plt.xlabel("Continente")
    plt.ylabel("USD Totales")
    plt.title("Budget total vs Revenue total por continente")
    plt.grid(axis="y", alpha=0.3)
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

    df_cont = map_countries_to_continent(df)
    plot_movies_per_continent(df_cont)
    plot_budget_vs_revenue_continent(df_cont)
