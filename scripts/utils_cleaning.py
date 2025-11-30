import pandas as pd


def analize(df):

    print("Dimensiones del dataset:", df.shape)
    print("-"*80)

    print("\nTipos de datos por columna y número de non-nulos:")
    df.info()
    print("-"*80)

    print("\nNúmero de duplicados:", df.duplicated().sum())
    print("-"*80)

    print("\nValores únicos por columna:")
    for col in df.columns:
        uniques = df[col].unique()
        num_uniques = len(uniques)

        print(f"\n--- {col} ---")
        print(f"Cantidad de valores únicos: {num_uniques}")

        if num_uniques > 20:
            print("Primeros 20 valores:", uniques[:20])
        else:
            print("Valores:", uniques)

    print("-"*80)







def cleaning(df):
    
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df[(df["release_date"].dt.year >= 1900) & (df["release_date"].dt.year <= 2025)]

    df = df[df["status"] == "Released"]

    if "adult" in df.columns and "genres" in df.columns:
        df["genres"] = df.apply(
            lambda row: "Adult" if row["adult"] == True else row["genres"],
            axis=1
        )

    df["n_nulls"] = df.isna().sum(axis=1)
    df = df.sort_values(by=["title", "n_nulls"], ascending=[True, True])
    df = df.drop_duplicates(subset="title", keep="first")
    df = df.drop(columns="n_nulls")

    popularity_25 = df["popularity"].quantile(0.25)
    df = df[df["popularity"] >= popularity_25]

    df = df[~((df["budget"] == 0) & (df["revenue"] == 0))].copy()

    return df










def drop_columns(df):
    cols_to_drop = [
        'id', 'status', 'adult', 'backdrop_path', 'production_companies', 'spoken_languages', 'original_language' 'homepage', 'overview',
        'poster_path', 'tagline', 'keywords','original_title', 'imdb_id', 'homepage'
    ]
    return df.drop(columns=cols_to_drop, errors="ignore")










country_to_continent = {
    # África
    "Algeria": "Africa",
    "Angola": "Africa",
    "Benin": "Africa",
    "Botswana": "Africa",
    "Burkina Faso": "Africa",
    "Burundi": "Africa",
    "Cameroon": "Africa",
    "Cape Verde": "Africa",
    "Central African Republic": "Africa",
    "Chad": "Africa",
    "Comoros": "Africa",
    "Congo": "Africa",
    "Djibouti": "Africa",
    "Egypt": "Africa",
    "Equatorial Guinea": "Africa",
    "Eritrea": "Africa",
    "Ethiopia": "Africa",
    "Gabon": "Africa",
    "Gambia": "Africa",
    "Ghana": "Africa",
    "Guinea": "Africa",
    "Guinea-Bissau": "Africa",
    "Ivory Coast": "Africa",
    "Kenya": "Africa",
    "Lesotho": "Africa",
    "Liberia": "Africa",
    "Libya": "Africa",
    "Madagascar": "Africa",
    "Malawi": "Africa",
    "Mali": "Africa",
    "Mauritania": "Africa",
    "Mauritius": "Africa",
    "Morocco": "Africa",
    "Mozambique": "Africa",
    "Namibia": "Africa",
    "Niger": "Africa",
    "Nigeria": "Africa",
    "Rwanda": "Africa",
    "Sao Tome and Principe": "Africa",
    "Senegal": "Africa",
    "Seychelles": "Africa",
    "Sierra Leone": "Africa",
    "Somalia": "Africa",
    "South Africa": "Africa",
    "South Sudan": "Africa",
    "Sudan": "Africa",
    "Tanzania": "Africa",
    "Togo": "Africa",
    "Tunisia": "Africa",
    "Uganda": "Africa",
    "Zambia": "Africa",
    "Zimbabwe": "Africa",
    # Asia
    "Afghanistan": "Asia",
    "Armenia": "Asia",
    "Azerbaijan": "Asia",
    "Bahrain": "Asia",
    "Bangladesh": "Asia",
    "Bhutan": "Asia",
    "Brunei Darussalam": "Asia",
    "Cambodia": "Asia",
    "China": "Asia",
    "East Timor": "Asia",
    "Georgia": "Asia",
    "Hong Kong": "Asia",
    "India": "Asia",
    "Indonesia": "Asia",
    "Iran": "Asia",
    "Iraq": "Asia",
    "Israel": "Asia",
    "Japan": "Asia",
    "Jordan": "Asia",
    "Kazakhstan": "Asia",
    "Kuwait": "Asia",
    "Kyrgyz Republic": "Asia",
    "Lao People's Democratic Republic": "Asia",
    "Lebanon": "Asia",
    "Malaysia": "Asia",
    "Maldives": "Asia",
    "Mongolia": "Asia",
    "Myanmar": "Asia",
    "Nepal": "Asia",
    "North Korea": "Asia",
    "Oman": "Asia",
    "Pakistan": "Asia",
    "Palestinian Territory": "Asia",
    "Philippines": "Asia",
    "Qatar": "Asia",
    "Saudi Arabia": "Asia",
    "Singapore": "Asia",
    "South Korea": "Asia",
    "Sri Lanka": "Asia",
    "Syria": "Asia",
    "Taiwan": "Asia",
    "Tajikistan": "Asia",
    "Thailand": "Asia",
    "Timor-Leste": "Asia",
    "Turkmenistan": "Asia",
    "United Arab Emirates": "Asia",
    "Uzbekistan": "Asia",
    "Vietnam": "Asia",
    "Yemen": "Asia",
    # Europa
    "Albania": "Europe",
    "Andorra": "Europe",
    "Austria": "Europe",
    "Belarus": "Europe",
    "Belgium": "Europe",
    "Bosnia and Herzegovina": "Europe",
    "Bulgaria": "Europe",
    "Croatia": "Europe",
    "Czech Republic": "Europe",
    "Denmark": "Europe",
    "Estonia": "Europe",
    "Finland": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Greece": "Europe",
    "Hungary": "Europe",
    "Iceland": "Europe",
    "Ireland": "Europe",
    "Italy": "Europe",
    "Kosovo": "Europe",
    "Latvia": "Europe",
    "Liechtenstein": "Europe",
    "Lithuania": "Europe",
    "Luxembourg": "Europe",
    "Macedonia": "Europe",
    "Malta": "Europe",
    "Moldova": "Europe",
    "Monaco": "Europe",
    "Montenegro": "Europe",
    "Netherlands": "Europe",
    "Norway": "Europe",
    "Poland": "Europe",
    "Portugal": "Europe",
    "Romania": "Europe",
    "Russia": "Europe",
    "San Marino": "Europe",
    "Serbia": "Europe",
    "Slovakia": "Europe",
    "Slovenia": "Europe",
    "Spain": "Europe",
    "Sweden": "Europe",
    "Switzerland": "Europe",
    "United Kingdom": "Europe",
    "Vatican": "Europe",
    # Norteamérica
    "United States of America": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Greenland": "North America",
    "Bermuda": "North America",
    "Cayman Islands": "North America",
    "Costa Rica": "North America",
    "El Salvador": "North America",
    "Guatemala": "North America",
    "Honduras": "North America",
    "Jamaica": "North America",
    "Panama": "North America",
    "Puerto Rico": "North America",
    "Saint Kitts and Nevis": "North America",
    "Saint Lucia": "North America",
    "Saint Pierre and Miquelon": "North America",
    "Trinidad and Tobago": "North America",
    "US Virgin Islands": "North America",
    # Sudamérica
    "Argentina": "South America",
    "Brazil": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Peru": "South America",
    "Venezuela": "South America",
    "Suriname": "South America",
    "Guyana": "South America",
    "Bolivia": "South America",
    # Oceanía
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "Fiji": "Oceania",
    "Papua New Guinea": "Oceania",
    "Solomon Islands": "Oceania",
    "Tonga": "Oceania",
    "Vanuatu": "Oceania",
    "Samoa": "Oceania",
}

def add_columns(df, country_col="production_countries", runtime_col="runtime"):

    df["release_year"] = df["release_date"].dt.year

    def countries_to_continent(countries):
        if pd.isna(countries):
            return pd.NA  

        countries_list = [c.strip() for c in str(countries).split(",")]
        continents = set()

        for c in countries_list:
            cont = country_to_continent.get(c)
            if cont:
                continents.add(cont)

        if not continents:
            return pd.NA 

        return ", ".join(sorted(continents))

    df["continent"] = df[country_col].apply(countries_to_continent)

    def classify_length(mins):
        if pd.isna(mins):
            return pd.NA
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

    df["length_class"] = df[runtime_col].apply(classify_length)

    return df
