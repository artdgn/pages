# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] papermill={"duration": 0.013695, "end_time": "2020-03-27T06:31:15.895652", "exception": false, "start_time": "2020-03-27T06:31:15.881957", "status": "completed"} tags=[]
# # World progress projections (updated daily)
# > Visualising stacked projections for all countries.
#
# - comments: true
# - categories: [overview]
# - author: <a href=https://github.com/artdgn/>artdgn</a>
# - permalink: /covid-world-progress/
# - image: images/world-infected.png
# - toc: true
# - hide: false
# -

# > Important: This dashboard contains the results of a predictive model that was not built by an epidimiologist.

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import covid_helpers

helper = covid_helpers.OverviewData
stylers = covid_helpers.PandasStyling
df_all = helper.table_with_projections()
# -

#hide_input
from IPython.display import display, Markdown
Markdown(f"***Based on data up to: {pd.to_datetime(helper.dt_today).date().isoformat()}***")

# ## For details per country see [main notebook](/notebook-posts/covid-progress-projections/)

# ## World model plots (all countries stacked)
# The outputs of the models for all countries in stacked plots.
# > Tip: Hover the mouse of the area to see which country is which and the countries S/I/R ratios at that point. 
#
# > Tip: The plots are zoomable and draggable.

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
#hide_input
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
# -

#hide_input
alt.Chart(df_tot[df_tot['day'] < 30]).mark_area().encode(
    x="day:Q",
    y=alt.Y("Removed-total:Q", stack=True),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed']
).interactive()\
.properties(width=650, height=340)\
.properties(title='Removed (recovered / dead)')\
.configure_title(fontSize=20)

#hide_input
alt.Chart(df_tot[df_tot['day'] < 30]).mark_area().encode(
    x="day:O",
    y=alt.Y("Susceptible-total:Q", stack=True, 
            scale=alt.Scale(domain=(0, df_tot[df_tot['day']==1]['Susceptible-total'].sum()))),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed']
).interactive()\
.properties(width=650, height=340)\
.properties(title='Susceptible (not yet infected)')\
.configure_title(fontSize=20)

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/notebook-posts/covid-progress-projections/#appendix)
