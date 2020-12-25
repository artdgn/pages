# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] papermill={"duration": 0.013695, "end_time": "2020-03-27T06:31:15.895652", "exception": false, "start_time": "2020-03-27T06:31:15.881957", "status": "completed"} tags=[]
# # World progress projections
# > Visualising stacked progress & projections for all countries.
#
# - permalink: /covid-world-progress/
# - image: images/world-infected.png
# - toc: false
# - hide: false
# -

# > Important: This dashboard contains the results of a predictive model that was not built by an epidemiologist.

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import covid_helpers

covid_data = covid_helpers.CovidData()
stylers = covid_helpers.PandasStyling
df_all = covid_data.table_with_projections()
# -

#hide_input
from IPython.display import Markdown
Markdown(f"*Based on data up to:* ***{covid_data.cur_date}***")

# +
#hide
_, debug_dfs = covid_data.table_with_projections(debug_dfs=True)

df_alt = pd.concat([d.reset_index() for d in debug_dfs], axis=0)
# -

#hide
df_tot = df_alt.rename(columns={'country': covid_data.COL_REGION}
                      ).set_index(covid_data.COL_REGION)
df_tot['population'] = df_all['population']
for c in df_tot.columns[df_alt.dtypes == float]:
    df_tot[c + '-total'] = df_tot[c] * df_tot['population']
df_tot = df_tot.reset_index()
df_tot.columns = [c.replace('.', '-') for c in df_tot.columns]

#hide_input
df_now = df_tot[df_tot['day'] == 0]
pop = df_now['population'].sum()
s_now = df_now['Susceptible-total'].sum() / pop
i_now = df_now['Infected-total'].sum() / pop
r_now = df_now['Removed-total'].sum() / pop
Markdown("### World totals:\n"
         f"Infected &#128567;: **{i_now:.1%}**, "
         f"Removed &#128532;: **{r_now:.1%}**, "
         f"Susceptible &#128543;: **{s_now:.1%}**")

# ### Progress & projections from country models (all countries stacked)
# The outputs of the models for all countries in stacked plots. For details per country see [main notebook](/pages/covid-progress-projections/)
# > Tip: Hover the mouse of the area to see which country is which and the countries S/I/R ratios at that point. 
#
# > Tip: The plots are zoomable and draggable.

# +
#hide
# filter by days
days = 30
df_tot = df_tot[df_tot['day'].between(-days, days) | (df_tot['day'] % 10 == 0)]

# filter out noisy countries for actively infected plot:
df_filt = covid_data.filter_df(df_all)
df_tot_filt = df_tot[df_tot[covid_data.COL_REGION].isin(df_filt.index.unique())]

# +
#hide_input
import altair as alt
alt.data_transformers.disable_max_rows()

# today
today_line = (alt.Chart(pd.DataFrame({'x': [0]}))
                  .mark_rule(color='orange')
                  .encode(x='x', size=alt.value(1)))

# make plot
max_y = (df_tot_filt[df_tot_filt['day'].between(-days, days)]
         .groupby('day')['Infected-total'].sum().max())
stacked_inf = alt.Chart(df_tot_filt).mark_area().encode(
    x=alt.X('day:Q',
            title=f'days relative to today ({covid_data.cur_date})',
            scale=alt.Scale(domain=(-days, days))),
    y=alt.Y("Infected-total:Q", stack=True, title="Number of people",
           scale=alt.Scale(domain=(0, max_y))),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed'],    
)
(stacked_inf + today_line).interactive()\
.properties(width=650, height=340)\
.properties(title='Actively infected')\
.configure_title(fontSize=20)

# +
#hide_input
max_y = df_tot_filt[df_tot_filt['day']==days]['Removed-total'].sum()
stacked_rem = alt.Chart(df_tot_filt).mark_area().encode(
    x=alt.X('day:Q',
            title=f'days relative to today ({covid_data.cur_date})',
            scale=alt.Scale(domain=(-days, days))),
    y=alt.Y("Removed-total:Q", stack=True, title="Number of people",
           scale=alt.Scale(domain=(0, max_y))),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed']
)

(stacked_rem + today_line).interactive()\
.properties(width=650, height=340)\
.properties(title='Recovered or dead')\
.configure_title(fontSize=20)

# +
#hide_input
max_y = df_tot[df_tot['day']==-days]['Susceptible-total'].sum()
stacked_sus = alt.Chart(df_tot).mark_area().encode(
    x=alt.X('day:Q',
            title=f'days relative to today ({covid_data.cur_date})',
            scale=alt.Scale(domain=(-days, days))),
    y=alt.Y("Susceptible-max-total:Q", stack=True, 
            scale=alt.Scale(domain=(0, max_y)),
           title='Number of people'),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=['Country/Region', 'Susceptible', 'Infected', 'Removed']
)

(stacked_sus + today_line).interactive()\
.properties(width=650, height=340)\
.properties(title='Susceptible or not yet infected')\
.configure_title(fontSize=20)
# -

# ## Appendix and Methodology
# <a id='appendix'></a>
# [See appendix in main notebook](/pages/covid-progress-projections/#appendix)
