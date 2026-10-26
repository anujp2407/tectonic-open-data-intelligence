# TECTONIC — Open Data Intelligence

**Explore open data. Discover patterns. Turn information into insight.**

TECTONIC is a Python-based data intelligence project that collects, organizes, and visualizes open datasets through an interactive Streamlit dashboard. It brings together GitHub repository information and earthquake data from the USGS earthquake feed to help users explore software trends and seismic activity.

## Features

- **GitHub Repository Explorer** — Explore repository metadata, star counts, and programming languages.
- **Seismic Activity Monitor** — Analyze earthquake data, including magnitude and geographic coordinates.
- **Interactive Dashboard** — View key metrics, charts, and data through a Streamlit interface.
- **Data Processing** — Collect and organize data into CSV files for analysis and visualization.
- **Open Data Integration** — Work with publicly available data sources.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data collection and processing |
| Streamlit | Interactive dashboard |
| Pandas | Data manipulation and analysis |
| Plotly | Interactive visualizations |
| GitHub data | Repository metadata |
| USGS Earthquake API | Earthquake GeoJSON data |

## Project Structure

```text
rest-api-geospatial-visualizer/
├── dashboard.py          # Streamlit dashboard
├── main.py               # Data collection and processing
├── requirements.txt      # Python dependencies
├── .gitignore            # Files excluded from Git
└── output/               # Generated datasets and visualizations
    ├── github_repositories.csv
    └── earthquakes.csv
```

Generated output files may not be included in the repository. They can be recreated by running the data collection script.

## Getting Started

### 1. Prerequisites

- Python 3.10 or a compatible version
- Git
- Visual Studio Code (recommended)

### 2. Clone the repository

```bash
git clone https://github.com/anujp2407/tectonic-open-data-intelligence.git
cd tectonic-open-data-intelligence
```

### 3. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Generate the datasets

```bash
python main.py
```

This runs the data collection and processing script. Ensure the expected CSV files are generated in the `output/` directory before starting the dashboard.

### 6. Launch the dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## Data Sources

- **GitHub:** Public repository information.
- **USGS Earthquake Hazards Program:** Public earthquake data in GeoJSON format.

Data availability and API responses may vary over time.

## Future Enhancements

- Add more open-data sources.
- Expand geospatial analysis and filtering.
- Improve historical trend analysis.
- Add dashboard screenshots
