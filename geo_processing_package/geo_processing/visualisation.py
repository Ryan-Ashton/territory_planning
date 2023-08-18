import os
import geopandas as gpd
import folium


def all_suburbs(map_object):
    def styling(feature):
        style = {
                "fillColor": "yellow",
                "color": "white",
                "weight": 1,
                "fillOpacity": 0.3,
            }
        return style
    
    geojson_path = os.path.join(target_directory, "POA_2021_AUST_GDA2020.geojson")
    gdf = gpd.read_file(geojson_path)
    gdf = gdf[~gdf["geometry"].isna()]
    
    for _, row in gdf.iterrows():
        geojson = folium.GeoJson(row.geometry, style_function=styling)
        
        popup_text = row["POA_NAME21"]
        popup = folium.Popup(popup_text, max_width=300)
        
        geojson.add_child(popup)
        geojson.add_to(map_object)
    
    return map_object



def all_territories(map_object):
    def styling(feature):
        style = {
                "fillColor": "blue",
                "color": "white",
                "weight": 1,
                "fillOpacity": 0.8,
            }
        return style
    
    terr = processed_gdf.drop(columns=["cent"])
    terr = terr.to_json()
    geojson_layer = folium.GeoJson(terr, style_function=styling)
    geojson_layer.add_to(map_object)
    return map_object
