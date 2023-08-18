import geopandas as gpd
import pandas as pd

def concatenate_polygons(geodataframe):
    """
    Concatenate polygons within a GeoDataFrame to create a single polygon.

    Parameters:
        geodataframe (geopandas.geodataframe.GeoDataFrame): Input GeoDataFrame with polygons.

    Returns:
        geopandas.geodataframe.GeoDataFrame: GeoDataFrame containing a single concatenated polygon.
    """
    if geodataframe.empty:
        return None
    
    geodataframe = geodataframe[geodataframe.geometry.is_valid]
    
    if geodataframe.empty:
        return None
    
    concat_gdf = gpd.GeoDataFrame(geometry=[geodataframe.unary_union], crs=geodataframe.crs)
    
    return concat_gdf

def process_geo_data(df, postcode_col, territory_col):
    """
    Process geo data by filtering, concatenating polygons, and performing spatial operations.

    Parameters:
        df (pandas.DataFrame): Input DataFrame containing geo data.
        postcode_col (str): Name of the column containing Postcode information.
        territory_col (str): Name of the column containing New Territory information.

    Returns:
        geopandas.geodataframe.GeoDataFrame: Processed GeoDataFrame with spatial operations.
    """
    category_lists = {}

    for category in df[territory_col].unique():
        filtered_df = df[df[territory_col] == category]
        category_lists[category] = filtered_df[postcode_col].tolist()

    arr = []
    for category, values in category_lists.items():
        d = {}
        try:
            d["territory"] = category

            postcodes = category_lists[category]
            postcodes = [str(num) for num in postcodes]

            new_gdf = gdf[gdf['POA_CODE21'].isin(postcodes)]

            concatenated_polygon = concatenate_polygons(new_gdf)

            d["poly"] = concatenate_polygons(new_gdf).unary_union

            arr.append(d)
        except:
            continue

    new_df = pd.DataFrame(arr)
    new_gdf = gpd.GeoDataFrame(new_df)

    new_gdf.set_geometry('poly', inplace=True, crs="EPSG:7844")

    new_gdf["cent"] = new_gdf.centroid
    new_gdf["latitude"] = new_gdf["cent"].apply(lambda p: p.y)
    new_gdf["longitude"] = new_gdf["cent"].apply(lambda p: p.x)

    gdf_distance = new_gdf.to_crs(crs="EPSG:3112") 
    gdf_distance["area"] = gdf_distance["poly"].area / 1000000

    new_gdf = pd.merge(new_gdf, gdf_distance[["territory", "area"]], on="territory")

    new_gdf[["territory", "area"]].to_csv("distances.csv")
    
    return new_gdf