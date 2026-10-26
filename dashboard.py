
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# TECTONIC - OPEN DATA INTELLIGENCE
# ==========================================

st.set_page_config(
    page_title="TECTONIC | Open Data Intelligence",
    page_icon="🌐",
    layout="wide"
)

# ==========================================
# DARK UI DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #080D18;
    color: #F1F5F9;
}

[data-testid="stHeader"] {
    background-color: #080D18;
}

[data-testid="stSidebar"] {
    background-color: #101A2B;
}

[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}

h1, h2, h3, h4, p, label, li {
    color: #F1F5F9;
}

.stMarkdown, .stCaption {
    color: #D5DEEA;
}

[data-testid="stMetric"] {
    background-color: #142238;
    border: 1px solid #30435E;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #D5DEEA !important;
}

[data-testid="stMetricValue"] {
    color: #54D6FF !important;
}

[data-testid="stMetricDelta"] {
    color: #62E6B5 !important;
}

div[data-baseweb="select"] > div {
    background-color: #142238;
    color: #FFFFFF;
}

input, textarea {
    color: #FFFFFF !important;
}

.stTextInput label,
.stMultiSelect label,
.stSelectbox label,
.stSlider label {
    color: #FFFFFF !important;
}

.stButton button,
.stDownloadButton button {
    background-color: #17334A;
    color: #FFFFFF;
    border: 1px solid #54D6FF;
    border-radius: 8px;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background-color: #20516B;
    color: #FFFFFF;
    border: 1px solid #54D6FF;
}

hr {
    border-color: #30435E;
}

[data-testid="stDataFrame"] {
    border: 1px solid #30435E;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD DATA
# ==========================================

DATA_FOLDER = Path("output")
GITHUB_FILE = DATA_FOLDER / "github_repositories.csv"
EARTHQUAKE_FILE = DATA_FOLDER / "earthquakes.csv"


def load_csv(file_path):
    """Load a CSV safely."""
    if file_path.exists():
        try:
            return pd.read_csv(file_path)
        except Exception as error:
            st.error(f"Could not read {file_path.name}: {error}")
            return pd.DataFrame()

    return pd.DataFrame()


github = load_csv(GITHUB_FILE)
earthquakes = load_csv(EARTHQUAKE_FILE)


def to_number(data, column):
    """Convert a column to numeric values safely."""
    if column in data.columns:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )
    return data


# ==========================================
# HEADER
# ==========================================

st.title("🌐 TECTONIC")
st.subheader("Open Data Intelligence")
st.caption(
    "OPEN DATA, DECODED.  |  "
    "GitHub Repository Analytics + Global Seismic Activity"
)

st.divider()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🌐 TECTONIC")
st.sidebar.caption("OPEN DATA INTELLIGENCE")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Command Center",
        "Seismic Monitor",
        "Repository Observatory",
        "Data Vault"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("DATA SOURCES")

st.sidebar.write(
    "🟢 USGS Earthquake Dataset"
    if not earthquakes.empty
    else "🔴 Earthquake CSV Missing"
)

st.sidebar.write(
    "🟢 GitHub Repository Dataset"
    if not github.empty
    else "🔴 GitHub CSV Missing"
)

st.sidebar.divider()

if st.sidebar.button("🔄 Reload Dashboard"):
    st.rerun()

st.sidebar.caption("TECTONIC • Open Data Intelligence")


# ==========================================
# COMMAND CENTER
# ==========================================

if page == "Command Center":

    st.header("Command Center")
    st.write(
        "Your central overview of collected GitHub "
        "and earthquake datasets."
    )

    # Calculate metrics
    repository_count = len(github)
    earthquake_count = len(earthquakes)

    if "magnitude" in earthquakes.columns:
        eq_magnitudes = pd.to_numeric(
            earthquakes["magnitude"], errors="coerce"
        )
        strongest = eq_magnitudes.max()
        strongest = 0 if pd.isna(strongest) else strongest
    else:
        strongest = 0

    if "stars" in github.columns:
        repo_stars = pd.to_numeric(
            github["stars"], errors="coerce"
        )
        average_stars = repo_stars.mean()
        average_stars = (
            0 if pd.isna(average_stars) else average_stars
        )
    else:
        average_stars = 0

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Repositories Indexed",
        f"{repository_count:,}"
    )

    col2.metric(
        "Earthquakes Recorded",
        f"{earthquake_count:,}"
    )

    col3.metric(
        "Strongest Magnitude",
        f"{strongest:.2f}"
    )

    col4.metric(
        "Average Repository Stars",
        f"{average_stars:,.0f}"
    )

    st.divider()

    # Main charts
    left, right = st.columns(2)

    with left:

        st.subheader("🌍 Global Seismic Activity")

        required_columns = {
            "latitude", "longitude", "magnitude"
        }

        if required_columns.issubset(earthquakes.columns):

            eq = earthquakes.copy()

            for column in [
                "latitude", "longitude", "magnitude"
            ]:
                eq[column] = pd.to_numeric(
                    eq[column], errors="coerce"
                )

            eq = eq.dropna(
                subset=["latitude", "longitude", "magnitude"]
            )

            # Marker sizes must never be negative.
            eq["marker_size"] = (
                eq["magnitude"].clip(lower=0) + 1
            )

            if not eq.empty:

                fig = px.scatter_geo(
                    eq,
                    lat="latitude",
                    lon="longitude",
                    size="marker_size",
                    color="magnitude",
                    hover_name=(
                        "place" if "place" in eq.columns else None
                    ),
                    color_continuous_scale="Turbo",
                    title="Earthquake Locations"
                )

                fig.update_layout(
                    paper_bgcolor="#101A2B",
                    plot_bgcolor="#101A2B",
                    font=dict(color="#F1F5F9"),
                    title_font_color="#FFFFFF",
                    geo=dict(
                        bgcolor="#101A2B",
                        showland=True,
                        landcolor="#26364A",
                        showocean=True,
                        oceancolor="#0B1424",
                        showcountries=True,
                        countrycolor="#52647D",
                        showcoastlines=True,
                        coastlinecolor="#52647D"
                    ),
                    margin=dict(
                        l=0, r=0, t=55, b=0
                    )
                )

                st.plotly_chart(
                    fig, use_container_width=True
                )

            else:
                st.info(
                    "No valid earthquake coordinates are available."
                )

        else:
            st.warning(
                "Earthquake CSV needs latitude, longitude "
                "and magnitude columns."
            )

    with right:

        st.subheader("⭐ Top GitHub Repositories")

        if {"name", "stars"}.issubset(github.columns):

            repos = github.copy()

            repos["stars"] = pd.to_numeric(
                repos["stars"], errors="coerce"
            )

            repos = repos.dropna(subset=["stars"])
            repos = repos.nlargest(10, "stars")

            if not repos.empty:

                fig = px.bar(
                    repos.sort_values("stars"),
                    x="stars",
                    y="name",
                    orientation="h",
                    color="stars",
                    color_continuous_scale="Teal",
                    title="Top 10 Repositories by Stars"
                )

                fig.update_layout(
                    paper_bgcolor="#101A2B",
                    plot_bgcolor="#101A2B",
                    font=dict(color="#F1F5F9"),
                    title_font_color="#FFFFFF",
                    xaxis_title="Stars",
                    yaxis_title="Repository",
                    margin=dict(
                        l=10, r=10, t=55, b=10
                    )
                )

                fig.update_xaxes(
                    gridcolor="#30435E"
                )

                fig.update_yaxes(
                    gridcolor="#30435E"
                )

                st.plotly_chart(
                    fig, use_container_width=True
                )

            else:
                st.info(
                    "No repository star information is available."
                )

        else:
            st.warning(
                "GitHub CSV needs name and stars columns."
            )

    st.divider()
    st.caption(
        "Metrics reflect the records currently stored in your CSV files."
    )


# ==========================================
# SEISMIC MONITOR
# ==========================================

elif page == "Seismic Monitor":

    st.header("🌍 Seismic Monitor")
    st.write(
        "Filter earthquake events by magnitude and "
        "explore their geographic distribution."
    )

    if "magnitude" not in earthquakes.columns:

        st.warning(
            "Your earthquake CSV must contain a magnitude column."
        )

    else:

        eq = earthquakes.copy()

        eq["magnitude"] = pd.to_numeric(
            eq["magnitude"], errors="coerce"
        )

        eq = eq.dropna(subset=["magnitude"])

        if eq.empty:

            st.info("No valid earthquake records found.")

        else:

            minimum = float(eq["magnitude"].min())
            maximum = float(eq["magnitude"].max())

            if minimum == maximum:
                st.info(
                    f"All recorded events have magnitude {minimum:.2f}."
                )
                filtered = eq.copy()

            else:

                low, high = st.slider(
                    "Select magnitude range",
                    min_value=minimum,
                    max_value=maximum,
                    value=(minimum, maximum)
                )

                filtered = eq[
                    (eq["magnitude"] >= low)
                    & (eq["magnitude"] <= high)
                ].copy()

            st.metric(
                "Matching Earthquake Events",
                f"{len(filtered):,}"
            )

            if {
                "latitude", "longitude"
            }.issubset(filtered.columns):

                filtered["latitude"] = pd.to_numeric(
                    filtered["latitude"], errors="coerce"
                )

                filtered["longitude"] = pd.to_numeric(
                    filtered["longitude"], errors="coerce"
                )

                filtered = filtered.dropna(
                    subset=["latitude", "longitude"]
                ).copy()

                filtered["marker_size"] = (
                    filtered["magnitude"].clip(lower=0) + 1
                )

                if not filtered.empty:

                    fig = px.scatter_geo(
                        filtered,
                        lat="latitude",
                        lon="longitude",
                        size="marker_size",
                        color="magnitude",
                        hover_name=(
                            "place"
                            if "place" in filtered.columns
                            else None
                        ),
                        color_continuous_scale="Turbo",
                        title="Filtered Earthquake Map"
                    )

                    fig.update_layout(
                        paper_bgcolor="#101A2B",
                        plot_bgcolor="#101A2B",
                        font=dict(color="#F1F5F9"),
                        title_font_color="#FFFFFF",
                        geo=dict(
                            bgcolor="#101A2B",
                            showland=True,
                            landcolor="#26364A",
                            showocean=True,
                            oceancolor="#0B1424",
                            showcountries=True,
                            countrycolor="#52647D"
                        ),
                        margin=dict(
                            l=0, r=0, t=55, b=0
                        )
                    )

                    st.plotly_chart(
                        fig, use_container_width=True
                    )

                else:
                    st.info(
                        "No valid earthquake coordinates match the filter."
                    )

            else:
                st.warning(
                    "Your earthquake CSV needs latitude "
                    "and longitude columns to show a map."
                )

            st.subheader("Earthquake Records")

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )


# ==========================================
# REPOSITORY OBSERVATORY
# ==========================================

elif page == "Repository Observatory":

    st.header("⭐ Repository Observatory")
    st.write(
        "Search, filter and explore collected GitHub repositories."
    )

    if github.empty:

        st.warning(
            "No GitHub data found. Check "
            "output/github_repositories.csv."
        )

    else:

        filtered = github.copy()

        # Search by repository name
        if "name" in filtered.columns:

            search = st.text_input(
                "🔎 Search repository name",
                placeholder="Enter a repository name..."
            )

            if search:
                filtered = filtered[
                    filtered["name"].astype(str).str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

        # Filter by language
        if "language" in filtered.columns:

            language_values = (
                filtered["language"]
                .fillna("Unknown")
                .astype(str)
            )

            languages = sorted(language_values.unique())

            selected_languages = st.multiselect(
                "Filter by programming language",
                options=languages,
                default=languages
            )

            filtered = filtered[
                language_values.loc[filtered.index].isin(
                    selected_languages
                )
            ]

        # Sort by stars
        if "stars" in filtered.columns:

            filtered["stars"] = pd.to_numeric(
                filtered["stars"], errors="coerce"
            )

            filtered = filtered.sort_values(
                "stars",
                ascending=False,
                na_position="last"
            )

        st.metric(
            "Repositories Found",
            f"{len(filtered):,}"
        )

        # Language chart
        if (
            "language" in filtered.columns
            and not filtered.empty
        ):

            st.subheader("Programming Language Landscape")

            language_counts = (
                filtered["language"]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )

            language_counts.columns = [
                "Language", "Repositories"
            ]

            fig = px.bar(
                language_counts,
                x="Language",
                y="Repositories",
                color="Language",
                title="Repositories by Language"
            )

            fig.update_layout(
                paper_bgcolor="#101A2B",
                plot_bgcolor="#101A2B",
                font=dict(color="#F1F5F9"),
                title_font_color="#FFFFFF",
                showlegend=False
            )

            fig.update_xaxes(
                gridcolor="#30435E"
            )

            fig.update_yaxes(
                gridcolor="#30435E"
            )

            st.plotly_chart(
                fig, use_container_width=True
            )

        st.subheader("Repository Data")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Filtered Repositories",
            data=filtered.to_csv(index=False),
            file_name="filtered_repositories.csv",
            mime="text/csv"
        )


# ==========================================
# DATA VAULT
# ==========================================

elif page == "Data Vault":

    st.header("🗄️ Data Vault")
    st.write(
        "Inspect and download the raw datasets collected by TECTONIC."
    )

    github_tab, earthquake_tab = st.tabs(
        ["GitHub Data", "Earthquake Data"]
    )

    with github_tab:

        st.subheader("GitHub Repository Records")

        if not github.empty:

            st.write(
                f"Total records: {len(github):,}"
            )

            st.dataframe(
                github,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download GitHub CSV",
                data=github.to_csv(index=False),
                file_name="github_repositories.csv",
                mime="text/csv"
            )

        else:
            st.warning(
                "GitHub CSV was not found or contains no records."
            )

    with earthquake_tab:

        st.subheader("Earthquake Records")

        if not earthquakes.empty:

            st.write(
                f"Total records: {len(earthquakes):,}"
            )

            st.dataframe(
                earthquakes,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download Earthquake CSV",
                data=earthquakes.to_csv(index=False),
                file_name="earthquakes.csv",
                mime="text/csv"
            )

        else:
            st.warning(
                "Earthquake CSV was not found or contains no records."
            )

    st.divider()

    st.subheader("Dataset Status")

    status1, status2 = st.columns(2)

    with status1:
        st.write("**GitHub Dataset**")
        st.write(f"File: `{GITHUB_FILE}`")
        st.write(
            "🟢 Available"
            if GITHUB_FILE.exists()
            else "🔴 File missing"
        )

    with status2:
        st.write("**Earthquake Dataset**")
        st.write(f"File: `{EARTHQUAKE_FILE}`")
        st.write(
            "🟢 Available"
            if EARTHQUAKE_FILE.exists()
            else "🔴 File missing"
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "TECTONIC | Open Data Intelligence | "
    "Built with Python, Streamlit and Plotly"
)
