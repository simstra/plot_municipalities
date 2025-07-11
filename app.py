import geopandas as gpd
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__)

# Load data from Google Sheets
sheet_id = "1Hxh2_yL5S8cMJCNi-XaPqgbIpy-ptkfacQy7GWSWHgA"
sheet_name = "Kommunvisiter2025"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url)

# Load shapefile and convert to WGS84
shapefile_path = "Kommun_Sweref99TM.shp"
gdf = gpd.read_file(shapefile_path).to_crs("EPSG:4326")
municipality_column = "KnNamn"

# Get list of people from the dataframe (excluding the 'Kommun' column)
people = [col for col in df.columns if col not in ["Kommun", "Kommun långt namn", "Unnamed: 6", "Topplista", "Poäng"]]

# App layout
app.layout = html.Div([
    html.H1("Svenska kommunbesök 2025"),
    html.Label("Välj person:"),
    dcc.Dropdown(
        id="person-dropdown",
        options=[{"label": name, "value": name} for name in people],
        value="Emma"
    ),
    html.H3(id="total-visited"),
    dcc.Graph(id="map-graph")
])

# Callback to update map and total count
@app.callback(
    Output("map-graph", "figure"),
    Output("total-visited", "children"),
    Input("person-dropdown", "value")
)
def update_map(selected_person):
    df = pd.read_csv(url)
    visited = df["Kommun"].loc[df[selected_person] == 1].values
    gdf["color"] = gdf[municipality_column].apply(
        lambda x: "Visited" if x in visited else "Not visited"
    )
    fig = px.choropleth_map(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color="color",
        color_discrete_map={"Visited": "blue", "Not visited": "white"},
        map_style="carto-positron",
        center={"lat": 62.0, "lon": 15.0},
        zoom=4.5,
        opacity=0.6,
        hover_name=municipality_column,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1100, width=900)
    total = df[selected_person].sum()
    return fig, f"Totalt antal kommuner besökta: {total}"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

