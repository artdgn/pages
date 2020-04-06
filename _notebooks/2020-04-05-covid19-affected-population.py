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
# # Affected Population by Country (full table)
# > Modeling current and future affected population percentage.
#
# - categories: [overview]
# - comments: true
# - author: <a href=https://github.com/artdgn/>artdgn</a>
# - image: images/affected-pop.png
# - permalink: /covid-affected-population/
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

# ## Projected Affected Population percentage
#
# > Countries sorted by number of new cases in last 5 days
#
# - Details of estimation and prediction calculations are in [Appendix](#appendix).

# - Column definitions:
#     - <font size=2><b>Estimated <i>new</i> cases in last 5 days</b>: estimated new cases in last 5 days.</font>
#     - <font size=2><b>Estimated <i>total</i> affected population percentage</b>: estimated percentage of total population already affected (infected, recovered, or dead).</font>
#     - <font size=2><b>Projected in 14 days</b>: projected percentage of total affected population in 14 days.</font>
#     - <font size=2><b>Projected in 30 days</b>: projected percentage of total affected population in 30 days.</font>
#     - <font size=2><b>Reported fatality percentage</b>: reported total deaths divided by total cases.</font>
#     - <font size=2><b>Estimated daily case growth rate</b>: percentage daily change in total cases during last 5 days</font>.

#hide_input
rename_cols = {'Cases.new.est': 'Estimated <br> <i>new</i> cases <br> in last 5 days', 
               'affected_ratio.est': 'Estimated <br> <i>total</i> affected <br> population <br> percentage',
               'affected_ratio.est.+14d': 'Projected <br> In 14 days',
               'affected_ratio.est.+30d': 'Projected <br> In 30 days',
               'Fatality Rate': 'Reported <br> fatality <br> percentage',
               'growth_rate': 'Estimated <br> daily case <br> growth rate',
              }
progress_cols = list(rename_cols.values())[:4]
df_progress_bars = df.rename(rename_cols, axis=1)
df_progress_bars.sort_values(rename_cols['Cases.new.est'], ascending=False)\
[rename_cols.values()].style\
    .bar(subset=progress_cols[0], color='#b57b17')\
    .bar(subset=progress_cols[1], color='#5dad64', vmin=0, vmax=1.0)\
    .bar(subset=progress_cols[2], color='#719974', vmin=0, vmax=1.0)\
    .bar(subset=progress_cols[3], color='#a1afa3', vmin=0, vmax=1.0)\
    .bar(subset=[rename_cols['Fatality Rate']], color='#420412', vmin=0, vmax=0.1)\
    .applymap(lambda _: 'color: red', subset=[rename_cols['Fatality Rate']])\
    .bar(subset=[rename_cols['growth_rate']], color='#d65f5f', vmin=0, vmax=0.33)\
    .format('<b>{:,.0f}</b>', subset=list(rename_cols.values())[0])\
    .format('<b>{:.1%}</b>', subset=list(rename_cols.values())[1:])

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
 .configure_axis(labelFontSize=15, titleFontSize=18, grid=True))
# -

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/notebook-posts/covid-progress-projections/#appendix)
