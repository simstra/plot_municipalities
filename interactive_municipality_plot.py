import geopandas as gpd
import plotly.express as px
import pandas as pd

#Read in visited municipalities from drive document
sheet_id = "1Hxh2_yL5S8cMJCNi-XaPqgbIpy-ptkfacQy7GWSWHgA"
sheet_name = "Kommunvisiter2025"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url)

municipalities_visited = df["Kommun"].loc[df["Emma"] == 1].values

# Load the shapefile (make sure all required files are present)
shapefile_path = "Kommun_Sweref99TM.shp"
gdf = gpd.read_file(shapefile_path)

# Convert to WGS84 for compatibility with web maps
gdf = gdf.to_crs(epsg=4326)

# Replace with the actual column name for municipality names
municipality_column = "KnNamn"

# Create a new column for coloring
gdf["color"] = gdf[municipality_column].apply(
    lambda x: "Visited" if x in municipalities_visited else "Not visited"
)

# Create the interactive map
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

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()

import plotly.io as pio

pio.write_html(fig, file="map.html", auto_open=True)

