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
# > Visualising projections and estimations on maps
#
# - comments: true
# - categories: [overview, maps]
# - author: <a href=https://github.com/Junikab/>Junikab</a>, <a href=https://github.com/artdgn/>artdgn</a>
# - permalink: /covid-world-maps/
# - image: images/world_map.png
# - toc: true
# - sticky_rank: 1
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
df_all.columns.sort_values()

#hide_input
from IPython.display import Markdown
Markdown(f"***Based on data up to: {pd.to_datetime(helper.dt_today).date().isoformat()}***")

#hide
df_plot = (df_all.reset_index().rename(columns={'Country/Region': 'country'}))

# +
#hide
### geopandas
import geopandas

shapefile = 'data_files/110m_countries/ne_110m_admin_0_countries.shp'
world = geopandas.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
world.columns = ['country', 'iso_code', 'geometry']
world = world[world['country'] != "Antarctica"].copy()
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
import plotly.graph_objects as go
import plotly.express as px

fig = go.FigureWidget(
    data=go.Choropleth(
        locations=df_plot_geo['iso_code'],
        z=df_plot_geo['needICU.per100k'].fillna(0),
        zmin=0,
        zmax=10,
        text=df_plot_geo['country'],
        colorscale='sunsetdark',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='ICU need<br>(current)',
    ))

fig.update_layout(
    width=800,
    height=450,
    autosize=True,
    margin=dict(t=0, b=0, l=0, r=0),
    template="plotly_white",
    geo=dict(
        showframe=False,
        projection_type='natural earth',
        resolution=110,
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="Grey",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="LightBlue",
        fitbounds="locations"
    )
);


# -

#hide
def button_dict(col, title, colorscale, scale_max=None, percent=False):    
    series = df_plot_geo[col].fillna(0)
#     series_text = (df_plot_geo['country'] + '<br>' + 
#                    (series.apply('{:.1%}'.format) if percent 
#                    else series.apply('{:.2f}'.format)))    
    series *= 100 if percent else 1

    scale_obj = getattr(px.colors.sequential, colorscale)
    scale_arg = [[(i - 1) / (len(scale_obj) - 1), c] for i, c in enumerate(scale_obj, start=1)]

    max_arg = series.max() if scale_max is None else min(scale_max, series.max())

    return dict(args=[{'z': [series.to_list()],
#                        'text': [series_text.to_list()],
                       'zmax': [max_arg],
                       'colorbar': [{'title': {'text': title}}],
                       'colorscale': [scale_arg]}],
                label=title, method="restyle")


#hide
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                button_dict('needICU.per100k', 
                            'ICU need<br>(current)', 'Sunsetdark', 10),
                button_dict('needICU.per100k.+14d', 
                            'ICU need<br>(in 14 days)', 'Sunsetdark', 10),
                button_dict('needICU.per100k.+30d', 
                            'ICU need<br>(in 30 days)', 'Sunsetdark', 10),
                button_dict('icu_capacity_per100k', 'ICU Capacity', 'Blues'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.05, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                button_dict('affected_ratio.est', 
                            'Affected percent<br>(Current)', 'Bluyl', percent=True),
                button_dict('affected_ratio.est.+14d', 
                            'Affected percent<br>(in 14 days)', 'Bluyl', 25, percent=True),
                button_dict('affected_ratio.est.+30d', 
                            'Affected percent<br>(in 30 days)', 'Bluyl', 25, percent=True),
                button_dict('Cases.total.per100k.est', 
                            'Total cases<br>estimated per 100k', 'YlOrRd'),
                button_dict('Cases.total.est', 'Total cases<br>(estimated)', 'YlOrRd'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.23, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                button_dict('infection_rate', 
                            'Infection rate<br>percent (blue-red)', 'Bluered', 10, percent=True),
                button_dict('infection_rate', 
                            'Infection rate<br>percent', 'YlOrRd', 33, percent=True),                
                button_dict('Cases.new.per100k.est', 
                            'New cases<br>estimated per 100k', 'YlOrRd'),
                button_dict('Cases.new.est', 'New cases<br>(estimated)', 'YlOrRd'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.45, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                button_dict('Deaths.total.per100k', 'Deaths<br>per 100k', 'Reds'),
                button_dict('Deaths.total', 'Deaths<br>Total', 'Reds'),
                button_dict('lagged_fatality_rate', 
                            'Fatality rate %<br>(lagged)', 'PuRd', 20, percent=True),
                
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.67, xanchor="left", y=1.1, yanchor="top"),
    ])

# # World map (choose column)
#
# For details per country see [main notebook](/notebook-posts/covid-progress-projections/)
#
# > Tip: Select columns to show on map to from the dropdown menus. The map is zoomable and draggable.

#hide_input
from IPython.display import HTML
HTML(fig.to_html())

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/notebook-posts/covid-progress-projections/#appendix)
