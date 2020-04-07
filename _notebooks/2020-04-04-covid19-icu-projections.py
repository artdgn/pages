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
stylers = covid_helpers.PandasStyling
df = helper.filter_df(helper.table_with_projections())
df.columns
# -
# ## Projected need for ICU beds
# > Countries sorted by current ICU demand
#
# - ICU need is estimated as [6% of active cases](https://medium.com/@joschabach/flattening-the-curve-is-a-deadly-delusion-eea324fe9727).
# - ICU capacities are from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_by_hospital_beds) (OECD countries mostly) and [CCB capacities in Asia](https://www.researchgate.net/publication/338520008_Critical_Care_Bed_Capacity_in_Asian_Countries_and_Regions).
# - ICU spare capacity is based on 70% normal occupancy rate ([66% in US](https://www.sccm.org/Blog/March-2020/United-States-Resource-Availability-for-COVID-19), [75% OECD](https://www.oecd-ilibrary.org/social-issues-migration-health/health-at-a-glance-2019_4dd50c09-en))
# - Details of estimation and prediction calculations are in [Appendix](#appendix).
#
# - Column definitions:
#     - <font size=2><b>Estimated ICU need per 100k population</b>: number of ICU beds estimated to be needed per 100k population by COVID-19 patents.</font>
#     - <font size=2><b>Estimated daily case growth rate</b>: percentage daily change in total cases during last 5 days.</font>
#     - <font size=2><b>Projected ICU need per 100k in 14 days</b>: self explanatory.</font>
#     - <font size=2><b>Projected ICU need per 100k in 30 days</b>: self explanatory.</font>
#     - <font size=2><b>ICU capacity per 100k</b>: number of ICU beds per 100k population.</font>
#     - <font size=2><b>Estimated ICU Spare capacity per 100k</b>: estimated ICU capacity per 100k population based on assumed normal occupancy rate of 70% and number of ICU beds (only for countries with ICU beds data).</font>
#

# > Tip: The <b><font color="b21e3e">red (need for ICU)</font></b>  and the <b><font color="3ab1d8">blue (ICU spare capacity)</font></b>  bars are on the same 0-10 scale, for easy visual comparison of columns.


# +
#hide_input
df_data = df.sort_values('needICU.per100k', ascending=False)
df_pretty = df_data.copy()
df_pretty['needICU.per100k.+14d'] = stylers.with_errs_float(
    df_pretty, 'needICU.per100k.+14d', 'needICU.per100k.+14d.err')
df_pretty['needICU.per100k.+30d'] = stylers.with_errs_float(
    df_pretty, 'needICU.per100k.+30d', 'needICU.per100k.+30d.err')
df_pretty['growth_rate'] = stylers.with_errs_ratio(df_pretty, 'growth_rate', 'growth_rate_std')

cols = {'needICU.per100k': 'Estimated<br>current<br>ICU need<br>per 100k<br>population',
        'growth_rate': 'Estimated<br>daily case<br>growth rate',
       'needICU.per100k.+14d': 'Projected<br>ICU need<br>per 100k<br>In 14 days',
       'needICU.per100k.+30d': 'Projected<br>ICU need<br>per 100k<br>In 30 days',
       'icu_capacity_per100k': 'ICU<br>capacity<br> per 100k',
       'icu_spare_capacity_per100k': 'Estimated ICU<br>Spare capacity<br>per 100k',
      }

df_pretty[cols.keys()].rename(cols, axis=1).style\
    .bar(subset=cols['needICU.per100k'], color='#b21e3e', vmin=0, vmax=10)\
    .apply(stylers.add_bar, color='#f43d64',
           s_v=df_data['needICU.per100k.+14d']/10, subset=cols['needICU.per100k.+14d'])\
    .apply(stylers.add_bar, color='#ef8ba0',
           s_v=df_data['needICU.per100k.+30d']/10, subset=cols['needICU.per100k.+30d'])\
    .apply(stylers.add_bar, color='#f49d5a',
           s_v=df_data['growth_rate']/0.33, subset=cols['growth_rate'])\
    .bar(subset=[cols['icu_spare_capacity_per100k']], color='#3ab1d8', vmin=0, vmax=10)\
    .applymap(lambda _: 'color: blue', subset=cols['icu_spare_capacity_per100k'])\
    .format('<b>{:.1f}</b>', subset=cols['icu_capacity_per100k'], na_rep="-")\
    .format('<b>{:.1f}</b>', subset=cols['icu_spare_capacity_per100k'], na_rep="-")\
    .format('<b>{:.2f}</b>', subset=cols['needICU.per100k'])
# -

# <a id='examples'></a>
#
# ## Interactive plot of Model predictions
#
# For top 20 countries by estimated new cases.
#
# > Tip: Choose a country from the drop-down menu to see the calculations used in the tables above and the dynamics of the model.

# +
#hide_input
sir_plot_countries = df.sort_values('Cases.new.est', ascending=False).head(20).index
_, debug_dfs = helper.table_with_projections(debug_countries=sir_plot_countries)

df_alt = pd.concat([d.reset_index() for d in debug_dfs], axis=0)
covid_helpers.altair_sir_plot(df_alt, sir_plot_countries[0])
# -

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/notebook-posts/covid-progress-projections/#appendix)
