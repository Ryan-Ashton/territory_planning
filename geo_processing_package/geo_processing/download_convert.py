
import os
import requests
import zipfile
import geopandas as gpd
import pandas as pd


def download_convert_read_geojson(zip_url, target_directory):
    """
    Downloads a zip file from a given URL, extracts its contents,
    converts a specific shapefile to GeoJSON, and returns the GeoDataFrame.

    Parameters:
        zip_url (str): URL of the zip file to download.
        target_directory (str): Directory where the zip file will be downloaded and extracted.

    Returns:
        geopandas.geodataframe.GeoDataFrame: The GeoDataFrame containing the converted data.
    """
    # Create the directory if it doesn't exist
    os.makedirs(target_directory, exist_ok=True)

    # Download the zip file
    response = requests.get(zip_url)
    zip_filename = os.path.join(target_directory, "downloaded_file.zip")

    with open(zip_filename, "wb") as zip_file:
        zip_file.write(response.content)

    # Unzip the downloaded file
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(target_directory)

    # Remove the downloaded zip file
    os.remove(zip_filename)

    print("Zip file downloaded and extracted successfully.")

    # Read the shapefile and convert to GeoJSON
    shapefile_path = os.path.join(target_directory, "POA_2021_AUST_GDA2020.shp")
    gdf = gpd.read_file(shapefile_path)
    gdf.to_file(os.path.join(target_directory, "POA_2021_AUST_GDA2020.geojson"), driver='GeoJSON')

    # Read the GeoJSON file and return the GeoDataFrame
    geojson_path = os.path.join(target_directory, "POA_2021_AUST_GDA2020.geojson")
    gdf = gpd.read_file(geojson_path)
    gdf = gdf[~gdf["geometry"].isna()]

    return gdf