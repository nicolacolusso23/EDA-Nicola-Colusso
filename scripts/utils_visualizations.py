
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def movies_per_year(df):
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






def movies_by_length_per_year(df):
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






def finances_per_year(df):

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






def movies_per_continent(df):
    df_exp = df.copy()
    df_exp = df_exp[df_exp["continent"].notna()]
    df_exp["continent"] = df_exp["continent"].astype(str).str.split(",").apply(lambda lst: [c.strip() for c in lst])
    df_exp = df_exp.explode("continent")

    movies_per_continent = df_exp["continent"].value_counts()
    
    movies_per_continent = movies_per_continent.sort_values(ascending=False)

    plt.figure(figsize=(10,6))
    movies_per_continent.plot(kind="bar", color="skyblue")
    plt.xlabel("Continent")
    plt.ylabel("Total movies")
    plt.title("Total number of films produced by continent")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()






def budget_vs_revenue_continent(df):
    df_exp = df.copy()
    df_exp = df_exp[df_exp["continent"].notna()]
    df_exp["continent"] = df_exp["continent"].astype(str).str.split(",").apply(lambda lst: [c.strip() for c in lst])
    df_exp = df_exp.explode("continent")

    df_exp["budget"] = pd.to_numeric(df_exp["budget"], errors="coerce")
    df_exp["revenue"] = pd.to_numeric(df_exp["revenue"], errors="coerce")

    budget_revenue_continent = df_exp.groupby("continent")[["budget", "revenue"]].sum()

    budget_revenue_continent = budget_revenue_continent.sort_values(by="budget", ascending=False)

    plt.figure(figsize=(12,7))
    budget_revenue_continent.plot(kind="bar", figsize=(12,7))
    plt.xlabel("Continent")
    plt.ylabel("USD Total")
    plt.title("Budget total vs Revenue total per continent")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()




def budget_vs_revenue_continent_relation(df):
    df_exp = df.copy()
    df_exp = df_exp[df_exp["continent"].notna()]
    df_exp["continent"] = (
        df_exp["continent"]
        .astype(str)
        .str.split(",")
        .apply(lambda lst: [c.strip() for c in lst])
    )
    df_exp = df_exp.explode("continent")

    df_exp["budget"] = pd.to_numeric(df_exp["budget"], errors="coerce")
    df_exp["revenue"] = pd.to_numeric(df_exp["revenue"], errors="coerce")

    budget_revenue_continent = df_exp.groupby("continent")[["budget", "revenue"]].sum()

    budget_revenue_continent["ratio"] = (
        budget_revenue_continent["revenue"] / budget_revenue_continent["budget"]
    )

    budget_revenue_continent = budget_revenue_continent.sort_values(by="ratio", ascending=False)

    plt.figure(figsize=(10,6))
    budget_revenue_continent["ratio"].plot(kind="bar")
    plt.xlabel("Continent")
    plt.ylabel("Revenue / Budget")
    plt.title("Ratio revenue/budget per continent")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()








def avg_vote_per_genere(df):

    df_filtered = df[df['vote_count'] > 0].copy()
    
    df_filtered = df_filtered[df_filtered['genres'].notna()]
    
    df_exploded = df_filtered.assign(genres=df_filtered['genres'].str.split(',')).explode('genres')
    
    df_exploded['genres'] = df_exploded['genres'].str.strip()
    
    median_order = df_exploded.groupby('genres')['vote_average'].median().sort_values(ascending=False).index
    
    plt.figure(figsize=(12,6))
    sns.boxplot(x='genres', y='vote_average', data=df_exploded, order=median_order)
    plt.xticks(rotation=45, ha='right')
    plt.title('Distribution of vote average by genre')
    plt.xlabel('genre')
    plt.ylabel('Vote Average')
    plt.tight_layout()
    plt.show()