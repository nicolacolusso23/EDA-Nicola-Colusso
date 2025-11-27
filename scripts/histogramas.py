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



# HISTOGRAMA 1: Películas por año

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



# HISTOGRAMA 2: Duración por categorías

def classify_length(mins):
    if mins < 5:
        return "Micro-short"
    elif mins < 40:
        return "Short Film"
    elif mins < 60:
        return "Medium-length Film"
    elif mins < 120:
        return "Feature Film"
    elif mins < 180:
        return "Extended Feature"
    elif mins < 240:
        return "Ultra-long Film"
    else:
        return "Extremely Long Film"

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



# HISTOGRAMA 3: Finanzas (solo filtrando budget=0 & revenue=0)

df_finance = df[~((df["budget"] == 0) & (df["revenue"] == 0))].copy()

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



# HISTOGRAMA 4: Promedio de voto por año (vote_count > percentil 75)


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
