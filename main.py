
import os
import requests
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GITHUB_API = "https://api.github.com/search/repositories"
EARTHQUAKE_API = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/"
    "summary/all_day.geojson"
)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Python-REST-API-Geospatial-Visualizer"
}


# --------------------------------------------------
# 2. FETCH GITHUB DATA
# --------------------------------------------------

def fetch_github_repositories():
    print("Fetching GitHub repository data...")

    params = {
        "q": "language:python",
        "sort": "stars",
        "order": "desc",
        "per_page": 30
    }

    response = requests.get(
        GITHUB_API,
        params=params,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    repositories = []

    for repo in data.get("items", []):
        repositories.append({
            "name": repo.get("full_name"),
            "owner": repo.get("owner", {}).get("login"),
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language"),
            "description": repo.get("description"),
            "url": repo.get("html_url")
        })

    df = pd.DataFrame(repositories)

    if not df.empty:
        df["stars"] = pd.to_numeric(
            df["stars"], errors="coerce"
        )
        df = df.dropna(subset=["name", "stars"])
        df["stars"] = df["stars"].astype(int)
        df = df.sort_values("stars", ascending=False)

    df.to_csv(
        os.path.join(OUTPUT_DIR, "github_repositories.csv"),
        index=False
    )

    print(f"GitHub repositories collected: {len(df)}")
    return df


# --------------------------------------------------
# 3. FETCH EARTHQUAKE DATA
# --------------------------------------------------

def fetch_earthquake_data():
    print("Fetching earthquake GeoJSON data...")

    response = requests.get(
        EARTHQUAKE_API,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    earthquakes = []

    for feature in data.get("features", []):
        properties = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        coordinates = geometry.get("coordinates") or []

        # GeoJSON point coordinates:
        # [longitude, latitude, depth in km]
        if len(coordinates) < 2:
            continue

        longitude = coordinates[0]
        latitude = coordinates[1]
        depth = coordinates[2] if len(coordinates) > 2 else None

        if latitude is None or longitude is None:
            continue

        earthquakes.append({
            "magnitude": properties.get("mag"),
            "place": properties.get("place") or "Unknown",
            "time": properties.get("time"),
            "url": properties.get("url"),
            "longitude": longitude,
            "latitude": latitude,
            "depth_km": depth
        })

    df = pd.DataFrame(earthquakes)

    if not df.empty:
        df["magnitude"] = pd.to_numeric(
            df["magnitude"], errors="coerce"
        )
        df["latitude"] = pd.to_numeric(
            df["latitude"], errors="coerce"
        )
        df["longitude"] = pd.to_numeric(
            df["longitude"], errors="coerce"
        )
        df["depth_km"] = pd.to_numeric(
            df["depth_km"], errors="coerce"
        )

        df = df.dropna(
            subset=["magnitude", "latitude", "longitude"]
        )

        df["time"] = pd.to_datetime(
            df["time"], unit="ms", utc=True, errors="coerce"
        )

        df = df.dropna(subset=["time"])

    df.to_csv(
        os.path.join(OUTPUT_DIR, "earthquakes.csv"),
        index=False
    )

    print(f"Earthquake records collected: {len(df)}")
    return df


# --------------------------------------------------
# 4. CREATE GITHUB RANKING CHART
# --------------------------------------------------

def create_github_chart(df):
    if df.empty:
        print("No GitHub data available for the chart.")
        return

    chart_df = df.head(15).sort_values("stars")

    fig = px.bar(
        chart_df,
        x="stars",
        y="name",
        orientation="h",
        color="stars",
        hover_data=["owner", "language", "description"],
        title="Top Python GitHub Repositories by Stars",
        labels={
            "stars": "Number of Stars",
            "name": "Repository",
            "owner": "Owner",
            "language": "Language"
        }
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Repository",
        xaxis_title="Stars",
        height=650
    )

    fig.write_html(
        os.path.join(OUTPUT_DIR, "github_dashboard.html")
    )


# --------------------------------------------------
# 5. CREATE EARTHQUAKE WORLD MAP
# --------------------------------------------------

def create_earthquake_map(df):
    if df.empty:
        print("No earthquake data available for the map.")
        return

    df = df.copy()

    # Use a minimum marker size for visibility.
    df["marker_size"] = df["magnitude"].clip(lower=0.5)

    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        size="marker_size",
        color="magnitude",
        hover_name="place",
        hover_data={
            "magnitude": True,
            "depth_km": True,
            "time": True,
            "latitude": True,
            "longitude": True,
            "marker_size": False
        },
        color_continuous_scale="Turbo",
        projection="natural earth",
        title="Earthquakes Around the World — Past Day"
    )

    fig.update_layout(
        template="plotly_white",
        height=700
    )

    fig.write_html(
        os.path.join(OUTPUT_DIR, "earthquake_map.html")
    )


# --------------------------------------------------
# 6. RUN THE PIPELINE
# --------------------------------------------------

def main():
    try:
        github_df = fetch_github_repositories()
        earthquake_df = fetch_earthquake_data()

        create_github_chart(github_df)
        create_earthquake_map(earthquake_df)

        print("\nPipeline completed.")
        print("Check the output folder for CSV and HTML files.")

    except requests.RequestException as error:
        print(f"API/network error: {error}")

    except (ValueError, KeyError) as error:
        print(f"Data processing error: {error}")


if __name__ == "__main__":
    main()
