# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] papermill={"duration": 0.013695, "end_time": "2020-03-27T06:31:15.895652", "exception": false, "start_time": "2020-03-27T06:31:15.881957", "status": "completed"} tags=[]
# # World maps (updated daily)
# > Visualising data on maps
#
# - comments: true
# - categories: [overview, maps]
# - author: <a href=https://github.com/Junikab/>Junikab</a>
# - permalink: /covid-world-maps/
# - toc: true
# - hide: false
# -

# > Important: This dashboard contains the results of a predictive model that was not built by an epidimiologist.

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import covid_helpers

helper = covid_helpers.OverviewData
df_all = helper.table_with_projections()
# -

#hide
df_all.columns

#hide
df_plot = (df_all.reset_index().rename(columns={'Country/Region': 'country'}))

# +
#hide
### geopandas
import geopandas

shapefile= 'data_files/110m_countries/ne_110m_admin_0_countries.shp'
world = geopandas.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
world.columns = ['country', 'iso_code', 'geometry']
world = world[world['country']!="Antarctica"].copy()
world['country'] = world['country'].map({
    'United States of America': 'US',
    'Taiwan': 'Taiwan*',
    'Palestine': 'West Bank and Gaza',
    'Côte d\'Ivoire': 'Cote d\'Ivoire',
    'Bosnia and Herz.': 'Bosnia and Herzegovina',    
}).fillna(world['country'])

df_plot_geo = pd.merge(world, df_plot, on='country', how='left')
# df_plot_geo.plot(column='needICU.per100k');

# +
#hide
### plotly
import plotly.graph_objects as go

fig = go.FigureWidget(
    data=go.Choropleth(
        locations = df_plot_geo['iso_code'],
        z = df_plot_geo['needICU.per100k'].fillna(0),
#         z = df_plot_geo['affected_ratio.est']*100,
#         z = df_plot_geo['growth_rate']*100,
        zmin=0, 
        zmax=10,
        text = df_plot_geo['country'],
        colorscale = 'sunsetdark',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'ICU need',
))

fig.update_layout(
    width=800,
    height=350,
    autosize=False,
    margin=dict(t=0, b=0, l=0, r=0),
    template="plotly_white",
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='natural earth'
    )
)

fig.update_geos(fitbounds="locations")

fig.show()
# -

# # World map of current ICU need
# For details per country see [main notebook](/notebook-posts/covid-progress-projections/)
#
# > Tip: The map is zoomable and draggable

#hide_input
from IPython.display import HTML
HTML(fig.to_html())

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/notebook-posts/covid-progress-projections/#appendix)
