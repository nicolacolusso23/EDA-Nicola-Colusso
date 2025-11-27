import pandas as pd
import matplotlib.pyplot as plt


# 1. CARGA DEL DATASET

df = pd.read_csv("/Users/nicolacolusso/Downloads/Data Science/test1001/data/TMDB_movie_dataset_v11.csv")


# 2. LIMPIEZA INICIAL

df = df[df["imdb_id"].notna()]
df = df[df["release_date"].notna()]
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

df = df[(df["release_date"].dt.year >= 1900) & (df["release_date"].dt.year <= 2025)]
df = df[df["status"] == "Released"]


# 3. ELIMINAR COLUMNAS INÚTILES

cols_to_drop = [
    'id', 'status', 'backdrop_path', 'homepage', 'overview',
    'poster_path', 'tagline', 'keywords'
]
df = df.drop(columns=cols_to_drop, errors="ignore")


# 4. DEDUPLICAR POR imdb_id

df["n_nulls"] = df.isna().sum(axis=1)
df = df.sort_values(by=["imdb_id", "n_nulls"], ascending=[True, True])
df = df.drop_duplicates(subset="imdb_id", keep="first")
df = df.drop(columns="n_nulls")

df["release_year"] = df["release_date"].dt.year
df["release_month"] = df["release_date"].dt.month


# 5. GRAFICO 1: PELÍCULAS POR MES

df = df[~((df["release_date"].dt.day == 1) & (df["release_date"].dt.month == 1))]

df["release_month"] = df["release_date"].dt.month

movies_per_month = df.groupby("release_month").size()

plt.figure(figsize=(12,6))
plt.bar(movies_per_month.index, movies_per_month.values)
plt.xlabel("Mes")
plt.ylabel("Número de películas")
plt.title("Películas lanzadas por mes (sin fechas del 1 de enero)")
plt.xticks(range(1,13))
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()



# 6. MAPA PAÍS A CONTINENTE

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

df["production_countries"] = df["production_countries"].astype(str)
df_countries = (
    df.assign(production_countries=df["production_countries"].str.split(", "))
      .explode("production_countries")
)

df_countries["continent"] = df_countries["production_countries"].map(country_to_continent)
df_cont = df_countries[df_countries["continent"].notna()].copy()


# 7. GRAFICO 2: TOTAL DE PELÍCULAS POR CONTINENTE

movies_per_continent = df_cont["continent"].value_counts()

plt.figure(figsize=(10,6))
movies_per_continent.plot(kind="bar", color="skyblue")
plt.xlabel("Continente")
plt.ylabel("Total películas")
plt.title("Total de películas producidas por continente")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()


# 8. GRAFICO 3: BUDGET vs REVENUE POR CONTINENTE

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
