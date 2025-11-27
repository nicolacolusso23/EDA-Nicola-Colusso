# scripts/utils_cleaning.py
import pandas as pd

# ============================
# FUNCIONES DE LIMPIEZA
# ============================

def load_dataset(path):
    """Carga el dataset CSV en un DataFrame"""
    return pd.read_csv(path)

def initial_cleaning(df):
    """Filtra filas nulas y convierte release_date a datetime"""
    df = df[df["imdb_id"].notna()]
    df = df[df["release_date"].notna()]
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df[(df["release_date"].dt.year >= 1900) & (df["release_date"].dt.year <= 2025)]
    df = df[df["status"] == "Released"]
    return df

def drop_unused_columns(df):
    """Elimina columnas que no se usan"""
    cols_to_drop = [
        'id', 'status', 'backdrop_path', 'homepage', 'overview',
        'poster_path', 'tagline', 'keywords'
    ]
    return df.drop(columns=cols_to_drop, errors="ignore")

def deduplicate_imdb(df):
    """Elimina duplicados por imdb_id, priorizando filas con menos nulos"""
    df["n_nulls"] = df.isna().sum(axis=1)
    df = df.sort_values(by=["imdb_id", "n_nulls"], ascending=[True, True])
    df = df.drop_duplicates(subset="imdb_id", keep="first")
    df = df.drop(columns="n_nulls")
    df["release_year"] = df["release_date"].dt.year
    df["release_month"] = df["release_date"].dt.month
    return df

def classify_length(mins):
    """Clasifica la duración de la película"""
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

def filter_finance(df):
    """Filtra películas con budget=0 y revenue=0"""
    return df[~((df["budget"] == 0) & (df["revenue"] == 0))].copy()
