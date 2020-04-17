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

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import covid_helpers

helper = covid_helpers.OverviewData
stylers = covid_helpers.PandasStyling
df_all = helper.table_with_projections()

# +
#hide
_, debug_dfs = helper.table_with_projections(debug_dfs=True)

df_alt = pd.concat([d.reset_index() for d in debug_dfs], axis=0)
# -

#hide
df_tot = df_alt.rename(columns={'country': 'Country/Region'}).set_index('Country/Region')
df_tot['population'] = df_all['population']
for c in df_tot.columns[df_alt.dtypes == float]:
    df_tot[c + '-total'] = df_tot[c] * df_tot['population']
df_tot = df_tot.reset_index()
df_tot.columns = [c.replace('.', '-') for c in df_tot.columns]

# +
#hide
import altair as alt
alt.data_transformers.disable_max_rows()

alt.Chart(df_tot[df_tot['day'] < 30]).mark_area().encode(
    x="day:Q",
    y=alt.Y("Infected-total:Q", stack=True),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed'],    
).interactive()\
.properties(width=650, height=340)\
.properties(title='Infected')\
.configure_title(fontSize=20)

# +
#hide_input
import altair as alt
from vega_datasets import data

counties = alt.topo_feature(data.us_10m.url, 'counties')
source = data.unemployment.url

alt.Chart(counties).mark_geoshape().encode(
    color='rate:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(source, 'id', ['rate'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300
)
