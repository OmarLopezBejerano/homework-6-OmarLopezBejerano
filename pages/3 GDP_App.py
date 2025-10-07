## Reuse your python file that webscrapes [GDP by country](https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)) and plots a stacked interactive bar plot using plotly. Stack countries within regions using the IMF numbers. Create streamlit app that displays a stacked bar plot of country GDPs stacked within regions. Allow the user to select between the IMF, UN and World Bank reported numbers. Create a short (5-10 second) gif demonstrating your app functioning. Note I use the Chrome Capture extension for this. Add your gif to your repository.

import pandas as pd
import requests as rq
import bs4
from io import StringIO
import streamlit as st

## Getting the data from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/102.0.0.0 Safari/537.36"
}
response = rq.get(url.strip(), headers=headers, timeout=10)
bs4page = bs4.BeautifulSoup(response.text, 'html.parser')
tables = bs4page.find_all('table',{'class':"wikitable"})
gdp = pd.read_html(StringIO(str(tables[0])))[0]
gdp = gdp.dropna()
gdp = gdp.drop(gdp.index[0]) # drop world from list
gdp.rename(columns={"IMF (2025)[1][6]": "IMF"}, inplace=True)
gdp.rename(columns={"World Bank (2022–24)[7]": "World Bank"}, inplace=True)
gdp.rename(columns={"United Nations (2023)[8]": "United Nations"}, inplace=True)
gdp["IMF"] = pd.to_numeric(gdp["IMF"], errors="coerce")
gdp["World Bank"] = pd.to_numeric(gdp["World Bank"], errors="coerce")
gdp["United Nations"] = pd.to_numeric(gdp["United Nations"], errors="coerce")
gdp = gdp.dropna()
gdp["gdp_quantile_group"] = pd.qcut(gdp["IMF"], q=4, labels=["Low", "Medium", "High", "Very High"])

## Streamlit app
st.title("GDP by Country and Region")
st.write("This app displays a stacked bar plot of country GDPs stacked within regions. You can select between the IMF, UN and World Bank reported numbers and filter by GDP quantile groups.")
selection = st.radio("Select GDP Source", options=["IMF", "World Bank", "United Nations"])
st.write(f"### You selected: {selection}")

## Selecting only the data to be plotted based on the user selection
## Creating the filter based on quantile groups
groups_in_order = pd.Index(gdp["gdp_quantile_group"]).unique().tolist()
selected_groups = st.multiselect(
    "Select GDP quantile group(s):",
    options=groups_in_order,
    default=groups_in_order
)
## This applies the filter to the dataframe
filtered = gdp[gdp["gdp_quantile_group"].isin(selected_groups)].copy()
## This solves the issue of alphabetical ordering in the x-axis
filtered["Country/Territory"] = pd.Categorical(
    filtered["Country/Territory"],
    categories=filtered["Country/Territory"],
    ordered=True
)
## Plotting
st.bar_chart(
    filtered,
    x="Country/Territory",
    y=selection,
    color="gdp_quantile_group",
    stack=False,
    height=600,
    width=800
)
