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
# - author: <a href=https://github.com/artdgn/>artdgn</a>
# - image: images/covid-icu-projections.png
# - permalink: /covid-icu-projections/
# - toc: false
# - hide: false
# -

# > Important: This dashboard contains the results of a predictive model that was not built by an epidimiologist.

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import overview_helpers

helper = overview_helpers.OverviewDataExtras
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

# # Appendix
#

# <a id='appendix'></a>
# ## Methodology & Assumptions
#
# - Total case estimation calculated from deaths by:
#     - Assuming that unbiased fatality rate is 1.5% (from heavily tested countries / the cruise ship data) and that it takes 8 days on average for a case to go from being confirmed positive (after incubation + testing lag) to death. This is the same figure used by ["Estimating The Infected Population From Deaths"](https://covid19dashboards.com/covid-infected/) in this repo.
#     - Testing bias: the actual lagged fatality rate is than divided by the 1.5% figure to estimate the testing bias in a country. The estimated testing bias then multiplies the reported case numbers to estimate the *true* case numbers (*=case numbers if testing coverage was as comprehensive as in the heavily tested countries*).
#     - The testing bias calculation is a high source of uncertainty in all these estimations and projections. Better source of testing bias (or just *true case* numbers), should make everything more accurate.
# - Projection is done using a simple [SIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model) with (see [examples](#examples)) combined with the approach in [Total Outstanding Cases](https://covid19dashboards.com/outstanding_cases/#Appendix:-Methodology-of-Predicting-Recovered-Cases):
#     - Growth rate calculated over the 5 past days. This is pessimistic - because it includes the testing rate growth rate as well, and is slow to react to both improvements in test coverage and "flattening" due to social isolation.
#     - Recovery probability being 1/20 (for 20 days to recover) where the rate estimated from [Total Outstanding Cases](https://covid19dashboards.com/outstanding_cases/#Appendix:-Methodology-of-Predicting-Recovered-Cases) is too high (on down-slopes).
# - ICU need is calculated as being [6% of active cases](https://medium.com/@joschabach/flattening-the-curve-is-a-deadly-delusion-eea324fe9727) where:
#     - Active cases are taken from the SIR model.
#     - This is both pessimistic - because real ICU rate may in reality be lower, due to testing biases, and especially in "younger" populations), and optimistic - because active cases which are on ICU take longer (so need the ICUs for longer).
#     - ICU capacities are from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_by_hospital_beds) (OECD countries mostly) and [CCB capacities in Asia](https://www.researchgate.net/publication/338520008_Critical_Care_Bed_Capacity_in_Asian_Countries_and_Regions).
#     - ICU spare capacity is based on 70% normal occupancy rate ([66% in US](https://www.sccm.org/Blog/March-2020/United-States-Resource-Availability-for-COVID-19), [75% OECD](https://www.oecd-ilibrary.org/social-issues-migration-health/health-at-a-glance-2019_4dd50c09-en))

# <a id='examples'></a>
#
# **Examples of modeling plots**
#
# For the 5 countries with highest estimated number of new cases.
# > Note: The purpose of the below plots is to demonstrate the actual calculations used in the tables above and the dynamics of the model.

#hide_input
sir_plot_countries = df.sort_values('Cases.new.est', ascending=False).head(5).index
helper.table_with_projections(plot_countries=sir_plot_countries);
