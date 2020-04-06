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
# # ICU need by Country (full table)
# > Modeling current and future ICU demand.
#
# - categories: [overview]
# - comments: true
# - author: <a href=https://github.com/artdgn/>artdgn</a>
# - image: images/icu-need.png
# - permalink: /covid-icu-projections/
# - toc: true
# - hide: false
# -

# > Important: This dashboard contains the results of a predictive model that was not built by an epidimiologist.

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import covid_helpers

helper = covid_helpers.OverviewData
df = helper.filter_df(helper.table_with_projections())
df.columns
# -

# ## Estimated need for ICU beds
#
# > Countries sorted by current ICU demand
#
# - ICU need is estimated as [6% of active cases](https://medium.com/@joschabach/flattening-the-curve-is-a-deadly-delusion-eea324fe9727).
# - ICU capacities are from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_by_hospital_beds) (OECD countries mostly) and [CCB capacities in Asia](https://www.researchgate.net/publication/338520008_Critical_Care_Bed_Capacity_in_Asian_Countries_and_Regions).
# - ICU spare capacity is based on 70% normal occupancy rate ([66% in US](https://www.sccm.org/Blog/March-2020/United-States-Resource-Availability-for-COVID-19), [75% OECD](https://www.oecd-ilibrary.org/social-issues-migration-health/health-at-a-glance-2019_4dd50c09-en))
# - Details of estimation and prediction calculations are in [Appendix](#appendix).
# - Column definitions:
#     - <font size=2><b>Estimated ICU need per 100k population</b>: number of ICU beds estimated to be needed per 100k population by COVID-19 patents.</font>
#     - <font size=2><b>Projected in 14 days</b>: projected ICU need per 100k population in 14 days.</font>
#     - <font size=2><b>Projected in 30 days</b>: projected ICU need per 100k population in 30 days.</font>
#     - <font size=2><b>ICU capacity per 100k</b>: number of ICU beds per 100k population.</font>
#     - <font size=2><b>Estimated ICU Spare capacity per 100k</b>: estimated ICU capacity per 100k population based on assumed normal occupancy rate of 70% and number of ICU beds (only for countries with ICU beds data).</font>
#     - <font size=2><b>Estimated daily case growth rate</b>: percentage daily change in total cases during last 5 days.</font>

#hide_input
rename_cols = {'needICU.per100k': 'Estimated <br> ICU need <br> per 100k <br> population',
               'needICU.per100k.+14d': 'Projected <br> In 14 days', 
               'needICU.per100k.+30d': 'Projected <br> In 30 days',               
               'icu_capacity_per100k': 'ICU <br> capacity <br> per 100k',
               'icu_spare_capacity_per100k': 'Estimated ICU <br> Spare capacity <br> per 100k',               
               'growth_rate': 'Estimated <br> daily case <br> growth rate',
              }
icu_cols = list(rename_cols.values())[:3]
df_icu_bars = df.rename(rename_cols, axis=1)
df_icu_bars.sort_values(rename_cols['needICU.per100k'], ascending=False)\
[rename_cols.values()].style\
    .bar(subset=icu_cols[0], color='#b21e3e', vmin=0, vmax=10)\
    .bar(subset=icu_cols[1], color='#f43d64', vmin=0, vmax=10)\
    .bar(subset=icu_cols[2], color='#ef8ba0', vmin=0, vmax=10)\
    .bar(subset=[rename_cols['icu_spare_capacity_per100k']], color='#3ab1d8', vmin=0, vmax=10)\
    .applymap(lambda _: 'color: blue', subset=[rename_cols['icu_spare_capacity_per100k']])\
    .bar(subset=[rename_cols['growth_rate']], color='#d65f5f', vmin=0, vmax=0.33)\
    .format('<b>{:.1%}</b>', subset=[rename_cols['growth_rate']])\
    .format('<b>{:.1f}</b>', subset=[rename_cols['icu_capacity_per100k']], na_rep="-")\
    .format('<b>{:.1f}</b>', subset=[rename_cols['icu_spare_capacity_per100k']], na_rep="-")\
    .format('<b>{:.2f}</b>', subset=icu_cols)\
    .set_precision(2)

# <a id='examples'></a>
#
# ## Interactive plot of Model predictions
#
# For top 20 countries by estimated new cases.
#
# > Tip: Choose a country from the drop-down menu to see the calculations used in the tables above and the dynamics of the model.

# +
#hide
sir_plot_countries = df.sort_values('Cases.new.est', ascending=False).head(20).index
_, debug_dfs = helper.table_with_projections(debug_countries=sir_plot_countries)

df_alt = pd.concat([d.reset_index() for d in debug_dfs], axis=0)

# +
#hide_input
import altair as alt

alt.data_transformers.disable_max_rows()

select_country = alt.selection_single(
    name='Select',
    fields=['country'],
    init={'country': sir_plot_countries[0]},
    bind=alt.binding_select(options=sorted(sir_plot_countries))
)

title = (alt.Chart(df_alt[['country', 'title']].drop_duplicates())
              .mark_text(dy=-180, dx=0, size=16)
              .encode(text='title:N')
              .transform_filter(select_country))

base = alt.Chart(df_alt).encode(x='day:Q')

line_cols = ['Infected', 'Susceptible', 'Removed']
colors = ['red', 'blue', 'green']
lines = (base.mark_line()
       .transform_fold(line_cols)
       .encode(x='day:Q',
                y=alt.Y('value:Q',
                        axis=alt.Axis(format='%', title='Percentage of Population')),
                color=alt.Color('key:N',
                                scale=alt.Scale(domain=line_cols, range=colors))))

import functools
bands = functools.reduce(alt.Chart.__add__,
                         [base.mark_area(opacity=0.1, color=color)
                          .encode(y=f'{col}\.max:Q',y2=f'{col}\.min:Q')
                          for col, color in zip(line_cols, colors)])


((lines + bands + title)
 .add_selection(select_country)
 .transform_filter(select_country)
 .configure_title(fontSize=20)
 .configure_axis(labelFontSize=15, titleFontSize=18, grid=True)
 .properties(width=550, height=340))
# -

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/notebook-posts/covid-progress-projections/#appendix)
