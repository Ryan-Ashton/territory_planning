from setuptools import setup, find_packages

setup(
    name='geo_processing_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'geopandas',
        'folium',
    ],
    author='Ryan Ashton',
    author_email='ryan.ashton@rmanalytics.com.au',
    description='A package for processing and visualizing geo data.',
)
