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
# # ICU Demand and Total Affected Population projections per Country
# > Modeling current and future ICU demand and percentage of affected population. 
#
# - permalink: /covid-progress-projections/
# - image: images/icu-need.png
# - toc: true
# - sticky_rank: 0
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
df = helper.filter_df(df_all)
df.columns
# -

#hide_input
from IPython.display import display, Markdown
Markdown(f"***Based on data up to: {pd.to_datetime(helper.dt_today).date().isoformat()}***")

# ## Projected need for ICU beds
# > Countries sorted by current estimated need, split into Growing and Recovering countries by current infection rate.
#
# - Details of estimation and prediction calculations are in [Appendix](#appendix).
# - Column definitions:
#     - <font size=2><b>Estimated ICU need per 100k population</b>: number of ICU beds estimated to be needed per 100k population by COVID-19 patents.</font>
#     - <font size=2><b>Estimated daily infection rate</b>: daily percentage rate of new infections relative to active infections during last 5 days.</font>
#     - <font size=2><b>Projected ICU need per 100k in 14 days</b>: self explanatory.</font>
#     - <font size=2><b>Projected ICU need per 100k in 30 days</b>: self explanatory.</font>
#     - <font size=2><b>ICU capacity per 100k</b>: number of ICU beds per 100k population.</font>
#     - <font size=2><b>Estimated ICU Spare capacity per 100k</b>: estimated ICU capacity per 100k population based on assumed normal occupancy rate of 70% and number of ICU beds (only for countries with ICU beds data).</font>
#     

# > Tip: The <b><font color="b21e3e">red (need for ICU)</font></b>  and the <b><font color="3ab1d8">blue (ICU spare capacity)</font></b>  bars are on the same 0-10 scale, for easy visual comparison of columns.

# +
#hide
df_data = df.sort_values('needICU.per100k', ascending=False)
df_pretty = df_data.copy()
df_pretty['needICU.per100k.+14d'] = stylers.with_errs_float(
    df_pretty, 'needICU.per100k.+14d', 'needICU.per100k.+14d.err')
df_pretty['needICU.per100k.+30d'] = stylers.with_errs_float(
    df_pretty, 'needICU.per100k.+30d', 'needICU.per100k.+30d.err')
df_pretty['infection_rate'] = stylers.with_errs_ratio(df_pretty, 'infection_rate', 'growth_rate_std')

cols = {'needICU.per100k': 'Estimated<br>current<br>ICU need<br>per 100k<br>population',
        'infection_rate': 'Estimated<br>daily infection<br>rate',
       'needICU.per100k.+14d': 'Projected<br>ICU need<br>per 100k<br>In 14 days', 
       'needICU.per100k.+30d': 'Projected<br>ICU need<br>per 100k<br>In 30 days',               
       'icu_capacity_per100k': 'ICU<br>capacity<br> per 100k',
       'icu_spare_capacity_per100k': 'Estimated ICU<br>Spare capacity<br>per 100k',               
      }

def style_icu_table(df_pretty, filt):
    return df_pretty[filt][cols.keys()].rename(cols, axis=1).style\
        .bar(subset=cols['needICU.per100k'], color='#b21e3e', vmin=0, vmax=10)\
        .apply(stylers.add_bar, color='#f43d64',
               s_v=df_data[filt]['needICU.per100k.+14d']/10, subset=cols['needICU.per100k.+14d'])\
        .apply(stylers.add_bar, color='#ef8ba0',
               s_v=df_data[filt]['needICU.per100k.+30d']/10, subset=cols['needICU.per100k.+30d'])\
        .apply(stylers.add_bar, color='#f49d5a',
               s_v=df_data[filt]['infection_rate']/0.33, subset=cols['infection_rate'])\
        .bar(subset=[cols['icu_spare_capacity_per100k']], color='#3ab1d8', vmin=0, vmax=10)\
        .applymap(lambda _: 'color: blue', subset=cols['icu_spare_capacity_per100k'])\
        .format('<b>{:.1f}</b>', subset=cols['icu_capacity_per100k'], na_rep="-")\
        .format('<b>{:.1f}</b>', subset=cols['icu_spare_capacity_per100k'], na_rep="-")\
        .format('<b>{:.2f}</b>', subset=cols['needICU.per100k'])


# -

# ### Growing countries (infection rate above 5%)

#hide_input
style_icu_table(df_pretty, df_data['infection_rate'] > 0.05)

# ### Recovering countries (infection rate below 5%)

#hide_input
style_icu_table(df_pretty, df_data['infection_rate'] <= 0.05)

# ## Projected Affected Population percentages
# > Top 20 countries with most estimated new cases.
#
# - Sorted by number of estimated new cases during the last 5 days.
# - Details of estimation and prediction calculations are in [Appendix](#appendix).
# - Column definitions:
#     - <font size=2><b>Estimated <i>new</i> cases in last 5 days</b>: self explanatory.</font>
#     - <font size=2><b>Estimated <i>total</i> affected population percentage</b>: estimated percentage of total population already affected (infected, recovered, or dead).</font>
#     - <font size=2><b>Estimated daily infection rate</b>: daily percentage rate of new infections relative to active infections during last 5 days.</font>
#     - <font size=2><b>Projected total affected percentage in 14 days</b>: of population.</font>
#     - <font size=2><b>Projected total affected percentage in 30 days</b>: of population.</font>        
#     - <font size=2><b>Lagged fatality rate</b>: reported total deaths divided by total cases 8 days ago.</font>

# +
#hide_input
df_data = df.sort_values('Cases.new.est', ascending=False).head(20)
df_pretty = df_data.copy()
df_pretty['affected_ratio.est.+14d'] = stylers.with_errs_ratio(
    df_pretty, 'affected_ratio.est.+14d', 'affected_ratio.est.+14d.err')
df_pretty['affected_ratio.est.+30d'] = stylers.with_errs_ratio(
    df_pretty, 'affected_ratio.est.+30d', 'affected_ratio.est.+30d.err')
df_pretty['infection_rate'] = stylers.with_errs_ratio(df_pretty, 'infection_rate', 'growth_rate_std')

cols = {'Cases.new.est': 'Estimated <br> <i>new</i> cases <br> in last 5 days',        
       'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',
       'infection_rate': 'Estimated <br>daily infection<br>rate',
       'affected_ratio.est.+14d': 'Projected<br><i>total</i><br>affected<br>percentage<br>In 14 days',
       'affected_ratio.est.+30d': 'Projected<br><i>total</i><br>affected<br>percentage<br>In 30 days',       
       'lagged_fatality_rate': 'Lagged<br>fatality <br> percentage',
      }

df_pretty[cols.keys()].rename(cols, axis=1).style\
    .apply(stylers.add_bar, color='#719974',
           s_v=df_data['affected_ratio.est.+14d'], subset=cols['affected_ratio.est.+14d'])\
    .apply(stylers.add_bar, color='#a1afa3',
           s_v=df_data['affected_ratio.est.+30d'], subset=cols['affected_ratio.est.+30d'])\
    .apply(stylers.add_bar, color='#f49d5a',
           s_v=df_data['infection_rate']/0.33, subset=cols['infection_rate'])\
    .bar(subset=cols['Cases.new.est'], color='#b57b17')\
    .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)\
    .bar(subset=cols['lagged_fatality_rate'], color='#420412', vmin=0, vmax=0.2)\
    .applymap(lambda _: 'color: red', subset=cols['lagged_fatality_rate'])\
    .format('<b>{:,.0f}</b>', subset=cols['Cases.new.est'])\
    .format('<b>{:.1%}</b>', subset=[cols['lagged_fatality_rate'], cols['affected_ratio.est']])
# -


# ## For world maps with all projections: [world maps notebook](/pages/covid-world-maps/)

# <a id='examples'></a>
#
# ## Interactive plot of Model predictions
#
# > Tip: Choose a country from the drop-down menu to see the calculations used in the tables above and the dynamics of the model.
#
# > Note: For stacked plots of all countries see [world plots notebook](/pages/covid-world-progress/)

#hide_input
_, debug_dfs = helper.table_with_projections(debug_dfs=True)
df_alt = pd.concat([d.reset_index() for d in debug_dfs], axis=0)
covid_helpers.altair_sir_plot(df_alt, df['needICU.per100k.+14d.min'].idxmax())

# ## Full table with more details
#  - Contains reported data, estimations, projections, and numbers relative to population.
#  - This is a busy table in order to present as many stats as possible for each country for people to be able to inspect their counties of interest in maximum amount detail (without running the code).
#  - Sorted by projected need for ICU beds per 100k in 14 days. 
#  - **New** in this table means **during last 5 days**.
#  - Includes only countries with at least 10 deaths.
#  > Tip: use Ctrl + F to find your country of interest in the table.

# +
#hide_input
pretty_cols = {}

pretty_cols['cases'] = 'Cases<br>-Reported(+new)<br>-<i>Estimated(+new)</i>'
df[pretty_cols['cases']] =(df.apply(lambda r: f" \
                         {r['Cases.total']:,.0f}\
                         (+<b>{r['Cases.new']:,.0f}</b>)<br>\
                         <i>{r['Cases.total.est']:,.0f}\
                         (+<b>{r['Cases.new.est']:,.0f}</b></i>)\
                         ", axis=1))

pretty_cols['progress'] = ('Affected<br>percentage<br>\
                      -Reported<br>-<i>Estimated<br>-Now<br>-In <b>14</b> / 30</i>')
df[pretty_cols['progress']] =(df.apply(lambda r: f" \
                        {r['affected_ratio']:.2%} <br>\
                        <i>{r['affected_ratio.est']:.1%}<br>\
                        <b>{r['affected_ratio.est.+14d']:.1%}</b> /\
                        {r['affected_ratio.est.+30d']:.0%}</i>", axis=1))

pretty_cols['icu'] = ('Estimated<br>Need for ICU<br>per 100k<br>\
                      -Now <i><br>-In <b>14</b> / 30</i>')
df[pretty_cols['icu']] =(df.apply(lambda r: f"\
                        {r['needICU.per100k']:.1f}<br>\
                        <i><b>{r['needICU.per100k.+14d']:.1f}</b> /\
                        {r['needICU.per100k.+30d']:.0f}</i>", axis=1))

pretty_cols['deaths'] = 'Reported<br>Deaths<br>-Total(+new)<br>-<i>Per100k(+new)</i>'
df[pretty_cols['deaths']] =(df.apply(lambda r: f"\
                         {r['Deaths.total']:,.0f}\
                         (+<b>{r['Deaths.new']:,.0f}</b>) <br>\
                         <i>{r['Deaths.total.per100k']:,.1f}\
                         (+<b>{r['Deaths.new.per100k']:,.1f}</b></i>) \
                         ", axis=1))

pretty_cols['rates'] = 'Rates:<br>-Cases<br>-Infection<br>-Lagged<br>fatality<br>(<i>Reported</i>)'
df[pretty_cols['rates']] =(df.apply(lambda r: f" \
                         {r['growth_rate']:,.1%} \
                         ± <font size=1><i>{r['growth_rate_std']:.0%}</i></font><br>\
                         <b>{r['infection_rate']:,.1%}</b><br>\
                         <b><font color='red'>{r['lagged_fatality_rate']:,.1%}</font></b>\
                         <font size=1>(<i>{r['Fatality Rate']:,.1%}</i>)</font>\
                         ", axis=1))

df_data = df.sort_values('needICU.per100k.+14d', ascending=False)
df_data[pretty_cols.values()].style\
    .apply(stylers.add_bar, color='#b57b17',
           s_v=df_data['Cases.new.est']/df_data['Cases.new.est'].max(), 
           subset=pretty_cols['cases'])\
    .apply(stylers.add_bar, color='#5dad64',
           s_v=df_data['affected_ratio.est.+14d'], 
           subset=pretty_cols['progress'])\
    .apply(stylers.add_bar, color='#f43d64',
           s_v=df_data['needICU.per100k.+14d']/10, 
           subset=pretty_cols['icu'])\
    .apply(stylers.add_bar, color='#918f93',
           s_v=df_data['Deaths.new.per100k']/df_data['Deaths.new.per100k'].max(), 
           subset=pretty_cols['deaths'])\
    .apply(stylers.add_bar, color='#f49d5a',
           s_v=df_data['infection_rate']/0.3,
           subset=pretty_cols['rates'])\
# -

# <a id='appendix'></a>
# ## Methodology and assumptions
# - I'm not an epidemiologist. This is an attempt to understand what's happening, and what the future looks like if current trends remain unchanged.
# - Everything is approximated and depends heavily on underlying assumptions.
# - Projection is done using a simple [SIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model) with (see [examples](#examples)) combined with the approach in [Total Outstanding Cases](https://covid19dashboards.com/outstanding_cases/#Appendix:-Methodology-of-Predicting-Recovered-Cases):
#     - Growth rate calculated over the 5 past days. This is pessimistic - because it includes the testing rate growth rate as well, and is slow to react to both improvements in test coverage and "flattening" due to social isolation.
#     - Confidence bounds are calculated by from the weighted STD of the growth rate over the last 5 days. Model predictions are calculated for growth rates within 1 STD of the weighted mean. The maximum and minimum values for each day are used as confidence bands.
#     - For projections (into future) very noisy projections (with broad confidence bounds) are not shown in the tables.
#     - Recovery probability being 1/20 (for 20 days to recover) where the rate estimated from [Total Outstanding Cases](https://covid19dashboards.com/outstanding_cases/#Appendix:-Methodology-of-Predicting-Recovered-Cases) is too high (on down-slopes).  
# - ICU need is calculated as being [4.4% of active reported cases](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf) where:
#     - Active cases are taken from the SIR model. The ICU need is calculated from reported cases rather than from total estimated active cases. This is because the ICU ratio (4.4%) is based on symptomatic reported cases.
#     - ICU capacities are from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_by_hospital_beds) (OECD countries mostly) and [CCB capacities in Asia](https://www.researchgate.net/publication/338520008_Critical_Care_Bed_Capacity_in_Asian_Countries_and_Regions).
#     - ICU spare capacity is based on 70% normal occupancy rate ([66% in US](https://www.sccm.org/Blog/March-2020/United-States-Resource-Availability-for-COVID-19), [75% OECD](https://www.oecd-ilibrary.org/social-issues-migration-health/health-at-a-glance-2019_4dd50c09-en))
# - Total case estimation calculated from deaths by:
#     - Assuming that unbiased fatality rate is 0.72% ([current meta estimate in](https://www.cebm.net/covid-19/global-covid-19-case-fatality-rates/)). 
#     - The average fatality lag is assumed to be 8 days on average for a case to go from being confirmed positive (after incubation + testing lag) to death. This is the same figure used by ["Estimating The Infected Population From Deaths"](https://covid19dashboards.com/covid-infected/).
#     - Testing bias: the actual lagged fatality rate is than divided by the 0.72% figure to estimate the testing bias in a country. The estimated testing bias then multiplies the reported case numbers to estimate the *true* case numbers (*=case numbers if testing coverage was as comprehensive as in the heavily tested countries*).
#     - The testing bias calculation is a high source of uncertainty in all these estimations and projections. Better source of testing bias (or just *true case* numbers), should make everything more accurate.  
