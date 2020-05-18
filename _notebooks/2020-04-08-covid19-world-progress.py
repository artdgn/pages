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
# # World progress projections
# > Visualising stacked projections for all countries.
#
# - permalink: /covid-world-progress/
# - image: images/world-infected.png
# - toc: false
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
from IPython.display import Markdown
cur_date = pd.to_datetime(covid_helpers.OverviewData.dt_today).date().isoformat()
Markdown(f"***Based on data up to: {cur_date}***")

# ## For details per country see [main notebook](/pages/covid-progress-projections/)

# ## World projections from country models (all countries stacked)
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
df_tot = df_alt.rename(columns={'country': covid_helpers.COL_REGION}
                      ).set_index(covid_helpers.COL_REGION)
df_tot['population'] = df_all['population']
for c in df_tot.columns[df_alt.dtypes == float]:
    df_tot[c + '-total'] = df_tot[c] * df_tot['population']
df_tot = df_tot.reset_index()
df_tot.columns = [c.replace('.', '-') for c in df_tot.columns]

# +
#hide_input
import altair as alt
alt.data_transformers.disable_max_rows()

# filter out noisy countries for actively infected plot:
df_filt = helper.filter_df(df_all)
df_tot_filt = df_tot[df_tot[covid_helpers.COL_REGION].isin(df_filt.index.unique())]

# make plot
alt.Chart(df_tot_filt[df_tot_filt['day'] < 30]).mark_area().encode(
    x=alt.X('day:Q', title=f'days after today ({cur_date})'),
    y=alt.Y("Infected-min-total:Q", stack=True, title="Number of people"),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed'],    
).interactive()\
.properties(width=650, height=340)\
.properties(title='Actively infected (conservative estimate)')\
.configure_title(fontSize=20)
# -

#hide_input
alt.Chart(df_tot[df_tot['day'] < 30]).mark_area().encode(
    x=alt.X('day:Q', title=f'days after today ({cur_date})'),
    y=alt.Y("Removed-min-total:Q", stack=True, title="Number of people"),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed']
).interactive()\
.properties(width=650, height=340)\
.properties(title='Recovered or dead (conservative estimate)')\
.configure_title(fontSize=20)

#hide_input
alt.Chart(df_tot[df_tot['day'] < 30]).mark_area().encode(
    x=alt.X('day:Q', title=f'days after today ({cur_date})'),
    y=alt.Y("Susceptible-max-total:Q", stack=True, 
            scale=alt.Scale(domain=(0, df_tot[df_tot['day']==1]['Susceptible-total'].sum())),
           title='Number of people'),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed']
).interactive()\
.properties(width=650, height=340)\
.properties(title='Susceptible or not yet infected (conservative estimate)')\
.configure_title(fontSize=20)

# ## Appendix and Methodology
# <a id='appendix'></a>
# [See appendix in main notebook](/pages/covid-progress-projections/#appendix)
